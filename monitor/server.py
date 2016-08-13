#coding=utf-8

import socket
import sys
from thread import start_new_thread

def clientThread(conn):
    print "Welcome to the server. Type something and hit enter !"
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print data.split("#")
    conn.close()

def startServer():
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 50091 # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    
    print "Host Any, PORT ", PORT
    s.listen(10)
    
    #now keep talking with the client
    while True:
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        start_new_thread(clientThread, (conn, ))
    s.close()

if __name__ == "__main__":
    startServer()
