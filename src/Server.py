import json
from uuid import uuid4
from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import ast
from src import Blockchain
from random import randint
#
# import threading
# from twisted.internet import reactor, protocol
#
#
# class ServerThread(threading.Thread):
#     def __init__(self):
#         super().__init__()
#         self.factory = protocol.ServerFactory()
#         self.factory.protocol = Echo
#         reactor.listenTCP(8001, self.factory)
#
#     def run(self):
#         reactor.run()
#
#
# class ClientThread(threading.Thread):
#     def __init__(self):
#         super(ClientThread, self).__init__()
#         f = EchoFactory()
#         reactor.connectTCP("localhost", 8000, f)
#
#     def run(self):
#         reactor.run()
#
#
# class EchoClient(protocol.Protocol):
#     """Once connected, send a message, then print the result."""
#
#     def connectionMade(self):
#         self.transport.write(b"hello))))")
#
#     def dataReceived(self, data):
#         "As soon as any data is received, write it back."
#         print("Server said:", data)
#         self.transport.loseConnection()
#
#     def connectionLost(self, reason):
#         print("connection lost")
#
#
# class EchoFactory(protocol.ClientFactory):
#     protocol = EchoClient
#
#     def clientConnectionFailed(self, connector, reason):
#         print("Connection failed - goodbye!")
#         reactor.stop()
#
#     def clientConnectionLost(self, connector, reason):
#         print("Connection lost - goodbye!")
#         reactor.stop()
#
#
# # # this connects the protocol to a server running on port 8000
# # def main():
# #     f = EchoFactory()
# #     reactor.connectTCP("localhost", 8000, f)
# #     reactor.run()
#
#
# # *********************Сервер*************************
# class Echo(protocol.Protocol):
#     """This is just about the simplest possible protocol"""
#
#     def dataReceived(self, data):
#         "As soon as any data is received, write it back."
#         self.transport.write(data)


import asyncore


class BlockChainServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        # self.listen(5)
        self.buffer = b"Hello"

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    # автоматически вызывается когда в сокет приходят данные
    # тут мы выведем хост с откуда они идут, и сделаем стандартное чтение с сокета
    def handle_read(self):
        # print(self.host)
        print(self.recv(4096))

    # этот метод сигнал о том что сокет готов записывать
    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


class BlockChainClient(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)

# def main():
#     """This runs the protocol on port 8000"""
#     factory = protocol.ServerFactory()
#     factory.protocol = Echo
#     reactor.listenTCP(8000, factory)
#     reactor.run()
#
#
# # this only runs if the module was *not* imported
# if __name__ == '__main__':
#     main()

# class ConnProtocol(Protocol):
#     def __init__(self):
#         self.proof = None
#         self.state = "ACTIVE"
#         self.remote_nodeid = None
#         self.nodeid = self.factory.nodeid
#         self.blockchain = Blockchain.Blockchain(self.nodeid)
#
#     def connectionMade(self):
#         self.factory.peers.append(self.transport.getPeer)
#         print("Connection from", self.transport.getPeer())
#         BOOTSTRAP_NODES.append(f"localhost:{5000+len(BOOTSTRAP_NODES)}")
#
#     def connectionLost(self, **kwargs):
#         if self.remote_nodeid in self.factory.peers:  # ?
#             self.factory.peers.pop(self.remote_nodeid)
#         print(self.nodeid, "disconnected")
#
#     def dataReceived(self, data):
#         pure_data = ast.literal_eval(data)
#         if self.state == "ACTIVE":
#             self.handle_arrived_block(pure_data)
#         elif self.state == "INACTIVE":
#             pass
#
#     def handle_arrived_block(self, data):
#         try:
#             self.blockchain.chain.append(data)
#             self.proof = int(data['proof']) + 1
#         except Exception as e:
#             print(e)
#         # print(f"following block added {data}")
#
#     def send_block(self, block):
#         for peer in self.factory.peers:
#             self.transport.write(str(block))
#
#     # def handle_hello(self, hello):
#     #     hello = json.loads(hello)
#     #     self.remote_nodeid = hello["nodeid"]
#     #     if self.remote_nodeid == self.nodeid:
#     #         print("Connected to myself.")
#     #         self.transport.loseConnection()
#     #     else:
#     #         self.factory.peers[self.remote_nodeid] = self
#
#
# BOOTSTRAP_NODES = []
#
# for bootstrap in BOOTSTRAP_NODES:
#     host, port = bootstrap.split(":")
#     point = TCP4ClientEndpoint(reactor, host, int(port))
#     d = connectProtocol(point, ConnProtocol())
#     # d.addCallback(gotProtocol)
#
#
# class ServerFactory(Factory):
#     def __init__(self):
#         self.peers = {}
#         self.nodeid = self.generate_nodeid()
#
#     def startFactory(self):
#         pass
#
#     def stopFactory(self):
#         pass
#
#     def buildProtocol(self, addr):
#         return ConnProtocol(self)
#
#     @staticmethod
#     def generate_nodeid():
#         return str(uuid4())
#
#
# def run_server():
#     endpoint = TCP4ServerEndpoint(reactor, 5999)
#     SF = ServerFactory()
#     endpoint.listen(SF)
#     endpoint.run()
#     return SF.nodeid
