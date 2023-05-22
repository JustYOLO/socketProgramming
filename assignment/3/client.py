'''
DNS server
client.py

d {domain} -> return: {status code} {status message}\n{ip}
i {ip} -> return: {status code} {status message}\n{domain}
w {domain} {ip} -> return: {status code} {status message}\n
!e -> end connection to server

!!! do not use spaces in domain and ip !!!

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
    clientSocket.send(msg.encode("utf-8"))
    if msg == "!e":
        break
    
    data = clientSocket.recv(1024)
    msg = data.decode("utf-8")
    print("received raw data:", msg, end="\n\n")
    if msg[:3] == "404": print("server cannot find requested data")
    elif msg[:3] == "400": print("server cannot accept operation.")
    
    print("--------------------------")
clientSocket.close()