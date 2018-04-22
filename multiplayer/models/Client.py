import json
import netifaces
import socket
import nmap.nmap as nmap
import threading

import pprint
class Client:
    server_address = None
    server_port = None
    notifi_flag = False

    def __init__(self, blockchain, pipe):
        self.blockchain = blockchain
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_interfaces = netifaces.interfaces()
        self.port = None
        self.host_addr = None
        self.broadcast = None
        self.sibling_peers = None
        # self.discover_peers()
        self.pipe = pipe
        self.receive_message()

    def receive_message(self):  # Получаем сообщения предупреждения или блоки
        th = MyThread(self)
        th.start()

    def send_block(self, block):
        point = None
        for peer_addr in self.sibling_peers:
            if peer_addr != self.host_addr:
                try:
                    point = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    point.sendto(json.dumps({"type": "block", "block": block}).encode(), (peer_addr,self.port))
                except ConnectionRefusedError:
                    print("Not our peer")
                except OSError:
                    point.close()

    def send_notifi(self):
        if not self.server_address is None:
            self.sock.sendto("Notification!".encode(), (self.server_address, self.server_port))

    def define_type_message(self, mes):
        print("Client data came to client")
        if type(mes) is str and mes.find("Notification") != -1:
            self.notifi_flag = True
        else:
            if type(mes) is list:
                print("It`s chain")
                # pprint.pprint()
                print("checking age")
                print("Their: ", float(mes[0]["timestamp"]), "Our: ", self.blockchain.chain[0]["timestamp"])
                if float(mes[0]["timestamp"]) < self.blockchain.chain[0]["timestamp"]:
                    print("Our genesis is younger")
                    self.blockchain.chain = mes
                    print("Client chain added successfully")

                pprint.pprint(mes)
            elif type(mes) is dict:
                print("It`s block")

                if not  "peers_ip" in mes:

                    if self.blockchain.chain[-1]["hash"] == mes["previous_hash"]:
                        print("Client add block to blockhain successfully")
                        self.blockchain.chain.append(mes)
                        self.blockchain.curr_proof = mes['proof']
                    else:
                        print("Client failed to add block")
                else:
                    print("We found peers in client")
                    self.sibling_peers = mes["peers_ip"]
                    self.host_addr = mes["host_addr"]
                    self.port = mes["port"]
                    self.broadcast = mes["broadcast"]

            elif mes == 'get_chain':
                print("They ask to send chain")
                self.pipe.send(self.blockchain.chain)


class MyThread(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        while True:
            try:
                data = self.client.pipe.recv()
                self.client.define_type_message(data)
            except Exception as e:
                print(e.__str__())
