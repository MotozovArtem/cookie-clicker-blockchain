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
        # self.lc_hello = LoopingCall(self.send_hello)
        self.peertype = peertype
        self.lastping = None
        self.pipe = pipe

    def connectionMade(self):
        remote_host = self.transport.getPeer()
        host = self.transport.getHost()
        self.remote_host = "{0}:{1}".format(remote_host.host, remote_host.port)
        self.host = "{0}:{1}".format(host.host, host.port)
        if host.host not in self.factory.peers:  # Если кто-то новый в сети появился после запуска приложения, добавить его в список peer'ов
            self.factory.peers.append(host.host)
        print("Connection from", self.transport.getPeer(), self.factory.peers)
        if self.factory.first:
            self.send_hello()
            self.factory.first = False

    def connectionLost(self, reason=None):
        if self.remote_nodeid in self.factory.peers:
            self.factory.peers.pop(self.remote_nodeid)
            self.lc_hello.stop()
        print(self.nodeid, "disconnected")

    def dataReceived(self, data):
        message = json.JSONDecoder().decode(data.decode())
        print(message)
        if message['type'] == 'hi':
            self.handle_hello(message)
        elif message['type'] == "block":
            self.handle_block(message['block'])
        elif message['type'] == "chain":
            self.handle_chain(message['chain'])
        # elif message['type'] == "send_chain":
        #     self.send_chain()
        elif message['type'] == '':
            pass

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
        hello = json.dumps({"type": "hi", "ip": self.host})
        self.transport.write("{0}\n".format(hello).encode())

    def handle_hello(self, data):
        if data['ip'] not in self.factory.peers:  # Если ip не в peers, то добавляем его туда и отправляем... обратно?
            self.factory.peers.append(data['ip'])
        self.pipe.send("get_chain")
        chain_for_send = json.dumps({"type": "chain", "chain": self.pipe.recv()})
        self.transport.write("{0}\n".format(chain_for_send).encode())

    def send_block(self, block):
        d_block = json.dumps(block)
        self.transport.write(d_block)

    def handle_chain(self, chain):
        print(type(chain))
        self.pipe.send(chain)

    def handle_block(self, block):
        self.pipe.send(block)


class MyFactory(Factory):
    def __init__(self, peers, pipe):
        self.peers = peers
        self.pipe = pipe
        self.first = True

    def startFactory(self):
        self.nodeid = generate_nodeid()

    def buildProtocol(self, addr):
        return MyProtocol(self, 1, self.pipe)


def get_netmask_CIDR(net_info):
    host_addr = net_info[netifaces.AF_INET][0]["netmask"]
    return sum([bin(int(x)).count("1") for x in host_addr.split(".")])


def get_netID(net_info):
    return ".".join([str(ad & mask) for ad, mask in zip(
        [int(x) for x in net_info[netifaces.AF_INET][0]["addr"].split(".")],
        [int(x) for x in net_info[netifaces.AF_INET][0]["netmask"].split(".")]
    )])


def discover_hosts(mask, net_id):
    port_scanner = nmap.PortScanner()
    port_scanner.scan(hosts='{0}/{1}'.format(net_id, mask), arguments='-n -sP')
    return port_scanner.all_hosts()


def main(pipe):
    interfaces = netifaces.interfaces()
    try:
        addr = netifaces.ifaddresses(interfaces[2])
        host_addr = addr[netifaces.AF_INET][0]["addr"]
    except KeyError:
        addr = netifaces.ifaddresses(interfaces[1])
        host_addr = addr[netifaces.AF_INET][0]["addr"]
    port = 5500
    endpoint = TCP4ServerEndpoint(reactor, port)
    hosts_list = discover_hosts(get_netmask_CIDR(addr), get_netID(addr))
    factory = MyFactory(hosts_list, pipe)
    endpoint.listen(factory)
    for host in hosts_list:
        if host != host_addr:
            point = TCP4ClientEndpoint(reactor, host, int(port))
            point.connect(factory)
    reactor.run()
