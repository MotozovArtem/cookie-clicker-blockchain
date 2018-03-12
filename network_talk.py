import nmap.nmap as nmap
import netifaces
import socket


def main():
    interfaces = netifaces.interfaces()
    try:
        addr = netifaces.ifaddresses(interfaces[2])
        host_addr = addr[netifaces.AF_INET][0]["addr"]
    except:
        addr = netifaces.ifaddresses(interfaces[1])
        host_addr = addr[netifaces.AF_INET][0]["addr"]
    port = 5994
    point = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    point.connect((host_addr, port))
    point.send(b"Hello")
    # point.recv(1024)
    point.close()


if __name__ == '__main__':
    main()
