import tkinter
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os

from Range import Range_main
from Settin import Settin_main
from translate import translate_main


def UI_main():

    path = os.getcwd() + '\\config\\'
    file = open (path+'Init.txt')
    string = file.read().split(',')
    height = int(string[9]) * 21
    font_size,font_name = string[-1:-3:-1]

    window = tkinter.Tk()
    window.wm_attributes('-topmost',1)
    window.geometry('800x%s'%(115+height))
    window.iconbitmap(path+'图标.ico')
    window.title(' 团子翻译器 ver 2.0 --- By：胖次团子    交流群①：779594427   交流群②：1038904947    更新时间：2020-02-06')
    window.resizable(0,0)

    canvas = tkinter.Canvas(window, width=10000, height=10000, bg='white')
    image = Image.open(path+'背景.gif')
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, -300, image=photo, anchor='nw')
    canvas.pack()

    font = tkFont.Font(family=font_name,size=int(font_size))
    Text = tkinter.Text(window, font=font)
    Text.place(x=15, y=15, width=680, height=height+84)

    Text.tag_add('pink',tkinter.END)
    Text.tag_config('pink', foreground='#FF69B4')
    
    Text.tag_add('blue',tkinter.END)
    Text.tag_config('blue', foreground='blue')
    
    Text.tag_add('red',tkinter.END)
    Text.tag_config('red', foreground='red')

    Text.tag_add('yellow',tkinter.END)
    Text.tag_config('yellow', foreground='yellow')

    Text.tag_add('green',tkinter.END)
    Text.tag_config('green', foreground='green')

    Text.tag_add('orange',tkinter.END)
    Text.tag_config('orange', foreground='orange')

    Text.tag_add('cyan',tkinter.END)
    Text.tag_config('cyan', foreground='cyan')

    Text.tag_add('purple',tkinter.END)
    Text.tag_config('purple', foreground='purple')

    Text.tag_add('black',tkinter.END)
    Text.tag_config('black', foreground='black')


    scrollbar = tkinter.Scrollbar(Text, command=Text.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    Text.config(yscrollcommand=scrollbar.set)

    tkinter.Button(window, text="翻译", width=7, height=1, command=lambda:translate_main(Text,window)).place(x=720, y=8, anchor='nw')
    tkinter.Button(window, text="设置", width=7, height=1, command=lambda:Settin_main(window)).place(x=720, y=43, anchor='nw')
    tkinter.Button(window, text="范围", width=7, height=1, command=lambda:Range_main(window)).place(x=720, y=78, anchor='nw')

    window.mainloop()