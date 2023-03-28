import os
from socket import *

def file_open(fileName, DIR):
    # receive file name with file extension
    return open(DIR + fileName, 'r')


# 확장자명을 제외하고 같은 이름은 없는것으로 간주

SERVER_PORT = 12000 # 서버에 사용될 포트 번호를 상수로 선언
serverSocket = socket(AF_INET, SOCK_DGRAM) # 서버에 사용될 소켓을 선언
serverSocket.bind(("", SERVER_PORT)) # 수신받을 IP와 포트번호를 지정. 매개변수는 튜플로 받으며, 첫번째 원소는 ip주소(빈 문자열은 모든 ip를 받겠다는 것을 의미), 두번째 원소는 포트번호를 의미
DIR = "/Users/lee/documents/socketProgramming/fileReturn/serverFile/"
file_list = os.listdir(DIR)
file_dict = dict()
for file in file_list:
    name, extension = file.split('.')
    file_dict[name] = extension
print(file_dict)


print("The server is ready to receive")
while True:
    file_name, clientAddress = serverSocket.recvfrom(2048) # client.py와 동일
    file_name = file_name.decode()
    print(f"received from {clientAddress}. file_name is: {file_name}") # client의 주소와 메세지를 표시
    if file_name in file_list:
        print("file found with file extension")
        targetFile = file_open(file_name, DIR)
        print(type(targetFile))


    elif file_name in file_dict.keys():
        print("file found without file extension")
        targetFile = file_open(f"{file_name}.{file_dict[file_name]}", DIR)
        print(type(targetFile))
    
    fileData = targetFile.read()
    
    serverSocket.sendto(fileData.encode(), clientAddress)
    targetFile.close()