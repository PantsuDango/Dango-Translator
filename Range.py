import interface

import tkinter
import tkinter.messagebox

from os import startfile

from PIL import Image, ImageTk, ImageGrab


def get_Coordinates():

    startfile('.\\config\\获取屏幕坐标.exe')


def get_image(X1,Y1,X2,Y2):
    
    x1 = X1.get(1.0,'end').replace('\n','').replace(' ','')
    y1 = Y1.get(1.0,'end').replace('\n','').replace(' ','')
    x2 = X2.get(1.0,'end').replace('\n','').replace(' ','')
    y2 = Y2.get(1.0,'end').replace('\n','').replace(' ','')

    try:
        bbox = (int(x1), int(y1), int(x2), int(y2))
        image = ImageGrab.grab(bbox)
        image.save('.\\config\\image.png')
        startfile('.\\config\\image.png')
    except Exception:
        tkinter.messagebox.showerror(title='error', message='坐标错误！')


def Range_save(X1,Y1,X2,Y2,game_name,sign,coordinates_window):

    x1 = X1.get(1.0,'end').replace(' ','').replace('\n','')
    y1 = Y1.get(1.0,'end').replace(' ','').replace('\n','')
    x2 = X2.get(1.0,'end').replace(' ','').replace('\n','')
    y2 = Y2.get(1.0,'end').replace(' ','').replace('\n','')
    game_name = game_name.get(1.0,'end').replace('\n','')

    data = interface.get_config()
    data['coordinate'][sign]['X1'] = x1
    data['coordinate'][sign]['Y1'] = y1
    data['coordinate'][sign]['X2'] = x2
    data['coordinate'][sign]['Y2'] = y2
    data['coordinate'][sign]['name'] = game_name
    interface.save_config(data)

    coordinates_window.destroy()


def sure(var,Range_window):

    data = interface.get_config()
    data['coordinate']['Type'] = str(var.get())
    interface.save_config(data)

    Range_window.destroy()


def coordinates_UI(sign,Range_window):

    Range_window.destroy()
    
    if sign == 'One':
        title = '坐标一设定'
    elif sign == 'Two':
        title = '坐标二设定'
    elif sign == 'Three':
        title = '坐标三设定'
    elif sign == 'Four':
        title = '坐标四设定'

    coordinates_window = tkinter.Tk()
    coordinates_window.wm_attributes('-topmost',1)
    interface.window_center(coordinates_window,260,260)
    coordinates_window.iconbitmap('.\\config\\图标.ico')
    coordinates_window.title(title)
    #coordinates_window.resizable(0,0)

    tkinter.Label(coordinates_window , text='游戏名：').place(x=20, y=10, anchor='nw')
    game_name = tkinter.Text(coordinates_window, width=22, height=1)
    game_name.place(x=75, y=14) 


    tkinter.Label(coordinates_window , text='文本框左上角坐标：').place(x=20, y=40, anchor='nw')
   
    tkinter.Label(coordinates_window , text='X1：').place(x=20, y=60, anchor='nw')
    X1 = tkinter.Text(coordinates_window, width=10, height=1)
    X1.place(x=40, y=64)  
    
    tkinter.Label(coordinates_window , text='Y1：').place(x=130, y=60, anchor='nw')
    Y1 = tkinter.Text(coordinates_window, width=10, height=1)
    Y1.place(x=160, y=64)

    tkinter.Label(coordinates_window , text='文本框右下角坐标：').place(x=20, y=90, anchor='nw')
    
    tkinter.Label(coordinates_window , text='X2：').place(x=20, y=110, anchor='nw')
    X2 = tkinter.Text(coordinates_window, width=10, height=1)
    X2.place(x=40, y=114)
    
    tkinter.Label(coordinates_window , text='Y2：').place(x=130, y=110, anchor='nw')
    Y2 = tkinter.Text(coordinates_window, width=10, height=1)
    Y2.place(x=160, y=114)

    data = interface.get_config()['coordinate'][sign]
    X1.insert(0.0,data['X1'])
    Y1.insert(0.0,data['Y1'])
    X2.insert(0.0,data['X2'])
    Y2.insert(0.0,data['Y2'])
    game_name.insert(0.0,data['name'])

    tkinter.Label(coordinates_window , text='*填入获取到的坐标值，保存后生效').place(x=20, y=140, anchor='nw')

    tkinter.Button(coordinates_window, text="获取坐标", width=7, height=1, command=get_Coordinates).place(x=45, y=170, anchor='nw')
    tkinter.Button(coordinates_window, text="查看效果", width=7, height=1, command=lambda:get_image(X1,Y1,X2,Y2)).place(x=150, y=170, anchor='nw')
    tkinter.Button(coordinates_window, text="保存", width=7, height=1, command=lambda:Range_save(X1,Y1,X2,Y2,game_name,sign,coordinates_window)).place(x=45, y=210, anchor='nw')
    tkinter.Button(coordinates_window, text="取消", width=7, height=1, command=coordinates_window.destroy).place(x=150, y=210, anchor='nw')
    
    coordinates_window.mainloop()
    range_UI()


def range_UI():

    Range_window = tkinter.Tk()
    Range_window.wm_attributes('-topmost',1)
    interface.window_center(Range_window,260,270)
    Range_window.iconbitmap('.\\config\\图标.ico')
    Range_window.title('翻译范围设置')
    #Range_window.resizable(0,0)

    frame = tkinter.Frame(Range_window).pack()
    var = tkinter.StringVar()
    data = interface.get_config()
    var.set(data['coordinate']['Type'])
    
    tkinter.Label(Range_window , text='选择要使用的坐标：').place(x=20, y=10, anchor='nw')
    tkinter.Radiobutton(frame, text='使用坐标一', variable=var, value='One').place(x=20, y=40, anchor='nw')
    tkinter.Button(Range_window, text="坐标一设定", width=10, height=1, command=lambda:coordinates_UI('One',Range_window)).place(x=150, y=40, anchor='nw')

    tkinter.Radiobutton(frame, text='使用坐标二', variable=var, value='Two').place(x=20, y=80, anchor='nw')
    tkinter.Button(Range_window, text="坐标二设定", width=10, height=1, command=lambda:coordinates_UI('Two',Range_window)).place(x=150, y=80, anchor='nw')

    tkinter.Radiobutton(frame, text='使用坐标三', variable=var, value='Three').place(x=20, y=120, anchor='nw')
    tkinter.Button(Range_window, text="坐标三设定", width=10, height=1, command=lambda:coordinates_UI('Three',Range_window)).place(x=150, y=120, anchor='nw')

    tkinter.Radiobutton(frame, text='使用坐标四', variable=var, value='Four').place(x=20, y=160, anchor='nw')
    tkinter.Button(Range_window, text="坐标四设定", width=10, height=1, command=lambda:coordinates_UI('Four',Range_window)).place(x=150, y=160, anchor='nw')

    tkinter.Button(Range_window, text="确定", width=7, height=1, command=lambda:sure(var,Range_window)).place(x=45, y=210, anchor='nw')
    tkinter.Button(Range_window, text="取消", width=7, height=1, command=Range_window.destroy).place(x=150, y=210, anchor='nw')
    
    Range_window.mainloop()


def range_main(window):
    
    window.destroy()
    range_UI()
    interface.interface_main()