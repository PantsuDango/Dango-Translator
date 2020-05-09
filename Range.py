import tkinter
from PIL import Image, ImageTk
import os
import UI

from PIL import ImageGrab
import tkinter
import tkinter.messagebox


def get_Coordinates():

    path = os.getcwd() + '\\config\\'
    os.startfile(path+'获取屏幕坐标.exe')


def get_image(X1,Y1,X2,Y2,path):
    
    x1 = int(X1.get(1.0,'end').replace('\n','').replace(' ',''))
    y1 = int(Y1.get(1.0,'end').replace('\n','').replace(' ',''))
    x2 = int(X2.get(1.0,'end').replace('\n','').replace(' ',''))
    y2 = int(Y2.get(1.0,'end').replace('\n','').replace(' ',''))

    try:
        bbox = (x1,y1,x2,y2)
        image = ImageGrab.grab(bbox)
        image.save(path+'image.png')
        os.startfile(path+'image.png')
    except Exception:
        tkinter.messagebox.showerror(title='error', message='坐标错误！')


def Range_save(X1,Y1,X2,Y2,game_name,sign,path,Coordinates_window):

    with open(path+'屏幕坐标.txt') as file:
        string = file.read().split('\n')

    x1 = X1.get(1.0,'end').replace('\n','').replace(' ','').replace(',','')
    y1 = Y1.get(1.0,'end').replace('\n','').replace(' ','').replace(',','')
    x2 = X2.get(1.0,'end').replace('\n','').replace(' ','').replace(',','')
    y2 = Y2.get(1.0,'end').replace('\n','').replace(' ','').replace(',','')
    game_name = game_name.get(1.0,'end').replace('\n','').replace(',','，')

    string[sign] = '%s,%s,%s,%s,%s'%(x1,y1,x2,y2,game_name)
    string = '\n'.join(string)

    with open(path+'屏幕坐标.txt', 'w') as file:
        file.write(string)

    Coordinates_window.destroy()


def sure(path,var,Range_window):

    with open(path+'屏幕坐标.txt') as file:
        string = file.read().split('\n')

    string[0] = str(var.get())
    string = '\n'.join(string)
    with open(path+'屏幕坐标.txt', 'w') as file:
        file.write(string)

    Range_window.destroy()


def Coordinates_UI(path,sign):

    with open(path+'屏幕坐标.txt') as file:
        string = file.read().split('\n')

    if sign == 1:
        title = '坐标一设定'
    elif sign == 2:
        title = '坐标二设定'
    elif sign == 3:
        title = '坐标三设定'
    elif sign == 4:
        title = '坐标四设定'

    Coordinates_window = tkinter.Tk()
    Coordinates_window.wm_attributes('-topmost',1)
    Coordinates_window.geometry('260x260')
    Coordinates_window.iconbitmap(path+'图标.ico')
    Coordinates_window.title(title)
    Coordinates_window.resizable(0,0)

    tkinter.Label(Coordinates_window , text='游戏名：').place(x=20, y=10, anchor='nw')
    game_name = tkinter.Text(Coordinates_window, width=22, height=1)
    game_name.place(x=75, y=14) 


    tkinter.Label(Coordinates_window , text='文本框左上角坐标：').place(x=20, y=40, anchor='nw')
   
    tkinter.Label(Coordinates_window , text='X1：').place(x=20, y=60, anchor='nw')
    X1 = tkinter.Text(Coordinates_window, width=10, height=1)
    X1.place(x=40, y=64)  
    
    tkinter.Label(Coordinates_window , text='Y1：').place(x=130, y=60, anchor='nw')
    Y1 = tkinter.Text(Coordinates_window, width=10, height=1)
    Y1.place(x=160, y=64)

    tkinter.Label(Coordinates_window , text='文本框右下角坐标：').place(x=20, y=90, anchor='nw')
    
    tkinter.Label(Coordinates_window , text='X2：').place(x=20, y=110, anchor='nw')
    X2 = tkinter.Text(Coordinates_window, width=10, height=1)
    X2.place(x=40, y=114)
    
    tkinter.Label(Coordinates_window , text='Y2：').place(x=130, y=110, anchor='nw')
    Y2 = tkinter.Text(Coordinates_window, width=10, height=1)
    Y2.place(x=160, y=114)

    coordinates = string[sign].split(',')
    X1.insert(0.0,coordinates[0])
    Y1.insert(0.0,coordinates[1])
    X2.insert(0.0,coordinates[2])
    Y2.insert(0.0,coordinates[3])
    game_name.insert(0.0,coordinates[4])

    tkinter.Label(Coordinates_window , text='*填入获取到的坐标值，保存后生效').place(x=20, y=140, anchor='nw')

    tkinter.Button(Coordinates_window, text="获取坐标", width=7, height=1, command=get_Coordinates).place(x=45, y=170, anchor='nw')
    tkinter.Button(Coordinates_window, text="查看效果", width=7, height=1, command=lambda:get_image(X1,Y1,X2,Y2,path)).place(x=150, y=170, anchor='nw')
    tkinter.Button(Coordinates_window, text="保存", width=7, height=1, command=lambda:Range_save(X1,Y1,X2,Y2,game_name,sign,path,Coordinates_window)).place(x=45, y=210, anchor='nw')
    tkinter.Button(Coordinates_window, text="取消", width=7, height=1, command=Coordinates_window.destroy).place(x=150, y=210, anchor='nw')
    
    Coordinates_window.mainloop()


def Range_UI():

    path = os.getcwd() + '\\config\\'
    with open(path+'屏幕坐标.txt') as file:
        string = file.read().split('\n')

    Range_window = tkinter.Tk()
    Range_window.wm_attributes('-topmost',1)
    Range_window.geometry('260x270')
    Range_window.iconbitmap(path+'图标.ico')
    Range_window.title('翻译范围设置')
    Range_window.resizable(0,0)

    frame = tkinter.Frame(Range_window).pack()
    var = tkinter.IntVar()
    var.set(int(string[0]))
    
    tkinter.Label(Range_window , text='选择要使用的坐标：').place(x=20, y=10, anchor='nw')
    tkinter.Radiobutton(frame, text='使用坐标一', variable=var, value=1).place(x=20, y=40, anchor='nw')
    tkinter.Button(Range_window, text="坐标一设定", width=10, height=1, command=lambda:Coordinates_UI(path,1)).place(x=150, y=40, anchor='nw')

    tkinter.Radiobutton(frame, text='使用坐标二', variable=var, value=2).place(x=20, y=80, anchor='nw')
    tkinter.Button(Range_window, text="坐标二设定", width=10, height=1, command=lambda:Coordinates_UI(path,2)).place(x=150, y=80, anchor='nw')

    tkinter.Radiobutton(frame, text='使用坐标三', variable=var, value=3).place(x=20, y=120, anchor='nw')
    tkinter.Button(Range_window, text="坐标三设定", width=10, height=1, command=lambda:Coordinates_UI(path,3)).place(x=150, y=120, anchor='nw')

    tkinter.Radiobutton(frame, text='使用坐标四', variable=var, value=4).place(x=20, y=160, anchor='nw')
    tkinter.Button(Range_window, text="坐标四设定", width=10, height=1, command=lambda:Coordinates_UI(path,4)).place(x=150, y=160, anchor='nw')

    tkinter.Button(Range_window, text="确定", width=7, height=1, command=lambda:sure(path,var,Range_window)).place(x=45, y=210, anchor='nw')
    tkinter.Button(Range_window, text="取消", width=7, height=1, command=Range_window.destroy).place(x=150, y=210, anchor='nw')
    
    Range_window.mainloop()


def Range_main(window):
    
    window.destroy()
    Range_UI()
    UI.UI_main()