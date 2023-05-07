'''
file read
server.py

server receives:

    {file name}.txt

if receives "!e": close connection

if file not found: return "404 Not Found"
if file found:

    200 OK\n
    {file body}...\n
    .

msg should end with a single dot
'''

import os
from socket import *

FILE_NOT_FOUND = "404 Not Found\n"
OK = "200 OK\n"
DIR = "/Users/lee/Documents/socketProgramming/assignment/serverFile/"

def get_file_data(file_dir):
    file = open(file_dir, 'r')
    body = ""
    while True:
        line = file.readline()
        if not line: break
        body += line
    file.close()
    return body

def send_msg(socket, status, body = ""):
    msg = ''
    msg += status
    msg += body
    msg += "\n."
    socket.send(msg.encode("utf-8"))

file_list = os.listdir(DIR) # make a list contains file name w/ extension
file_dict = dict() # make a dictionary that key is file name, value is extension. 
for file in file_list:
    name, extension = file.split('.')
    file_dict[name] = extension

host = "127.0.0.1"
port = 9120

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)
print("Waiting for connection...")
connectedSocket, address = serverSocket.accept()
print(f"Connected to {str(address)}")

while True:
    data = connectedSocket.recv(1024)
    print("received msg:", data.decode("utf-8"))
    msg = data.decode("utf-8")

    if msg[:2] == "!e":
        print("'!e' received. Closing connection.")
        break
    else:
        file_name, ext = msg.split('.')
        if file_name in file_dict.keys(): # server found the file
            print("server found requested file\n")
            body = get_file_data(DIR+file_name+'.txt')
            send_msg(connectedSocket, OK, body)
        else:
            print("server cannot found requested file")
            send_msg(connectedSocket, FILE_NOT_FOUND)
    print("--------------------------")

serverSocket.close()