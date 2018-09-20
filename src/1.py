from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from socket import SOL_SOCKET, SO_BROADCAST


class EchoClientDatagramProtocol(DatagramProtocol):
    strings = [
        "Hello, worldaawdawd!",
        "What a fine day it is.",
        "Bye-bye!"
    ]

    def startProtocol(self):
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        #self.transport.connect("255.255.255.255", 8000) <- not needed
        self.sendDatagram()

    def sendDatagram(self):
        if len(self.strings):
            datagram = self.strings.pop(0)
            datagram = datagram.encode()
            print(type(datagram))
            self.transport.setBroadcastAllowed(True)
            self.transport.write(datagram, ('10.192.223.255', 8001)) # <- write to broadcast address here
        else:
            reactor.stop()

    # def datagramReceived(self, datagram, host):
    #     print('Datagram received: ', repr(datagram))
    #     self.sendDatagram()

def main():
    protocol = EchoClientDatagramProtocol()
    #0 means any port
    t = reactor.listenUDP(8000, protocol)
    reactor.run()


if __name__ == '__main__':
   main()