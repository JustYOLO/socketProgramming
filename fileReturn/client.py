''' 
https://docs.python.org/3/library/socket.html
https://realpython.com/python-sockets/
host로 소문자로된 한줄의     메세지(\n로 구분)를 보내고 수신받는 client프로그램
'''
from socket import * # socket 모듈 내부의 모든 함수, 상수등을 import함
SERVER_NAME = 'localhost' # 연결할 서버의 이름을 상수로 선언
# ppt에는 hostname으로 적혀있는데 저흰 개인 pc에 먼저 실행할 예정임으로 자기 자신을 나타내는 'localhost'로 변경
SERVER_PORT = 12000 # 소켓의 포트 번호를 상수로 선언(상호가 같으면 다른 숫자로 지정 가능)
clientSocket = socket(AF_INET, SOCK_DGRAM) # client가 사용할 소켓을 선언
# AF_NET은 IPv4를 사용하겠다는 것으로 추정...? 
# SOCK_DGRAM은 UDP를 사용하겠다는 상수
# 두 상수(AF_NET, SOCK_DGRAM) 모두 socket 모듈에 포함되어있음
message = input('Input request: ') # client가 보낼 메세지를 저장
clientSocket.sendto(message.encode(), (SERVER_NAME, SERVER_PORT)) # message contains "{filename}.{file extension} {write or open}".

receivedData, serverAddress = clientSocket.recvfrom(2048)
print(receivedData)

lines = list(map(str, receivedData.decode().split("\n")))
print(lines[0])
if lines[0][:3] == "200":
    del lines[0]
    f = open('test.txt', 'w')
    for line in lines:
        f.write(f"{line}\n")
    f.close()


clientSocket.close()
# 소켓 닫음
