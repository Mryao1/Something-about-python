import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Host = ''
port = 8080
s.bind((Host, port))
s.listen(5)
while True:
    sock, addr = s.accept()
    print("connected with %s:%s" % addr)
    sock.send(b"welcome")
    while True:
        data = sock.recv(1024)
        sock.send("hello".encode())
        if not data or data.decode('utf-8') == 'exit':
            print("missed connected with %s:%s", addr)
            break
        else:
            print("get words from %s:%s, :" % addr, data.decode())
    sock.close()
    print("socked has closed %s:%s", addr)

