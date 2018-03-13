import json
import netifaces
import socket
import nmap.nmap as nmap


class Client:
    server_address = None
    server_port = None
    notifi_flag = False

    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_STREAM)  # TCP
        self.client_interfaces = netifaces.interfaces()
        self.client_net_info = self.get_net_info()
        self.port = 5500
        self.client_address = self.client_net_info[netifaces.AF_INET][0]['addr']

    def receive_message(self):  # Получаем сообщения предупреждения или блоки
        pass
        # print("receiving")
        # while True:
        #     try:
        #         data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
        #         self.server_address, self.server_port = addr[0], addr[1]
        #         self.define_type_message(data.decode())
        #     except Exception as e:
        #         logging.info(str(e))

    def send_block(self, block):
        point = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        point.connect((self.client_address, self.port))
        point.send(json.JSONEncoder().encode(block).encode())
        point.close()
        # if not self.server_address is None:
        #     self.sock.sendto(block.encode(), (self.server_address, self.server_port))

    def send_notifi(self):
        if not self.server_address is None:
            self.sock.sendto("Notification!".encode(), (self.server_address, self.server_port))

    def get_net_info(self):
        try:
            addr = netifaces.ifaddresses(self.client_interfaces[2])
        except:
            addr = netifaces.ifaddresses(self.client_interfaces[1])
        return addr

    def get_netmask_CIDR(self):
        host_addr = self.client_net_info[netifaces.AF_INET][0]["netmask"]
        return sum([bin(int(x)).count("1") for x in host_addr.split(".")])

    def discover_peers(self):
        netifaces.interfaces()
        port_scanner = nmap.PortScanner()
        port_scanner.scan(hosts='{0}/{1}'.format(self.get_netID(), self.get_netmask_CIDR()), arguments='-n -sP')
        return [(x, port_scanner[x]['status']['state']) for x in port_scanner.all_hosts()]

    def get_netID(self):
        return ".".join([str(ad & mask) for ad, mask in zip(
            [int(x) for x in self.client_address.split(".")],
            [int(x) for x in self.client_net_info[netifaces.AF_INET][0]["netmask"].split(".")]
        )])

    def define_type_message(self, mes):
        if mes.find("Notification") != -1:
            self.notifi_flag = True
        else:
            data = json.JSONDecoder().decode(mes)
            if type(data) == list:
                self.blockchain.chain = data
            elif type(data) == dict:
                self.blockchain.chain.append(data)
                self.blockchain.curr_proof = data['proof']
