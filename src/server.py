import socket

class server:
    
    def __init__(self, myPort, parentIP, parentPort, ipsFileName):
        self.__myPort = myPort
        self.__parentIP = parentIP
        self.__parentPort = parentPort
        self.__ipsFileName = ipsFileName
        self.__map = mapper()

    def open(self):
        self.__map.readFile()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        s.bind(('', self.__myPort))

        while True:
            data, addr = s.recvfrom(1024)
            result = self.handleRequest(data)
            s.sendto(result, addr)

    def handleRequest(self, domain):
        return self.__map.getProps(domain)[1]

class mapper:

    def __init__(self, fileName):
        self.__file = open(self.__ipsFileName, "a+")
        self.__map = {}

    def readFile(self):
        lines = self.__file.readlines()
        for line in lines:
            properties = line.split(",")
            self.__map[properties[0]] = (properties[1], properties[2])

    def getProps(self, key):
        return self.__map[key]

    def append(self, props):
        self.__map[props[0]] = (props[1], props[2])
        line = ''
        for prop in props:
            line += props + ','
        line = line[0, len(line) - 2]
        self.__file.write(line)
