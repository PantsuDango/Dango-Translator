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


def get_image(X1,Y1,X2,Y2):
    
    path = os.getcwd() + '\\config\\'

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


def Range_save(X1,Y1,X2,Y2,Range_window):

    x1 = X1.get(1.0,'end').replace('\n','').replace(' ','')
    y1 = Y1.get(1.0,'end').replace('\n','').replace(' ','')
    x2 = X2.get(1.0,'end').replace('\n','').replace(' ','')
    y2 = Y2.get(1.0,'end').replace('\n','').replace(' ','')

    path = os.getcwd() + '\\config\\'
    with open(path+'屏幕坐标.txt', 'w') as file:
        file.write('%s,%s,%s,%s'%(x1,y1,x2,y2))

    Range_window.destroy()


def Range_UI(x1,y1,x2,y2):

    path = os.getcwd() + '\\config\\'

    Range_window = tkinter.Tk()
    Range_window.wm_attributes('-topmost',1)
    Range_window.geometry('260x230')
    Range_window.iconbitmap(path+'图标.ico')
    Range_window.title('翻译范围设置')

    tkinter.Label(Range_window , text='文本框左上角坐标：').place(x=20, y=10, anchor='nw')
   
    tkinter.Label(Range_window , text='X1：').place(x=20, y=30, anchor='nw')
    X1 = tkinter.Text(Range_window, width=10, height=1)
    X1.place(x=40, y=34)  
    
    tkinter.Label(Range_window , text='Y1：').place(x=130, y=30, anchor='nw')
    Y1 = tkinter.Text(Range_window, width=10, height=1)
    Y1.place(x=160, y=34)

    tkinter.Label(Range_window , text='文本框右下角坐标：').place(x=20, y=60, anchor='nw')
    
    tkinter.Label(Range_window , text='X2：').place(x=20, y=80, anchor='nw')
    X2 = tkinter.Text(Range_window, width=10, height=1)
    X2.place(x=40, y=84)
    
    tkinter.Label(Range_window , text='Y2：').place(x=130, y=80, anchor='nw')
    Y2 = tkinter.Text(Range_window, width=10, height=1)
    Y2.place(x=160, y=84)

    X1.insert(0.0,x1)
    Y1.insert(0.0,y1)
    X2.insert(0.0,x2)
    Y2.insert(0.0,y2)

    tkinter.Label(Range_window , text='*填入获取到的坐标值，保存后生效').place(x=20, y=110, anchor='nw')

    tkinter.Button(Range_window, text="获取坐标", width=7, height=1, command=get_Coordinates).place(x=45, y=140, anchor='nw')
    tkinter.Button(Range_window, text="查看效果", width=7, height=1, command=lambda:get_image(X1,Y1,X2,Y2)).place(x=150, y=140, anchor='nw')
    tkinter.Button(Range_window, text="保存", width=7, height=1, command=lambda:Range_save(X1,Y1,X2,Y2,Range_window)).place(x=45, y=180, anchor='nw')
    tkinter.Button(Range_window, text="取消", width=7, height=1, command=Range_window.destroy).place(x=150, y=180, anchor='nw')
    
    Range_window.mainloop()


def Range_main(window):
    
    window.destroy()
    path = os.getcwd() + '\\config\\'
    with open(path+'屏幕坐标.txt') as file:
        x1,y1,x2,y2 = file.read().split(',')

    Range_UI(x1,y1,x2,y2)
    UI.UI_main()