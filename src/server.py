import socket
import sys

class server:
    
    def __init__(self, port, clientHandler):
        self.__port = port
        self.__clientHandler = clientHandler

    def open(self):
        self.__clientHandler.initializeDomainsMap()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        s.bind(('', self.__port))

        while True:
            data, addr = s.recvfrom(1024)   
            result = self.__clientHandler.handleRequest(data.decode())
            s.sendto(result.encode(), addr)

class clienthandler:

    def __init__(self, fileHandler, parentServerIP, parentServerPort):
        self.__domainsMap = {}
        self.__fileHandler = fileHandler
        self.__parentServerIP = parentServerIP
        self.__parentServerPort = parentServerPort

    def handleRequest(self, data):
        # for d in self.__domainsMap:
        #     startTime = self.__domainsMap[d][2]
        #     ttl = self.__domainsMap[d][1]
        #     if (currentTime - startTime > ttl):
        #         del self.__domainsMap[d]
        #         self.__filehandler.removeLine(d)

        #check my ips
        if data in self.__domainsMap:
            return self.__domainsMap[data][0]
        #check parent ips
        else:
            pass
            # self.__domainsMap[ip] = ...
            # return ip
        return ''

    def initializeDomainsMap(self):
        lines = self.__fileHandler.getLines()
        for line in lines:
            properties = line.split(',')
            self.__domainsMap[properties[0]] = (properties[1], properties[2], 0)

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
        file = open(self.__fileName, "a+")
        file.write(line)
        file.close()

    def appendEntry(self, properties):
        file = open(self.__fileName, "a+")
        self.__map[properties[0]] = (properties[1], properties[2])
        line = properties[0] + ',' + properties[1] + ',' + properties[2]
        file.write(line)
        file.close()

    def removeLine(self, prefix):
        lines = self.getLines()
        file = open(self.__fileName, 'w')
        for line in lines:
            if (line.startswith(prefix) == False):
                file.write(line)
        file.close()

fileHandler = filehandler('ips.txt')
clientHandler = clienthandler(fileHandler, '127.0.0.1', 12346)
ser = server(12345, clientHandler)
ser.open()