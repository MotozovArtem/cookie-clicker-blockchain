if __name__ == '__main__':
    addr = "192.168.1.6"
    netmask = "255.0.0.0"
    print([bin(int(x)) for x in addr.split(".")])
    netID = ".".join([str(ad & mask) for ad, mask in zip(
        [int(x) for x in addr.split(".")],
        [int(x) for x in netmask.split(".")]
    )])
    print(netID)
    print(type(netID))
