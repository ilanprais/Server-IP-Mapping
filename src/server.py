import socket
import sys

class server:
    
    def __init__(self, port, clientHandler):
        self.__port = port
        self.__fileHandler = fileHandler

    def open(self):
        clienthandler.initializeDomainsMap()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        s.bind(('', self.__myPort))

        while True:
            data, addr = s.recvfrom(1024)   
            result = self.handleRequest(data.decode())
            s.sendto(result.encode(), addr)

    def handleRequest(self, domain):
        return self.__map.getProperties(domain)[0]

class clienthandler:

    def __init__(self, fileHandler, parentServerIP, parentServerPort):
        self.__domainsMap = {}
        self.__fileHandler = fileHandler
        self.__parentServerIP = parentServerIP
        self.__parentServerPort = parentServerPort

    def handleRequest(self, socket):
        for d in self.__domainsMap:
            startTime = self.__domainsMap[d][2]
            ttl = self.__domainsMap[d][1]
            if (currentTime - startTime > ttl):
                del self.__domainsMap[d]
                self.__filehandler.removeLine(d)

        data, addr = socket.recvfrom(1024)
        domain = data.decode()
            
        if domain in self.__domainsMap:
            return self.__domainsMap[domain][0]
        
        #request from the parent server to get ip
        self.__domainsMap[ip] = ...
        return ip

    def initializeDomainsMap(self):
        lines = self.__fileHandler.getLines()
        for line in lines:
            properties = line.split(',')
            self.__domainsMap[properties[0]] = (properties[1], properties[2], currentTime)


class filehandler:

    def __init__(self, fileName):
        self.__fileName = fileName

    def getLines(self):
        try:
            file = open(self.__fileName, "r")
        except:
            file = open(self.__fileName, "w+")

        lines = file.readlines()
        file.close()
        return lines

    def addLine(self, line):
        with open(self.__fileName, "a+") as f:
            file.write(line)

    def removeLine(self, prefix):
        lines = self.getLines()
        with open(self.__fileName, 'w') as f:
            for line in lines:
                if (line.startswith(prefix) == False):
                    f.write(line)

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
            self.__map[properties[0]] = (properties[1], properties[2])
        file.close()
    
    def getProperties(self, key):
        try:
            return self.__map[key]
        except:
            return ('','')

    def append(self, properties):
        file = open(self.__fileName, "a+")
        self.__map[properties[0]] = (properties[1], properties[2])
        line = properties[0] + ',' + properties[1] + ',' + properties[2]
        file.write(line)
        file.close()

ser = server(12345, None, None, "ips.txt")
ser.open()