import tkinter
from PIL import Image, ImageTk
import os
import UI


def Baidu_API_save(APP_ID,password,Baidu_API_window):

    API_Key = APP_ID.get(1.0,'end').replace('\n','').replace(' ','')
    Secret_Key = password.get(1.0,'end').replace('\n','').replace(' ','')

    path = os.getcwd() + '\\config\\'
    with open(path+'Baidu_Key.txt', 'w') as file:
        file.write('%s,%s'%(API_Key,Secret_Key))

    Baidu_API_window.destroy()


def Baidu_API():

    path = os.getcwd() + '\\config\\'
    with open(path+'Baidu_Key.txt') as file:
        API_Key,Secret_Key = file.read().split(',')

    Baidu_API_window = tkinter.Tk()
    Baidu_API_window.wm_attributes('-topmost',1)
    Baidu_API_window.geometry('260x180')
    Baidu_API_window.iconbitmap(path+'图标.ico')
    Baidu_API_window.title('百度翻译API设定')

    tkinter.Label(Baidu_API_window , text='APP ID：').place(x=20, y=10, anchor='nw')
    APP_ID = tkinter.Text(Baidu_API_window, width=30, height=1)
    APP_ID.place(x=20, y=34)

    tkinter.Label(Baidu_API_window, text='密钥：').place(x=20, y=60, anchor='nw')
    password = tkinter.Text(Baidu_API_window, width=30, height=1)
    password.place(x=20, y=84)

    tkinter.Button(Baidu_API_window, text="保存", width=7, height=1, command=lambda:Baidu_API_save(APP_ID,password,Baidu_API_window)).place(x=45, y=125, anchor='nw')
    tkinter.Button(Baidu_API_window, text="取消", width=7, height=1, command=Baidu_API_window.destroy).place(x=150, y=125, anchor='nw')

    APP_ID.insert(0.0,API_Key)
    password.insert(0.0,Secret_Key)

    Baidu_API_window.mainloop()


def Tencent_API_save(APP_ID,password,Tencent_API_window):

    API_Key = APP_ID.get(1.0,'end').replace('\n','').replace(' ','')
    Secret_Key = password.get(1.0,'end').replace('\n','').replace(' ','')

    path = os.getcwd() + '\\config\\'
    with open(path+'Tencent_Key.txt', 'w') as file:
        file.write('%s,%s'%(API_Key,Secret_Key))

    Tencent_API_window.destroy()


def Tencent_API():

    path = os.getcwd() + '\\config\\'
    with open(path+'Tencent_Key.txt') as file:
        API_Key,Secret_Key = file.read().split(',')

    Tencent_API_window = tkinter.Tk()
    Tencent_API_window.wm_attributes('-topmost',1)
    Tencent_API_window.geometry('310x180')
    Tencent_API_window.iconbitmap(path+'图标.ico')
    Tencent_API_window.title('腾讯翻译API设定')

    tkinter.Label(Tencent_API_window , text='SecretId：').place(x=20, y=10, anchor='nw')
    APP_ID = tkinter.Text(Tencent_API_window, width=37, height=1)
    APP_ID.place(x=20, y=34)

    tkinter.Label(Tencent_API_window, text='SecretKey：').place(x=20, y=60, anchor='nw')
    password = tkinter.Text(Tencent_API_window, width=37, height=1)
    password.place(x=20, y=84)

    tkinter.Button(Tencent_API_window, text="保存", width=7, height=1, command=lambda:Tencent_API_save(APP_ID,password,Tencent_API_window)).place(x=55, y=125, anchor='nw')
    tkinter.Button(Tencent_API_window, text="取消", width=7, height=1, command=Tencent_API_window.destroy).place(x=160, y=125, anchor='nw')

    APP_ID.insert(0.0,API_Key)
    password.insert(0.0,Secret_Key)

    Tencent_API_window.mainloop()


def Settin_save(API_Key_Entry,Secret_Key_Entry,Settin_window,var1,var2,time_Scale,var4):

    API_Key = API_Key_Entry.get(1.0,'end').replace('\n','').replace(' ','')
    Secret_Key = Secret_Key_Entry.get(1.0,'end').replace('\n','').replace(' ','')

    path = os.getcwd() + '\\config\\'
    with open(path+'ORC_Key.txt', 'w') as file:
        file.write('%s,%s'%(API_Key,Secret_Key))

    var1 = var1.get()
    var2 = var2.get()
    time = time_Scale.get()
    var4 = var4.get()
    with open(path+'Init.txt', 'w') as file:
        file.write('%s,%s,%s,%s'%(var1,var2,time,var4))

    Settin_window.destroy()


def Settin_UI(API_Key,Secret_Key,value1,value2,value3,value4):

    path = os.getcwd() + '\\config\\'
    Settin_window = tkinter.Tk()
    Settin_window.wm_attributes('-topmost',1)
    Settin_window.geometry('320x430')
    Settin_window.iconbitmap(path+'图标.ico')
    Settin_window.title('设置')

    tkinter.Label(Settin_window, text='ORC API Key：').place(x=20, y=10, anchor='nw')
    API_Key_Entry = tkinter.Text(Settin_window, width=38, height=1)
    API_Key_Entry.place(x=20, y=35, anchor='nw')

    tkinter.Label(Settin_window, text='ORC Secret Key：').place(x=20, y=60, anchor='nw')
    Secret_Key_Entry = tkinter.Text(Settin_window, width=38, height=1)
    Secret_Key_Entry.place(x=20, y=80, anchor='nw')

    tkinter.Label(Settin_window, text='翻译源设定：').place(x=20, y=110, anchor='nw')
    frame1 = tkinter.Frame(Settin_window).pack()
    var1 = tkinter.IntVar()
    tkinter.Radiobutton(frame1, text='有道翻译', variable=var1, value=1,).place(x=20, y=135, anchor='nw')
    
    tkinter.Radiobutton(frame1, text='百度翻译', variable=var1, value=2,).place(x=120, y=135, anchor='nw')
    tkinter.Button(Settin_window, text="设定", width=7, height=1, command=Baidu_API).place(x=130, y=165, anchor='nw')

    tkinter.Radiobutton(frame1, text='腾讯翻译', variable=var1, value=3,).place(x=220, y=135, anchor='nw')
    tkinter.Button(Settin_window, text="设定", width=7, height=1, command=Tencent_API).place(x=230, y=165, anchor='nw')

    var1.set(int(value1))

    tkinter.Label(Settin_window, text='翻译方式设定：').place(x=20, y=200, anchor='nw')

    frame2 = tkinter.Frame(Settin_window).pack()
    var2 = tkinter.IntVar()
    tkinter.Radiobutton(frame2, text='手动翻译（建议）', variable=var2, value=1,).place(x=20, y=225, anchor='nw')
    tkinter.Radiobutton(frame2, text='自动翻译', variable=var2, value=2,).place(x=170, y=225, anchor='nw')
    var2.set(int(value2))

    frame3 = tkinter.Frame(Settin_window).pack()
    var3=tkinter.IntVar()
    tkinter.Label(Settin_window, text='自动时的翻译频率设定（秒）：').place(x=20, y=260, anchor='nw')
    time_Scale = tkinter.Scale(frame3, from_=2, to=10, orient=tkinter.HORIZONTAL, variable=var3, length=270, showvalue=0,tickinterval=1, resolution=1)
    time_Scale.place(x=20, y=285, anchor='nw')
    var3.set(int(value3))

    frame4 = tkinter.Frame(Settin_window).pack()
    var4=tkinter.IntVar()    
    Checkbutton = tkinter.Checkbutton(frame4, text='是否显示原文',variable=var4, onvalue=1, offvalue=0).place(x=20, y=330, anchor='nw')
    var4.set(int(value4))

    tkinter.Button(Settin_window, text="保存", width=7, height=1, command=lambda:Settin_save(API_Key_Entry,Secret_Key_Entry,Settin_window,var1,var2,time_Scale,var4)).place(x=70, y=365, anchor='nw')
    tkinter.Button(Settin_window, text="取消", width=7, height=1, command=Settin_window.destroy).place(x=170, y=365, anchor='nw')

    API_Key_Entry.insert(0.0,API_Key)
    Secret_Key_Entry.insert(0.0,Secret_Key)

    Settin_window.mainloop()


def Settin_main(window):

    window.destroy()
    path = os.getcwd() + '\\config\\'
    with open(path+'ORC_Key.txt') as file:
        API_Key,Secret_Key = file.read().split(',')

    with open(path+'Init.txt') as file:
        value1,value2,value3,value4 = file.read().split(',')

    Settin_UI(API_Key,Secret_Key,value1,value2,value3,value4)
    UI.UI_main()