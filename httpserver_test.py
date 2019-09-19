import json
from socket import *
from config import *

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)
s.bind(('0.0.0.0', 8080))
s.listen(3)

c,addr = s.accept()
data = c.recv(1024).decode()
print(data)

c.send(json.dumps({'status':'200', 'data':'http test'}).encode())
c.close()
s.close()