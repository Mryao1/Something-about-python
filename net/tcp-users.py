import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
h1 = '223.104.187.97'
h2 = '192.168.219.1'
h3 = '192.168.198.1'
h4 = '192.168.43.138'
s.connect((h4, 8899))
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah']:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()

