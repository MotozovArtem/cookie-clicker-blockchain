from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Protocol, Factory
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

# host_interface = netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])[netifaces.AF_INET][0]
# host_addr = host_interface["addr"]
# broadcast = host_interface["broadcast"]


from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Echo(DatagramProtocol):

    def datagramReceived(self, data, host):
        print("received %r from %s" % (data, host))

        self.transport.write(data, host)

host_interface = netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])[netifaces.AF_INET][0]
host_addr = host_interface["addr"]
broadcast = host_interface["broadcast"]
print(broadcast)
reactor.listenUDP(9999, Echo())
reactor.run()

# def falldown():
#     raise Exception('I fall down.')
#
#
# def upagain():
#     print('But I get up again.')
#     reactor.stop()
#
#
# from twisted.internet import reactor
#
# reactor.callWhenRunning(falldown)
# reactor.callWhenRunning(upagain)
#
# print('Starting the reactor.')
# reactor.run()
# print(host_addr)
# print(broadcast)
#
# interfaces = netifaces.interfaces()
# print("TEST " + str(netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])))
# # addr = netifaces.gateways()['default'][netifaces.AF_INET][1]
# test = netifaces.gateways()['default'][netifaces.AF_INET][1]
# # host_addr = netifaces.ifaddresses(addr)[netifaces.AF_INET][0]["addr"]
# # import pprint
# # pprint.pprint(interfaces)
# #
# print("AAAAADDDDDDDDRRRRRRRRRR000000")
# broadcat = netifaces.ifaddresses(test)[2][0]["broadcast"]
# pprint.pprint(addr0)
# print(netifaces.AF_INET)
# for i in range(len(interfaces)):
#     try:
#         print(i,"    ",netifaces.ifaddresses(interfaces[i]))
#         pprint.pprint(interfaces.ifaddresses(interfaces[3]))
#     except Exception as e:
#         continue
# try:
#     addr = netifaces.ifaddresses(interfaces[4])
#     host_addr = addr[netifaces.AF_INET][0]["addr"]
# except Exception:
#     for i in range(len(interfaces)):
#         try:
#             print(i, "    ", netifaces.ifaddresses(interfaces[i]))
#             pprint.pprint(interfaces.ifaddresses(interfaces[3]))
#         except Exception as e:
#             continue
#     # addr = netifaces.ifaddresses(interfaces[1])
#     # host_addr = addr[netifaces.AF_INET][0]["addr"]
# port = 5500
# endpoint = TCP4ServerEndpoint(reactor, port)
# # hosts_list = discover_hosts(get_netmask_CIDR(addr), get_netID(addr))
# factory = MyFactory([], pipe, broadcat)
# endpoint.listen(factory)
# print(test)
# point = TCP4ClientEndpoint(reactor, host_addr, int(port))
# point.connect(factory)
# # for host in hosts_list:
# #     if host != host_addr:
# #         point = TCP4ClientEndpoint(reactor, host, int(port))
# #         point.connect(factory)
# reactor.run()
