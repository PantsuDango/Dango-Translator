# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

import image
import json
import webbrowser
from os import startfile

from API import get_Access_Token
from API import message_thread, message


def register_OCR():
    
    try:
        startfile('.\\各种API注册教程\\（必填）OCR API注册方法.docx')
    except Exception:
        pass


def select_baidu():

    url = 'https://api.fanyi.baidu.com/api/trans/product/desktop'
    try:
        webbrowser.open(url, new=0, autoraise=True)
    except Exception:
        pass


def register_baidu():

    try:
        startfile('.\\各种API注册教程\\百度翻译API注册方法.docx')
    except Exception:
        pass


def register_tencent():
    
    try:
        startfile('.\\各种API注册教程\\腾讯翻译API注册方法.docx')
    except Exception:
        pass

def select_tencent():
    
    url = 'https://console.cloud.tencent.com/tmt'
    try:
        webbrowser.open(url, new=0, autoraise=True)
    except Exception:
        pass


class SettinInterface(QWidget):

    def __init__(self):
        
        super(SettinInterface, self).__init__()
        self.get_settin()
        self.setupUi()
    

    def setupUi(self):

        # 窗口尺寸及不可拉伸
        self.resize(406, 476)
        self.setMinimumSize(QtCore.QSize(406, 476))
        self.setMaximumSize(QtCore.QSize(406, 476))

        # 窗口标题
        self.setWindowTitle("团子翻译器 Ver3.1 - 设置")

        # 窗口样式
        self.setStyleSheet("QWidget {""font: 10pt \"华康方圆体W7\";"
                                      "background-image: url(Background.jpg);"
                                      "background-repeat: no-repeat;"
                                      "background-size:cover;""}")
        
        # 窗口图标
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/image/图标.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setWindowIcon(self.icon)

        # 鼠标样式
        self.pixmap = QPixmap('.\\config\\光标.png')
        self.cursor = QCursor(self.pixmap, 0, 0)
        self.setCursor(self.cursor)
        
        # 顶部工具栏
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 408, 478))
        self.tabWidget.setCurrentIndex(0)

        # 工具栏样式
        self.tabWidget.setStyleSheet("QTabBar::tab {""min-width:74px;"
                                                     "background: rgba(255, 255, 255, 0.4);""}"
                                     "QTabBar::tab:selected {""border-bottom: 2px solid #4796f0;""}"
                                     "QLabel{""background: transparent;""}"
                                     "QCheckBox{""background: transparent;""}")
        
        # 工具栏1
        self.tab_1 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_1, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), "API设定")

        # 此Label用于雾化工具栏1的背景图
        self.bgImage1 = QLabel(self.tab_1)
        self.bgImage1.setGeometry(QRect(0, 0, 406, 476))
        self.bgImage1.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        
        # OCR API标签
        self.OCR_label_1 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_1.setGeometry(QtCore.QRect(20, 20, 261, 16))
        self.OCR_label_1.setText("<font color=red>（必填）</font><font >OCR API：用于识别要翻译的文字</font>")

        # OCR API Key输入框
        self.OCR_Key_Text = QtWidgets.QTextEdit(self.tab_1)
        self.OCR_Key_Text.setGeometry(QtCore.QRect(30, 45, 330, 22))
        self.OCR_Key_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                                     "border-width:0; border-style:outset;"
                                                     "border-bottom: 2px solid #92a8d1;""}"
                                        "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.OCR_Key_Text.setPlaceholderText("OCR API Key")
        self.OCR_Key_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Key_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Key_Text.setPlainText(self.OCR_Key)

        # OCR API Key输入框右侧红点标签
        self.OCR_label_4 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_4.setGeometry(QtCore.QRect(370, 50, 16, 16))
        self.OCR_label_4.setStyleSheet("color: #f00000")
        self.OCR_label_4.setText("*")

        # OCR API Secret输入框
        self.OCR_Secret_Text = QtWidgets.QTextEdit(self.tab_1)
        self.OCR_Secret_Text.setGeometry(QtCore.QRect(30, 70, 330, 22))
        self.OCR_Secret_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                                     "border-width:0; border-style:outset;"
                                                     "border-bottom: 2px solid #92a8d1;""}"
                                           "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.OCR_Secret_Text.setPlaceholderText("OCR API Secret")
        self.OCR_Secret_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Secret_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Secret_Text.setPlainText(self.OCR_Secret)

        # OCR API Secret输入框右侧红点标签
        self.OCR_label_5 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_5.setGeometry(QtCore.QRect(370, 75, 16, 16))
        self.OCR_label_5.setStyleSheet("color: #f00000")
        self.OCR_label_5.setText("*")
        
        # 注册OCR API按钮
        self.OCRRegister_Button = QtWidgets.QPushButton(self.tab_1)
        self.OCRRegister_Button.setGeometry(QtCore.QRect(160, 95, 80, 30))
        self.OCRRegister_Button.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.OCRRegister_Button.clicked.connect(register_OCR)
        self.OCRRegister_Button.setText("注册OCR")
        
        # 百度翻译API标签
        self.baiduAPI_label_1 = QtWidgets.QLabel(self.tab_1)
        self.baiduAPI_label_1.setGeometry(QtCore.QRect(20, 140, 281, 16))
        self.baiduAPI_label_1.setText("（选填）百度翻译 API：每月额度200万字符")
        
        # 百度翻译API APP ID输入框
        self.baidu_Key_Text = QtWidgets.QTextEdit(self.tab_1)
        self.baidu_Key_Text.setGeometry(QtCore.QRect(30, 165, 330, 22))
        self.baidu_Key_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                                     "border-width:0; border-style:outset;"
                                                     "border-bottom: 2px solid #92a8d1;""}"
                                          "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.baidu_Key_Text.setPlaceholderText("百度翻译API APP ID")
        self.baidu_Key_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Key_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Key_Text.setPlainText(self.baidu_Key)

        # 百度翻译API 密钥输入框
        self.baidu_Secret_Text = QtWidgets.QTextEdit(self.tab_1)
        self.baidu_Secret_Text.setGeometry(QtCore.QRect(30, 190, 330, 22))
        self.baidu_Secret_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                                     "border-width:0; border-style:outset;"
                                                     "border-bottom: 2px solid #92a8d1;""}"
                                             "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.baidu_Secret_Text.setPlaceholderText("百度翻译API 密钥")
        self.baidu_Secret_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Secret_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Secret_Text.setPlainText(self.baidu_Secret)

        # 百度翻译API注册按钮
        self.baiduRegister_Button = QtWidgets.QPushButton(self.tab_1)
        self.baiduRegister_Button.setGeometry(QtCore.QRect(90, 220, 80, 30))
        self.baiduRegister_Button.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.baiduRegister_Button.clicked.connect(register_baidu)
        self.baiduRegister_Button.setText("注册百度")

        # 百度翻译API额度查询按钮
        self.baiduSelect_Button = QtWidgets.QPushButton(self.tab_1)
        self.baiduSelect_Button.setGeometry(QtCore.QRect(237, 220, 80, 30))
        self.baiduSelect_Button.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.baiduSelect_Button.clicked.connect(select_baidu)
        self.baiduSelect_Button.setText("额度查询")

        # 腾讯翻译API标签
        self.TencentAPI_laber_1 = QtWidgets.QLabel(self.tab_1)
        self.TencentAPI_laber_1.setGeometry(QtCore.QRect(20, 260, 281, 16))
        self.TencentAPI_laber_1.setText("（选填）腾讯翻译 API：每月额度500万字符")

        # 腾讯翻译API Secretld输入框
        self.tencent_Key_Text = QtWidgets.QTextEdit(self.tab_1)
        self.tencent_Key_Text.setGeometry(QtCore.QRect(30, 285, 330, 22))
        self.tencent_Key_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                                     "border-width:0; border-style:outset;"
                                                     "border-bottom: 2px solid #92a8d1;""}"
                                            "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.tencent_Key_Text.setPlaceholderText("腾讯翻译API Secretld")
        self.tencent_Key_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Key_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Key_Text.setPlainText(self.tencent_Key)
        
        # 腾讯翻译API SecretKey输入框
        self.tencent_Secret_Text = QtWidgets.QTextEdit(self.tab_1)
        self.tencent_Secret_Text.setGeometry(QtCore.QRect(30, 310, 330, 22))
        self.tencent_Secret_Text.setStyleSheet("QTextEdit {""background: transparent;"
                                                     "border-width:0; border-style:outset;"
                                                     "border-bottom: 2px solid #92a8d1;""}"
                                               "QTextEdit:focus {""border-bottom: 2px dashed #9265d1;""}")
        self.tencent_Secret_Text.setPlaceholderText("腾讯翻译API SecretKey")
        self.tencent_Secret_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Secret_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Secret_Text.setPlainText(self.tencent_Secret)

        # 腾讯翻译API注册按钮
        self.tencentRegister_Button = QtWidgets.QPushButton(self.tab_1)
        self.tencentRegister_Button.setGeometry(QtCore.QRect(90, 340, 80, 30))
        self.tencentRegister_Button.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.tencentRegister_Button.setObjectName("tencentRegister_Button")
        self.tencentRegister_Button.clicked.connect(register_tencent)
        self.tencentRegister_Button.setText("注册腾讯")

        # 腾讯翻译API额度查询按钮
        self.tencentSelect_Button = QtWidgets.QPushButton(self.tab_1)
        self.tencentSelect_Button.setGeometry(QtCore.QRect(237, 340, 80, 30))
        self.tencentSelect_Button.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.tencentSelect_Button.setObjectName("tencentSelect_Button")
        self.tencentSelect_Button.clicked.connect(select_tencent)
        self.tencentSelect_Button.setText("额度查询")
        

        # 工具栏2
        self.tab_2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "翻译源设定")

        # 此Label用于雾化工具栏2的背景图
        self.bgImage2 = QLabel(self.tab_2)
        self.bgImage2.setGeometry(QRect(0, 0, 406, 476))
        self.bgImage2.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        
        # 翻译源标签
        self.translateSource_label_1 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_1.setGeometry(QtCore.QRect(30, 20, 191, 16))
        self.translateSource_label_1.setText("翻译源：选择你想使用的翻译")

        # 公共翻译接口标签
        self.translateSource_label_2 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_2.setGeometry(QtCore.QRect(30, 50, 220, 16))
        self.translateSource_label_2.setText("公共（可直接使用，但可能会失效）")

        # 有道翻译checkBox
        self.youdao_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.youdao_checkBox.setGeometry(QtCore.QRect(30, 80, 80, 16))
        self.youdao_checkBox.setChecked(self.youdaoUse)
        self.youdao_checkBox.setText("有道翻译")
        
        # 彩云翻译checkBox
        self.caiyun_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.caiyun_checkBox.setGeometry(QtCore.QRect(160, 80, 80, 16))
        self.caiyun_checkBox.setChecked(self.caiyunUse)
        self.caiyun_checkBox.setText("彩云小泽")
        
        # 金山翻译checkBox
        self.jinshan_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.jinshan_checkBox.setGeometry(QtCore.QRect(290, 80, 80, 16))
        self.jinshan_checkBox.setChecked(self.jinshanUse)
        self.jinshan_checkBox.setText("金山词霸")

        # yeekit翻译checkBox
        self.yeekit_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.yeekit_checkBox.setGeometry(QtCore.QRect(30, 110, 91, 16))
        self.yeekit_checkBox.setChecked(self.yeekitUse)
        self.yeekit_checkBox.setText("yeekit")

        # ALAPI翻译checkBox
        self.ALAPI_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.ALAPI_checkBox.setGeometry(QtCore.QRect(160, 110, 80, 16))
        self.ALAPI_checkBox.setChecked(self.alapiUse)
        self.ALAPI_checkBox.setText("ALAPI")

        # 网页翻译接口标签
        self.translateSource_label_4 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_4.setGeometry(QtCore.QRect(30, 150, 320, 16))
        self.translateSource_label_4.setText("网页版（可直接使用，以后会考虑加入其它网页版）")

        # 百度翻译网页版checkBox
        self.baiduweb_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.baiduweb_checkBox.setGeometry(QtCore.QRect(30, 190, 131, 16))
        self.baiduweb_checkBox.setChecked(self.baiduwebUse)
        self.baiduweb_checkBox.setText("网页版百度翻译")

        # 私人翻译接口标签
        self.translateSource_label_3 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_3.setGeometry(QtCore.QRect(30, 240, 271, 16))
        self.translateSource_label_3.setText("私人API（使用稳定，但需注册后才可使用）")

        # 百度翻译私人版checkBox
        self.baidu_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.baidu_checkBox.setGeometry(QtCore.QRect(30, 280, 80, 16))
        self.baidu_checkBox.setChecked(self.baiduUse)
        self.baidu_checkBox.setText("百度翻译")
        
        # 腾讯翻译私人版checkBox
        self.tencent_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.tencent_checkBox.setGeometry(QtCore.QRect(160, 280, 80, 16))
        self.tencent_checkBox.setChecked(self.tencentUse)
        self.tencent_checkBox.setText("腾讯翻译")

        # 翻译语种标签
        self.translateSource_label_6 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_6.setGeometry(QtCore.QRect(30, 330, 151, 16))
        self.translateSource_label_6.setText("选择你要翻译的原语言：")

        # 翻译语种comboBox
        self.language_comboBox = QtWidgets.QComboBox(self.tab_2)
        self.language_comboBox.setGeometry(QtCore.QRect(200, 327, 131, 22))
        self.language_comboBox.addItem("")
        self.language_comboBox.addItem("")
        self.language_comboBox.addItem("")
        self.language_comboBox.setItemText(0, "日语（Japanese）")
        self.language_comboBox.setItemText(1, "英语（English）")
        self.language_comboBox.setItemText(2, "韩语（Korean）")
        self.language_comboBox.setCurrentIndex(self.language)


        # 工具栏3
        self.tab_3 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_3, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "翻译样式")

        # 此Label用于雾化工具栏3的背景图
        self.bgImage3 = QLabel(self.tab_3)
        self.bgImage3.setGeometry(QRect(0, 0, 406, 476))
        self.bgImage3.setStyleSheet("background: rgba(255, 255, 255, 0.4);")

        # 翻译字体颜色设定标签
        self.colour_label_2 = QtWidgets.QLabel(self.tab_3)
        self.colour_label_2.setGeometry(QtCore.QRect(30, 20, 141, 16))
        self.colour_label_2.setText("翻译文字的颜色设定：")

        # 有道翻译颜色按钮
        self.youdaoColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.youdaoColour_toolButton.setGeometry(QtCore.QRect(30, 50, 71, 25))
        self.youdaoColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.youdaoColor))
        self.youdaoColour_toolButton.clicked.connect(lambda:self.get_font_color(1))
        self.youdaoColour_toolButton.setText("有道翻译")

        # 彩云翻译颜色按钮
        self.caiyunColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.caiyunColour_toolButton.setGeometry(QtCore.QRect(150, 50, 71, 25))
        self.caiyunColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.caiyunColor))
        self.caiyunColour_toolButton.clicked.connect(lambda:self.get_font_color(2))
        self.caiyunColour_toolButton.setText("彩云小泽")

        # 金山翻译颜色按钮
        self.jinshanColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.jinshanColour_toolButton.setGeometry(QtCore.QRect(270, 50, 71, 25))
        self.jinshanColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.jinshanColor))
        self.jinshanColour_toolButton.clicked.connect(lambda:self.get_font_color(3))
        self.jinshanColour_toolButton.setText("金山词霸")

        # yeekit翻译颜色按钮
        self.yeekitColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.yeekitColour_toolButton.setGeometry(QtCore.QRect(30, 90, 71, 25))
        self.yeekitColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.yeekitColor))
        self.yeekitColour_toolButton.clicked.connect(lambda:self.get_font_color(4))
        self.yeekitColour_toolButton.setText("yeekit")

        # alapi翻译颜色按钮
        self.alapiColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.alapiColour_toolButton.setGeometry(QtCore.QRect(150, 90, 71, 25))
        self.alapiColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.ALAPIColor))
        self.alapiColour_toolButton.clicked.connect(lambda:self.get_font_color(5))
        self.alapiColour_toolButton.setText("ALAPI")
 
        # 百度翻译网页版颜色按钮
        self.baiduwebColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.baiduwebColour_toolButton.setGeometry(QtCore.QRect(270, 90, 71, 25))
        self.baiduwebColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.baiduwebColor))
        self.baiduwebColour_toolButton.clicked.connect(lambda:self.get_font_color(6))
        self.baiduwebColour_toolButton.setText("网页百度")

        # 百度翻译私人版颜色按钮
        self.baiduColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.baiduColour_toolButton.setGeometry(QtCore.QRect(30, 130, 71, 25))
        self.baiduColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.baiduColor))
        self.baiduColour_toolButton.clicked.connect(lambda:self.get_font_color(7))
        self.baiduColour_toolButton.setText("私人百度")

        # 腾讯翻译颜色按钮
        self.tencentColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.tencentColour_toolButton.setGeometry(QtCore.QRect(150, 130, 71, 25))
        self.tencentColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.tencentColor))
        self.tencentColour_toolButton.clicked.connect(lambda:self.get_font_color(8))
        self.tencentColour_toolButton.setText("私人腾讯")
        
        # 原文颜色按钮
        self.originalColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.originalColour_toolButton.setGeometry(QtCore.QRect(270, 130, 71, 25))
        self.originalColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.originalColor))
        self.originalColour_toolButton.clicked.connect(lambda:self.get_font_color(9))
        self.originalColour_toolButton.setText("原  文")

        # 翻译字体大小设定标签
        self.colour_label_3 = QtWidgets.QLabel(self.tab_3)
        self.colour_label_3.setGeometry(QtCore.QRect(30, 180, 141, 16))
        self.colour_label_3.setText("翻译文字的大小设定：")

        # 翻译字体大小设定
        self.fontSize_spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.fontSize_spinBox.setGeometry(QtCore.QRect(180, 175, 40, 25))
        self.fontSize_spinBox.setMinimum(10)
        self.fontSize_spinBox.setMaximum(20)
        self.fontSize_spinBox.setValue(self.fontSize)

        # 翻译字体样式设定标签
        self.colour_label_4 = QtWidgets.QLabel(self.tab_3)
        self.colour_label_4.setGeometry(QtCore.QRect(30, 220, 141, 20))
        self.colour_label_4.setText("翻译文字的字体设定：")

        # 翻译字体样式设定        
        self.fontComboBox = QtWidgets.QFontComboBox(self.tab_3)
        self.fontComboBox.setGeometry(QtCore.QRect(180, 220, 151, 25))
        self.fontComboBox.activated[str].connect(self.get_fontType)
        self.ComboBoxFont = QtGui.QFont(self.fontType)
        self.fontComboBox.setCurrentFont(self.ComboBoxFont)

        # 显示原文checkBox
        self.showOriginal_checkBox = QtWidgets.QCheckBox(self.tab_3)
        self.showOriginal_checkBox.setGeometry(QtCore.QRect(30, 260, 201, 20))
        self.showOriginal_checkBox.setChecked(self.showOriginal)
        self.showOriginal_checkBox.setText("翻译时是否显示识别到的原文")

        # 自动翻译设置标签
        self.translateSource_label_5 = QtWidgets.QLabel(self.tab_3)
        self.translateSource_label_5.setGeometry(QtCore.QRect(30, 305, 271, 16))
        self.translateSource_label_5.setText("自动翻译设置：设置自动翻译时的刷新频率")

        # 自动模式速率标签1
        self.translateMode_label_2 = QtWidgets.QLabel(self.tab_3)
        self.translateMode_label_2.setGeometry(QtCore.QRect(30, 345, 91, 16))
        self.translateMode_label_2.setText("自动模式下每")

        # 自动模式速率设定
        self.autoSpeed_spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.autoSpeed_spinBox.setGeometry(QtCore.QRect(130, 340, 40, 25))
        self.autoSpeed_spinBox.setStyleSheet("background: transparent;")
        self.autoSpeed_spinBox.setMinimum(1)
        self.autoSpeed_spinBox.setMaximum(5)
        self.autoSpeed_spinBox.setValue(self.translateSpeed)
        
        # 自动模式速率标签2
        self.translateMode_label_3 = QtWidgets.QLabel(self.tab_3)
        self.translateMode_label_3.setGeometry(QtCore.QRect(190, 345, 101, 16))
        self.translateMode_label_3.setText("秒刷新一次翻译")
        

        # 工具栏4
        self.tab_4 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_4, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), "其他设定")

        # 此Label用于雾化工具栏4的背景图
        self.bgImage4 = QLabel(self.tab_4)
        self.bgImage4.setGeometry(QRect(0, 0, 406, 476))
        self.bgImage4.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        
        # 翻译框透明度设定标签1
        self.tab4_label_1 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_1.setGeometry(QtCore.QRect(30, 25, 211, 16))
        self.tab4_label_1.setText("翻译框透明度：调节其背景色深度")
        
        # 翻译框透明度设定
        self.horizontalSlider = QtWidgets.QSlider(self.tab_4)
        self.horizontalSlider.setGeometry(QtCore.QRect(30, 55, 347, 22))
        self.horizontalSlider.setStyleSheet("background: transparent;")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setValue(self.horizontal)
        self.horizontalSlider.valueChanged.connect(self.get_horizontal)

        # 翻译框透明度设定标签2
        self.tab4_label_2 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_2.setGeometry(QtCore.QRect(30, 85, 61, 20))
        self.tab4_label_2.setObjectName("tab4_label_2")
        self.tab4_label_2.setText("完全透明")
        
        # 翻译框透明度设定标签3
        self.tab4_label_3 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_3.setGeometry(QtCore.QRect(310, 85, 71, 20))
        self.tab4_label_3.setText("完全不透明")

        # 其他设定标签
        self.tab4_label_4 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_4.setGeometry(QtCore.QRect(30, 120, 201, 16))
        self.tab4_label_4.setText("其他设定：一些独立的其他设定")
        
        # 原文自动复制到剪贴板checkBox
        self.Clipboard_checkBox = QtWidgets.QCheckBox(self.tab_4)
        self.Clipboard_checkBox.setGeometry(QtCore.QRect(30, 155, 231, 16))
        self.Clipboard_checkBox.setChecked(self.showClipboard)
        self.Clipboard_checkBox.setText("是否启用将原文自动复制到剪贴板")

        # 快捷键checkBox
        self.shortcutKey_checkBox = QtWidgets.QCheckBox(self.tab_4)
        self.shortcutKey_checkBox.setGeometry(QtCore.QRect(30, 200, 131, 16))
        self.shortcutKey_checkBox.setStyleSheet("background: transparent;")
        self.shortcutKey_checkBox.setChecked(self.showHotKey)
        self.shortcutKey_checkBox.setText("是否启用快捷键：")

        # 快捷键键1输入框
        self.shortcutKey_textEdit_1 = QtWidgets.QComboBox(self.tab_4)
        self.shortcutKey_textEdit_1.setGeometry(QtCore.QRect(170, 195, 51, 21))
        self.shortcutKey_textEdit_1.addItem("")
        self.shortcutKey_textEdit_1.addItem("")
        self.shortcutKey_textEdit_1.addItem("")
        self.shortcutKey_textEdit_1.setItemText(0, "alt")
        self.shortcutKey_textEdit_1.setItemText(1, "ctrl")
        self.shortcutKey_textEdit_1.setItemText(2, "shift")
        self.shortcutKey_textEdit_1.setCurrentIndex(self.showHotKeyValue1)

        # 快捷键+号标签
        self.tab4_label_8 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_8.setGeometry(QtCore.QRect(230, 195, 10, 20))
        self.tab4_label_8.setText("+")
        
        # 快捷键键2输入框
        self.shortcutKey_textEdit_2 = QtWidgets.QTextEdit(self.tab_4)
        self.shortcutKey_textEdit_2.setGeometry(QtCore.QRect(245, 195, 51, 21))
        self.shortcutKey_textEdit_2.setStyleSheet("background: transparent;")
        self.shortcutKey_textEdit_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.shortcutKey_textEdit_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.shortcutKey_textEdit_2.setPlainText(self.showHotKeyValue2)

        # 快捷键说明标签
        self.tab4_label_7 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_7.setGeometry(QtCore.QRect(30, 230, 341, 16))
        self.tab4_label_7.setText("说明：设定的两个按键同时按下生效，无效则表示冲突")

        # 背景设定标签
        self.tab4_label_5 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_5.setGeometry(QtCore.QRect(30, 270, 261, 16))
        self.tab4_label_5.setText("自定义背景：设置你喜欢的图片作为背景")
        
        # 选择背景图按钮
        self.openfileButton = QtWidgets.QPushButton(self.tab_4)
        self.openfileButton.setGeometry(QtCore.QRect(30, 310, 75, 23))
        self.openfileButton.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.openfileButton.clicked.connect(self.Select_background)
        self.openfileButton.setText("浏览文件")
        
        # 背景图路径显示框
        self.openfileText = QtWidgets.QTextBrowser(self.tab_4)
        self.openfileText.setGeometry(QtCore.QRect(120, 310, 251, 21))
        self.openfileText.setStyleSheet("background: transparent;")
        self.openfileText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.openfileText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # 背景图设定说明标签
        self.tab4_label_6 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_6.setGeometry(QtCore.QRect(30, 350, 331, 16))
        self.tab4_label_6.setText("说明：不支持png，以分辨率407 x 475时效果最佳")


        # 工具栏5
        self.tab_5 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_5, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), "支持作者")

        # 此Label用于雾化工具栏5的背景图
        self.bgImage5 = QLabel(self.tab_5)
        self.bgImage5.setGeometry(QRect(0, 0, 406, 476))
        self.bgImage5.setStyleSheet("background: rgba(255, 255, 255, 0.4);")

        # 充电独白标签
        self.Mysay_label = QtWidgets.QLabel(self.tab_5)
        self.Mysay_label.setGeometry(QtCore.QRect(40, 10, 281, 141))
        self.Mysay_label.setText("<html><head/><body><p>大家好，我是胖次团子 ❤\
                                  </p><p>谢谢大家使用团子翻译器Ver3.1 ~\
                                  </p><p>软件是免费的，但是若能收到你的充电支持 ~\
                                  </p><p>我会非常开心的，这会是我后续更新的动力 ~\
                                  </p><p>联系方式：QQ 394883561</p></body></html>")

        # 放置微信收款图片
        self.WechatImage_label = QtWidgets.QLabel(self.tab_5)
        self.WechatImage_label.setGeometry(QtCore.QRect(20, 170, 170, 170))
        self.WechatImage_label.setStyleSheet("border-image: url(:/image/Wechat.png);")

        # 放置支付宝收款图片
        self.AlipayImage_label = QtWidgets.QLabel(self.tab_5)
        self.AlipayImage_label.setGeometry(QtCore.QRect(215, 170, 170, 170))
        self.AlipayImage_label.setStyleSheet("background-image: url(:/image/Alipay.jpg);")

        # 微信充电标签
        self.Wechat_label = QtWidgets.QLabel(self.tab_5)
        self.Wechat_label.setGeometry(QtCore.QRect(60, 350, 81, 16))
        self.Wechat_label.setStyleSheet("font: 14pt")
        self.Wechat_label.setText("微信充电")
        
        # 支付宝充电标签
        self.Alipay_label = QtWidgets.QLabel(self.tab_5)
        self.Alipay_label.setGeometry(QtCore.QRect(250, 350, 101, 16))
        self.Alipay_label.setStyleSheet("font: 14pt")
        self.Alipay_label.setText("支付宝充电")

        # 设置保存按钮
        self.SaveButton = QtWidgets.QPushButton(self)
        self.SaveButton.setGeometry(QtCore.QRect(85, 420, 90, 30))
        self.SaveButton.setStyleSheet("background-image: url(:/image/Wechat.png);font: 12pt")
        self.SaveButton.clicked.connect(lambda:message_thread(self.save_settin))
        self.SaveButton.setText("保存设置")

        # 设置返回按钮
        self.CancelButton = QtWidgets.QPushButton(self)
        self.CancelButton.setGeometry(QtCore.QRect(232, 420, 90, 30))
        self.CancelButton.setStyleSheet("background-image: url(:/image/Wechat.png);font: 12pt")
        self.CancelButton.setText("返 回")


    def get_settin(self):  # 获取所有预设值

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)

        # 获取各翻译源颜色预设值
        self.youdaoColor = self.data["fontColor"]["youdao"]
        self.caiyunColor = self.data["fontColor"]["caiyun"]
        self.jinshanColor = self.data["fontColor"]["jinshan"]
        self.yeekitColor = self.data["fontColor"]["yeekit"]
        self.ALAPIColor = self.data["fontColor"]["ALAPI"]
        self.baiduwebColor = self.data["fontColor"]["baiduweb"]
        self.baiduColor = self.data["fontColor"]["baidu"]
        self.tencentColor = self.data["fontColor"]["tencent"]
        self.originalColor = self.data["fontColor"]["original"]

        # 获取翻译字体大小预设值
        self.fontSize = self.data["fontSize"]

        # 获取翻译字体样式预设值
        self.fontType = self.data["fontType"]

        # 获取是否显示原文预设值
        self.showOriginal = self.data["showOriginal"]
        if self.showOriginal == "True":
            self.showOriginal = True
        else:
            self.showOriginal = False

        # 获取是否将原文复制到剪贴板预设值
        self.showClipboard = self.data["showClipboard"]
        if self.showClipboard == "True":
            self.showClipboard = True
        else:
            self.showClipboard = False

        # 获取快捷键的热键预设值
        self.showHotKeyValue1 = self.data["showHotKeyValue1"]
        if self.showHotKeyValue1 == 'control':
            self.showHotKeyValue1 = 1
        elif self.showHotKeyValue1 == 'shift':
            self.showHotKeyValue1 = 2
        else:
            self.showHotKeyValue1 = 0
        self.showHotKeyValue2 = self.data["showHotKeyValue2"]

        # 获取是否启用快捷键预设值
        self.showHotKey = self.data["showHotKey"]
        if self.showHotKey == "True":
            self.showHotKey = True
        else:
            self.showHotKey = False

        # 获取文本框透明度预设值
        self.horizontal = self.data["horizontal"]

        # 获取是否使用有道翻译预设值
        self.youdaoUse = self.data["youdaoUse"]
        if self.youdaoUse == "True":
            self.youdaoUse = True
        else:
            self.youdaoUse = False

        # 获取是否使用彩云翻译预设值
        self.caiyunUse = self.data["caiyunUse"]
        if self.caiyunUse == "True":
            self.caiyunUse = True
        else:
            self.caiyunUse = False

        # 获取是否使用金山翻译预设值
        self.jinshanUse = self.data["jinshanUse"]
        if self.jinshanUse == "True":
            self.jinshanUse = True
        else:
            self.jinshanUse = False

        # 获取是否使用yeekit翻译预设值
        self.yeekitUse = self.data["yeekitUse"]
        if self.yeekitUse == "True":
            self.yeekitUse = True
        else:
            self.yeekitUse = False

        # 获取是否使用alapi翻译预设值
        self.alapiUse = self.data["alapiUse"]
        if self.alapiUse == "True":
            self.alapiUse = True
        else:
            self.alapiUse = False

        # 获取是否使用百度翻译网页版预设值
        self.baiduwebUse = self.data["baiduwebUse"]
        if self.baiduwebUse == "True":
            self.baiduwebUse = True
        else:
            self.baiduwebUse = False

        # 获取是否使用百度翻译预设值
        self.baiduUse = self.data["baiduUse"]
        if self.baiduUse == "True":
            self.baiduUse = True
        else:
            self.baiduUse = False

        # 获取是否使用腾讯翻译预设值
        self.tencentUse = self.data["tencentUse"]
        if self.tencentUse == "True":
            self.tencentUse = True
        else:
            self.tencentUse = False

        # 获取自动翻译时的刷新间隔预设值
        self.translateSpeed = self.data["translateSpeed"]

        # 获取各API预设值
        self.OCR_Key = self.data["OCR"]["Key"]
        self.OCR_Secret = self.data["OCR"]["Secret"]
        self.baidu_Key = self.data["baiduAPI"]["Key"]
        self.baidu_Secret = self.data["baiduAPI"]["Secret"]
        self.tencent_Key = self.data["tencentAPI"]["Key"]
        self.tencent_Secret = self.data["tencentAPI"]["Secret"]

        # 获取翻译语言预设值
        self.language = self.data["language"]
        if self.language == 'ENG':
            self.language = 1
        elif self.language == 'KOR':
            self.language = 2
        else:
            self.language = 0


    def Select_background(self):  # 将背景图片路径打印在显示框
        
        self.image_path = QFileDialog.getOpenFileName(self,'选择要作为背景的图片文件','','image files(*.jpg , *.png)')[0]
        if self.image_path:
            self.openfileText.setText(self.image_path)


    def get_font_color(self, sign):  # 各翻译源字体颜色

        color = QColorDialog.getColor()
        if sign == 1 :
            self.youdaoColor = color.name()
            self.youdaoColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["youdao"] = self.youdaoColor
        elif sign == 2 :
            self.caiyunColor = color.name()
            self.caiyunColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["caiyun"] = self.caiyunColor
        elif sign == 3 :
            self.jinshanColor = color.name()
            self.jinshanColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["jinshan"] = self.jinshanColor
        elif sign == 4 :
            self.yeekitColor = color.name()
            self.yeekitColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["yeekit"] = self.yeekitColor
        elif sign == 5 :
            self.ALAPIColor = color.name()
            self.alapiColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["ALAPI"] = self.ALAPIColor
        elif sign == 6 :
            self.baiduwebColor = color.name()
            self.baiduwebColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["baiduweb"] = self.baiduwebColor
        elif sign == 7 :
            self.baiduColor = color.name()
            self.baiduColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["baidu"] = self.baiduColor
        elif sign == 8 :
            self.tencentColor = color.name()
            self.tencentColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["tencent"] = self.tencentColor
        elif sign == 9 :
            self.originalColor = color.name()
            self.originalColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["original"] = self.originalColor


    def change_background(self):  # 改变背景图片

        try:
            with open(self.image_path, 'rb') as file:
                self.new_image = file.read()
        except AttributeError:
            pass
        else:
            with open('Background.jpg', 'wb') as file:
                file.write(self.new_image)
            self.setStyleSheet("QWidget {""font: 10pt \"华康方圆体W7\";"
                               "background-image: url(Background.jpg);"
                               "background-repeat: no-repeat;"
                               "background-size:cover;""}")


    def get_fontType(self, text):  # 字体样式
        
        self.fontType = text
        self.data["fontType"] = self.fontType

    
    def showOriginal_state(self):  # 是否显示原文

        if self.showOriginal_checkBox.isChecked():
            self.showOriginal = "True"
        else:
            self.showOriginal = "False"
        self.data["showOriginal"] = self.showOriginal


    def showClipboard_state(self):  # 是否将原文自动复制到剪贴板

        if self.Clipboard_checkBox.isChecked():
            self.showClipboard = "True"
        else:
            self.showClipboard = "False"
        self.data["showClipboard"] = self.showClipboard


    def showHotKey_state(self):  # 是否启用快捷键

        if self.shortcutKey_checkBox.isChecked():
            self.showHotKey = "True"
        else:
            self.showHotKey = "False"
        self.data["showHotKey"] = self.showHotKey
        
        self.showHotKeyValue2 = self.shortcutKey_textEdit_2.toPlainText().replace(' ','').replace('\n','').replace('\t','')
        char = 'zxcvbnmasdfghjklqwertyuiop1234567890'
        if (self.showHotKeyValue2 in char) or (self.showHotKeyValue2 == 'space'):
            self.data["showHotKeyValue2"] = self.showHotKeyValue2
        else:
            message_thread(message, "无效的快捷键2", "快捷键2仅支持a-z，0-9，space（空格） (〃'▽'〃)")


    def get_horizontal(self):  # 文本框透明度

        self.horizontal = self.horizontalSlider.value()
        self.data["horizontal"] = self.horizontal


    def save_fontSize(self):  # 翻译源字体大小

        self.data["fontSize"] = self.fontSize_spinBox.value()


    def youdaoUse_state(self):  # 是否使用有道翻译

        if self.youdao_checkBox.isChecked():
            self.youdaoUse = "True"
        else:
            self.youdaoUse = "False"
        self.data["youdaoUse"] = self.youdaoUse


    def caiyunUse_state(self):  # 是否使用彩云翻译

        if self.caiyun_checkBox.isChecked():
            self.caiyunUse = "True"
        else:
            self.caiyunUse = "False"
        self.data["caiyunUse"] = self.caiyunUse


    def jinshanUse_state(self):  # 是否使用金山翻译

        if self.jinshan_checkBox.isChecked():
            self.jinshanUse = "True"
        else:
            self.jinshanUse = "False"
        self.data["jinshanUse"] = self.jinshanUse


    def yeekitUse_state(self):  # 是否使用yeekit翻译

        if self.yeekit_checkBox.isChecked():
            self.yeekitUse = "True"
        else:
            self.yeekitUse = "False"
        self.data["yeekitUse"] = self.yeekitUse


    def alapiUse_state(self):  # 是否使用ALAPI翻译

        if self.ALAPI_checkBox.isChecked():
            self.alapiUse = "True"
        else:
            self.alapiUse = "False"
        self.data["alapiUse"] = self.alapiUse


    def baiduwebUse_state(self):  # 是否使用百度翻译网页版

        if self.baiduweb_checkBox.isChecked():
            self.baiduwebUse = "True"
        else:
            self.baiduwebUse = "False"
        self.data["baiduwebUse"] = self.baiduwebUse


    def baiduUse_state(self):  # 是否使用百度翻译

        if self.baidu_checkBox.isChecked():
            self.baiduUse = "True"
        else:
            self.baiduUse = "False"
        self.data["baiduUse"] = self.baiduUse


    def tencentUse_state(self):  # 是否使用腾讯翻译

        if self.tencent_checkBox.isChecked():
            self.tencentUse = "True"
        else:
            self.tencentUse = "False"
        self.data["tencentUse"] = self.tencentUse


    def saveAPI(self):

        self.OCR_Key = self.OCR_Key_Text.toPlainText().replace(' ','').replace('\n','').replace('\t','')
        self.OCR_Secret = self.OCR_Secret_Text.toPlainText().replace(' ','').replace('\n','').replace('\t','')
        self.baidu_Key = self.baidu_Key_Text.toPlainText().replace(' ','').replace('\n','').replace('\t','')
        self.baidu_Secret = self.baidu_Secret_Text.toPlainText().replace(' ','').replace('\n','').replace('\t','')
        self.tencent_Key = self.tencent_Key_Text.toPlainText().replace(' ','').replace('\n','').replace('\t','')
        self.tencent_Secret = self.tencent_Secret_Text.toPlainText().replace(' ','').replace('\n','').replace('\t','')

        self.data["OCR"]["Key"] = self.OCR_Key
        self.data["OCR"]["Secret"] = self.OCR_Secret
        self.data["baiduAPI"]["Key"] = self.baidu_Key
        self.data["baiduAPI"]["Secret"] = self.baidu_Secret
        self.data["tencentAPI"]["Key"] = self.tencent_Key
        self.data["tencentAPI"]["Secret"] = self.tencent_Secret

    def range(self):

        with open('.\\config\\settin.json') as file:
            data1 = json.load(file)

            self.data["range"]["X1"] = data1["range"]["X1"]
            self.data["range"]["Y1"] = data1["range"]["Y1"]
            self.data["range"]["X2"] = data1["range"]["X2"]
            self.data["range"]["Y2"] = data1["range"]["Y2"]

    def save_language(self): # 保存翻译语种

        if self.language_comboBox.currentIndex() == 1:
            self.data["language"] = 'ENG'
        elif self.language_comboBox.currentIndex() == 2:
            self.data["language"] = 'KOR'
        else:
            self.data["language"] = 'JAP'

    def save_showHotKeyValue1(self): # 保存快捷键1

        if self.shortcutKey_textEdit_1.currentIndex() == 1:
            self.data["showHotKeyValue1"] = 'control'
        elif self.shortcutKey_textEdit_1.currentIndex() == 2:
            self.data["showHotKeyValue1"] = 'shift'
        else:
            self.data["showHotKeyValue1"] = 'alt'

    def save_settin(self):

        self.range()
        self.change_background()
        self.save_fontSize()
        self.showOriginal_state()
        self.showClipboard_state()
        self.get_horizontal()
        self.youdaoUse_state()
        self.caiyunUse_state()
        self.jinshanUse_state()
        self.yeekitUse_state()
        self.alapiUse_state()
        self.baiduwebUse_state()
        self.save_language()
        self.baiduUse_state()
        self.tencentUse_state()
        self.showHotKey_state()
        self.save_showHotKeyValue1()
        self.data["translateSpeed"] = self.autoSpeed_spinBox.value()
        self.saveAPI()

        with open('.\\config\\settin.json','w') as file:
            json.dump(self.data,file)

        get_Access_Token()


if __name__ == "__main__":
    
    import sys
    APP = QApplication(sys.argv)
    Settin = SettinInterface()
    Settin.show()
    sys.exit(APP.exec_())
