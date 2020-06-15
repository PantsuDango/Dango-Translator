# -*- coding: utf-8 -*-

from API import baidu_orc, youdao, caiyun, jinshan, yeekit, ALAPI, baidu, tencent, caiyunAPI
from baidufanyi import BaiduWeb
from Tencent import TencentTrans
from Google import GoogleTranslate
from Bing import BingTranslate

from PIL import ImageGrab
from skimage.measure import compare_ssim
from cv2 import imread,cvtColor,COLOR_BGR2GRAY

import time
import json

from pyperclip import copy
from traceback import print_exc

from PyQt5.QtWidgets import QApplication


# 截图
def image_cut(window, data):

    x1 = data["range"]['X1']
    y1 = data["range"]['Y1']
    x2 = data["range"]['X2']
    y2 = data["range"]['Y2']

    try:
        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1)
        pix.save('.\\config\\image.jpg')

    except Exception:
        print_exc()


# 判断图片相似度
def compare_image(imageA,imageB):

    grayA = cvtColor(imageA, COLOR_BGR2GRAY)
    grayB = cvtColor(imageB, COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    score = float(score)
    
    return score


def __call_entry(translate_name: str, translate_data) -> str:
    """
    调用入口
    :parem: translate_name 翻译名称
    :parem: translate_data
    :return:
    """
    __api_tradition = {
        'youdaoUse': youdao,
        'caiyunUse': caiyun,
        'jinshanUse': jinshan,
        'yeekitUse': yeekit,
        'alapiUse': ALAPI,
    }

    __api_web = {
        'baiduwebUse': BaiduWeb,
        'tencentwebUse': TencentTrans,
        'googleUse': GoogleTranslate,
        'BingUse': BingTranslate,
    }

    __api_private = {
        'baiduUse': baidu,
        'tencentUse': tencent,
        'caiyunPrivateUse': caiyunAPI,
    }
    ret = ''
    # TODO 有待合并成统一的调用方式, 需要调整对应的 api 的结构
    if translate_name in __api_tradition:

        ret = __api_tradition[translate_name](translate_data['original'])

        if translate_name == 'yeekitUse':
            ret = __api_tradition[translate_name](translate_data['original'], translate_data['yeekitLanguage'])

    elif translate_name in __api_web:
        ret = __api_web[translate_name](translate_data['original']).translate()

        if translate_name == 'BingUse':
            ret = __api_web[translate_name]().translate(translate_data["BingLanguage"], translate_data['original'])

    elif translate_name in __api_private:
        ret = __api_private[translate_name](translate_data['original'], translate_data)

    return ret


# 翻译主函数
def translate(window, data):

    text = window.translateText.toPlainText()
    if text[:5] == "团子翻译器" or (not text[:1]):
        score = 0.97
        image_cut(window, data)
    else:
        imageA = imread('.\\config\\image.jpg')
        image_cut(window, data)
        imageB = imread('.\\config\\image.jpg')
        try:
            score = compare_image(imageA, imageB)
        except Exception:
            score = 0.97

    result = dict()
    translate_platform = {
        'youdaoUse': 'youdao',
        'caiyunUse': 'caiyun',
        'jinshanUse': 'jinshan',
        'yeekitUse': 'yeekit',
        'alapiUse': 'alapi',
        'baiduwebUse': 'baiduweb',
        'tencentwebUse': 'tencentweb',
        'googleUse': 'google',
        'BingUse': 'Bing',
        'baiduUse': 'baidu',
        'tencentUse': 'tencent',
        'caiyunPrivateUse': 'caiyunPrivate',
    }

    if score < 0.98:

        sign, original = baidu_orc(data)

        if sign and original and (original != window.original):

            # 过滤不需要加入翻译的字符
            try:
                with open(".\\config\\filter.txt") as file:
                    char = file.read()
                char.split('''&''')
                for ch in char:
                    original = original.replace(ch, '')
            except Exception:
                print_exc()

            # 是否复制到剪贴板
            if data["showClipboard"] == 'True':
                copy(original)
        
        data['original'] = original
        result = {y: __call_entry(x, data) if data[x] == 'True' else '' for x, y in translate_platform.items()}

    else:
        original = ''
        sign = True

    result["original"] = original
    result["sign"] = sign

    return result
