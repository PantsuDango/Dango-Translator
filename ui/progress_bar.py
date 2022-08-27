from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ui.static.icon
import utils.thread

import sys
import os
import base64
import requests


# 进度条
class ProgressBar(QWidget) :

    def __init__(self, rate, title) :

        super().__init__()
        self.rate = rate
        self.title = title

        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口标题
        self.setWindowTitle(self.title)
        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        # 窗口图标
        icon = QIcon()
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(ui.static.icon.APP_LOGO))
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)
        # 设置字体
        self.setStyleSheet("font: %spt '%s';" % (self.font_size, self.font_type))

        self.progress_bar = QProgressBar(self)
        self.customSetGeometry(self.progress_bar, 20, 20, 260, 25)
        self.progress_bar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.show()

        url = "https://l2.drive.c4a15wh.cn/api/v3/slave/source/0/dXBsb2Fkcy8yMDIyLzA4LzIyL1NXdHlkNHRNX29jci00LjIuNy56aXA/ocr-4.2.7.zip?sign=JwHd6RhdpNaXA7P89oxg_UcRbW2rJfXCqchRrnilnA8%3D%3A0"
        file_name = "ocr_zip"
        utils.thread.createThread(self.download, url, file_name)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 初始化配置
    def getInitConfig(self):

        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 10
        # 界面尺寸
        self.window_width = int(300 * self.rate)
        self.window_height = int(100 * self.rate)


    # 下载
    def download(self, url, file_name):

        size = 0
        chunk_size = 1024
        try:
            response = requests.get(url, stream=True)
            content_size = int(response.headers["content-length"])
            if response.status_code == 200:
                print("文件大小:{size:.2f} MB".format(size=content_size / chunk_size / 1024))
                with open(file_name, "wb") as file :
                    for data in response.iter_content(chunk_size=chunk_size) :
                        file.write(data)
                        size += len(data)
                        # self.progress_bar.setFormat("{size:.2f} MB  {:.2f}%".format(
                        #     size=content_size/chunk_size/1024),
                        #     float(size/content_size*100)
                        # )
                        #self.progress_bar.setFormat("1111")
                        self.progress_bar.setValue(int(size/content_size*100))
                        print("\r" + "[下载进度]:%s%.2f%%" % (">" * int(size * 50 / content_size), float(size / content_size * 100)), end=" ")
            return None
        except Exception as err :
            os.remove(file_name)


if __name__ == "__main__" :

    app = QApplication(sys.argv)
    obj = ProgressBar(1.5, "进度条")
    sys.exit(app.exec_())