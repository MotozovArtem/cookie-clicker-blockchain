from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Protocol, Factory,DatagramProtocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import nmap.nmap as nmap
import pprint
import json
import os
import hashlib
from time import time
import netifaces
import sys
sys.path.append('C:\\Program Files (x86)\\Nmap')
from socket import SOL_SOCKET, SO_BROADCAST
def generate_nodeid():
    return hashlib.sha256(os.urandom(256 // 8)).hexdigest()[:10]


class Server(DatagramProtocol):
    def __init__(self, pipe,host_addr,broadcast,port):
    # def __init__(self, host_addr,broadcast,port):
        self.broadcast = broadcast
        self.host_addr = host_addr
        self.port = port
        self.peers = []
        self.pipe = pipe


    def startProtocol(self):
        self.send_hello()

    def datagramReceived(self, data, addr):
        print("---------------------------------------------------------------------")
        print(addr)
        print(self.host_addr)
        if addr[0] != self.host_addr:
            if not addr[0] in self.peers:
                self.peers.append(addr[0])
                peer_dict = {"type": "peers_info", "peers_ip": self.peers, "host_addr": self.host_addr,
                             "broadcast": self.broadcast, "port": self.port}
                self.pipe.send(peer_dict)
            print("---------------------------------------------------------------------")
            print("DATA RECEIVED")

            pprint.pprint(data.decode())
            message = json.JSONDecoder().decode(data.decode())
            if message['type'] == 'hi':
                print("---------------------------------------------------------------------")
                print("Network It`s hello message")
                self.handle_hello(message,addr)
            elif message['type'] == "block":
                print("---------------------------------------------------------------------")
                print("Network It`s block")
                self.handle_block(message['block'])
            elif message['type'] == "chain":
                print("---------------------------------------------------------------------")
                print("Network It`s chain")
                self.handle_chain(message['chain'])


    def send_hello(self):
        print("---------------------------------------------------------------------")
        print("Network We are sending hello")
        hello = json.dumps({"type": "hi", "ip": self.host_addr})
        print(hello)
        self.transport.write(hello.encode(), (self.broadcast, self.port))

    def handle_hello(self, data,addr):
        print("---------------------------------------------------------------------")
        print("Network We catched hello from "+data["ip"])
        if data['ip'] not in self.peers:
            self.peers.append(data['ip'])

            peer_dict = {"type":"peers_info","peers_ip": self.peers, "host_addr":self.host_addr,"broadcast":self.broadcast, "port":self.port}
            self.pipe.send(peer_dict)
        self.pipe.send("get_chain")
        pprint.pprint("Peer list")
        pprint.pprint(self.peers)
        # chain = [[],[]]
        chain_for_send = json.dumps({"type": "chain", "chain": self.pipe.recv()})
        print("Trying to send chain")
        # chain_for_send = json.dumps({"type": "chain", "chain": chain})
        self.transport.write("{0}\n".format(chain_for_send).encode(), addr)

    def send_block(self, block):
        print("---------------------------------------------------------------------")
        print("Network We send ")
        d_block = json.dumps(block)
        self.transport.write(d_block)

    def handle_chain(self, chain):
        print("---------------------------------------------------------------------")
        print("Network We catched chain")
        pprint.pprint(chain)

        self.pipe.send(chain)

    def handle_block(self, block):
        print("---------------------------------------------------------------------")
        print("Network We catched  block")
        pprint.pprint(block)

        # print("TYPE:")
        # print(type(block["block"]["timestamp"]))
        self.pipe.send(block)



def main(pipe):
# def main():
    host_interface = netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])[netifaces.AF_INET][0]
    host_addr = host_interface["addr"]
    broadcast = host_interface["broadcast"]
    port = 5500

    # reactor.listenUDP(0, Server(pipe, host_addr, broadcast, port))
    reactor.listenUDP(5500, Server(pipe,host_addr, broadcast, port))
    reactor.run()

# main()
