'''
DNS server

server.py
server receives:

    d {domain_name} => sends: {ip_address}
    i {ip_address} => sends: {domain_name}
    w {domain} {ip} => accepts and add record to database

!!! do not use spaces in domain and ip !!!

server handles resource record from mysql database
server can handle multiple client's request
'''

import pymysql, time, threading
from socket import *

OK = "200 OK\n"
NOT_FOUND = "404 Not Found\n"
BAD_REQUEST = "400 Bad Request\n"
# client에게 반환할 상태 메세지 상수
REJECT = "'\";:~\\!@#$%^&*()-_+=,?/|" 
# SQL INJECTION 예방을 위한 특수문자 제외
host = "127.0.0.1"
port = 9120
# 서버의 ip주소와 포트번호
def send_msg(socket: socket, status: str, body = ""):
    '''
    매개변수로 받은 소켓으로 상태 메세지와 본문을 전송
    return: void
    '''
    msg = ''
    msg += status
    msg += body
    socket.send(msg.encode("utf-8"))

def get_rr(db: pymysql.Connection):
    '''
    매개변수로 받은 db로 MySQL 서버에서 Resource Record를 받는다.
    return: 2-dimensional list. 1st element: ip, 2nd element: domain
    '''
    cur = db.cursor()
    query = "SELECT * FROM rr;"
    cur.execute(query)
    rows = cur.fetchall()
    return rows
def add_rr(db: pymysql.Connection, ip: str, domain: str):
    '''
    매개변수로 받은 db로 MySQL 서버의 Resource Record에 새로운 record를 추가한다.
    return: void
    '''
    cur = db.cursor()
    query = "INSERT INTO rr (ip, domain) VALUES (%s, %s)"
    cur.execute(query, (ip, domain))
def get_ip_dict(db: pymysql.Connection):
    '''
    매개변수로 받은 db로 MySQL 서버에서 RR를 받은뒤 ip가 key인 dict 생성
    return: dict
    '''
    rows = get_rr(db)
    ip_dict = dict(rows)
    return ip_dict
def get_domain_dict(db: pymysql.Connection):
    '''
    매개변수로 받은 db로 MySQL 서버에서 RR를 받은뒤 domain이 key인 dict 생성
    return: dict
    '''
    ip_dict = get_ip_dict(db)
    domain_dict = {y: x for x, y in ip_dict.items()}
    return domain_dict
def is_ip(ip: str):
    '''
    주어진 str(ip)이 IPv4 형식인지 확인하는 함수
    return: boolean
    '''
    try:
        nums = list(map(int, ip.split('.')))
    except ValueError:
        print("IP string format is not valid")
        return False
    if len(nums) != 4:
        return False
    for num in nums:
        if num < 0 or num > 255:
            return False
    return True



def f1(soc: socket, address: str, db: pymysql.Connection):
    '''
    각 client의 연결을 f1 함수로 설정하여 thread를 생성

    soc = each client's socket
    db = MySQL socket
    f1 function is a thread for each client connection
    '''
    start = time.time() # 연결시간을 측정하기 위해 시작 시간 저장
    try:
        while True:
            data = soc.recv(1024) # client로 부터 요청 수령
            msg = data.decode("utf-8") # 유니코드로 decode
            if msg[0] == 'd': # 명령이 'd'일 경우(도메인 입력 -> ip 반환
                domain_dict = get_domain_dict(db)
                # 도메인 dict 가져오기
                operator, domain = msg.split(' ')
                # 명령어와 도메인 분리
                if domain in domain_dict.keys(): # 도메인이 서버의 RR에 존재할 경우
                    ip = domain_dict[domain]
                    send_msg(soc, OK, ip)
                    # 해당하는 ip를 client에 전송
                else: # 없을 경우
                    send_msg(soc, NOT_FOUND)
                    # 에러 메세지를 전달
            elif msg[0] == 'i': # 명령이 'i'일 경우(ip 입력 -> 도메인 반환)
                ip_dict = get_ip_dict(db)
                # ip dict 가져오기
                operator, ip = msg.split(' ')
                # 명령어와 ip 분리하기
                if ip in ip_dict.keys(): # ip가 서버의 RR에 존재할 경우
                    domain = ip_dict[ip] 
                    send_msg(soc, OK, domain)
                    # 해당하는 도메인을 client에 전송
                else: # 없을 경우
                    send_msg(soc, NOT_FOUND)
                    # 에러 메세지를 전달
            elif msg[0] == 'w': # 명령이 'w'일 경우(RR에 새로운 record 추가)
                operator, domain, ip = msg.split(' ') # 명령어와 도메인, ip를 분리
                if any(char in REJECT for char in domain) and any(char in REJECT for char in ip): # 도메인과 명령어에 허용되지 않은 특수문자가 들어갈 경우
                    send_msg(soc, BAD_REQUEST) # 에러 메세지 전달
                elif not is_ip(ip):
                    send_msg(soc, BAD_REQUEST, "Given IP is not valid IP address")
                else:
                    add_rr(db, ip, domain) # 허용될 경우
                    send_msg(soc, OK)
            elif msg == "!e": # 명령이 '!e'일 경우(연결 종료 요청)
                print(f"connection close request by: {address}", end= ' ')
                break # 반복문을 중단
            else: # 위 명령어중 아무것도 해당하지 않을 경우
                send_msg(soc, BAD_REQUEST)
        end = time.time() # 종료 시간을 측정
        print("time elapsed:", end - start) # 연결된 시간을 출력
        soc.close() # client와 연결된 소켓을 닫음
    except: # error Exception
        print("unexpected internal server error")
        print(f"closing connection from: {address}", end= ' ')
        end = time.time()
        print("time elapsed:", end - start)
        soc.close()
        # 에러 발생시 소켓 닫기 및 thread 삭제

def main():
    db = pymysql.connect(host='localhost', user = 'dns', password='010112', db = 'dns', autocommit=True, charset='utf8')
    # pymysql을 이용한 MySQL서버 접근
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    # server의 소켓 설정
    server_socket.listen()
    print("Waiting for connection...")
    # 연결 요청 대기
    while True: # 다중 연결을 위한 반복문
        try:
            client_socket, address = server_socket.accept()
            th = threading.Thread(target=f1, args=(client_socket, address, db,))
            th.start()
            # 연결 요청을 받아서 thread 생성
            print(f"Connected to {str(address)}")
        except KeyboardInterrupt: # ctrl+c로 프로그램 종료
            print("\nKeyboardInterrupt detected.")
            break

    server_socket.close() # 서버를 종료할 경우 서버 소켓도 닫음
    db.close() # MySQL 서버와 연결된 소켓도 종료
    return 0

main() # 실행