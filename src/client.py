import socket
import sys

#opening the client socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#getting the user input domain, sending it to the server, and printing the answer of the server
while True:
    domain = input()
    s.sendto(domain.encode(), (sys.argv[1], int(sys.argv[2])))
    data, addr = s.recvfrom(1024)
    print(data.decode().split(',')[1])