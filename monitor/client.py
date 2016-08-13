#!/usr/bin/env python
# coding=utf-8

import sys
import socket

class Client:
    def __init__(self, host, port):
        self.addr = (host, port)
        self.client = None
        self.isMaster = False
    
    def createConnection(self):
        if self.client != None:
            self.client.close()
        try: 
            self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client.connect(self.addr)
        except Exception as msg:
            print msg.args
            self.client = None

    def sendData(self, data):
        if self.client == None:
            print "Send Data Failed !"
            return 
        local_name, local_ip = self.getLocalInfo()
        self.client.send(local_name + "#" + local_ip)

    def getLocalInfo(self):
        hostname = socket.getfqdn(socket.gethostname())
        if "master" in hostname:
            self.isMaster = True
        hostip = socket.gethostbyname(hostname)
        return hostname, hostip

    def revcData(self):
        if self.isMaster:
            while True:
                recvdata = self.client.recv(1024)
                if str(recvdata) == "FINISHED":
                   self.closeClient() 
                else:
                    # hostname#hostip
                    with open("/etc/hosts", 'a') as handle:
                        info = recvdata.split("#")
                        handle.write('    '.join([info[1], info[0]]))
                        handle.write('\n')
                        handle.flush()
        else:
            self.closeClient()

    def closeClient(self):
        self.client.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Input Parameters Error !"
        sys.exit(-1)

    host = str(sys.argv[1])
    port = int(sys.argv[2])
    obj = Client(host, port)
    obj.createConnection()
    obj.sendData()

