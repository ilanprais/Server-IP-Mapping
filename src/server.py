import socket
import sys
class server:
    
    def __init__(self, myPort, parentIP, parentPort, ipsFileName):
        self.__myPort = myPort
        self.__parentIP = parentIP
        self.__parentPort = parentPort
        self.__ipsFileName = ipsFileName
        self.__map = mapper(ipsFileName)

    def open(self):
        self.__map.readFile()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        s.bind(('', self.__myPort))

        while True:
            data, addr = s.recvfrom(1024)   
            result = self.handleRequest(data.decode())
            s.sendto(result.encode(), addr)

    def handleRequest(self, domain):
        return self.__map.getProps(domain)[0]

class mapper:

    def __init__(self, fileName):
        self.__fileName = fileName
        self.__map = {}

    def readFile(self):
        try:
            file = open(self.__fileName, "r")
        except:
            file = open(self.__fileName, "w+")
        lines = file.readlines()
        for line in lines:
            properties = line.split(",")
            self.__map[properties[0]] = [properties[1], properties[2]]
        file.close()
    
    def getProps(self, key):
        try:
            return self.__map[key]
        except:
            return ['','']

    def append(self, props):
        file = open(self.__fileName, "a+")
        self.__map[props[0]] = [props[1], props[2]]
        line = ''
        for prop in props:
            line += props + ','
        line = line[0, len(line) - 2]
        file.write(line)
        file.close()

ser = server(12345, None, None, "ips.txt")
ser.open()