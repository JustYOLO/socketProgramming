'''
ASCII return
client.py

client sends ASCII encoded string, receives ASCII code of sent string.
'''
from socket import *

ip = "127.0.0.1" # loop back ip
port = 9120 # just random port

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((ip, port))
print("connected to server")
print("input '!e' for close connection and exit")
while True:
    msg = input("input message: ")
    if msg == '!e':
        clientSocket.send('!e'.encode("ASCII"))
        break
    clientSocket.send(msg.encode("ASCII"))
    print("message sent")
    recv_data = clientSocket.recv(1024)
    msg = recv_data.decode("ASCII") # decodes with ASCII
    print("received raw data:", msg)
    print("decoded with ASCII:", end=' ') 
    codes = msg.split(' ') # spilts msg. divide codes with spaces
    for code in codes: # from "codes" get each ascii "code"
        if code == '': continue # if empty string, continues
        print(chr(int(code)), end='') # chr() function returns character that corresponding int input
    print() # just for line break

clientSocket.close()