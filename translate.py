# -*- coding: utf-8 -*-

from API import baidu_orc, dango_ocr

from skimage.measure import compare_ssim
from cv2 import imread,cvtColor,COLOR_BGR2GRAY
from PIL import Image

import time
import json

from pyperclip import copy
from traceback import print_exc
from difflib import SequenceMatcher

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *
import qtawesome


def processImage(filename, mwidth=400, mheight=400):

    image = Image.open(filename)
    w, h = image.size

    if w <= mwidth and h <= mheight:
        return

    if (1.0 * w / mwidth) > (1.0 * h / mheight):
        scale = 1.0 * w / mwidth
        new_im = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
    else:
        scale = 1.0 * h / mheight
        new_im = image.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)

    new_im.save(filename)
    new_im.close()


# 截图
def image_cut(data):

    x1 = data["range"]['X1']
    y1 = data["range"]['Y1']
    x2 = data["range"]['X2']
    y2 = data["range"]['Y2']

    try:
        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1)
        pix.save('.\\config\\image.jpg')
        #processImage('.\\config\\image.jpg', 600, 600)

    except Exception:
        print_exc()


# 判断图片相似度
def compare_image(imageA,imageB):

    grayA = cvtColor(imageA, COLOR_BGR2GRAY)
    grayB = cvtColor(imageB, COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    score = float(score)
    
    return score


# 判断原文相似度
def get_equal_rate(str1, str2):

    score = SequenceMatcher(None, str1, str2).quick_ratio()
    return score


# 翻译主函数
def translate(window, data, use_translate_signal):

    text = window.translateText.toPlainText()

    if text[:2] == "欢迎你" or (not text[:1]) or window.is_fail == True :
        score = 0.98
        image_cut(data)
        window.is_fail = False
    else:
        imageA = imread('.\\config\\image.jpg')
        image_cut(data)
        imageB = imread('.\\config\\image.jpg')
        try:
            score = compare_image(imageA, imageB)
        except Exception:
            score = 0.98

    if score < 0.99:

        # ocr
        now = time.time()
        ocrUse = data.get("ocrUse", "False")
        if ocrUse == "True" :
            sign, original = baidu_orc(data)
        else :
            sign, original = dango_ocr(data)
        print("time:", time.time()-now)

        signal_list = list()

        # 原文相似度
        str_score = get_equal_rate(original, window.original)
        
        if sign and original and (original != window.original) and str_score < 0.9 :

            window.original = original

            # 是否复制到剪贴板
            if data["showClipboard"] == 'True':
                copy(original)

            youdaoUse = data["youdaoUse"]  # 有道
            caiyunUse = data["caiyunUse"]  # 公共彩云
            jinshanUse = data["jinshanUse"]  # 金山
            yeekitUse = data["yeekitUse"]  #yeekit
            alapiUse = data["alapiUse"]  # alapi
            
            baiduwebUse = data["baiduwebUse"]  # 百度网页版
            tencentwebUse = data["tencentwebUse"]  # 腾讯网页版
            googleUse = data["googleUse"]  # google网页版
            BingUse = data["BingUse"]  # Bing网页版
            
            baiduUse = data["baiduUse"]  # 百度私人版
            tencentUse = data["tencentUse"]  # 腾讯私人版
            caiyunPrivateUse = data["caiyunPrivateUse"]  # 私人彩云

            if data["showOriginal"] == "True":
                signal_list.append("original")
            # 有道
            if youdaoUse == "True":
                signal_list.append("youdao")
            # 公共彩云
            if caiyunUse == "True":
                signal_list.append("caiyun")
            # 金山
            if jinshanUse == "True":
                signal_list.append("jinshan")
            #yeekit
            if yeekitUse == "True":
                signal_list.append("yeekit")
            # alapi
            if alapiUse == "True":
                signal_list.append("ALAPI")
            # 百度网页版
            if baiduwebUse == "True":
                signal_list.append("baiduweb")
            # 腾讯网页版
            if tencentwebUse == "True":
                signal_list.append("tencentweb")
            # 谷歌网页版
            if googleUse == "True":
                signal_list.append("google")
            # Bing网页版
            if BingUse == "True":
                signal_list.append("Bing")
            # 百度私人版
            if baiduUse == "True":
                signal_list.append("baidu")
            # 腾讯私人版
            if tencentUse == "True":
                signal_list.append("tencent")
            # 彩云私人版
            if caiyunPrivateUse == "True":
                signal_list.append("caiyunPrivate")

            # 保存原文
            content = "\n\n[原文]\n%s"%original
            with open(".\\config\\翻译历史.txt", "a+", encoding="utf-8") as file:
                file.write(content)

            use_translate_signal.emit(signal_list, original, data)

        elif not sign :

            window.is_fail = True
            signal_list.append("error")
            use_translate_signal.emit(signal_list, original, data)


class TranslateThread(QThread):

    use_translate_signal = pyqtSignal(list, str, dict)
 
    def __init__(self, window, mode):
        
        self.window = window
        self.mode = mode
        super(TranslateThread, self).__init__()

    def run(self):
        
        with open('.\\config\\settin.json') as file:
            data = json.load(file)
        
        if not self.mode :
            try:
                if self.window.thread_state == 0:
                    translate(self.window, data, self.use_translate_signal)
            except Exception:
                print_exc()
        else:
            data["sign"] += 1
            with open('.\\config\\settin.json','w') as file:
                json.dump(data, file)
            try:
                if data["sign"] % 2 == 0:
                    self.window.StartButton.setIcon(qtawesome.icon('fa.pause', color='white'))

                while True:

                    with open('.\\config\\settin.json') as file:
                        data = json.load(file)

                    if data["sign"] % 2 == 0:
                        try:
                            if self.window.thread_state == 0:
                                translate(self.window, data, self.use_translate_signal)
                            sec = data["translateSpeed"] - 0.5
                            time.sleep(sec)

                        except Exception:
                            print_exc()
                            break
                    else:
                        self.window.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
                        break

            except Exception:
                print_exc()