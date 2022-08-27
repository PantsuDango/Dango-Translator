# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"
QQ_GROUP_IMAGE_PATH = "./config/other/交流群.png"
BG_IMAGE_PATH = "./config/background/settin-desc.jpg"


class Desc(QWidget) :

    def __init__(self, object) :

        super(Desc, self).__init__()

        self.object = object
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
        pixmap = pixmap.scaled(int(20*self.rate),
                               int(20*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size, self.font_type))

        # 背景图
        image_label = QLabel(self)
        image_label.setGeometry(QRect(0, 0, self.window_width, self.window_height))

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
        self.desc_text.setCursor(cursor)
        # self.document = self.desc_text.document()
        # self.document.contentsChanged.connect(self.textAreaChanged)

        pix = QPixmap(QQ_GROUP_IMAGE_PATH)
        pix = pix.scaled(int(200 * self.rate),
                         int(210 * self.rate),
                         Qt.KeepAspectRatio,
                         Qt.SmoothTransformation)
        qq_group_image = QLabel(self)
        self.customSetGeometry(qq_group_image, 0, 0, 200, 250)
        qq_group_image .setPixmap(pix)
        qq_group_image.hide()


    def textAreaChanged(self) :

        self.document.adjustSize()
        newHeight = self.document.size().height() + 20
        if newHeight != self.desc_text.height():
            self.setFixedHeight(newHeight)


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 10
        # 界面尺寸
        self.window_width = int(250 * self.rate)
        self.window_height = int(300 * self.rate)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))