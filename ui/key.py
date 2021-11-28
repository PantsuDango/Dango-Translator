# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"
EDIT_PATH = "./config/icon/edit.png"


class Key(QWidget) :

    def __init__(self, object) :

        super(Key, self).__init__()

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
        icon = QIcon()
        icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        # 鼠标样式
        pixmap = QPixmap(PIXMAP_PATH)
        pixmap = pixmap.scaled(int(20*self.rate),
                               int(20*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 鼠标编辑状态图标
        edit_pixmap = QPixmap(EDIT_PATH)
        edit_pixmap = edit_pixmap.scaled(int(20 * self.rate),
                                         int(25 * self.rate),
                                         Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
        edit_pixmap = QCursor(edit_pixmap, 0, 0)

        self.setStyleSheet("QWidget { font: 9pt '华康方圆体W7';"
                                     "color: %s;"
                                     "background: rgba(255, 255, 255, 1); }"
                           "QLineEdit { background: transparent;"
                                       "border-width:0;"
                                       "border-style:outset;"
                                       "border-bottom: 2px solid %s; }"
                          "QLineEdit:focus { border-bottom: 2px "
                                            "dashed %s; }"
                           %(self.color, self.color, self.color))

        # 百度OCR API Key 输入框
        self.baidu_ocr_key_textEdit = QLineEdit(self)
        self.customSetGeometry(self.baidu_ocr_key_textEdit, 20, 10, 330, 25)
        self.baidu_ocr_key_textEdit.setPlaceholderText("百度OCR API Key")
        self.baidu_ocr_key_textEdit.setText(self.object.config["OCR"]["Key"])
        self.baidu_ocr_key_textEdit.hide()
        self.baidu_ocr_key_textEdit.setCursor(edit_pixmap)

        # 百度OCR Secret Key 输入框
        self.baidu_ocr_secret_textEdit = QLineEdit(self)
        self.customSetGeometry(self.baidu_ocr_secret_textEdit, 20, 45, 330, 25)
        self.baidu_ocr_secret_textEdit.setPlaceholderText("百度OCR Secret Key")
        self.baidu_ocr_secret_textEdit.setText(self.object.config["OCR"]["Secret"])
        self.baidu_ocr_secret_textEdit.hide()
        self.baidu_ocr_secret_textEdit.setCursor(edit_pixmap)

        # 私人腾讯 SecretId 输入框
        self.tencent_private_key_textEdit = QLineEdit(self)
        self.customSetGeometry(self.tencent_private_key_textEdit, 20, 10, 330, 25)
        self.tencent_private_key_textEdit.setPlaceholderText("私人腾讯 SecretId")
        self.tencent_private_key_textEdit.setText(self.object.config["tencentAPI"]["Key"])
        self.tencent_private_key_textEdit.hide()
        self.tencent_private_key_textEdit.setCursor(edit_pixmap)

        # 私人腾讯 SecretKey 输入框
        self.tencent_private_secret_textEdit = QLineEdit(self)
        self.customSetGeometry(self.tencent_private_secret_textEdit, 20, 45, 330, 25)
        self.tencent_private_secret_textEdit.setPlaceholderText("私人腾讯 SecretKey")
        self.tencent_private_secret_textEdit.setText(self.object.config["tencentAPI"]["Secret"])
        self.tencent_private_secret_textEdit.hide()
        self.tencent_private_secret_textEdit.setCursor(edit_pixmap)

        # 私人百度 APP ID 输入框
        self.baidu_private_key_textEdit = QLineEdit(self)
        self.customSetGeometry(self.baidu_private_key_textEdit, 20, 10, 330, 25)
        self.baidu_private_key_textEdit.setPlaceholderText("私人百度 APP ID")
        self.baidu_private_key_textEdit.setText(self.object.config["baiduAPI"]["Key"])
        self.baidu_private_key_textEdit.hide()
        self.baidu_private_key_textEdit.setCursor(edit_pixmap)

        # 私人百度 密钥 输入框
        self.baidu_private_secret_textEdit = QLineEdit(self)
        self.customSetGeometry(self.baidu_private_secret_textEdit, 20, 45, 330, 25)
        self.baidu_private_secret_textEdit.setPlaceholderText("私人百度 密钥")
        self.baidu_private_secret_textEdit.setText(self.object.config["baiduAPI"]["Secret"])
        self.baidu_private_secret_textEdit.hide()
        self.baidu_private_secret_textEdit.setCursor(edit_pixmap)

        # 私人彩云 APP ID 输入框
        self.caiyun_private_key_textEdit = QLineEdit(self)
        self.customSetGeometry(self.caiyun_private_key_textEdit, 20, 20, 330, 25)
        self.caiyun_private_key_textEdit.setPlaceholderText("私人彩云 令牌")
        self.caiyun_private_key_textEdit.setText(self.object.config["caiyunAPI"])
        self.caiyun_private_key_textEdit.hide()
        self.caiyun_private_key_textEdit.setCursor(edit_pixmap)


    # 初始化配置
    def getInitConfig(self) :

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面尺寸
        self.window_width = int(370 * self.rate)
        self.window_height = int(95 * self.rate)
        # 颜色
        self.color = "#5B8FF9"


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    def filterNullWord(self, obj) :

        return obj.text().replace(' ', '').replace('\n', '').replace('\t', '')


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.object.config["OCR"]["Key"] = self.filterNullWord(self.baidu_ocr_key_textEdit)
        self.object.config["OCR"]["Secret"] = self.filterNullWord(self.baidu_ocr_secret_textEdit)
        self.object.config["tencentAPI"]["Key"] = self.filterNullWord(self.tencent_private_key_textEdit)
        self.object.config["tencentAPI"]["Secret"] = self.filterNullWord(self.tencent_private_secret_textEdit)
        self.object.config["baiduAPI"]["Key"] = self.filterNullWord(self.baidu_private_key_textEdit)
        self.object.config["baiduAPI"]["Secret"] = self.filterNullWord(self.baidu_private_secret_textEdit)
        self.object.config["caiyunAPI"] = self.filterNullWord(self.caiyun_private_key_textEdit)

        self.baidu_ocr_key_textEdit.hide()
        self.baidu_ocr_secret_textEdit.hide()
        self.tencent_private_key_textEdit.hide()
        self.tencent_private_secret_textEdit.hide()
        self.baidu_private_key_textEdit.hide()
        self.baidu_private_secret_textEdit.hide()
        self.caiyun_private_key_textEdit.hide()