# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"
QQ_GROUP_IMAGE_PATH = "./config/other/交流群.png"


class Desc(QWidget) :

    def __init__(self, config) :

        super(Desc, self).__init__()

        self.config = config
        self.getInitConfig()

        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("说明")

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 鼠标样式
        pixmap = QPixmap(PIXMAP_PATH)
        pixmap = pixmap.scaled(int(30*self.rate),
                               int(34*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 设置字体
        self.setStyleSheet("font: 9pt '华康方圆体W7';")

        # 背景图
        image_label = QLabel(self)
        image_label.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        image_label.setStyleSheet("border-image: url(./config/background/settin-desc.jpg);")

        # 说明框
        self.desc_text = QTextBrowser(self)
        self.desc_text.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        self.desc_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.desc_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.desc_text.setStyleSheet("QTextBrowser { border-width: 0;"
                                                    "border-style: outset;"
                                                    "border-top:0px solid #e8f3f9;"
                                                    "color: #5B8FF9;"
                                                    "background: rgba(255, 255, 255, 0.7); }")

        pix = QPixmap(QQ_GROUP_IMAGE_PATH)
        pix = pix.scaled(int(200 * self.rate),
                         int(210 * self.rate),
                         Qt.KeepAspectRatio,
                         Qt.SmoothTransformation)
        self.qq_group_image = QLabel(self)
        self.customSetGeometry(self.qq_group_image, 0, 0, 200, 250)
        self.qq_group_image.setPixmap(pix)
        self.qq_group_image.hide()


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.config["screenScaleRate"]
        # 界面尺寸
        self.window_width = int(200 * self.rate)
        self.window_height = int(250 * self.rate)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))