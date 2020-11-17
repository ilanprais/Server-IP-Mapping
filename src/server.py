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
        remove = []
        for d in self.__domainsMap:
            startTime = self.__domainsMap[d][2] 
            ttl = self.__domainsMap[d][1]
            if ((datetime.datetime.now() - datetime.datetime(2020, 11, 11)).total_seconds() - startTime > ttl):
                remove.append(d)
                self.__fileHandler.removeLine(d)

        for rem in remove:
            del self.__domainsMap[rem]
            
        #check my ips
        if data in self.__domainsMap:
            ret = data + ','
            for prop in self.__domainsMap[data][0:-1]:
                ret += str(prop) + ","
            ret = ret[0:-1]
            return ret
        #check parent ips
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(data.encode(), (self.__parentServerIP, self.__parentServerPort))
            result, addr = s.recvfrom(1024)
            resList = result.decode().split(',')
            newEntry = (data, resList[1], resList[2], (datetime.datetime.now() - datetime.datetime(2020, 11, 11)).total_seconds())
            self.__domainsMap[data] = newEntry[1:]
            self.__fileHandler.appendEntry(newEntry)
            return result.decode()
        return ''

    def initializeDomainsMap(self):
        updated = []
        lines = self.__fileHandler.getLines()
        for line in lines:
            properties = line.split(',')
            properties.append((datetime.datetime.now() - datetime.datetime(2020, 11, 11)).total_seconds())
            properties = (properties[0], properties[1], int(properties[2]), float(properties[3]))
            self.__domainsMap[properties[0]] = properties[1:]
            updated.append(properties)

        self.__fileHandler.replaceAllEntries(updated)
        
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
        line = properties[0] + ',' + properties[1] + "," + str(properties[2]) + ',' + str(properties[3])
        file.write(line)
        file.close()

    def replaceAllEntries(self, entries):
        file = open(self.__fileName, "w+")
        for entry in entries:
            line = entry[0] + ',' + entry[1] + "," + str(entry[2]) + ',' + str(entry[3])
            file.write(line + '\n')
        file.close()

    def removeLine(self, prefix):
        lines = self.getLines()
        file = open(self.__fileName, 'w')
        for line in lines:
            if (line.startswith(prefix) == False):
                file.write(line)
        file.close()

fileHandler = filehandler('ips.txt')
clientHandler = clienthandler(fileHandler, '127.0.0.1', 12346) # parent props
ser = server(12345, clientHandler) # my props
ser.open()
