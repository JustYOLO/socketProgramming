from socket import *

ip = "127.0.0.1"
port = 9120

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((ip, port))

print("연결 되었습니다.")
clientSocket.send("w 1.txt\nclient sending msg\nthis is the last line.\n.".encode("utf-8"))
print("msg를 송신했습니다.")

data = clientSocket.recv(1024)

print("받은 데이터:", data.decode("utf-8"))
while True:
    msg = input("명령어 및 파일 이름 입력: ")
    if msg == "e":
        msg = "e\n."
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