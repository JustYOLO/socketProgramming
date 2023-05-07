'''
client.py


'''
from socket import *

ip = "127.0.0.1"
port = 9120

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((ip, port))

print("Connected to server.")
print("input '!e' for close connection and exit.")
while True:
    msg = input("Input operation and file name: ")
    if msg == "!e":
        msg = "!e\n."
        clientSocket.send(msg.encode("utf-8"))
        break
    else:
        msg = msg.replace("\\n", '\n')
        print(msg)
        msg += "\n."
        clientSocket.send(msg.encode("utf-8"))
    
    data = clientSocket.recv(1024)
    print("받은 데이터:", data.decode("utf-8"))
clientSocket.close()