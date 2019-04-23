import socket
from tkinter import *
from tkinter.messagebox import *
import threading
import os


class user:

    def __init__(self):
        self.root = Tk()
        self.root.title("五子棋v0--客户端")
        self.imgs = [PhotoImage(file="black.png"), PhotoImage(file="white.png")]
        self.turn = 0
        self.myturn = -2
        self.cv = Canvas(self.root, bg='gray', width=610, height=610)
        self.label1 = Label(self.root, text="客户端....")
        self.button = Button(self.root, text="退出游戏")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 8899
        self.host = '114.115.236.27'
        self.x = 0
        self.y = 0

    def begin(self):
        self.s.connect((self.host, self.port))
        pos = self.s.recv(1024)
        data = pos.decode('utf-8').split('|')
        print(1)
        if data[0] == 'begin':
            self.myturn = 0
        else:
            self.myturn = 1
        self.draw()
        print(2)
        self.cv.bind("<Button-1>", self.click)
        self.button.bind("<Button-1>", self.close)
        self.cv.pack()
        self.button.pack()
        self.label1.pack()
        self.start_new_thread()
        self.root.mainloop()

    def click(self, event):
        if self.myturn != self.turn:
            showinfo(title="提示", message="还没轮到你走棋")
            return
        else:
            self.x = (event.x)//40
            self.y = (event.y)//40
            print("click at ", self.x, self.y, self.myturn)
            pos = str(self.x) + ',' + str(self.y)
            pos = "move|"+pos
            self.s.send(pos.encode('utf-8'))
            print(pos)

    def close(self, event):
        self.s.send("exit|".encode('utf-8'))
        os._exit(0)

    def draw(self):
        cv = self.cv
        for i in range(0, 15):
            cv.create_line(20, 20+40*i, 580, 20+40*i, width=2)
            cv.create_line(20+40*i, 20, 20+40*i, 580, width=2)
        cv.pack()

    def start_new_thread(self):
        thread = threading.Thread(target=self.receve_message, args=())
        thread.setDaemon(True)
        thread.start()

    def draw_other(self, x, y):
        img = self.imgs[1-self.myturn]
        self.cv.create_image((x*40+20, y*40+20), image=img)
        self.cv.pack()

    def receve_message(self):
        s = self.s
        while True:
            pos = s.recv(1024)
            print(pos)
            data = pos.decode('utf-8')
            data = data.split('|')
            if data[0] == "exit":
                showinfo(title="提示", message="对方已退出，你获胜了！")
                self.label1['text'] = "恭喜你获胜啦！"
            elif data[0] == "lose":
                showinfo(title="提示", message="很遗憾，你输了，再接再厉吧")
                self.label1['text'] = "很遗憾你输了"
            elif data[0] == "win":
                showinfo(title="提示", message="恭喜你获胜啦")
                self.label1['text'] = "恭喜你赢了"
            elif data[0] == "move":
                print(data[1])
                xy = data[1].split(',')
                print(xy)
                self.draw_other(int(xy[0]), int(xy[1]))
                if self.turn == 0:
                    self.turn = 1
                else:
                    self.turn = 0
            elif data[0] == 'can':
                img = self.imgs[self.myturn]
                self.cv.create_image((self.x*40+20, self.y*40+20), image=img)
                self.cv.pack()
                self.label1['text'] = "你走得位置是：" + str(self.x) + str(self.y)
                if self.turn == 0:
                    self.turn = 1
                else:
                    self.turn = 0
            elif data[0] == "can't":
                showinfo(title='提示', message="已有棋子")
            else:
                print("无法解读")


u = user()
u.begin()

