import socket
client = socket.socket()     # 有一些默认参数，即可使用ipv4，这一句是声明socket类型和返回socket连接对象
client.connect(("114.115.236.27", 8080))    # 建立连接：传入服务器端IP号和要连接的应用程序的端口号
# client.send(b'Hello') # 这里只能发生字节流信息，否则报错
client.send('我是Hello'.encode(encoding='utf-8'))      # 需要变成utf-8编码形式
data = client.recv(1024)     # 客户端可以接收服务器端的消息
print(data.decode())
client.close()


