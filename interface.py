import tkinter
import tkinter.font as tkFont
from PIL import Image, ImageTk
import json

from range import range_main
from settin import settin_main
from translate import translate_main


def get_config():

    with open('.\\config\\init.json') as file:
        return json.load(file)


def save_config(data):

    with open('.\\config\\init.json','w') as file:
        json.dump(data,file)


def text_colour_tag(Text):

    colours = ('pink','blue','red','yellow','green','orange','cyan','purple','black')
    for colour in colours:
        Text.tag_add(colour,tkinter.END)
        if colour == 'pink':
            Text.tag_config(colour, foreground='#FF69B4')
        else:
            Text.tag_config(colour, foreground=colour)


def window_center(window,width,height):
    
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    x = (screenwidth-width) / 2
    y = (screenheight-height) / 2
    window.geometry("%dx%d+%d+%d" %(width,height,x,y))


def interface_main():

    data = get_config()
    height = int(data['TextSize']) * 21
    font_name = data['Font']
    font_size = int(data['FontSize'])
    data['sign'] = 1
    save_config(data)
    
    window = tkinter.Tk()
    window.wm_attributes('-topmost',1)
    window_center(window,800,115+height)
    window.iconbitmap('.\\config\\图标.ico')
    window.title(' 团子翻译器 ver 2.1 --- By：胖次团子    交流群①：779594427   交流群②：1038904947    更新时间：2020-02-10')
    #window.resizable(0,0)
    
    canvas = tkinter.Canvas(window, width=10000, height=10000, bg='white')
    image = Image.open('.\\config\\背景.gif')
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, -300, image=photo, anchor='nw')
    canvas.pack()

    font = tkFont.Font(family=font_name, size=font_size)
    Text = tkinter.Text(window, font=font)
    Text.place(x=15, y=15, width=680, height=height+84)
    text_colour_tag(Text)

    scrollbar = tkinter.Scrollbar(Text, command=Text.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    Text.config(yscrollcommand=scrollbar.set)

    Mode = data['Mode']
    if Mode == '1':
        tkinter.Button(window, text="翻译", width=10, height=1, command=lambda:translate_main(Text,window)).place(x=707, y=8, anchor='nw')
    else:
        tkinter.Button(window, text="开始 / 停止", width=10, height=1, command=lambda:translate_main(Text,window)).place(x=707, y=8, anchor='nw')

    tkinter.Button(window, text="设置", width=10, height=1, command=lambda:settin_main(window)).place(x=707, y=43, anchor='nw')
    tkinter.Button(window, text="范围", width=10, height=1, command=lambda:range_main(window)).place(x=707, y=78, anchor='nw')
    
    window.mainloop()