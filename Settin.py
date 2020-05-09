import tkinter
from tkinter import font
from PIL import Image, ImageTk
import os
import UI
import webbrowser

from translate import get_Access_Token


def Baidu_API_save(APP_ID,password,Baidu_API_window):

    API_Key = APP_ID.get(1.0,'end').replace('\n','').replace(' ','')
    Secret_Key = password.get(1.0,'end').replace('\n','').replace(' ','')

    path = os.getcwd() + '\\config\\'
    with open(path+'Baidu_Key.txt', 'w') as file:
        file.write('%s,%s'%(API_Key,Secret_Key))

    Baidu_API_window.destroy()


def select_baidu():

    url = 'https://api.fanyi.baidu.com/api/trans/product/desktop'
    try:
        webbrowser.open(url, new=0, autoraise=True)
    except Exception:
        pass


def register_baidu():

    try:
        os.startfile('百度翻译API注册方法.docx')
    except Exception:
        pass


def Baidu_API():

    path = os.getcwd() + '\\config\\'
    with open(path+'Baidu_Key.txt') as file:
        API_Key,Secret_Key = file.read().split(',')

    Baidu_API_window = tkinter.Tk()
    Baidu_API_window.wm_attributes('-topmost',1)
    Baidu_API_window.geometry('260x330')
    Baidu_API_window.iconbitmap(path+'图标.ico')
    Baidu_API_window.title('百度翻译API设定')
    Baidu_API_window.resizable(0,0)

    tkinter.Label(Baidu_API_window , text='APP ID：').place(x=20, y=10, anchor='nw')
    APP_ID = tkinter.Text(Baidu_API_window, width=30, height=1)
    APP_ID.place(x=20, y=34)

    tkinter.Label(Baidu_API_window, text='密钥：').place(x=20, y=60, anchor='nw')
    password = tkinter.Text(Baidu_API_window, width=30, height=1)
    password.place(x=20, y=84)

    tkinter.Label(Baidu_API_window , text='说明：').place(x=20, y=105, anchor='nw')
    tkinter.Label(Baidu_API_window , text='1、百度翻译每月免费额度为200万字符').place(x=20, y=125, anchor='nw')
    tkinter.Label(Baidu_API_window , text='     于每月1日更新额度').place(x=20, y=145, anchor='nw')
    tkinter.Label(Baidu_API_window , text='2、如超出额度请自行注册新的API，否').place(x=20, y=170, anchor='nw')
    tkinter.Label(Baidu_API_window , text='     则会计费').place(x=20, y=190, anchor='nw')
    
    tkinter.Button(Baidu_API_window, text="注册方法", width=10, height=1, command=register_baidu).place(x=30, y=220, anchor='nw')
    tkinter.Button(Baidu_API_window, text="查询额度", width=10, height=1, command=select_baidu).place(x=140, y=220, anchor='nw')
    tkinter.Button(Baidu_API_window, text="保存", width=10, height=1, command=lambda:Baidu_API_save(APP_ID,password,Baidu_API_window)).place(x=30, y=265, anchor='nw')
    tkinter.Button(Baidu_API_window, text="取消", width=10, height=1, command=Baidu_API_window.destroy).place(x=140, y=265, anchor='nw')

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


def register_tencent():
    
    try:
        os.startfile('腾讯翻译API注册方法.docx')
    except Exception:
        pass

def select_tencent():
    
    url = 'https://console.cloud.tencent.com/tmt'
    try:
        webbrowser.open(url, new=0, autoraise=True)
    except Exception:
        pass   


def Tencent_API():

    path = os.getcwd() + '\\config\\'
    with open(path+'Tencent_Key.txt') as file:
        API_Key,Secret_Key = file.read().split(',')

    Tencent_API_window = tkinter.Tk()
    Tencent_API_window.wm_attributes('-topmost',1)
    Tencent_API_window.geometry('310x320')
    Tencent_API_window.iconbitmap(path+'图标.ico')
    Tencent_API_window.title('腾讯翻译API设定')
    Tencent_API_window.resizable(0,0)

    tkinter.Label(Tencent_API_window , text='SecretId：').place(x=20, y=10, anchor='nw')
    APP_ID = tkinter.Text(Tencent_API_window, width=37, height=1)
    APP_ID.place(x=20, y=34)

    tkinter.Label(Tencent_API_window, text='SecretKey：').place(x=20, y=60, anchor='nw')
    password = tkinter.Text(Tencent_API_window, width=37, height=1)
    password.place(x=20, y=84)

    tkinter.Label(Tencent_API_window , text='说明：').place(x=20, y=105, anchor='nw')
    tkinter.Label(Tencent_API_window , text='1、腾讯翻译每月免费额度为500万字符，于每月').place(x=20, y=125, anchor='nw')
    tkinter.Label(Tencent_API_window , text='     1日更新额度').place(x=20, y=145, anchor='nw')
    tkinter.Label(Tencent_API_window , text='2、如超出额度请自行注册新的API，否则会计费').place(x=20, y=170, anchor='nw')
    
    tkinter.Button(Tencent_API_window, text="注册方法", width=10, height=1, command=register_tencent).place(x=50, y=205, anchor='nw')
    tkinter.Button(Tencent_API_window, text="查询额度", width=10, height=1, command=select_tencent).place(x=170, y=205, anchor='nw')
    tkinter.Button(Tencent_API_window, text="保存", width=10, height=1, command=lambda:Tencent_API_save(APP_ID,password,Tencent_API_window)).place(x=50, y=250, anchor='nw')
    tkinter.Button(Tencent_API_window, text="取消", width=10, height=1, command=Tencent_API_window.destroy).place(x=170, y=250, anchor='nw')

    APP_ID.insert(0.0,API_Key)
    password.insert(0.0,Secret_Key)

    Tencent_API_window.mainloop()


def Settin_save(API_Key_Entry,Secret_Key_Entry,Settin_window,var1_1,var1_2,var1_3,var2,time_Scale,var_original,var_youdao,var_baidu,var_tencent,var_height,var_font,var_font_size):

    API_Key = API_Key_Entry.get(1.0,'end').replace('\n','').replace(' ','')
    Secret_Key = Secret_Key_Entry.get(1.0,'end').replace('\n','').replace(' ','')

    path = os.getcwd() + '\\config\\'
    with open(path+'ORC_Key.txt', 'w') as file:
        file.write('%s,%s'%(API_Key,Secret_Key))
    get_Access_Token(path)

    var1_1 = var1_1.get()
    var1_2 = var1_2.get()
    var1_3 = var1_3.get()
    var2 = var2.get()
    time = time_Scale.get()
    original = var_original.get()
    youdao = var_youdao.get()
    baidu = var_baidu.get()
    tencent = var_tencent.get()
    
    height = var_height.get()
    font_name = var_font.get()
    font_size = var_font_size.get()

    with open(path+'Init.txt', 'w') as file:
        file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'%(var1_1,var1_2,var1_3,var2,time,original,youdao,baidu,tencent,height,font_name,font_size))

    Settin_window.destroy()


def Settin_UI(API_Key,Secret_Key,value1_1,value1_2,value1_3,value2,value3,original,youdao,baidu,tencent,height,font_name,font_size):

    path = os.getcwd() + '\\config\\'
    Settin_window = tkinter.Tk()
    Settin_window.wm_attributes('-topmost',1)
    Settin_window.geometry('320x530')
    Settin_window.iconbitmap(path+'图标.ico')
    Settin_window.title('设置')
    Settin_window.resizable(0,0)

    tkinter.Label(Settin_window, text='OCR API Key（必填）：').place(x=20, y=10, anchor='nw')
    API_Key_Entry = tkinter.Text(Settin_window, width=38, height=1)
    API_Key_Entry.place(x=20, y=35, anchor='nw')

    tkinter.Label(Settin_window, text='OCR Secret Key（必填）：').place(x=20, y=60, anchor='nw')
    Secret_Key_Entry = tkinter.Text(Settin_window, width=38, height=1)
    Secret_Key_Entry.place(x=20, y=80, anchor='nw')

    tkinter.Label(Settin_window, text='翻译源设定（可多选同时翻译）：').place(x=20, y=110, anchor='nw')
    frame1 = tkinter.Frame(Settin_window).pack()
    var1_1 = tkinter.IntVar()
    var1_2 = tkinter.IntVar()
    var1_3 = tkinter.IntVar()
    
    Checkbutton_1 = tkinter.Checkbutton(frame1, text='有道翻译', variable=var1_1, onvalue=1, offvalue=0)
    Checkbutton_1.place(x=20, y=135, anchor='nw')
    
    Checkbutton_2 = tkinter.Checkbutton(frame1, text='百度翻译', variable=var1_2, onvalue=1, offvalue=0)
    Checkbutton_2.place(x=120, y=135, anchor='nw')
    tkinter.Button(Settin_window, text="百度API", width=8, height=1, command=Baidu_API).place(x=125, y=165, anchor='nw')

    Checkbutton_3 = tkinter.Checkbutton(frame1, text='腾讯翻译', variable=var1_3, onvalue=1, offvalue=0)
    Checkbutton_3.place(x=220, y=135, anchor='nw')
    tkinter.Button(Settin_window, text="腾讯API", width=8, height=1, command=Tencent_API).place(x=225, y=165, anchor='nw')

    var1_1.set(int(value1_1))
    var1_2.set(int(value1_2))
    var1_3.set(int(value1_3))

    tkinter.Label(Settin_window, text='翻译方式设定：').place(x=20, y=200, anchor='nw')

    frame2 = tkinter.Frame(Settin_window).pack()
    var2 = tkinter.IntVar()
    tkinter.Radiobutton(frame2, text='手动翻译（建议）', variable=var2, value=1,).place(x=20, y=225, anchor='nw')
    tkinter.Radiobutton(frame2, text='自动翻译', variable=var2, value=2,).place(x=170, y=225, anchor='nw')
    var2.set(int(value2))

    frame3 = tkinter.Frame(Settin_window).pack()
    var3=tkinter.IntVar()
    tkinter.Label(Settin_window, text='自动翻译时的刷新频率设定（秒）：').place(x=20, y=260, anchor='nw')
    time_Scale = tkinter.Scale(frame3, from_=3, to=10, orient=tkinter.HORIZONTAL, variable=var3, length=270, showvalue=0,tickinterval=1, resolution=1)
    time_Scale.place(x=20, y=285, anchor='nw')
    var3.set(int(value3))
    
    tkinter.Label(Settin_window, text='翻译文本颜色设定：').place(x=20, y=330, anchor='nw')

    menubutton_original = tkinter.Menubutton(Settin_window, text='原文', width=5, height=1, relief="raised")
    menubutton_original.place(x=20, y=355, anchor='nw')
    var_original = tkinter.StringVar()
    var_original.set(original)
    color_menu_original = tkinter.Menu(menubutton_original, tearoff=False)
    color_menu_original.add_radiobutton(label='pink', variable=var_original, value='pink', foreground='#FF69B4')
    color_menu_original.add_radiobutton(label='blue', variable=var_original, value='blue', foreground='blue')
    color_menu_original.add_radiobutton(label='red', variable=var_original, value='red', foreground='red')
    color_menu_original.add_radiobutton(label='yellow', variable=var_original, value='yellow', foreground='yellow')
    color_menu_original.add_radiobutton(label='green', variable=var_original, value='green', foreground='green')
    color_menu_original.add_radiobutton(label='orange', variable=var_original, value='orange', foreground='orange')
    color_menu_original.add_radiobutton(label='cyan', variable=var_original, value='cyan', foreground='cyan')
    color_menu_original.add_radiobutton(label='purple', variable=var_original, value='purple', foreground='purple')
    color_menu_original.add_radiobutton(label='black', variable=var_original, value='black', foreground='black')
    menubutton_original.config(menu=color_menu_original)

    menubutton_youdao = tkinter.Menubutton(Settin_window, text='有道', width=5, height=1, relief="raised")
    menubutton_youdao.place(x=95, y=355, anchor='nw')
    var_youdao = tkinter.StringVar()
    var_youdao.set(youdao)
    color_menu_youdao = tkinter.Menu(menubutton_youdao, tearoff=False)
    color_menu_youdao.add_radiobutton(label='pink', variable=var_youdao, value='pink', foreground='#FF69B4')
    color_menu_youdao.add_radiobutton(label='blue', variable=var_youdao, value='blue', foreground='blue')
    color_menu_youdao.add_radiobutton(label='red', variable=var_youdao, value='red', foreground='red')
    color_menu_youdao.add_radiobutton(label='yellow', variable=var_youdao, value='yellow', foreground='yellow')
    color_menu_youdao.add_radiobutton(label='green', variable=var_youdao, value='green', foreground='green')
    color_menu_youdao.add_radiobutton(label='orange', variable=var_youdao, value='orange', foreground='orange')
    color_menu_youdao.add_radiobutton(label='cyan', variable=var_youdao, value='cyan', foreground='cyan')
    color_menu_youdao.add_radiobutton(label='purple', variable=var_youdao, value='purple', foreground='purple')
    color_menu_youdao.add_radiobutton(label='black', variable=var_youdao, value='black', foreground='black')
    menubutton_youdao.config(menu=color_menu_youdao)

    menubutton_baidu = tkinter.Menubutton(Settin_window, text='百度', width=5, height=1, relief="raised")
    menubutton_baidu.place(x=170, y=355, anchor='nw')
    var_baidu = tkinter.StringVar()
    var_baidu.set(baidu)
    color_menu_baidu = tkinter.Menu(menubutton_baidu, tearoff=False)
    color_menu_baidu.add_radiobutton(label='pink', variable=var_baidu, value='pink', foreground='#FF69B4')
    color_menu_baidu.add_radiobutton(label='blue', variable=var_baidu, value='blue', foreground='blue')
    color_menu_baidu.add_radiobutton(label='red', variable=var_baidu, value='red', foreground='red')
    color_menu_baidu.add_radiobutton(label='yellow', variable=var_baidu, value='yellow', foreground='yellow')
    color_menu_baidu.add_radiobutton(label='green', variable=var_baidu, value='green', foreground='green')
    color_menu_baidu.add_radiobutton(label='orange', variable=var_baidu, value='orange', foreground='orange')
    color_menu_baidu.add_radiobutton(label='cyan', variable=var_baidu, value='cyan', foreground='cyan')
    color_menu_baidu.add_radiobutton(label='purple', variable=var_baidu, value='purple', foreground='purple')
    color_menu_baidu.add_radiobutton(label='black', variable=var_baidu, value='black', foreground='black')
    menubutton_baidu.config(menu=color_menu_baidu)

    menubutton_tencent = tkinter.Menubutton(Settin_window, text='腾讯', width=5, height=1, relief="raised")
    menubutton_tencent.place(x=245, y=355, anchor='nw')
    var_tencent = tkinter.StringVar()
    var_tencent.set(tencent)
    color_menu_tencent = tkinter.Menu(menubutton_tencent, tearoff=False)
    color_menu_tencent.add_radiobutton(label='pink', variable=var_tencent, value='pink', foreground='#FF69B4')
    color_menu_tencent.add_radiobutton(label='blue', variable=var_tencent, value='blue', foreground='blue')
    color_menu_tencent.add_radiobutton(label='red', variable=var_tencent, value='red', foreground='red')
    color_menu_tencent.add_radiobutton(label='yellow', variable=var_tencent, value='yellow', foreground='yellow')
    color_menu_tencent.add_radiobutton(label='green', variable=var_tencent, value='green', foreground='green')
    color_menu_tencent.add_radiobutton(label='orange', variable=var_tencent, value='orange', foreground='orange')
    color_menu_tencent.add_radiobutton(label='cyan', variable=var_tencent, value='cyan', foreground='cyan')
    color_menu_tencent.add_radiobutton(label='purple', variable=var_tencent, value='purple', foreground='purple')
    color_menu_tencent.add_radiobutton(label='black', variable=var_tencent, value='black', foreground='black')
    menubutton_tencent.config(menu=color_menu_tencent)

    tkinter.Label(Settin_window, text='翻译框大小设定：').place(x=20, y=390, anchor='nw')
    
    menubutton_height = tkinter.Menubutton(Settin_window, text='宽度', width=5, height=1, relief="raised")
    menubutton_height.place(x=20, y=415, anchor='nw')
    var_height = tkinter.IntVar()
    var_height.set(int(height))
    menu_height = tkinter.Menu(menubutton_height, tearoff=False)
    menu_height.add_radiobutton(label='X1.00', variable=var_height, value=0)
    menu_height.add_radiobutton(label='X1.25', variable=var_height, value=1)
    menu_height.add_radiobutton(label='X1.50', variable=var_height, value=2)
    menu_height.add_radiobutton(label='X1.75', variable=var_height, value=3)
    menu_height.add_radiobutton(label='X2.00', variable=var_height, value=4)
    menu_height.add_radiobutton(label='X2.25', variable=var_height, value=5)
    menu_height.add_radiobutton(label='X2.50', variable=var_height, value=6)
    menu_height.add_radiobutton(label='X2.75', variable=var_height, value=7)
    menu_height.add_radiobutton(label='X3.00', variable=var_height, value=8)
    menubutton_height.config(menu=menu_height)

    tkinter.Label(Settin_window, text='翻译字体设定：').place(x=170, y=390, anchor='nw')
    
    menubutton_font = tkinter.Menubutton(Settin_window, text='样式', width=5, height=1, relief="raised")
    menubutton_font.place(x=170, y=415, anchor='nw')
    var_font = tkinter.StringVar()
    var_font.set(font_name)
    menu_font = tkinter.Menu(menubutton_font, tearoff=False)
    count = 1
    for font_name in font.families():
        if font_name[0] != '@':
            if count % 40 == 0:
                sign = True
            else:
                sign = False
            menu_font.add_radiobutton(label=font_name, variable=var_font, value=font_name, columnbreak=sign)
            count += 1
    menubutton_font.config(menu=menu_font)

    menubutton_font_size = tkinter.Menubutton(Settin_window, text='大小', width=5, height=1, relief="raised")
    menubutton_font_size.place(x=245, y=415, anchor='nw')
    var_font_size = tkinter.IntVar()
    var_font_size.set(int(font_size))
    menu_font_size = tkinter.Menu(menubutton_font_size, tearoff=False)
    for size in range(10,21):
        menu_font_size.add_radiobutton(label=size, variable=var_font_size, value=size)
    menubutton_font_size.config(menu=menu_font_size)

    tkinter.Button(Settin_window, text="保存设置", width=10, height=1, command=lambda:Settin_save(API_Key_Entry,Secret_Key_Entry,Settin_window,var1_1,var1_2,var1_3,var2,time_Scale,var_original,var_youdao,var_baidu,var_tencent,var_height,var_font,var_font_size)).place(x=65, y=465, anchor='nw')
    tkinter.Button(Settin_window, text="取消", width=7, height=1, command=Settin_window.destroy).place(x=175, y=465, anchor='nw')

    API_Key_Entry.insert(0.0,API_Key)
    Secret_Key_Entry.insert(0.0,Secret_Key)

    Settin_window.mainloop()


def Settin_main(window):

    window.destroy()
    path = os.getcwd() + '\\config\\'
    with open(path+'ORC_Key.txt') as file:
        API_Key,Secret_Key = file.read().split(',')

    with open(path+'Init.txt') as file:
        value1_1,value1_2,value1_3,value2,value3,original,youdao,baidu,tencent,height,font_name,font_size = file.read().split(',')

    Settin_UI(API_Key,Secret_Key,value1_1,value1_2,value1_3,value2,value3,original,youdao,baidu,tencent,height,font_name,font_size)
    UI.UI_main()