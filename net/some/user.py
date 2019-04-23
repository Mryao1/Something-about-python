import socket

Host = '192.168.219.1'
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((Host, port))
data = s.recv(1024)
print(data.decode())
s.send(b"good night")
data = s.recv(1024)
print(data.decode('utf-8'))
s.send(b'exit')
s.close()
