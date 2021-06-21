import socket

### Variables de conexion ###

FROM_HOST = ""
TO_HOST = ""
PORT_SMTP = 25
PORT_POP = 110
IPV4 = socket.AF_INET
TCP = socket.SOCK_STREAM

def defFromHost(host):
  global _FROM_HOST
  _FROM_HOST = host

def defToHost(toHost):
  global _HOST
  _HOST = toHost