from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from skimage.metrics import structural_similarity
from cv2 import imread, cvtColor, COLOR_BGR2GRAY
from difflib import SequenceMatcher
from traceback import format_exc
import time
import pyperclip

import utils.thread
import utils.config

import translator.ocr.baidu
import translator.ocr.dango
import translator.api


IMAGE_PATH = ".\config\image.jpg"


# 翻译处理线程
class TranslaterProccess(QThread) :

    display_signal = pyqtSignal(str, str)

    def __init__(self, object, trans_type) :

        super(TranslaterProccess, self).__init__()
        self.object = object
        self.trans_type = trans_type
        self.logger = object.logger


    def run(self) :

        result = ""

        # 公共翻译一
        if self.trans_type == "webdriver_1" :
            if self.object.translation_ui.webdriver1.open_sign :
                result = self.object.translation_ui.webdriver1.translater(self.object.translation_ui.original)
            else :
                result = "%s翻译: 我抽风啦"%self.object.translation_ui.webdriver1.translater_map[self.object.translation_ui.webdriver1.web_type]

        # 公共翻译二
        elif self.trans_type == "webdriver_2" :
            if self.object.translation_ui.webdriver2.open_sign :
                result = self.object.translation_ui.webdriver2.translater(self.object.translation_ui.original)
            else :
                result = "%s翻译: 我抽风啦"%self.object.translation_ui.webdriver2.translater_map[self.object.translation_ui.webdriver2.web_type]

        # 公共翻译三
        elif self.trans_type == "webdriver_3":
            if self.object.translation_ui.webdriver3.open_sign :
                result = self.object.translation_ui.webdriver3.translater(self.object.translation_ui.original)
            else:
                result = "%s翻译: 我抽风啦" % self.object.translation_ui.webdriver3.translater_map[self.object.translation_ui.webdriver3.web_type]

        # 私人百度
        elif self.trans_type == "baidu_private" :
            secret_id = self.object.config["baiduAPI"]["Key"]
            secret_key = self.object.config["baiduAPI"]["Secret"]
            result = translator.api.baidu(self.object.translation_ui.original, secret_id, secret_key, self.logger)

        # 私人腾讯
        elif self.trans_type == "tencent_private" :
            secret_id = self.object.config["tencentAPI"]["Key"]
            secret_key = self.object.config["tencentAPI"]["Secret"]
            result = translator.api.tencent(self.object.translation_ui.original, secret_id, secret_key, self.logger)

        # 私人彩云
        elif self.trans_type == "caiyun_private" :
            secret_key = self.object.config["caiyunAPI"]
            result = translator.api.caiyun(self.object.translation_ui.original, secret_key, self.logger)

        elif self.trans_type == "original" :
            result = self.object.translation_ui.original

        self.display_signal.emit(result, self.trans_type)


# 翻译处理模块
class Translater(QThread) :

    clear_text_sign = pyqtSignal(bool)

    def __init__(self, object) :

        super(Translater, self).__init__()
        self.object = object
        self.logger = object.logger

    # 截图
    def imageCut(self):

        x1 = self.object.yaml["range"]["X1"]
        y1 = self.object.yaml["range"]["Y1"]
        x2 = self.object.yaml["range"]["X2"]
        y2 = self.object.yaml["range"]["Y2"]

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

        if self.object.translation_ui.thread_state == 0 :
            # 发送清屏信号
            self.clear_text_sign.emit(True)
            self.object.translation_ui.statusbar.showMessage("翻译中...")
            QApplication.processEvents()

        self.object.translation_ui.thread_state += 1
        thread = TranslaterProccess(self.object, trans_type)
        thread.display_signal.connect(self.object.translation_ui.display_text)
        thread.start()
        thread.wait()


    # 翻译主模块
    def translate(self) :

        # 如果还未选取范围就操作翻译
        if self.object.yaml["range"]["X2"] == 0 :
            self.clear_text_sign.emit(True)
            self.object.translation_ui.original = "还未选取翻译范围, 请先使用范围键框选要翻译的屏幕区域"
            utils.thread.createThread(self.creatTranslaterThread, "original")
            # 关闭翻译界面自动开关
            if self.object.translation_ui.translate_mode == True :
                self.object.translation_ui.switch_button.mousePressEvent(1)
                self.object.translation_ui.switch_button.updateValue()
            return

        try:
            # 首次执行或手动模式下, 直接跳过图片相似度检测
            if not self.object.translation_ui.original or not self.object.translation_ui.translate_mode :
                self.imageCut()
            else :
                # 判断两张图片的相似度
                imageA = imread(IMAGE_PATH)
                self.imageCut()
                imageB = imread(IMAGE_PATH)
                image_score = self.compareImage(imageA, imageB)

                # 在自动模式下, 如果如果相似度过高则不检测
                if (image_score > self.object.config["imageSimilarity"]):
                    return
        except Exception :
            self.logger.error(format_exc())

        # OCR开始时间
        ocr_start_time = time.time()

        # 百度OCR
        if self.object.config["baiduOCR"] :
            ocr_sign, original = translator.ocr.baidu.baiduOCR(self.object.config, self.logger)
        # 团子OCR
        elif self.object.config["onlineOCR"] :
            ocr_sign, original = translator.ocr.dango.dangoOCR(self.object)
        # 离线OCR
        elif self.object.config["offlineOCR"] :
            ocr_sign, original = translator.ocr.dango.offlineOCR(self.object)

        else :
            original = "OCR错误: 未开启任何OCR, 请在设置-OCR设定中打开OCR开关"
            ocr_sign = False

        # 记录OCR耗时
        self.object.translation_ui.ocr_time = time.time()-ocr_start_time

        # 如果出错就显示原文
        if not ocr_sign :
            self.clear_text_sign.emit(True)
            self.object.translation_ui.original = original
            utils.thread.createThread(self.creatTranslaterThread, "original")
            return

        # 如果检测不到文字则跳过
        if not original :
            return

        # 自动模式下文字和上一次一样则跳过
        if self.object.translation_ui.translate_mode and original == self.object.translation_ui.original :
            return

        # 在自动模式下, 如果如果文本相似度过高则不翻译
        if self.object.translation_ui.translate_mode :
            text_score = self.getEqualRate(original, self.object.translation_ui.original)
            if text_score > self.object.config["textSimilarity"] :
                return

        # 更新原文
        self.object.translation_ui.original = original
        # 是否复制到剪贴板
        if self.object.config["showClipboard"] == "True":
            pyperclip.copy(original)
        # 保存原文
        utils.config.saveOriginalHisTory(original)
        # 判断是否未开任何翻译源
        nothing_sign = False

        # 公共翻译一
        if self.object.translation_ui.webdriver1.open_sign :
            utils.thread.createThread(self.creatTranslaterThread, "webdriver_1")
            nothing_sign = True

        # 公共翻译二
        if self.object.translation_ui.webdriver2.open_sign :
            utils.thread.createThread(self.creatTranslaterThread, "webdriver_2")
            nothing_sign = True

        # 公共翻译三
        if self.object.translation_ui.webdriver3.open_sign:
            utils.thread.createThread(self.creatTranslaterThread, "webdriver_3")
            nothing_sign = True

        # 私人百度
        if self.object.config["baiduUse"] == "True" :
            utils.thread.createThread(self.creatTranslaterThread, "baidu_private")
            nothing_sign = True

        # 私人百度
        if self.object.config["tencentUse"] == "True" :
            utils.thread.createThread(self.creatTranslaterThread, "tencent_private")
            nothing_sign = True

        # 私人彩云
        if self.object.config["caiyunPrivateUse"] == "True" :
            utils.thread.createThread(self.creatTranslaterThread, "caiyun_private")
            nothing_sign = True

        # 显示原文
        if self.object.config["showOriginal"] == "True" or not nothing_sign :
            if not nothing_sign :
                self.object.translation_ui.original += "\n\n未开启任何翻译源, 无法翻译, 请在设置-翻译源设定-打开要使用的翻译源"
            utils.thread.createThread(self.creatTranslaterThread, "original")


    def run(self) :

        # 手动翻译
        if not self.object.translation_ui.translate_mode :

            # 如果上一次翻译未结束则直接跳过
            if self.object.translation_ui.thread_state > 0 :
                return

            try :
                self.translate()
            except Exception:
                self.logger.error(format_exc())

        else :
            # 自动翻译
            self.object.translation_ui.auto_trans_exist = True

            while True :

                # 如果自动翻译被停止则退出循环
                if not self.object.translation_ui.translate_mode :
                    self.object.translation_ui.auto_trans_exist = False
                    break

                # 自动翻译暂停
                if self.object.translation_ui.stop_sign :
                    time.sleep(0.1)
                    continue

                # 如果上一次翻译未结束则直接跳过
                if self.object.translation_ui.thread_state > 0:
                    continue

                try :
                    self.translate()
                except Exception :
                    self.logger.error(format_exc())

                if self.object.config["onlineOCR"] :
                    time.sleep(self.object.config["translateSpeed"]-0.2)
                else :
                    time.sleep(self.object.config["translateSpeed"]-0.4)