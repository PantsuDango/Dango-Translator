# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import utils.message

LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"


class HotKey(QWidget):

    def __init__(self, object):

        super(HotKey, self).__init__()

        self.object = object
        self.getInitConfig()
        self.ui()

    def ui(self):

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 窗口图标
        icon = QIcon()
        icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        # 鼠标样式
        pixmap = QPixmap(PIXMAP_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
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
                           % (self.color_2, 6.66*self.rate))

        label = QLabel(self)
        self.customSetGeometry(label, 30, 10, 300, 50)
        label.setText("不支持单键\n"
                      "仅支持 ctrl/shitf/win/alt + 任意键\n"
                      "示例 ctrl+z / alt+f1")
        label.setStyleSheet("font: 10pt '华康方圆体W7';")

        # 键位一
        comboBox_list_1 = ["ctrl", "win", "alt", "shift"]
        self.comboBox_1 = QComboBox(self)
        self.customSetGeometry(self.comboBox_1, 30, 80, 100, 20)
        for index, val in enumerate(comboBox_list_1) :
            self.comboBox_1.addItem("")
            self.comboBox_1.setItemText(index, val)
        self.comboBox_1.setStyleSheet("background: rgba(255, 255, 255, 1);")

        label = QLabel(self)
        self.customSetGeometry(label, 145, 80, 50, 20)
        label.setText("+")

        # 键位二
        comboBox_list_2 = ["ctrl", "win", "alt", "shift"]
        comboBox_list_2 += [chr(ch) for ch in range(97, 123)]
        comboBox_list_2 += [chr(ch) for ch in range(48, 58)]
        comboBox_list_2 += ["f"+str(ch) for ch in range(0, 10)]
        self.comboBox_2 = QComboBox(self)
        self.customSetGeometry(self.comboBox_2, 170, 80, 100, 20)
        for index, val in enumerate(comboBox_list_2):
            self.comboBox_2.addItem("")
            self.comboBox_2.setItemText(index, val)
        self.comboBox_2.setStyleSheet("background: rgba(255, 255, 255, 1);")

        # 确定按钮
        self.sure_button = QPushButton(self)
        self.customSetGeometry(self.sure_button, 130, 160, 70, 25)
        self.sure_button.setText("确定")
        self.sure_button.setCursor(QCursor(Qt.PointingHandCursor))

        # 取消按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 210, 160, 70, 25)
        button.setText("取消")
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.clicked.connect(self.close)

    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
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


    # 按下确定键
    def sure(self, key_type) :

        if self.comboBox_1.currentText() == self.comboBox_2.currentText() :
            utils.message.MessageBox("这是来自团子的警告~",
                                     "键位一和键位二不可重复ヽ(･ω･´ﾒ)     ")
            return

        content = self.comboBox_1.currentText() + "+" + self.comboBox_2.currentText()

        if key_type == "translate" :
            self.object.settin_ui.translate_hotkey_button.setText(content)
            self.object.config["translateHotkeyValue1"] = self.comboBox_1.currentText()
            self.object.config["translateHotkeyValue2"] = self.comboBox_2.currentText()

        elif key_type == "range" :
            self.object.settin_ui.range_hotkey_button.setText(content)
            self.object.config["rangeHotkeyValue1"] = self.comboBox_1.currentText()
            self.object.config["rangeHotkeyValue2"] = self.comboBox_2.currentText()

        self.close()