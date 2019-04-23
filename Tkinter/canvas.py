from tkinter import *

root = Tk()
f = Frame(root, height=200, width=200)
f.pack()


#def click(event):
#    print('你按下了', event.char)


#entry = Entry(root)
#entry.bind('<KeyPress>', click)
#entry.pack()


def leftClick(event):
    print("x轴坐标：", event.x)
    print("y轴坐标：", event.y)
    print("相对于屏幕左上角x轴坐标：", event.x_root)
    print("相对于屏幕左上角y轴坐标：", event.y_root)



#def close():
#    root.destroy()


lab = Label(root, text='hello')
root.bind("<Button-1>", leftClick)
lab.pack()
#but = Button(root, text='退出', command=close).pack()

root.mainloop()
