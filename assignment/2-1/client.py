'''
file read and write
client.py

client gets three operations: 'r' (read), 'w' (write), '!e' (end)
input: {operation} {file_name}.{extension}
if operation is w ==> client accept input for writable data. Input single dot (.) to end input and send
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
    elif msg[0] == 'w':
        print("input single dot '.' to end write input: ")
        body = ''
        while True:
            line = input()
            if line == '.':
                body += '.'
                break
            body += line + '\n'
        msg += '\n'
        msg += body
        clientSocket.send(msg.encode("utf-8"))
    else:
        msg = msg.replace("\\n", '\n')
        print(msg)
        msg += "\n."
        clientSocket.send(msg.encode("utf-8"))
    
    data = clientSocket.recv(1024)
    print("recevied data:", data.decode("utf-8"))
    print("--------------------------")
clientSocket.close()