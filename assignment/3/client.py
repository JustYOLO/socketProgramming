'''
DNS server
client.py

test client.py
'''
from socket import *

ip = "127.0.0.1"
port = 9120

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((ip, port))

print("connected to server.")
print("input '!e' for close connection and exit.")
while True:
    msg = input("input operation: ")
    if msg == "!e":
        clientSocket.send(msg.encode("utf-8"))
        break
    else:
        clientSocket.send(msg.encode("utf-8"))
    
    data = clientSocket.recv(1024)
    msg = data.decode("utf-8")
    print("received raw data:", msg, end="\n\n")
    if msg[:3] == "400": print("server cannot accept operation.")
    print("--------------------------")
clientSocket.close()