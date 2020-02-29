import tkinter
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os

from Range import Range_main
from Settin import Settin_main
from translate import translate_main


def UI_main():

    path = os.getcwd() + '\\config\\'

    window = tkinter.Tk()
    window.wm_attributes('-topmost',1)
    window.geometry('600x115')
    window.iconbitmap(path+'图标.ico')
    window.title(' Galgame翻译器 ver 1.0 --- By：胖次团子     交流群：779594427')

    canvas = tkinter.Canvas(window, width=600, height=115, bg='white')
    image = Image.open(path+'背景.gif')
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(540, 220, image=photo)
    canvas.pack()

    tkinter.Button(window, text="翻译", width=7, height=1, command=lambda:translate_main(Text,window)).place(x=520, y=8, anchor='nw')
    tkinter.Button(window, text="设置", width=7, height=1, command=lambda:Settin_main(window)).place(x=520, y=43, anchor='nw')
    tkinter.Button(window, text="范围", width=7, height=1, command=lambda:Range_main(window)).place(x=520, y=78, anchor='nw')

    font = tkFont.Font(family='华康方圆体W7',size=15)
    Text = tkinter.Text(window, fg='#FF69B4', font=font)
    Text.place(x=15, y=15, width=480, height=85)

    scrollbar = tkinter.Scrollbar(Text, command=Text.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    Text.config(yscrollcommand=scrollbar.set)

    window.mainloop()