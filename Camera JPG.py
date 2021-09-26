import cv2
import os
import tkinter as tk
import glob
import tkinter.filedialog
from tkinter import *
from PIL import Image, ImageTk, ImageGrab
from math import sqrt

screen = tk.Tk()
pixelVirtual = tk.PhotoImage(width=1, height=1)
txtvar = tk.StringVar() # Для поля ввода мм в пкс
screen_name_jpg = ()
pic = 0
cnt = 0
tmp1 = [] # Координаты 1-го овала
tmp2 = [] # Координаты 2-го овала

# Захват кадра и сохранение
def jpg_camera():
    global screen_name_jpg
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            screen_name_jpg = 'file000.jpg'
            cv2.imwrite(screen_name_jpg, frame)
    cap.release()

# Открытие выбранного изображения
def openfile():
    global pic
    canvas.delete(tk.ALL)
    zz = Image.open(tk.filedialog.askopenfilename(title="Open Photo",
                                                filetypes=(
                                                ("jpeg files", "*.jpg"), ("all files", "*.*"))))
    pic = ImageTk.PhotoImage(zz)
    canvas.create_image(0, 0, anchor='nw', image=pic)

# Сохранение файла с запоминанием места сохранения(создаётся txt файл)
def savefile():
    if not os.path.exists('./config.txt'):
        savefolder = tkinter.filedialog.askdirectory(mustexist=True, title="Выбрать папку для сохранения")
        with open("config.txt", encoding='utf-8', mode="w") as file:
            file.write(savefolder+"\n")
            file.close()
        savefile()
    else:
        with open("config.txt", encoding='utf-8', mode="r") as file:
            savefolder = file.readline()[0:-1]
        filepaths = glob.glob(savefolder + '/' + 'file_*.jpg')
        image = ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(),
           canvas.winfo_rooty() + canvas.winfo_height()))
        if len(filepaths) == 0:
            image.save("{}file_000.jpg".format(savefolder+'/'))
        else:
            string = filepaths[-1]
            first_index = string.find("_", string.find("file_"))
            last_digits = string[first_index+1: first_index+4]
            image.save("{}file_{:03d}.jpg".format(savefolder+'/', int(last_digits)+1))

# Точка в меcте клика и вырисовка линии
def click(event):
    global cnt, tmp1, tmp2, im, screen_name_jpg, line, text_line
    if cnt == 0 or cnt == 2:
        cnt = 0
        tmp1.clear()
        tmp2.clear()
        canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3,
                      fill="#FF0000", activefill="#00FF00")
        tmp1.extend((event.x, event.y, event.x, event.y))
        print(tmp1)
        cnt += 1
    elif cnt == 1:
        canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3,
                      fill="#FF0000", activefill="#00FF00")
        tmp2.extend((event.x, event.y, event.x, event.y))
        print(tmp2)
        line = canvas.create_line(tmp1[0], tmp1[1], event.x, event.y)
        text_line = canvas.create_text((sum((tmp1[0], event.x))/2)+15, (sum((tmp1[1], event.y))/2)+10,
                      text=linelen(tmp1[0], event.x, tmp1[1], event.y))
        cnt += 1


    print("x: {}, y: {}".format(event.x, event.y))

# Расчёт расстояния
def linelen(x1, x2, y1, y2):
    return "{0:.2f} mm".format(float((sqrt((x2-x1)**2+(y2-y1)**2))*float(txtvar.get())))

# Удаление всех элементов
def clear_items():
    canvas.delete(tk.ALL)

# Ф-ция чтобы удалить запоминание места сохранения
def del_config():
    os.remove('config.txt')

# Ф-ция для передвижения точек
def move_item(event):
    item_teg = tk.CURRENT
    canvas.coords(item_teg, event.x - 3, event.y - 3, event.x + 3, event.y + 3)
    canvas.delete(line)
    canvas.delete(text_line)
    canvas.bind('<ButtonRelease-3>', create_line)

# Ф-ция, перед перемещением получаем координаты для сравнения, чтобы понимать какую точку двигаем
def info(event):
    global x_y_current
    item_teg = tk.CURRENT
    x_y_current = canvas.coords(item_teg)
    x_y_current = x_y_current[0] + 3, x_y_current[1] + 3, x_y_current[2] - 3, x_y_current[3] - 3
    x_y_current = list(map(int, x_y_current))
    print(x_y_current)

# Ф-ция, после передвижения точки строит линию и перезаписывает координаты точки
def create_line(event):
    global line, text_line
    if x_y_current[0] == tmp2[0]:
        line = canvas.create_line((tmp1[0], tmp1[1], event.x, event.y))
        text_line = canvas.create_text((sum((tmp1[0], event.x)) / 2) + 15, (sum((tmp1[1], event.y)) / 2) + 10,
                                       text=linelen(tmp1[0], event.x, tmp1[1], event.y))
        tmp2.clear()
        x_y_current.clear()
        tmp2.extend((event.x, event.y, event.x, event.y))
    elif x_y_current[0] == tmp1[0]:
        line = canvas.create_line((tmp2[0], tmp2[1], event.x, event.y))
        text_line = canvas.create_text((sum((tmp2[0], event.x)) / 2) + 15, (sum((tmp2[1], event.y)) / 2) + 10,
                                       text=linelen(tmp2[0], event.x, tmp2[1], event.y))
        tmp1.clear()
        x_y_current.clear()
        tmp1.extend((event.x, event.y, event.x, event.y))

# Ф-ция для удаления объектов
def delete_item(event):
    item_teg = tk.CURRENT
    canvas.delete(item_teg, event.x - 3, event.y - 3, event.x + 3, event.y + 3)

# Вызов ф-ции для начала работы с кадром
jpg_camera()

# Кнопка для открытия файла
open_btn = tk.Button(screen, text="Открыть файл", image=pixelVirtual,
                          width=150,
                          height=20,
                          compound="c", command=openfile)
open_btn.place(x=640, y=0)

# Кнопка для сохранения файла
save_btn = tkinter.Button(text="Сохранить в файл", image=pixelVirtual,
                          width=150,
                          height=20,
                          compound="c", command=savefile)
save_btn.place(x=640, y=30)


# Кнопка чтобы удалить запоминание места сохранения
del_config_btn = tk.Button(screen, text="Удалить привязку", image=pixelVirtual,
                          width=150,
                          height=20,
                          compound="c", command=del_config)
del_config_btn.place(x=640, y=60)

# Кнопка для очистки окна
clear_btn = tk.Button(screen, text="Удалить ВСЕ элементы", image=pixelVirtual,
                          width=150,
                          height=20,
                          compound="c", command=clear_items)
clear_btn.place(x=640, y=90)

# Поле ввода кол-ва мм в пкс
ent = tk.Entry(screen, textvariable=txtvar)
ent.insert(0, "Тут пкс в мм надо")
ent.place(x=642, y=120)

# Определение размера окна
im = Image.open(screen_name_jpg)
(width_screen, height_screen) = im.size
print("Разрешение изображения:", im.size)

screen.geometry('800x481')
canvas = tk.Canvas(screen, width = width_screen, height = height_screen)
canvas.pack()
photo = ImageTk.PhotoImage(im)
canvas.create_image(0, 0, anchor = 'nw', image = photo)
canvas.place(x = 0, y = 0)
canvas.bind('<Button-1>', click)
canvas.bind('<B3-Motion>', move_item)
canvas.bind('<Button-3>', info)
canvas.bind('<Button-2>', delete_item)
screen.mainloop()

'''
#Сохранение элемента
def save_screen():
    global im, screen_name_jpg
    box = (canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(),
           canvas.winfo_rooty() + canvas.winfo_height())
    im = ImageGrab.grab(bbox=box)
    im.save(screen_name_jpg)

save_btn = tk.Button(screen, text="Сохранить элементы",
                              command=save_screen)
save_btn.place(x=150, y=480)

'''
