import sys
sys.path.append("../lib")
import socket
import re
import params
switchesVarDefaults = (
    (('-1', '--listPort'), 'listPort', 50001),
    (('-?', '--usage'), "usage", False)
    )
progname = "fileServer"
paramMap = params.parseParams(switchVarDefaults)

listenPort = paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


from threading import Thread;
from encapFramedSock import EncapFramedSock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)

    def run(self):
        print("new thread handling connection from," self.addr)
        while True:
            payload = self.fsock.receive()
            if not payload:
                self.fsock.close()
                return
            payload = payload.decode()
            if exists(payload):
                self.fsock.send(b"True")
            else:
                self.fsock.send(b"False")
                payload2 = self.fock.receive()
                if not payload2:
                    break
                self.fsock.send(payload2)
                output = open(payload, 'wb')
                output.write(payload2)
                output.close()
                self.fsock.close()

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()
