from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

from skimage.measure import compare_ssim
from cv2 import imread,cvtColor,COLOR_BGR2GRAY


class Translater(QThread):

    def __init__(self, window):
        self.window = window
        self.config = window.config
        self.use_translate_signal = pyqtSignal(list, str, dict)
        super(Translater, self).__init__()


    def run(self) :

        # 手动翻译
        if not self.window.translateMode :
            self.translate()


    # 截图
    def image_cut(self):

        x1 = self.config["range"]['X1']
        y1 = self.config["range"]['Y1']
        x2 = self.config["range"]['X2']
        y2 = self.config["range"]['Y2']

        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1)
        pix.save(".\config\image.jpg")


    # 判断图片相似度
    def compare_image(self, imageA, imageB):

        grayA = cvtColor(imageA, COLOR_BGR2GRAY)
        grayB = cvtColor(imageB, COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(grayA, grayB, full=True)
        score = float(score)

        return score


    def translate(self) :

        score = 0
        if self.window.first_sign :
            self.image_cut()
            self.window.first_sign = False
        else :
            try :
                imageA = imread('.\config\image.jpg')
                self.image_cut()
                imageB = imread('.\config\image.jpg')
                score = self.compare_image(imageA, imageB)
            except :
                import traceback
                traceback.print_exc()

        print(score)