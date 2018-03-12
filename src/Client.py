import socket
import logging
import json
import traceback
from multiprocessing import Process


class Client:
    port = 6999
    server_address = None
    server_port = None
    notifi_flag = False

    def __init__(self, blockchain):
        try:
            self.blockchain = blockchain
            self.sock = socket.socket(socket.AF_INET,  # Internet
                                      socket.SOCK_DGRAM)  # UDP
            self.client_address = socket.gethostbyname(socket.gethostname())
            # self.client_address =  "127.0.0.1"
            self.sock.bind((self.client_address, self.port))
            self.send_hello()
            print("Yess")
            process = Process(target=self.receive_message)
            # process.daemon = True
            process.start()
            # process.join()
            # self.main_run()
        except Exception:
            print(traceback.format_exc())

    # def main_run(self):
    #     process = Process(target=self.receive_message)
    #     process.daemon = True
    #     process.start()
    #     process.join()
    #     # receive_thread = threading.Thread(target=self.receive_message)
    #     # receive_thread.daemon = True
    #     # receive_thread.start()
    #     print("yeg")
    #     # self.receive_message()

    def receive_message(self):  # Получаем сообщения предупреждения или блоки
        print("receiving")
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
                self.server_address, self.server_port = addr[0], addr[1]
                self.define_type_message(data.decode())
            except Exception as e:
                logging.info(str(e))

    def send_block(self, block):
        if not self.server_address is None:
            self.sock.sendto(block.encode(), (self.server_address, self.server_port))

    def send_notifi(self):
        if not self.server_address is None:
            self.sock.sendto("Notification!".encode(), (self.server_address, self.server_port))

    def send_hello(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        hello_message = "hello " + str("(" + str(self.client_address) + "," + str(self.port) + ")")
        self.sock.sendto(hello_message.encode(), ('255.255.255.255', 7000))  # TODO не забыть изменить обратно

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
