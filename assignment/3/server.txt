'''
DNS server

server.py
server receives:

    d {domain_name} => sends: {ip_address}
    i {ip_address} => sends: {domain_name}
    w i:{ip_address}, d:{domain_name} => accepts and add record to database

server handles resource record from mysql database
server can handle multiple client's request
'''

import pymysql, time, threading
from socket import *

OK = "200 OK\n"
NOT_FOUND = "404 Not Found\n"
BAD_REQUEST = "400 Bad Request\n"
host = "127.0.0.1"
port = 9120

def send_msg(socket, status, body = ""):
    msg = ''
    msg += status
    msg += body
    socket.send(msg.encode("utf-8"))

def get_rr(db):
    cur = db.cursor()
    query = "SELECT * FROM rr;"
    cur.execute(query)
    rows = cur.fetchall()
    return rows
def add_rr(db, ip, domain):
    cur = db.cursor()
    query = f"INSERT INTO rr VALUES('{ip}', '{domain}');"
    cur.execute(query)
def get_ip_dict(db):
    rows = get_rr(db)
    ip_dict = dict(rows)
    return ip_dict
def get_domain_dict(db):
    ip_dict = get_ip_dict(db)
    domain_dict = {y: x for x, y in ip_dict.items()}
    return domain_dict

def f1(soc, address, db):
    '''
    soc = each client's socket
    db = database access
    f1 function is a thread for each client connection
    '''
    start = time.time()
    try:
        while True:
            data = soc.recv(1024)
            msg = data.decode("utf-8")
            if msg[0] == 'd':
                domain_dict = get_domain_dict(db)
                operator, domain = msg.split(' ')
                if domain in domain_dict.keys():
                    ip = domain_dict[domain]
                    send_msg(soc, OK, ip)
                else:
                    send_msg(soc, NOT_FOUND)
            elif msg[0] == 'i':
                ip_dict = get_ip_dict(db)
                operator, ip = msg.split(' ')
                if ip in ip_dict.keys():
                    domain = ip_dict[ip]
                    send_msg(soc, OK, domain)
                else:
                    send_msg(soc, NOT_FOUND)
            elif msg[0] == 'w':
                pass
            elif msg == "!e": 
                print(f"connection close request by: {address}", end= ' ')
                break
            else:
                send_msg(soc, BAD_REQUEST)
        end = time.time()
        print("time elapsed:", end - start)
        soc.close()
    except:
        print("unexpected internal server error")
        print(f"closing connection from: {address}", end= ' ')
        end = time.time()
        print("time elapsed:", end - start)
        soc.close()

def main():
    db = pymysql.connect(host='localhost', user = 'dns', password='010112', db = 'dns', autocommit=True, charset='utf8')

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    server_socket.listen()
    print("Waiting for connection...")

    while True:
        try:
            client_socket, address = server_socket.accept()
            th = threading.Thread(target=f1, args=(client_socket, address, db,))
            th.start()
            print(f"Connected to {str(address)}")
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected.")
            break

    server_socket.close()
    db.close()
    return 0

main()