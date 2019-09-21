# made by Chun sung ho
# Server(python)- client(Android)
# you should share same wifi between android and python
# check my ip : terminal -> hostname -I

import socket
#import datetime

#ip = "211.217.27.120"
ip = "localhost"
#ip = '192.168.0.4' #내 자취방 ip

port = 7800 #포트

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('', port))     #왜 괄호가 2개지?
server.listen(20)


def handler(clinet):
    data = clinet.recv(1024)    #클라이언트로 부터 1024바이트 만큼 데이터를 받아온다.
    print(data) #데이터값 출력
    clinet.send(data)   #클라이언트에게 데이터값을 돌려준다.

while True:
    print("server wait...")
    client, addr = server.accept()  #서버소켓에 클라이언트가 연결되면 클라이언트 소켓, 주소를 반환한다.
    print(socket)  # 주솟값 출력
    print(addr) #주솟값 출력
    handler(client)     #핸들러 함수에 넘겨준다.
