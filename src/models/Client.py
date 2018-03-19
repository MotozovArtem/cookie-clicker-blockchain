import json
import netifaces
import socket
import nmap.nmap as nmap
import threading


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
        self.client_address = self.get_client_addr()
        self.discover_peers()
        self.pipe = pipe
        self.receive_message()

    def receive_message(self):  # Получаем сообщения предупреждения или блоки
        # print("receiving")
        th = MyThread(self)
        th.start()

    # def send_block_into_pipe(self, block):
    #     self.pipe.send(block)

    def send_block(self, block):
        point = None
        for peer_addr in self.sibling_peers:
            if peer_addr != self.client_address:
                try:
                    point = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    point.connect((peer_addr, self.port))
                    point.send(json.dumps({"type": "block", "block": block}).encode())
                    point.close()
                except ConnectionRefusedError:
                    print("Not our peer")
                except OSError:
                    point.close()

    def send_notifi(self):
        if not self.server_address is None:
            self.sock.sendto("Notification!".encode(), (self.server_address, self.server_port))

    def send_chain(self):
        point = None
        for peer_addr in self.sibling_peers:
            if peer_addr != self.client_address:
                try:
                    point = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    point.connect((peer_addr, self.port))
                    point.send(json.dumps({"type": "chain", "chain": self.blockchain.chain}).encode())
                    point.close()
                except ConnectionRefusedError:
                    print("Not our peer")
                except OSError:
                    point.close()

    def get_net_info(self):
        try:
            addr = netifaces.ifaddresses(self.client_interfaces[2])
            client_addr = addr[netifaces.AF_INET][0]['addr']
        except Exception:
            addr = netifaces.ifaddresses(self.client_interfaces[1])
        return addr

    def get_netmask_CIDR(self):
        host_addr = self.client_net_info[netifaces.AF_INET][0]["netmask"]
        return sum([bin(int(x)).count("1") for x in host_addr.split(".")])

    def get_netID(self):
        return ".".join([str(ad & mask) for ad, mask in zip(
            [int(x) for x in self.client_address.split(".")],
            [int(x) for x in self.client_net_info[netifaces.AF_INET][0]["netmask"].split(".")]
        )])

    def get_client_addr(self):
        return self.client_net_info[netifaces.AF_INET][0]['addr']

    def discover_peers(self):
        netifaces.interfaces()
        port_scanner = nmap.PortScanner()
        port_scanner.scan(hosts='{0}/{1}'.format(self.get_netID(), self.get_netmask_CIDR()), arguments='-n -sP')
        self.sibling_peers = port_scanner.all_hosts()
        return self.sibling_peers

    def define_type_message(self, mes):
        if type(mes) is str and mes.find("Notification") != -1:
            self.notifi_flag = True
        else:
            # data = json.loads(mes)
            # print("I'm block", type(mes))
            if type(mes) is list:
                self.blockchain.chain = mes
            elif type(mes) is dict:
                if self.blockchain.chain[-1]["hash"] == mes["previous_hash"]:
                    self.blockchain.chain.append(mes)
                    self.blockchain.curr_proof = mes['proof']


class MyThread(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        while True:
            try:
                data = self.client.pipe.recv()
                self.client.define_type_message(data)
                print(len(self.client.blockchain.chain))
            except Exception as e:
                print(e.__str__())
