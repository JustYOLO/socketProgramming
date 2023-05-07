'''
file read and write
server.py
server accepts operation: 'r'(read), 'w'(write) and '!e'(end)

first line: {operation} {file name}.{extension = txt}
if operation = 'w': left over lines will be writable data. The data should end with "\n." (single dot)
'''

import os
from socket import *

FILE_NOT_FOUND = "404 Not Found\n"
OK = "200 OK\n"
BAD_REQUEST = "400 Bad Request\n"
DIR = "/Users/lee/Documents/socketProgramming/assignment/serverFile/"

def get_file_name(line):
    file_name, extension = line.split('.')
    return file_name

def read_file_data(file_dir):
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

def check_end(lines):
    if lines[-1] == '.':
        lines.pop()
        return lines

file_list = os.listdir(DIR)
file_dict = dict()
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
    lines = data.decode("utf-8").split("\n")
    data = ""

    try:
        if lines[0][0] == 'w':
            lines = check_end(lines)
            file_name = get_file_name(lines[0][2:])
            file = open(f"{DIR}{file_name}.txt", 'w')
            print(lines[1:])
            for i, line in enumerate(lines[1:]):
                if i == len(lines) - 2:
                    file.write(line)
                    continue
                file.write(line + '\n')
            file.close()
            operation = OK

        elif lines[0][0] == 'r':
            file_name = get_file_name(lines[0][2:])
            if file_name in file_dict.keys():
                operation = OK
                data = read_file_data(f"{DIR}{file_name}.txt")
            else:
                operation = FILE_NOT_FOUND

        elif lines[0][:2] == "!e":
            print("Connection end requset")
            break
        else:
            print("400 Bad Request")
            operation = BAD_REQUEST
    except:
        operation = BAD_REQUEST
    send_msg(connectedSocket, operation, data)
    print("sent msg to client")

serverSocket.close()