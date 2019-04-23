import socket
import random
import threading


class sever:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Host = ''
    port = 8899
    usersock = []
    useraddr = []
    rool = {0: "黑方", 1: "白方"}
    map = [[[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "] for y in range(15)]
        , [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "] for z in range(15)]]

    def __init__(self):
        self.turn = int((2 * random.random())/1)

    def begin(self):
        self.s.bind((self.Host, self.port))
        self.s.listen(5)
        print("等待连接...")
        for i in range(0, 2):
            sock, addr = self.s.accept()
            self.usersock.append(sock)
            self.useraddr.append(addr)
            # self.usersock[i].send(b"wait|")
            print("user %s:%s has connected" % self.useraddr[i])
        print(1)
        self.usersock[self.turn].send(b"begin|")
        self.usersock[1-self.turn].send(b"after|")
        print(2)
        self.start_new_thread()

    def start_new_thread(self):
        print(3)
        thread = threading.Thread(target=self.receve_message(), args=())
        thread.setDaemon(True)
        thread.start()
        print(4)

    def send_message(self, pos):
        self.usersock[self.turn].send(pos)

    def receve_message(self):
        sock = self.usersock
        addr = self.useraddr
        while True:
            pos = sock[self.turn].recv(1024)
            data = pos.decode('utf-8').split('|')
            if not data:
                sock[1 - self.turn].send("exit|对方掉线，你赢了".encode('utf-8'))
                break
            elif data[0] == "move":
                xy = data[1].split(',')
                x = round(float(xy[0]))
                y = round(float(xy[1]))
                map = self.map[self.turn]
                if map[x][y] != ' ':
                    sock[self.turn].send("can't|".encode('utf-8'))
                else:
                    sock[self.turn].send("can|".encode('utf-8'))
                    self.map[self.turn][x][y] = chr(self.turn)
                    if self.charge(x, y):
                        sock[1 - self.turn].send(pos)
                        sock[1 - self.turn].send(("lose|"+self.rool[1 - self.turn]+"赢了").encode('utf-8'))
                        sock[self.turn].send("win|恭喜你赢了".encode('utf-8'))
                    else:
                        sock[1 - self.turn].send(pos)
                        print(pos)
                    if self.turn == 0:
                        self.turn = 1
                    else:
                        self.turn = 0
            elif data[0] == "exit":
                self.turn -= 1
                sock[self.turn].send("exit|对方退出，你赢了".encode('utf-8'))
                break

    def charge(self, x, y):
        m = self.map[self.turn]
        color = m[x][y]
        count = 0
        print(x, y)
        for i in range(5):
            if x+i > 15:
                break
            if color == m[x+i][y]:
                count += 1
                print(i)
            else:
                break
        for i in range(1, 5):
            if color == m[x-i][y]:
                count += 1
            else:
                break
        if count >= 5:
            return True
        count = 0
        for i in range(5):
            if y+i > 15:
                break
            if color == m[x][y+i]:
                count += 1
            else:
                break
        for i in range(1, 5):
            if color == m[x][y-i]:
                count += 1
            else:
                break
        if count >= 5:
            return True
        count = 0
        for i in range(5):
            if x+i > 15 or y+i > 15:
                break
            if color == m[x+i][y+i]:
                count += 1
            else:
                break
        for i in range(1, 5):
            if color == m[x-i][y-i]:
                count += 1
            else:
                break
        if count >= 5:
            return True
        count = 0
        for i in range(5):
            if x+i > 15:
                break
            if color == m[x+i][y-i]:
                count += 1
            else:
                break
        for i in range(1, 5):
            if color == m[x-i][y+i]:
                count += 1
            else:
                break
            if y+i > 15:
                break
        if count >= 5:
            return True
        return False


ss = sever()
ss.begin()
