import socket, sys, re
from os.path import exists

sys.path.append("../lib")
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False)
    )

from encapFramedSock import EncapFramedSock
progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server: port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

fsock = EncapFramedSock((s, addrPort))

finput = input("what file in the directory do you want to send: ")

if exists(finput):
    file_copy = open(finput, 'rb')
    file_data = file_copy.read()
    file_copy.close()
    file_name = input("what do you want to save the file as")
    fsock.send(file_name.encode())
    file_exists = fsock.receive()
    file_exists = file_exists.decode()
else:
    print("file doesnt exist")
    sys.exit(0)
