'''
server accepts operation: 'r'(read), 'w'(write) and 'e'(end)

first line: {operation} {file name}.{extension = txt}
if operation = 'w': left over lines will be written data. The data should end with "\n." (single dot)
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

def check_end(lines):
    if lines[-1] == '.':
        lines.pop()
        return lines

FILE_NOT_FOUND = "404 Not Found\n"
DIR = "/Users/lee/documents/socketProgramming/tcpFileReturn/serverFile/"

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
print("대기중 입니다.")

connectedSocket, address = serverSocket.accept()

print(f"{str(address)}에 연결 되었습니다.")

while True:
    data = connectedSocket.recv(1024)
    print("received msg: ", data.decode("utf-8"))
    lines = data.decode("utf-8").split("\n")
    lines = check_end(lines)

    if lines[0][0] == 'w':
        file_name, extension = lines[0][2:].split('.')
        file = open(f"{DIR}{file_name}.txt", 'w')
        print(lines[1:])
        for line in lines[1:]:
            file.write(line + '\n')
        file.close()
        data = "200 OK\n"

    elif lines[0][0] == 'r':
        file_name, extension = lines[0][2:].split('.')
        if file_name in file_dict.keys():
            data = "200 OK\n"
            file = open(f"{DIR}{file_name}.txt", 'r')
            while True:
                line = file.readline()
                if not line: break
                data += line
            file.close()
        else:
            data = FILE_NOT_FOUND

    elif lines[0][:1] == "!e":
        print("Connection End requset")
        break
    else:
        print("400 Bad Request")
        connectedSocket.send("400 Bad Request\n".encode("utf-8"))
        print("메세지를 송신했습니다.")
        continue
    connectedSocket.send(data.encode("utf-8"))
    print("메세지를 송신했습니다.")

serverSocket.close()