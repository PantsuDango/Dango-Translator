# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import fileinput
import collections
import re

import ui.static.icon
import translator.upload_trans_file
import utils.message


TRANS_FILE = "../翻译历史.txt"

# 翻译历史界面
class TransHistory(QWidget) :

    def __init__(self, object) :

        super(TransHistory, self).__init__()
        self.object = object
        self.getInitConfig()
        self.ui()


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 12
        # 界面尺寸
        self.window_width = int(800 * self.rate)
        self.window_height = int(500 * self.rate)
        # 存500条翻译历史
        self.data = collections.deque(maxlen=1000)
        # 是否读取翻译历史完毕
        self.read_file_finish = False


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("翻译历史(最多显示500行)")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size, self.font_type))

        # 说明框
        self.text = QTextBrowser(self)
        self.text.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        # self.text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text.setStyleSheet("QTextBrowser { border-width: 0;"
                                     "border-style: outset;"
                                     "border-top:0px solid #e8f3f9;"
                                     "color: #5B8FF9;"
                                     "background: rgba(255, 255, 255, 0.7); }")
        self.text.setCursor(ui.static.icon.PIXMAP_CURSOR)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 读取翻译历史
    def readTransHistory(self) :

        with open(TRANS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                self.data.append(line)
        self.read_file_finish = True


    # 窗口显示信号
    def showEvent(self, e) :

        self.text.clear()
        for val in self.data :
            self.text.append(val)


    # 窗口关闭处理
    def closeEvent(self, event):

        self.close()
        self.object.translation_ui.show()