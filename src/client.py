import socket
import sys

#opening the client socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#getting the user input domain, sending it to the server, and printing the answer of the server
while True:
    domain = input()
    s.sendto(domain, (sys.argv[0], sys.argv[1]))
    data, addr = s.recvfrom(1024)
    print(data.decode())