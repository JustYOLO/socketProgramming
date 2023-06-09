'''
file read
client.py

client sends:

    {file name}.txt\n
    .

msg should end with a single dot
'''
from socket import *

ip = "127.0.0.1"
port = 9120

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((ip, port))

print("connected to server.")
print("input '!e' for close connection and exit.")
while True:
    msg = input("input file name: ")
    if msg == "!e":
        msg = "!e\n."
        clientSocket.send(msg.encode("utf-8"))
        break
    else:
        clientSocket.send(msg.encode("utf-8"))
    
    data = clientSocket.recv(1024)
    msg = data.decode("utf-8")
    print("received raw data:", msg, end="\n\n")
    if msg[:3] == "404": print("server cannot find requested file.")
    else:
        lines = list(msg.split('\n'))
        lines.pop(0); lines.pop()
        print("Body of the requested file:")
        for line in lines:
            print(line)
    print("--------------------------")
clientSocket.close()