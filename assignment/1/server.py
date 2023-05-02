'''
server.py

server accepts ASCII encoded msg, sends ASCII code of recevied msg.
'''

from socket import *

host = "127.0.0.1" # loop back ip
port = 9120 # just random port

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)
print("Waiting for connection...")
connectedSocket, address = serverSocket.accept()
print(f"Connected to {str(address)}")
while True:
    data = connectedSocket.recv(1024)
    msg = data.decode("ASCII")
    if msg == "!e": 
        print("'!e' received. Closing connection.")
        break
    print("received msg:", msg)
    chars = msg
    msg = ""
    for char in chars:
        msg += f"{ord(char)} "
    print("msg to send:", msg)
    connectedSocket.send(msg.encode("ASCII"))

serverSocket.close()