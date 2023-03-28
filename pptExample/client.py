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
message = input('Input lowercase sentence: ') # client가 보낼 메세지를 저장
clientSocket.sendto(message.encode(), (SERVER_NAME, SERVER_PORT)) # clientSocket을 이용해 message의 내용을 인코딩 (.encode()시 utf-8로 인코딩)해서 보냄. 서버이름과 포트번호를 지정
modifiedMessage, serverAddress = clientSocket.recvfrom(2048) # clientSocket을 이용해서 서버의 응답을 수신. recvfrom은 receive_from의 약자로 추정. 매개변수는 버퍼 사이즈를 의미
print(modifiedMessage)
print(modifiedMessage.decode()) 
# 수신받은 메세지를 표시
print(serverAddress)
# 서버 주소를 표시
clientSocket.close()
# 소켓 닫음
