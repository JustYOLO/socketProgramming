'''
math expression
server.py

server receives:

    {math expression}

if receives "!e": close connection

if msg is not a math expression: returns 400 Bad Request
else returns the result of the input expression

msg should end with a single dot
'''
from socket import *

BAD_REQUEST = "400 Bad Request\n"
OK = "200 OK\n"
ACCEPT = set("1234567890-+*/() ")

def send_msg(socket, status, body = ""):
    msg = ''
    msg += status
    msg += body
    msg += "\n."
    socket.send(msg.encode("utf-8"))

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

    ans = ''
    try:
        if msg[:2] == "!e":
            print("'!e' received. Closing connection.")
            break
        else:
            flag = False
            for char in msg:
                if char not in ACCEPT:
                    operation = BAD_REQUEST
                    flag = True
                    continue
            if not flag:
                ans = str(eval(msg))
                operation = OK
    except:
        operation = BAD_REQUEST
    send_msg(connectedSocket, operation, ans)
    print("--------------------------")

serverSocket.close()