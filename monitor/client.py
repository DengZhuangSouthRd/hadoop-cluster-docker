#!/usr/bin/env python
# coding=utf-8

import json
import sys
import socket

class Client:
    def __init__(self, host, port):
        self.addr = (host, port)
        self.client = None
        self.isMaster = False
        self.node_info = {}
    
    def createConnection(self):
        if self.client != None:
            self.client.close()
        try: 
            self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client.connect(self.addr)
        except Exception as msg:
            print msg.args
            self.client = None

    def getLocalInfo(self):
        hostname = socket.getfqdn(socket.gethostname())
        if "master" in hostname:
            self.isMaster = True
            self.node_info["role"] = "master"
        else:
            self.isMaster = False
            self.node_info["role"] = "slave"
        hostip = socket.gethostbyname(hostname)
        self.node_info["is_alive"] = "True"
        self.node_info["hostname"] = hostname
        self.node_info["ip"] = hostip
        with open("/home/fighter/.ssh/id_rsa.pub", 'r') as handle:
            ssh_key_data = handle.readline()
            self.node_info["id_rsa.pub"] = ssh_key_data
        return json.dumps(self.node_info)
    
    def sendHeartBeat(self):
        if self.client == None:
            print "Send Data Failed"
            return 
        
        hostname = socket.getfqdn(socket.gethostname())
        if "master" in hostname:
            self.isMaster = True
            self.node_info["role"] = "master"
        else:
            self.isMaster = False
            self.node_info["role"] = "slave"
        hostip = socket.gethostbyname(hostname)
        self.node_info["is_alive"] = "True"
        self.node_info["hostname"] = hostname
        self.node_info["ip"] = hostip
        self.node_info["type"] = "heartbeat"
        self.client.send(json.dumps(self.node_info))

    def sendData(self, data):
        if self.client == None:
            print "Send Data Failed !"
            return 
        client_Package = self.getLocalInfo()
        self.client.send(client_Package)

    def revcData(self):
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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Input Parameters Error !"
        sys.exit(-1)

    host = str(sys.argv[1])
    port = int(sys.argv[2])
    obj = Client(host, port)
    obj.createConnection()
    obj.sendData()

