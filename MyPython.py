
import socket
import os
import sys

#내집ip =172.30.1.18
#bestbaram = 192.168.0.144
HOST = '192.168.0.138'

PORT = 7800

ADDR = (HOST,PORT)

BUFSIZE = 4096

videofile = "C:\kot.txt"
filename = "C:\kot.txt"


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind Socket

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


    #Close the Socket

print ('finished writing file')

conn.close()

serv.close()
