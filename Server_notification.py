# 소스 실행후 바로 재 실행이 안되면 serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 추가
# 파일입출력용 파일 생성후 파일안에 뭐라도 적어놔야함
# 핸드폰과 동일한 와이파이 사용해야함
# 본 파이썬용 서버소스 사용시 노트북의 ip주소 확인후 HOST에 저장

import socket
import os
import sys

#내집ip =172.30.1.18
#bestbaram = 192.168.0.144
#HOST = '192.168.0.138'
HOST = '121.129.63.44'
PORT = 7800

ADDR = (HOST,PORT)

BUFSIZE = 4096

#videofile = "C:\kot.txt"
filename = "/home/chun/PycharmProjects/Embedded_AnsimCamera/file"


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serv.bind(ADDR)

serv.listen(5)

conn, addr = serv.accept()

print ('client connected ... ', addr)


    #Open the file

    #Read and then Send to Client

f=open(filename,'rb')# open file as binary

data=f.read()

print (data,',,,')

exx=conn.sendall(data)

print (exx,'...')

f.flush()

f.close()


print ('finished writing file')

conn.close()

serv.close()
