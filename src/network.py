from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import nmap.nmap as nmap

import json
import os
import hashlib
from time import time
import netifaces


def generate_nodeid():
    return hashlib.sha256(os.urandom(256 // 8)).hexdigest()[:10]


class MyProtocol(Protocol):
    def __init__(self, factory, peertype, pipe):
        self.factory = factory
        self.state = "HELLO"
        self.remote_nodeid = None
        self.nodeid = self.factory.nodeid
        self.lc_hello = LoopingCall(self.send_hello)
        self.peertype = peertype
        self.lastping = None
        self.pipe = pipe

    def connectionMade(self):
        remote_host = self.transport.getPeer()
        host = self.transport.getHost()
        self.remote_host = "{0}:{1}".format(remote_host.host, remote_host.port)
        self.host = "{0}:{1}".format(host.host, host.port)
        # self.host_ip = host.host          ???!
        # self.lc_hello.start(1)
        print("Connection from", self.transport.getPeer(), self.factory.peers)
        # self.send_hello()

    def connectionLost(self, reason=None):
        if self.remote_nodeid in self.factory.peers:
            self.factory.peers.pop(self.remote_nodeid)
            self.lc_hello.stop()
        print(self.nodeid, "disconnected")

    def dataReceived(self, data):
        """
        :param data: нужно создать какой-то спец сигнал,
        который входит в data, чтобы определить, как действовать дальше
        *кто-то новый пришел и отправить весь blockchain
        *создан новый block и его нужно отправить
        *создан новый block и остальных нужно остановить на некоторое время
        :return:
        """
        # print(data)
        # print(type(data))
        message = json.JSONDecoder().decode(data.decode())
        print(message)
        if message['type'] == 'hi':
            self.handle_hello(message)
        elif message['type'] == "block":
            self.handle_block(message['block'])
        elif message['type'] == "chain":
            self.handle_chain(message)
        elif message['type'] == '':
            pass
        # self.transport.write(b"HAI")

    def send_addr(self, mine=False):
        now = time()
        if mine:
            peers = [self.host]
        else:
            peers = [(peer.remote_ip, peer.remote_nodeid)
                     for peer in self.factory.peers
                     if peer.peertype == 1 and peer.lastping > now - 240]
        addr = json.JSONEncoder().encode({'type': 'addr', 'peers': peers})
        self.transport.write("{0}\n".format(peers).encode())

    def send_hello(self):
        """Когда новый пир, он должен проверить, он первый или нет
        Если да, то генерить блок
        Иначе он должен принимать blockchain"""
        hello = json.dumps({"type": "hi", "ip": self.host}).encode()
        self.transport.write(hello)

    def handle_hello(self, data):
        # self.send_chain(self.)
        if data['ip'] not in self.factory.peers:  # Если ip не в peers, то добавляем его туда и отправляем... обратно?
            self.factory.peers.append(data['ip'])

        temp = self.pipe.recv()  # recv ждет, пока в него прилетит что-нибудь из pipe, но я хз как иначе организовать
        if type(temp) == dict:  # получение нового блока из Client
            block = json.dumps({"type": "block", "block": temp}).encode()
            self.transport.write(block)

    def send_block(self, block):
        """send_block
        block - это data, которую нам придет от GUIшки (блок по сути),
        а отправлять мы его будем через socket сюда, а потом рассылать другим пирам"""
        d_block = json.dumps(block)
        self.transport.write(d_block)

    def handle_chain(self, chain):
        pass

    def handle_block(self, block):
        # print(block)
        """Тута надо сделать передачу блока в GUI"""
        self.pipe.send(block)
        # pass


class MyFactory(Factory):
    def __init__(self, peers, pipe):
        self.peers = peers
        self.pipe = pipe

    def startFactory(self):
        # self.peers = []
        self.nodeid = generate_nodeid()

    def buildProtocol(self, addr):
        return MyProtocol(self, 1, self.pipe)


def discover_hosts(mask):
    port_scanner = nmap.PortScanner()
    port_scanner.scan(hosts='192.168.1.0/24', arguments='-n -sP')
    return port_scanner.all_hosts()


def main(pipe):
    interfaces = netifaces.interfaces()
    try:
        addr = netifaces.ifaddresses(interfaces[2])
        host_addr = addr[netifaces.AF_INET][0]["addr"]
    except Exception:
        addr = netifaces.ifaddresses(interfaces[1])
        host_addr = addr[netifaces.AF_INET][0]["addr"]
    port = 5500
    endpoint = TCP4ServerEndpoint(reactor, port)
    hosts_list = discover_hosts(None)
    factory = MyFactory(hosts_list, pipe)
    endpoint.listen(factory)
    for host in hosts_list:
        if host != host_addr:
            point = TCP4ClientEndpoint(reactor, host, int(port))
            point.connect(factory)
    reactor.run()


# if __name__ == '__main__':
#     main()
    # p = Process(target=main)
    # p.start()
    # print("It's a ME, Mario")
    # p.join()
