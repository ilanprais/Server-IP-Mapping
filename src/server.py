import socket
import sys
import datetime

class server:
    
    def __init__(self, port, clientHandler):
        self.__port = port
        self.__clientHandler = clientHandler

    def open(self):
        self.__clientHandler.initializeDomainsMap()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        s.bind(('', self.__port))

        while True:  
            self.__clientHandler.handleRequest(s)

class clienthandler:

    def __init__(self, fileHandler, parentServerIP, parentServerPort):
        self.__domainsMap = {}
        self.__fileHandler = fileHandler
        self.__parentServerIP = parentServerIP
        self.__parentServerPort = parentServerPort

    def handleRequest(self, socket):
        #trying to remove domains that their ttl has expired
        remove = []
        for d in self.__domainsMap:
            startTime = self.__domainsMap[d][2] 
            ttl = self.__domainsMap[d][1]
            if ((datetime.datetime.now() - datetime.datetime(2020, 11, 11)).total_seconds() - startTime > ttl):
                remove.append(d)
        for rem in remove:
            del self.__domainsMap[rem]
            self.__fileHandler.removeLine(d)

        #getting the message from the client
        data, addr = socket.recvfrom(1024)
            
        #checking if the given domain exists in the server
        if data in self.__domainsMap:
            result = data + ','
            for prop in self.__domainsMap[data]:
                result += str(prop) + ','
            result = result[0:-1]
            socket.sendto(result.encode(), addr)
        #if the given domain doesn't exist in the server, then sending the request to the parent server
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(data.encode(), (self.__parentServerIP, self.__parentServerPort))
            result, addr2 = s.recvfrom(1024)
            resList = result.decode().split(',')
            self.__domainsMap[data] = [resList[1], resList[2], (datetime.datetime.now() - datetime.datetime(2020, 11, 11)).total_seconds()]
            self.__fileHandler.addLine(data + ',' + self.__domainsMap[0] + ',' + self.__domainsMap[1] + ',' + self.__domainsMap[2])
            socket.sendto(result, addr)

    def initializeDomainsMap(self):
        updatedLines = []
        lines = self.__fileHandler.getLines()
        for line in lines:
            properties = line.split(',')
            properties.append((datetime.datetime.now() - datetime.datetime(2020, 11, 11)).total_seconds())
            properties = (properties[0], properties[1], int(properties[2]), float(properties[3]))
            self.__domainsMap[properties[0]] = properties[1:]
            updatedLines.append(properties[0] + ',' + properties[1] + ',' + properties[2] + ',' + properties[3])

        self.__fileHandler.replaceAllLines(updatedLines)
        
class filehandler:

    def __init__(self, fileName):
        self.__fileName = fileName

    def addLine(self, line):
        with open(self.__fileName, "a+") as f:
            f.write(line)

    def removeLine(self, prefix):
        lines = self.getLines()
        with open(self.__fileName, 'w') as f:
            for line in lines:
                if (line.startswith(prefix) == False):
                    file.write(line)

    def getLines(self):
        try:
            f = open(self.__fileName, "r")
        except:
            f = open(self.__fileName, "w+")

        lines = f.readlines()
        f.close()
        return lines

    def replaceAllLines(self, newLines):
        with open(self.__fileName, "w+") as f:
            for line in newLines:
                f.write(line)

fileHandler = filehandler('ips.txt')
clientHandler = clienthandler(fileHandler, '127.0.0.1', 12346) # parent props
ser = server(12345, clientHandler) # my props
ser.open()
