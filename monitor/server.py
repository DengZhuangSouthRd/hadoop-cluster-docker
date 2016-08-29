#coding=utf-8

import socket
import sys
from thread import start_new_thread

class Server:
    def __init__(self):
        self.HOST = ''   # Symbolic name, meaning all available interfaces
        self.PORT = 50091 # Arbitrary non-privileged port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def clientThread(self, conn):
        print "Welcome to the server. Type something and hit enter !"
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print data.split("#")
        conn.close()

    def startServer(self):
        try:
            self.server_socket.bind((self.HOST, self.PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        
        self.server_socket.listen(10)
        
        #now keep talking with the client
        while True:
            conn, addr = self..accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            start_new_thread(clientThread, (conn, ))
        s.close()

if __name__ == "__main__":
    startServer()
