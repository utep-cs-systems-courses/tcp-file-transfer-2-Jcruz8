import sys
sys.path.append("../lib")
import socket
import re
import params
switchesVarDefaults = (
    (('-1', '--listenPort'), 'listenPort', 50001),
    (('-?', '--usage'), "usage", False)
    )
progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

sock, addr = lsock.accept()

print("connection rec'd from", addr)

from framedSock import framedSend, framedReceive

while True:
    sock, addr = lsock.accept()
    if not os.fork():
        print("new child process handling connection from ", addr)
        payload = framedReceive(sock)
        if not payload:
            break
        payload += b"!"
        framedSend(sock, payload)
