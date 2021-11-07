from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

from skimage.metrics import structural_similarity
from cv2 import imread, cvtColor, COLOR_BGR2GRAY
from difflib import SequenceMatcher
import threading
from traceback import format_exc

from translator.ocr.baidu import baiduOCR
from translator import api


IMAGE_PATH = ".\config\image.jpg"


# 翻译处理线程
class TranslaterProccess(QThread) :

    display_signal = pyqtSignal(str, str)

    def __init__(self, window, original, trans_type, logger) :

        super(TranslaterProccess, self).__init__()
        self.window = window
        self.original = original
        self.trans_type = trans_type
        self.logger = logger


    def run(self) :

        result = ""

        # 公共翻译一
        if self.trans_type == "webdriver_1" :
            result = self.window.webdriver_1.translater(self.original)
            print("公共%s: %s"%(self.window.webdriver_1.web_type, result))

        # 公共翻译二
        elif self.trans_type == "webdriver_2" :
            result = self.window.webdriver_2.translater(self.original)
            print("公共%s: %s"%(self.window.webdriver_2.web_type, result))

        # 私人百度
        elif self.trans_type == "baidu_private" :
            secret_id = self.window.config["baiduAPI"]["Key"]
            secret_key = self.window.config["baiduAPI"]["Secret"]
            result = api.baidu(self.original, secret_id, secret_key, self.logger)
            print("私人百度: ", result)

        # 私人腾讯
        elif self.trans_type == "tencent_private" :
            secret_id = self.window.config["tencentAPI"]["Key"]
            secret_key = self.window.config["tencentAPI"]["Secret"]
            result = api.tencent(self.original, secret_id, secret_key, self.logger)
            print("私人腾讯: ", result)

        # 私人彩云
        elif self.trans_type == "caiyun_private" :
            secret_key = self.window.config["caiyunAPI"]
            result = api.caiyun(self.original, secret_key, self.logger)
            print("私人彩云: ", result)

        elif self.trans_type == "original" :
            result = self.original

        if result :
            self.display_signal.emit(result, self.trans_type)


# 翻译处理模块
class Translater(QThread) :

    create_trans_sign = pyqtSignal(str)
    clear_text_sign = pyqtSignal(bool)

    def __init__(self, window, logger):

        super(Translater, self).__init__()
        self.window = window
        self.logger = logger
        self.create_trans_sign.connect(self.creatTranslaterThread)

    # 截图
    def imageCut(self):

        x1 = self.window.config["range"]["X1"]
        y1 = self.window.config["range"]["Y1"]
        x2 = self.window.config["range"]["X2"]
        y2 = self.window.config["range"]["Y2"]

        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1)
        pix.save(IMAGE_PATH)


    # 判断图片相似度
    def compareImage(self, imageA, imageB):

        grayA = cvtColor(imageA, COLOR_BGR2GRAY)
        grayB = cvtColor(imageB, COLOR_BGR2GRAY)

        (score, diff) = structural_similarity(grayA, grayB, full=True)
        score = float(score) * 100

        return score


    # 判断原文相似度
    def getEqualRate(self, str1, str2):

        score = SequenceMatcher(None, str1, str2).quick_ratio()
        score = score* 100

        return score


    # 创建翻译线程
    def creatTranslaterThread(self, trans_type) :

        self.window.thread_state += 1
        thread = TranslaterProccess(self.window, self.window.original, trans_type, self.logger)
        thread.display_signal.connect(self.window.display_text)
        thread.start()
        thread.exec()


    # 翻译主模块
    def translate(self) :

        try:
            # 首次执行或手动模式下, 直接跳过图片相似度检测
            if not self.window.original or not self.window.translateMode :
                self.imageCut()
            else :
                # 判断两张图片的相似度
                imageA = imread(IMAGE_PATH)
                self.imageCut()
                imageB = imread(IMAGE_PATH)
                image_score = self.compareImage(imageA, imageB)

                # 在自动模式下, 如果如果相似度过高则不检测
                if (image_score > self.window.config["imageSimilarity"]):
                    return
        except Exception :
            self.logger.error(format_exc())

        # 百度OCR
        if self.window.config["baiduOCR"] :
            sign, original = baiduOCR(self.window.config, self.logger)
            print("百度OCR: ", original)
        else :
            original = ""

        # 如果检测不到文字或者文字和上一次一样则跳过
        if not original or original == self.window.original :
            return

        # 在自动模式下, 如果如果文本相似度过高则不翻译
        if self.window.translateMode :
            text_score = self.getEqualRate(original, self.window.original)
            if text_score > self.window.config["textSimilarity"] :
                return

        # 发送清屏信号
        self.clear_text_sign.emit(True)
        # 判断是否未开任何翻译源
        nothing_sign = False

        # 公共翻译一
        if self.window.webdriver_1.open_sign :
            self.create_trans_sign.emit("webdriver_1")
            nothing_sign = True

        # 公共翻译二
        if self.window.webdriver_2.open_sign :
            self.create_trans_sign.emit("webdriver_2")
            nothing_sign = True

        # 私人百度
        if self.window.config["baiduUse"] == "True" :
            self.create_trans_sign.emit("baidu_private")
            nothing_sign = True

        # 私人百度
        if self.window.config["tencentUse"] == "True" :
            self.create_trans_sign.emit("tencent_private")
            nothing_sign = True

        # 私人彩云
        if self.window.config["caiyunPrivateUse"] == "True" :
            self.create_trans_sign.emit("caiyun_private")
            nothing_sign = True

        # 显示原文
        if self.window.config["showOriginal"] == "True" or not nothing_sign :
            self.create_trans_sign.emit("original")

        # 更新原文
        if nothing_sign :
            self.window.original = original


    def run(self) :

        # 如果上一次翻译未结束则直接跳过
        if self.window.thread_state > 0 :
            return

        # 手动翻译
        if not self.window.translateMode :
            self.translate()