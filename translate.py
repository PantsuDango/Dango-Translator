# -*- coding: utf-8 -*-

from API import baidu_orc, youdao, caiyun, jinshan, yeekit, ALAPI, baidu, tencent
from baidufanyi import WebFanyi

from PIL import ImageGrab
from skimage.measure import compare_ssim
from cv2 import imread,cvtColor,COLOR_BGR2GRAY

import time
import json

from pyperclip import copy


def image_cut(data):
   
    with open('.\\config\\settin.json') as file:
        data = json.load(file)

    x1 = data["range"]['X1']
    y1 = data["range"]['Y1']
    x2 = data["range"]['X2']
    y2 = data["range"]['Y2']

    screenSize = data["screenSize"]
    if  1.5 <= screenSize < 2.5:
    	bbox = (x1*2, y1*2, x2*2, y2*2)
    elif 2.5 <= screenSize < 3.5:
        bbox = (x1*3, y1*3, x2*3, y2*3)
    elif 3.5 <= screenSize < 4.5:
        bbox = (x1*4, y1*4, x2*4, y2*4)
    else:
    	bbox = (x1, y1, x2, y2)
    image = ImageGrab.grab(bbox)
    image.save('.\\config\\image.jpg')


def compare_image(imageA,imageB):

    grayA = cvtColor(imageA, COLOR_BGR2GRAY)
    grayB = cvtColor(imageB, COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    score = float(score)
    
    return score


def translate(window, data):

    text = window.translateText.toPlainText()
    if text[:5] == "团子翻译器" or (not text[:1]):
        score = 0.98
        image_cut(data)
    else:
        imageA = imread('.\\config\\image.jpg')
        image_cut(data)
        imageB = imread('.\\config\\image.jpg')
        try:
            score = compare_image(imageA, imageB)
        except Exception:
            score = 0.98
    
    if score < 0.99:

        original = baidu_orc(data)

        if data["showClipboard"] == 'True':
            copy(original)

        youdaoUse = data["youdaoUse"]
        caiyunUse = data["caiyunUse"]
        jinshanUse = data["jinshanUse"]
        yeekitUse = data["yeekitUse"]
        alapiUse = data["alapiUse"]
        baiduwebUse = data["baiduwebUse"]
        baiduUse = data["baiduUse"]
        tencentUse = data["tencentUse"]

        if original:
            if youdaoUse == "True":
                result_youdao = youdao(original)
            else:
                result_youdao = ''

            if caiyunUse == "True":
                result_caiyun = caiyun(original)
            else:
                result_caiyun = ''
        
            if jinshanUse == "True":
                result_jinshan = jinshan(original)
            else:
                result_jinshan = ''

            if yeekitUse == "True":
                result_yeekit = yeekit(original)
            else:
                result_yeekit = ''

            if alapiUse == "True":
                result_alapi = ALAPI(original)
            else:
                result_alapi = ''

            if baiduwebUse == "True":
                webfanyi = WebFanyi(original, data)
                result_baiduweb = webfanyi.run()
            else:
                result_baiduweb = ''

            if baiduUse == "True":
                result_baidu = baidu(original, data)
            else:
                result_baidu = ''

            if tencentUse == "True":
                result_tencent = tencent(original, data)
            else:
                result_tencent = ''

        else:
            result_youdao = ''
            result_caiyun = ''
            result_jinshan = ''
            result_yeekit = ''
            result_alapi = ''
            result_baiduweb = ''
            result_baidu = ''
            result_tencent = ''
            original = ''
    else:
        result_youdao = ''
        result_caiyun = ''
        result_jinshan = ''
        result_yeekit = ''
        result_alapi = ''
        result_baiduweb = ''
        result_baidu = ''
        result_tencent = ''
        original = ''

    result = (result_youdao, result_caiyun, result_jinshan, result_yeekit, result_alapi, result_baiduweb, result_baidu, result_tencent, original)
    
    return result