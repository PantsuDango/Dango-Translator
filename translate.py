from API import get_Access_Token,baidu_orc,youdao,baidu,tencent
import interface

from PIL import ImageGrab,Image

import time

import tkinter
import tkinter.messagebox

from skimage.measure import compare_ssim
from cv2 import imread,cvtColor,COLOR_BGR2GRAY

from threading import Thread


def compare_image(imageA,imageB):

    grayA = cvtColor(imageA, COLOR_BGR2GRAY)
    grayB = cvtColor(imageB, COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    score = float(score)
    return score


def image_cut():
   
    data = interface.get_config()
    Type = data['coordinate']['Type']
    x1 = int(data['coordinate'][Type]['X1'])
    y1 = int(data['coordinate'][Type]['Y1'])
    x2 = int(data['coordinate'][Type]['X2'])
    y2 = int(data['coordinate'][Type]['Y2'])
 
    try:
        bbox = (x1, y1, x2, y2)
        image = ImageGrab.grab(bbox)
        image.save('.\\config\\image.png')
    except Exception:
        tkinter.messagebox.showerror(title='error', message='坐标错误！')


def String(result,font_size):
    
    if font_size == '10':
        number = 47
    elif font_size == '11':
        number = 41
    elif font_size == '12':
        number = 41
    elif font_size == '13':
        number = 36
    elif font_size == '14':
        number = 33
    elif font_size == '15':
        number = 33
    elif font_size == '16':
        number = 30
    elif font_size == '17':
        number = 27
    elif font_size == '18':
        number = 27
    elif font_size == '19':
        number = 25
    elif font_size == '20':
        number = 23
    else:
        number = 33

    result = result.replace('\n','')
    size = len(result) // number 
    if size > 0 and len(result) != number:
        result = list(result)
        for count in range(1,size+1):
            result.insert(count*number+(count-1),'\n')
        result = ''.join(result)
    return result


def thread_it(func,*args):
    
    thread = Thread(target=func, args=args) 
    thread.setDaemon(True) 
    thread.start()


def Translate(Text,Source_youdao,Source_baidu,Source_tencent,font_size,colour_original,colour_youdao,colour_baidu,colour_tencent):

    imageA = imread('.\\config\\image.png')
    image_cut()
    imageB = imread('.\\config\\image.png')

    result_old = Text.get(1.0,tkinter.END).replace('\n','')
    if result_old == '':
        score = 0.94
    else:
        score = compare_image(imageA,imageB)

    if score < 0.95:

        original = baidu_orc()
        Text.delete(1.0,tkinter.END)

        if Source_youdao == '1':
            result_youdao = youdao(original)
            if result_youdao != ' ':
                result_youdao = String(result_youdao,font_size)
                Text.insert(tkinter.END,result_youdao,colour_youdao)
                Text.insert(tkinter.END,'\n')

        if Source_baidu == '1':
            result_baidu = baidu(original)
            if result_baidu != ' ':
                result_baidu = String(result_baidu,font_size)
                Text.insert(tkinter.END,result_baidu,colour_baidu)
                Text.insert(tkinter.END,'\n')
        
        if Source_tencent == '1':
            result_tencent = tencent(original)
            if result_tencent != ' ':
                result_tencent = String(result_tencent,font_size)
                Text.insert(tkinter.END,result_tencent,colour_tencent)
                Text.insert(tkinter.END,'\n')

        original = String(original,font_size)
        Text.insert(tkinter.END,'\n')
        Text.insert(tkinter.END,original,colour_original)


def auto(Text,Source_youdao,Source_baidu,Source_tencent,font_size,colour_original,colour_youdao,colour_baidu,colour_tencent,sec,window):
    
    while True:
        data = interface.get_config()
        if data['sign'] % 2 == 0:
            Translate(Text,Source_youdao,Source_baidu,Source_tencent,font_size,colour_original,colour_youdao,colour_baidu,colour_tencent)
            window.update()
            time.sleep(sec-1.5)
        else:
            break


def translate_main(Text,window):

    start = time.time()
    data = interface.get_config()
    access_token = data['AccessToken']

    Source_youdao = data['Source']['youdao']
    Source_baidu = data['Source']['baidu']
    Source_tencent = data['Source']['tencent']
    font_size = data['FontSize']
    Mode = data['Mode']
    Speed = data['Speed']
    colour_original = data['Colour']['original']
    colour_youdao = data['Colour']['youdao']
    colour_baidu = data['Colour']['baidu']
    colour_tencent = data['Colour']['tencent']

    if Mode == '1':
        thread_it(Translate,Text,Source_youdao,Source_baidu,Source_tencent,font_size,colour_original,colour_youdao,colour_baidu,colour_tencent)

    elif Mode == '2':
        data['sign'] = data['sign'] + 1
        interface.save_config(data)
        sec = int(Speed)
        thread_it(auto,Text,Source_youdao,Source_baidu,Source_tencent,font_size,colour_original,colour_youdao,colour_baidu,colour_tencent,sec,window)