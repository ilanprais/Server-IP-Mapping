import socket

class server:
    
    def __init__(self, myPort, parentIP, parentPort, ipsFileName):
        self.__myPort = myPort
        self.__parentIP = parentIP
        self.__parentPort = parentPort
        self.__ipsFileName = ipsFileName

        self.__map = {}

    def open(self):
        f = open(self.__ipsFileName, "a+")
        lines = f.readlines()
        for line in lines:
            properties = line.split(",")
            self.__map[properties[0]] = (properties[1], properties[2])
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        s.bind(('', self.__myPort))
        while True:
            data, addr = s.recvfrom(1024)
            print(str(data), addr)
            s.sendto(data.upper(), addr)