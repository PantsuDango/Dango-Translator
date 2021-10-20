# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"


class HotKey(QWidget):

    def __init__(self, config):

        super(HotKey, self).__init__()

        self.config = config
        self.getInitConfig()

        self.ui()

    def ui(self):

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 鼠标样式
        pixmap = QPixmap(PIXMAP_PATH)
        pixmap = pixmap.scaled(int(30 * self.rate),
                               int(34 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 设置字体
        self.setStyleSheet("QWidget { font: 12pt '华康方圆体W7'; "
                           "background: rgb(255, 255, 255); "
                           "color: #5B8FF9; }"
                           "QPushButton { background: %s;"
                           "border-radius: %spx;"
                           "color: rgb(255, 255, 255); }"
                           "QPushButton:hover { background-color: #83AAF9; }"
                           "QPushButton:pressed { background-color: #4480F9;"
                           "padding-left:3px;"
                           "padding-top:3px; }"
                           % (self.color_2, 6.66 * self.rate))

        label = QLabel(self)
        self.customSetGeometry(label, 35, 40, 300, 20)
        label.setText("请直接在键盘上输入新的快捷键")

        # 快捷键说明标签
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        # 确定按钮
        self.sure_button = QPushButton(self)
        self.customSetGeometry(self.sure_button, 130, 160, 70, 25)
        self.sure_button.setText("确定")
        self.sure_button.setCursor(QCursor(Qt.PointingHandCursor))

        # 确定按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 210, 160, 70, 25)
        button.setText("取消")
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.clicked.connect(self.close)

    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.config["screenScaleRate"]
        # 界面尺寸
        self.window_width = int(300 * self.rate)
        self.window_height = int(200 * self.rate)
        # 所使用的颜色
        self.color_1 = "#595959"  # 灰色
        self.color_2 = "#5B8FF9"  # 蓝色


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))

    # 检测按下的按键
    def keyPressEvent(self, event):

        # F1-F2
        if 16777264 <= event.key() <= 16777275:
            arr = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
            index = event.key() - 16777264
            key = arr[index]
            self.key = key
        # 数字0-9
        elif 48 <= event.key() <= 57:
            key = chr(event.key())
            self.key = key
        # 字母A-Z
        elif 65 <= event.key() <= 90:
            key = chr(event.key())
            self.key = key
        else:
            key = "无效的键位"

        self.label.setText(key)
        width = self.label.width()
        self.customSetGeometry(self.label, (300 - width) // 2, 80, width, 20)


    # 按下确定键
    def sure(self, object):

        object.setText(self.key)
        self.close()
