import sys, os
sys.path.append("../lib")
import re, socket, params
from os.path import exists

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listen = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on: ", bindAddr)

from framedSock import framedSend, framedReceive

while True:
    sock, addr = lsock.accept()
    print("connection rec'd from", addr)
    if not os.fork():
        while True:
            payload = framedReceive(sock, debug)
            if not payload:
                break
            payload = payload.decode()

            if exists(payload):
                framedSend(sock, b"True", debug)
            else:
                framedSend(sock, b"False", debug)
                payload2 = framedReceive(sock,debug)
                if not payload2:
                    break
                framedSend(sock, payload2, debug)
                output = open(payload,'wb')
                output.write(payload2)
                sock.close()
