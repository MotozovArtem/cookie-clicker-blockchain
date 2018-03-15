import json
import netifaces
import socket
import nmap.nmap as nmap


class Client:
    server_address = None
    server_port = None
    notifi_flag = False

    def __init__(self, blockchain, pipe):
        self.blockchain = blockchain
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_STREAM)  # TCP
        self.client_interfaces = netifaces.interfaces()
        self.client_net_info = self.get_net_info()
        self.port = 5500
        self.client_address = self.client_net_info[netifaces.AF_INET][0]['addr']
        self.discover_peers()
        self.pipe = pipe
        self.receive_message()

    def receive_message(self):  # Получаем сообщения предупреждения или блоки
        print("receiving")
        while True:
            try:
                data = self.pipe.recv()
                self.define_type_message(data)
            except Exception as e:
                print(e.__str__())

    # def send_block_into_pipe(self, block):
    #     self.pipe.send(block)

    def send_block(self, block):
        self.pipe.send(block)
        point = None
        for peer_addr in self.sibling_peers:
            if peer_addr != self.client_address:
                try:
                    point = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    point.connect((peer_addr, self.port))
                    point.send(json.JSONEncoder().encode({"type": "block", "block": block}).encode())
                    point.close()
                except ConnectionRefusedError:
                    print("Not our peer")
                except OSError:
                    point.close()
                    # point.close()
        # if not self.server_address is None:
        #     self.sock.sendto(block.encode(), (self.server_address, self.server_port))

    def send_notifi(self):
        if not self.server_address is None:
            self.sock.sendto("Notification!".encode(), (self.server_address, self.server_port))

    def get_net_info(self):
        try:
            addr = netifaces.ifaddresses(self.client_interfaces[2])
        except Exception:
            addr = netifaces.ifaddresses(self.client_interfaces[1])
        return addr

    def get_netmask_CIDR(self):
        host_addr = self.client_net_info[netifaces.AF_INET][0]["netmask"]
        return sum([bin(int(x)).count("1") for x in host_addr.split(".")])

    def discover_peers(self):
        netifaces.interfaces()
        port_scanner = nmap.PortScanner()
        port_scanner.scan(hosts='{0}/{1}'.format(self.get_netID(), self.get_netmask_CIDR()), arguments='-n -sP')
        self.sibling_peers = port_scanner.all_hosts()
        return self.sibling_peers

    def get_netID(self):
        return ".".join([str(ad & mask) for ad, mask in zip(
            [int(x) for x in self.client_address.split(".")],
            [int(x) for x in self.client_net_info[netifaces.AF_INET][0]["netmask"].split(".")]
        )])

    def define_type_message(self, mes):
        if mes.find("Notification") != -1:
            self.notifi_flag = True
        else:
            # data = json.loads(mes)
            if type(mes) == list:
                self.blockchain.chain = mes
            elif type(mes) == dict:
                if self.blockchain.chain[-1]["hash"] == mes["previous_hash"]:
                    self.blockchain.chain.append(mes)
                    self.blockchain.curr_proof = mes['proof']

