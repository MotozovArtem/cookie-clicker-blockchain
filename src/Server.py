import json
from uuid import uuid4
from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import ast
from src import Blockchain
from random import randint


class ConnProtocol(Protocol):
    def __init__(self):
        self.proof = None
        self.state = "ACTIVE"
        self.remote_nodeid = None
        self.nodeid = self.factory.nodeid
        self.blockchain = Blockchain.Blockchain(self.nodeid)

    def connectionMade(self):
        self.factory.peers.append(self.transport.getPeer)
        print("Connection from", self.transport.getPeer())
        BOOTSTRAP_NODES.append(f"localhost:{5000+len(BOOTSTRAP_NODES)}")

    def connectionLost(self, **kwargs):
        if self.remote_nodeid in self.factory.peers:        #?
            self.factory.peers.pop(self.remote_nodeid)
        print(self.nodeid, "disconnected")

    def dataReceived(self, data):
        pure_data = ast.literal_eval(data)
        if self.state == "ACTIVE":
            self.handle_arrived_block(pure_data)
        elif self.state == "INACTIVE":
            pass

    def handle_arrived_block(self, data):
        try:
            self.blockchain.chain.append(data)
            self.proof = int(data['proof']) + 1
        except Exception as e:
            print(e)
        # print(f"following block added {data}")

    def send_block(self, block):
        for peer in self.factory.peers:
            self.transport.write(str(block))

    # def handle_hello(self, hello):
    #     hello = json.loads(hello)
    #     self.remote_nodeid = hello["nodeid"]
    #     if self.remote_nodeid == self.nodeid:
    #         print("Connected to myself.")
    #         self.transport.loseConnection()
    #     else:
    #         self.factory.peers[self.remote_nodeid] = self


BOOTSTRAP_NODES = []

for bootstrap in BOOTSTRAP_NODES:
    host, port = bootstrap.split(":")
    point = TCP4ClientEndpoint(reactor, host, int(port))
    d = connectProtocol(point, ConnProtocol())
    # d.addCallback(gotProtocol)


class ServerFactory(Factory):
    def __init__(self):
        self.peers = {}
        self.nodeid = self.generate_nodeid()

    def startFactory(self):
        pass

    def stopFactory(self):
        pass

    def buildProtocol(self, addr):
        return ConnProtocol(self)

    @staticmethod
    def generate_nodeid():
        return str(uuid4())


def run_server():
    endpoint = TCP4ServerEndpoint(reactor, 5999)
    SF = ServerFactory()
    endpoint.listen(SF)
    return SF.nodeid
