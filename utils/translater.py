from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

from skimage.metrics import structural_similarity
from cv2 import imread, cvtColor, COLOR_BGR2GRAY
from difflib import SequenceMatcher

from traceback import format_exc
from translator.ocr.baidu import baiduOCR
from translator import api


IMAGE_PATH = ".\config\image.jpg"


class Translater(QThread) :

    use_translate_signal = pyqtSignal(list, str, dict)

    def __init__(self, window, logger):

        super(Translater, self).__init__()
        self.window = window
        self.logger = logger
        self.translater_map = {
            "youdao": "有道",
            "baidu": "百度",
            "tencent": "腾讯",
            "caiyun": "彩云",
            "google": "谷歌",
            "deepl": "DeepL"
        }


    # 截图
    def image_cut(self):

        x1 = self.window.config["range"]["X1"]
        y1 = self.window.config["range"]["Y1"]
        x2 = self.window.config["range"]["X2"]
        y2 = self.window.config["range"]["Y2"]

        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1)
        pix.save(IMAGE_PATH)


    # 判断图片相似度
    def compare_image(self, imageA, imageB):

        grayA = cvtColor(imageA, COLOR_BGR2GRAY)
        grayB = cvtColor(imageB, COLOR_BGR2GRAY)

        (score, diff) = structural_similarity(grayA, grayB, full=True)
        score = float(score) * 100

        return score


    # 判断原文相似度
    def get_equal_rate(self, str1, str2):

        score = SequenceMatcher(None, str1, str2).quick_ratio()
        score = score* 100

        return score


    # 翻译主模块
    def translate(self) :

        try:
            # 首次执行或手动模式下, 直接跳过图片相似度检测
            if not self.window.original or not self.translateMode :
                self.image_cut()
            else :
                # 判断两张图片的相似度
                imageA = imread(IMAGE_PATH)
                self.image_cut()
                imageB = imread(IMAGE_PATH)
                image_score = self.compare_image(imageA, imageB)

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
        if self.translateMode :
            text_score = self.get_equal_rate(original, self.window.original)
            if text_score > self.window.config["textSimilarity"] :
                return

        # 更新原文
        self.window.original = original

        # 公共翻译一
        if self.window.webdriver_1.open_sign :
            try :
                result = self.window.webdriver_1.translater(original)
                print("公共%s: %s"%(self.translater_map[self.window.webdriver_1.web_type], result))
            except :
                self.logger.error(format_exc())

        # 公共翻译二
        if self.window.webdriver_2.open_sign :
            try :
                result = self.window.webdriver_2.translater(original)
                print("公共%s: %s"%(self.translater_map[self.window.webdriver_2.web_type], result))
            except Exception :
                self.logger.error(format_exc())

        # 私人百度
        if self.window.config["baiduUse"] == "True" :
            secret_id = self.window.config["baiduAPI"]["Key"]
            secret_key = self.window.config["baiduAPI"]["Secret"]
            result = api.baidu(original, secret_id, secret_key, self.logger)
            print("私人百度: ", result)

        # 私人百度
        if self.window.config["tencentUse"] == "True":
            secret_id = self.window.config["tencentAPI"]["Key"]
            secret_key = self.window.config["tencentAPI"]["Secret"]
            result = api.tencent(original, secret_id, secret_key, self.logger)
            print("私人腾讯: ", result)

        # 私人彩云
        if self.window.config["caiyunPrivateUse"] == "True":
            secret_key = self.window.config["caiyunAPI"]
            result = api.caiyun(original, secret_key, self.logger)
            print("私人彩云: ", result)

        print()


    def run(self) :

        # 手动翻译
        if not self.window.translateMode :
            self.translate()