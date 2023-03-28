from socket import *
SERVER_PORT = 12000 # 서버에 사용될 포트 번호를 상수로 선언
serverSocket = socket(AF_INET, SOCK_DGRAM) # 서버에 사용될 소켓을 선언
serverSocket.bind(("", SERVER_PORT)) # 수신받을 IP와 포트번호를 지정. 매개변수는 튜플로 받으며, 첫번째 원소는 ip주소(빈 문자열은 모든 ip를 받겠다는 것을 의미), 두번째 원소는 포트번호를 의미
print("The server is ready to receive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048) # client.py와 동일
    modifiedMessage = message.decode().upper() # 수신받은 메세지를 모두 대문자로 바꾼뒤 저장
    print(f"received from {clientAddress}. Message is: {message}") # client의 주소와 메세지를 표시
    serverSocket.sendto(modifiedMessage.encode(),clientAddress) # 변조된 메세지를 client에 전송