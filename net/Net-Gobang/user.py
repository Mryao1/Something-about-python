from tkinter import *
from tkinter.messagebox import *
import socket, threading, os


def draw():
    for i in range(0,15):
        cv.create_line(20, 20+40*i, 580, 20+40*i, width=2)
    for i in range(0, 15):
        cv.create_line(20+40*i, 20, 20+40*i, 580, width=2)
    cv.pack()


def print_map():
    for j in range(0, 15):
        for i in range(0, 15):
            print(map[i][j], end=' ')
        print('w')


def receiveMessage():
    global s
    while True:
        global addr
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        a = data.split("|")
        if not data:
            print('client has exited!')
            break
        elif a[0] == 'exit':
            print('client 对方退出')
            label1["text"] = 'client 对方退出，游戏结束'
            global other
            other = False
        elif a[0] == 'over':
            print('对方赢信息')
            label1["text"] = data.split("|")[0]
            showinfo(title='提示', message=data.split("|")[1])
        elif a[0] == 'move':
            print('received:', data, 'from', addr)
            p = a[1].split(",")
            x = int(p[0])
            y = int(p[1])
            print(p[0], p[1])
            label1["text"] = "客户端走的位置：" + p[0] + p[1]
            DrawOtherChess(x, y)
    s.close()


def mouse_click(event):
    global turn
    global Myturn
    if Myturn == -1:
        Myturn = turn
    else:
        if(Myturn!=turn):
            showinfo(title='提示', message='还没轮到你')
            return
    x = (event.x)//40
    y = (event.y)//40
    print('clicked at ', x, y, turn)
    if map[x][y] != " ":
        showinfo(title='提示', message='已有棋子')
    else:
        img1 = imges[turn]
        cv.create_image((x*40+20, y*40+20), image=img1)
        cv.pack()
        map[x][y] = str(turn)
        pos = str(x)+","+str(y)
        sendMessage("move|" + pos)
        print("客户端走的位置", pos)
        label1["text"] = "客户端走的位置" + pos
        if win_lose(x, y):
            if turn == 0:
                showinfo(title='提示', message='黑方你赢了')
                sendMessage("over|黑方你赢了")
            else:
                showinfo(title='提示', message='白方你赢了')
                sendMessage("over|白方你赢了")
        if turn == 0:
            turn = 1
        else:
            turn = 0


def win_lose(x, y):
    count = 1
    color = map[x][y]
    i = 1
    while color == map[x+i][y]:
        count += 1
        i += 1
    i = 1
    while color == map[x-i][y]:
        count += 1
        i += 1
    if count >= 5:
        return True
    count = 1
    color = map[x][y]
    i = 1
    while color == map[x][y+i]:
        count += 1
        i += 1
    i = 1
    while color == map[x][y-i]:
        count += 1
        i += 1
    if count >= 5:
        return True
    count = 1
    color = map[x][y]
    i = 1
    while color == map[x+i][y+i]:
        count += 1
        i += 1
    i = 1
    while color == map[x-i][y-i]:
        count += 1
        i += 1
    if count >= 5:
        return True
    count = 1
    color = map[x][y]
    i = 1
    while color == map[x+i][y-i]:
        count += 1
        i += 1
    i = 1
    while color == map[x-i][y+i]:
        count += 1
        i += 1
    if count >= 5:
        return True


def close(event):
    if other:
        pos = "exit|"
        sendMessage(pos)
    os._exit(0)


def startNewThread():
    thread = threading.Thread(target=receiveMessage, args=())
    thread.setDaemon(True)
    thread.start()


def sendMessage(pos):
    global s
    s.send(pos.encode())


def DrawOtherChess(x, y):
    global turn
    img1 = imges[turn]
    cv.create_image((x*40+20, y*40+20), image=img1)
    cv.pack()
    map[x][y] = str(turn)
    if turn == 0:
        turn = 1
    else:
        turn = 0



root = Tk()
root.title("五子棋v0.0客户端")
imges = [PhotoImage(file='black.png'), PhotoImage(file='white.png')]
turn = 0
Myturn = 1
map = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
       for y in range(15)]
cv = Canvas(root, bg='gray', width=610, height=610)
draw()
cv.bind('<Button-1>', mouse_click)
cv.pack()
label1 = Label(root, text="客户端...")
label1.pack()
button1 = Button(root, text="退出游戏")
button1.bind("<Button-1>", close)
button1.pack()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8080
host = '192.168.219.1'
s.connect((host, port))
poss = 'join|'
sendMessage(poss)
startNewThread()
root.mainloop()
