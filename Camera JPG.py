import cv2
import tkinter as tk
import tkinter.filedialog
from tkinter import *
from PIL import Image, ImageTk
from math import sqrt

screen = tk.Tk()
pixelVirtual = tk.PhotoImage(width=1, height=1)
txtvar = tk.StringVar()
screen_name_jpg = []
pic = 0
cnt = 0
tmp1 = []

def openfile():
    global pic, canvas
    zz = Image.open(tk.filedialog.askopenfilename(title="Open Photo",
                                                                filetypes=(
                                                                ("jpeg files", "*.jpg"), ("all files", "*.*"))))
    pic = ImageTk.PhotoImage(zz)
    canvas.create_image(0, 0, anchor='nw', image=pic)

def linelen(x1, x2, y1, y2):   ##Расчёт расстояния
    global txtvar
    return "{} mm".format(int((sqrt((x2-x1)**2+(y2-y1)**2))*float(txtvar.get())))

def click(event):              ##Точка в мете клика и вырисовка линии
    global cnt, tmp1
    if cnt == 0:
        canvas.create_oval(event.x - 2, event.y - 2, event.x + 2, event.y + 2,
                      fill="#FF0000", activefill="#00FF00")
        tmp1.extend((event.x, event.y))
        print(tmp1)
        cnt += 1
    elif cnt == 1:
        cnt = 0
        canvas.create_oval(event.x - 2, event.y - 2, event.x + 2, event.y + 2,
                      fill="#FF0000", activefill="#00FF00")
        canvas.create_line(tmp1[0], tmp1[1], event.x, event.y)
        canvas.create_text((sum((tmp1[0], event.x))/2)+15, (sum((tmp1[1], event.y))/2)+10,
                      text=linelen(tmp1[0], event.x, tmp1[1], event.y))
        tmp1.clear()

    print("x: {}, y: {}".format(event.x, event.y))

def jpg_camera():
    global screen_name_jpg
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            screen_name = input('Введите название файла: ')
            screen_name_jpg = screen_name + '.jpg'
            cv2.imwrite(screen_name_jpg, frame)
    cap.release()
    return
jpg_camera()

def clear_items():
    canvas.delete(tk.ALL)

clear_btn = tk.Button(screen, text="Удалить элементы",
                              command=clear_items)
clear_btn.place(x=100, y=490)
open_btn = tk.Button(screen, text="Открыть", image=pixelVirtual,
                          width=120,
                          height=20,
                          compound="c", command=openfile)
open_btn.place(x=650, y=0)

ent = tk.Entry(screen, textvariable=txtvar)
ent.insert(0, "тут мм писать нада")
ent.place(x=650, y=30)

scrollbar = tk.Scrollbar(screen, orient=VERTICAL) #
scrollbar.place(x=50, y=490)


def on_click():
    item = canvas.find_withtag(tk.CURRENT)
    canvas.delete(item)

clear_last_btn = tk.Button(screen, text="Удалить последнее",
                              command=on_click)
clear_last_btn.place(x=150, y=490)

im = Image.open(screen_name_jpg)
(width_screen, height_screen) = im.size
print("Качество изображения:", im.size)

canvas = tk.Canvas(screen, width = width_screen, height = height_screen)
canvas.pack()
image = Image.open(screen_name_jpg)
photo = ImageTk.PhotoImage(image)
canvas.place(x=0, y=0)
canvas.bind('<Button-1>', click)
screen.mainloop()

#Кнопка открытия файла

