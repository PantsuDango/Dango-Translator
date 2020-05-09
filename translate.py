# -*- coding: utf-8 -*-

from API import baidu_orc, youdao, caiyun, jinshan, baidu, tencent

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
    if screenSize >= 1.5:
    	bbox = (x1*2, y1*2, x2*2, y2*2)
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

        original = baidu_orc(window, data)
        original = original.replace('\n','')

        if data["showClipboard"] == 'True':
            copy(original)

        youdaoUse = data["youdaoUse"]
        caiyunUse = data["caiyunUse"]
        jinshanUse = data["jinshanUse"]
        baiduUse = data["baiduUse"]
        tencentUse = data["tencentUse"]
        showOriginal = data["showOriginal"]

        if original:
            if youdaoUse == "True":
                try:
                    result_youdao = youdao(window, original)
                except Exception:
                    print_exc()
                    result_youdao = ''
                else:
                    if result_youdao:
                        result_youdao += "<br>"
            else:
                result_youdao = ''

            if caiyunUse == "True":
                try:
                    result_caiyun = caiyun(window, original)
                except Exception:
                    print_exc()
                    result_caiyun = ''
                else:
                    if result_caiyun:
                        result_caiyun += "<br>"
            else:
                result_caiyun = ''
        
            if jinshanUse == "True":
                try:
                    result_jinshan = jinshan(window, original)
                except Exception:
                    print_exc()
                    result_jinshan = ''
                else:
                    if result_jinshan:
                        result_jinshan += "<br>"
            else:
                result_jinshan = ''

            if baiduUse == "True":
                try:
                    result_baidu = baidu(window, original, data)
                except Exception:
                    print_exc()
                    result_baidu = ''
                else:
                    if result_baidu:
                        result_baidu += "<br>"
            else:
                result_baidu = ''

            if tencentUse == "True":
                try:
                    result_tencent = tencent(window, original, data)
                except Exception:
                    print_exc()
                    result_tencent = ''
                else:
                    if result_tencent:
                        result_tencent += "<br>"
            else:
                result_tencent = ''

            if showOriginal != "True":
                original = ''

        else:
            result_youdao = ''
            result_caiyun = ''
            result_jinshan = ''
            result_baidu = ''
            result_tencent = ''
            original = ''
    else:
        result_youdao = ''
        result_caiyun = ''
        result_jinshan = ''
        result_baidu = ''
        result_tencent = ''
        original = ''

    result = (result_youdao, result_caiyun, result_jinshan, result_baidu, result_tencent, original)
    
    return result