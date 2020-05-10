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

        self.setObjectName("SettinInterface")
        self.resize(406, 476)
        self.setMinimumSize(QtCore.QSize(406, 476))
        self.setMaximumSize(QtCore.QSize(406, 476))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/图标.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.setWindowOpacity(1.0)
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 408, 478))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("background-image: url(Background.jpg); background-repeat: no-repeat;font: 10pt \"华康方圆体W7\"; border-width:0;")
        self.tabWidget.setObjectName("tabWidget")
        
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        
        self.OCR_Key_Text = QtWidgets.QTextEdit(self.tab_1)
        self.OCR_Key_Text.setGeometry(QtCore.QRect(110, 45, 250, 20))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.OCR_Key_Text.setFont(font)
        self.OCR_Key_Text.setEnabled(True)
        self.OCR_Key_Text.setStyleSheet("background: transparent;")
        self.OCR_Key_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Key_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Key_Text.setObjectName("OCR_Key_Text")
        
        self.OCR_label_1 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_1.setGeometry(QtCore.QRect(20, 20, 261, 16))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.OCR_label_1.setFont(font)
        self.OCR_label_1.setStyleSheet("background: transparent;")
        self.OCR_label_1.setObjectName("OCR_label_1")
        self.OCR_Secret_Text = QtWidgets.QTextEdit(self.tab_1)
        self.OCR_Secret_Text.setGeometry(QtCore.QRect(110, 70, 250, 20))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.OCR_Secret_Text.setFont(font)
        self.OCR_Secret_Text.setAcceptDrops(True)
        self.OCR_Secret_Text.setAutoFillBackground(False)
        self.OCR_Secret_Text.setStyleSheet("background: transparent;")
        self.OCR_Secret_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Secret_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OCR_Secret_Text.setObjectName("OCR_Secret_Text")
        self.OCR_label_2 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_2.setGeometry(QtCore.QRect(70, 45, 31, 16))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.OCR_label_2.setFont(font)
        self.OCR_label_2.setStyleSheet("background: transparent;")
        self.OCR_label_2.setObjectName("OCR_label_2")
        self.OCR_label_3 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_3.setGeometry(QtCore.QRect(20, 70, 91, 16))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.OCR_label_3.setFont(font)
        self.OCR_label_3.setStyleSheet("background: transparent;")
        self.OCR_label_3.setObjectName("OCR_label_3")
        self.OCR_label_4 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_4.setGeometry(QtCore.QRect(370, 50, 16, 16))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.OCR_label_4.setFont(font)
        self.OCR_label_4.setStyleSheet("background: transparent;color: rgb(255, 0, 0);")
        self.OCR_label_4.setObjectName("OCR_label_4")
        self.OCR_label_5 = QtWidgets.QLabel(self.tab_1)
        self.OCR_label_5.setGeometry(QtCore.QRect(370, 75, 16, 16))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.OCR_label_5.setFont(font)
        self.OCR_label_5.setStyleSheet("background: transparent;color: rgb(255, 0, 0);")
        self.OCR_label_5.setObjectName("OCR_label_5")
        
        self.OCRRegister_Button = QtWidgets.QPushButton(self.tab_1)
        self.OCRRegister_Button.setGeometry(QtCore.QRect(160, 95, 80, 30))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.OCRRegister_Button.setFont(font)
        self.OCRRegister_Button.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.OCRRegister_Button.setObjectName("OCRRegister_Button")
        self.OCRRegister_Button.clicked.connect(register_OCR)
        
        self.baiduAPI_label_1 = QtWidgets.QLabel(self.tab_1)
        self.baiduAPI_label_1.setGeometry(QtCore.QRect(20, 140, 281, 16))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.baiduAPI_label_1.setFont(font)
        self.baiduAPI_label_1.setStyleSheet("background: transparent;")
        self.baiduAPI_label_1.setObjectName("baiduAPI_label_1")
        self.baiduAPI_label_2 = QtWidgets.QLabel(self.tab_1)
        self.baiduAPI_label_2.setGeometry(QtCore.QRect(50, 165, 50, 20))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.baiduAPI_label_2.setFont(font)
        self.baiduAPI_label_2.setStyleSheet("background: transparent;")
        self.baiduAPI_label_2.setObjectName("baiduAPI_label_2")
        self.baiduAPI_label_3 = QtWidgets.QLabel(self.tab_1)
        self.baiduAPI_label_3.setGeometry(QtCore.QRect(63, 190, 41, 16))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.baiduAPI_label_3.setFont(font)
        self.baiduAPI_label_3.setStyleSheet("background: transparent;")
        self.baiduAPI_label_3.setObjectName("baiduAPI_label_3")
        self.baidu_Key_Text = QtWidgets.QTextEdit(self.tab_1)
        self.baidu_Key_Text.setGeometry(QtCore.QRect(110, 165, 250, 20))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.baidu_Key_Text.setFont(font)
        self.baidu_Key_Text.setAcceptDrops(True)
        self.baidu_Key_Text.setAutoFillBackground(False)
        self.baidu_Key_Text.setStyleSheet("background: transparent;")
        self.baidu_Key_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Key_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Key_Text.setObjectName("baidu_Key_Text")
        self.baidu_Secret_Text = QtWidgets.QTextEdit(self.tab_1)
        self.baidu_Secret_Text.setGeometry(QtCore.QRect(110, 190, 250, 20))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.baidu_Secret_Text.setFont(font)
        self.baidu_Secret_Text.setAcceptDrops(True)
        self.baidu_Secret_Text.setAutoFillBackground(False)
        self.baidu_Secret_Text.setStyleSheet("background: transparent;")
        self.baidu_Secret_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Secret_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.baidu_Secret_Text.setObjectName("baidu_Secret_Text")
        
        self.baiduRegister_Button = QtWidgets.QPushButton(self.tab_1)
        self.baiduRegister_Button.setGeometry(QtCore.QRect(90, 220, 80, 30))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.baiduRegister_Button.setFont(font)
        self.baiduRegister_Button.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.baiduRegister_Button.setObjectName("baiduRegister_Button")
        self.baiduRegister_Button.clicked.connect(register_baidu)

        self.baiduSelect_Button = QtWidgets.QPushButton(self.tab_1)
        self.baiduSelect_Button.setGeometry(QtCore.QRect(237, 220, 80, 30))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.baiduSelect_Button.setFont(font)
        self.baiduSelect_Button.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.baiduSelect_Button.setObjectName("baiduSelect_Button")
        self.baiduSelect_Button.clicked.connect(select_baidu)
        
        self.TencentAPI_laber_1 = QtWidgets.QLabel(self.tab_1)
        self.TencentAPI_laber_1.setGeometry(QtCore.QRect(20, 260, 281, 16))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.TencentAPI_laber_1.setFont(font)
        self.TencentAPI_laber_1.setStyleSheet("background: transparent;")
        self.TencentAPI_laber_1.setObjectName("TencentAPI_laber_1")
        self.TencentAPI_laber_2 = QtWidgets.QLabel(self.tab_1)
        self.TencentAPI_laber_2.setGeometry(QtCore.QRect(35, 285, 71, 20))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.TencentAPI_laber_2.setFont(font)
        self.TencentAPI_laber_2.setStyleSheet("background: transparent;")
        self.TencentAPI_laber_2.setObjectName("TencentAPI_laber_2")
        self.TencentAPI_laber_3 = QtWidgets.QLabel(self.tab_1)
        self.TencentAPI_laber_3.setGeometry(QtCore.QRect(28, 310, 71, 20))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        self.TencentAPI_laber_3.setFont(font)
        self.TencentAPI_laber_3.setStyleSheet("background: transparent;")
        self.TencentAPI_laber_3.setObjectName("TencentAPI_laber_3")
        self.tencent_Key_Text = QtWidgets.QTextEdit(self.tab_1)
        self.tencent_Key_Text.setGeometry(QtCore.QRect(110, 285, 250, 20))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tencent_Key_Text.setFont(font)
        self.tencent_Key_Text.setAcceptDrops(True)
        self.tencent_Key_Text.setAutoFillBackground(False)
        self.tencent_Key_Text.setStyleSheet("background: transparent;")
        self.tencent_Key_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Key_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Key_Text.setObjectName("tencent_Key_Text")
        self.tencent_Secret_Text = QtWidgets.QTextEdit(self.tab_1)
        self.tencent_Secret_Text.setGeometry(QtCore.QRect(110, 310, 250, 20))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tencent_Secret_Text.setFont(font)
        self.tencent_Secret_Text.setAcceptDrops(True)
        self.tencent_Secret_Text.setAutoFillBackground(False)
        self.tencent_Secret_Text.setStyleSheet("background: transparent;")
        self.tencent_Secret_Text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Secret_Text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tencent_Secret_Text.setObjectName("tencent_Secret_Text")
        
        self.tencentSelect_Button_2 = QtWidgets.QPushButton(self.tab_1)
        self.tencentSelect_Button_2.setGeometry(QtCore.QRect(90, 340, 80, 30))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tencentSelect_Button_2.setFont(font)
        self.tencentSelect_Button_2.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.tencentSelect_Button_2.setObjectName("tencentSelect_Button_2")
        self.tencentSelect_Button_2.clicked.connect(register_tencent)

        self.tencentSelect_Button = QtWidgets.QPushButton(self.tab_1)
        self.tencentSelect_Button.setGeometry(QtCore.QRect(237, 340, 80, 30))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tencentSelect_Button.setFont(font)
        self.tencentSelect_Button.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.tencentSelect_Button.setObjectName("tencentSelect_Button")
        self.tencentSelect_Button.clicked.connect(select_tencent)
        
        self.OCR_Key_Text.raise_()
        self.OCR_label_1.raise_()
        self.OCR_Secret_Text.raise_()
        self.OCR_label_2.raise_()
        self.OCR_label_3.raise_()
        self.OCR_label_4.raise_()
        self.OCR_label_5.raise_()
        self.baiduAPI_label_1.raise_()
        self.baiduAPI_label_2.raise_()
        self.baiduAPI_label_3.raise_()
        self.baidu_Key_Text.raise_()
        self.baidu_Secret_Text.raise_()
        self.baiduRegister_Button.raise_()
        self.baiduSelect_Button.raise_()
        self.TencentAPI_laber_1.raise_()
        self.TencentAPI_laber_2.raise_()
        self.TencentAPI_laber_3.raise_()
        self.tencent_Key_Text.raise_()
        self.tencent_Secret_Text.raise_()
        self.tencentSelect_Button_2.raise_()
        self.tencentSelect_Button.raise_()
        self.OCRRegister_Button.raise_()
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.translateSource_label_1 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_1.setGeometry(QtCore.QRect(20, 25, 191, 16))
        self.translateSource_label_1.setStyleSheet("background: transparent;")
        self.translateSource_label_1.setObjectName("translateSource_label_1")
        
        self.youdao_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.youdao_checkBox.setGeometry(QtCore.QRect(30, 90, 80, 16))
        self.youdao_checkBox.setStyleSheet("background: transparent;")
        self.youdao_checkBox.setObjectName("youdao_checkBox")
        self.youdao_checkBox.setChecked(self.youdaoUse)
        
        self.caiyun_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.caiyun_checkBox.setGeometry(QtCore.QRect(160, 90, 80, 16))
        self.caiyun_checkBox.setStyleSheet("background: transparent;")
        self.caiyun_checkBox.setObjectName("caiyun_checkBox")
        self.caiyun_checkBox.setChecked(self.caiyunUse)
        
        self.jinshan_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.jinshan_checkBox.setGeometry(QtCore.QRect(297, 90, 80, 16))
        self.jinshan_checkBox.setStyleSheet("background: transparent;")
        self.jinshan_checkBox.setObjectName("jinshan_checkBox")
        self.jinshan_checkBox.setChecked(self.jinshanUse)
        
        self.translateSource_label_2 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_2.setGeometry(QtCore.QRect(20, 60, 220, 16))
        self.translateSource_label_2.setStyleSheet("background: transparent;")
        self.translateSource_label_2.setObjectName("translateSource_label_2")
        self.translateSource_label_3 = QtWidgets.QLabel(self.tab_2)
        self.translateSource_label_3.setGeometry(QtCore.QRect(20, 125, 271, 16))
        self.translateSource_label_3.setStyleSheet("background: transparent;")
        self.translateSource_label_3.setObjectName("translateSource_label_3")
        
        self.baidu_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.baidu_checkBox.setGeometry(QtCore.QRect(30, 155, 80, 16))
        self.baidu_checkBox.setStyleSheet("background: transparent;")
        self.baidu_checkBox.setObjectName("baidu_checkBox")
        self.baidu_checkBox.setChecked(self.baiduUse)
        
        self.tencent_checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.tencent_checkBox.setGeometry(QtCore.QRect(160, 155, 80, 16))
        self.tencent_checkBox.setStyleSheet("background: transparent;")
        self.tencent_checkBox.setObjectName("tencent_checkBox")
        self.tencent_checkBox.setChecked(self.tencentUse)
        
        self.translateMode_label_1 = QtWidgets.QLabel(self.tab_2)
        self.translateMode_label_1.setGeometry(QtCore.QRect(20, 210, 211, 16))
        self.translateMode_label_1.setStyleSheet("background: transparent;")
        self.translateMode_label_1.setObjectName("translateMode_label_1")
        
        self.manual_radioButton = QtWidgets.QRadioButton(self.tab_2)
        self.manual_radioButton.setGeometry(QtCore.QRect(30, 245, 241, 16))
        self.manual_radioButton.setStyleSheet("background: transparent;")
        self.manual_radioButton.setObjectName("manual_radioButton")
        self.manual_radioButton.setChecked(self.manualMode)
        
        self.auto_radioButton = QtWidgets.QRadioButton(self.tab_2)
        self.auto_radioButton.setGeometry(QtCore.QRect(30, 285, 281, 16))
        self.auto_radioButton.setStyleSheet("background: transparent;")
        self.auto_radioButton.setObjectName("auto_radioButton")
        self.manual_radioButton.setChecked(self.autoMode)
        
        self.autoSpeed_spinBox = QtWidgets.QSpinBox(self.tab_2)
        self.autoSpeed_spinBox.setGeometry(QtCore.QRect(140, 320, 40, 25))
        self.autoSpeed_spinBox.setStyleSheet("background: transparent;")
        self.autoSpeed_spinBox.setMinimum(2)
        self.autoSpeed_spinBox.setMaximum(10)
        self.autoSpeed_spinBox.setObjectName("autoSpeed_spinBox")
        self.autoSpeed_spinBox.setValue(self.translateSpeed)
        
        self.translateMode_label_2 = QtWidgets.QLabel(self.tab_2)
        self.translateMode_label_2.setGeometry(QtCore.QRect(48, 325, 91, 16))
        self.translateMode_label_2.setStyleSheet("background: transparent;")
        self.translateMode_label_2.setObjectName("translateMode_label_2")
        self.translateMode_label_3 = QtWidgets.QLabel(self.tab_2)
        self.translateMode_label_3.setGeometry(QtCore.QRect(190, 325, 101, 16))
        self.translateMode_label_3.setStyleSheet("background: transparent;")
        self.translateMode_label_3.setObjectName("translateMode_label_3")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.colour_label_1 = QtWidgets.QLabel(self.tab_3)
        self.colour_label_1.setGeometry(QtCore.QRect(30, 25, 241, 16))
        self.colour_label_1.setStyleSheet("background: transparent;")
        self.colour_label_1.setObjectName("colour_label_1")
        self.youdaoColour_label = QtWidgets.QLabel(self.tab_3)
        self.youdaoColour_label.setGeometry(QtCore.QRect(30, 90, 71, 16))
        self.youdaoColour_label.setStyleSheet("background: transparent;")
        self.youdaoColour_label.setObjectName("youdaoColour_label")
        self.caiyunColour_label = QtWidgets.QLabel(self.tab_3)
        self.caiyunColour_label.setGeometry(QtCore.QRect(30, 130, 71, 16))
        self.caiyunColour_label.setStyleSheet("background: transparent;")
        self.caiyunColour_label.setObjectName("caiyunColour_label")
        self.jinshanColour_label = QtWidgets.QLabel(self.tab_3)
        self.jinshanColour_label.setGeometry(QtCore.QRect(30, 170, 71, 16))
        self.jinshanColour_label.setStyleSheet("background: transparent;")
        self.jinshanColour_label.setObjectName("jinshanColour_label")
        self.baiduColour_label = QtWidgets.QLabel(self.tab_3)
        self.baiduColour_label.setGeometry(QtCore.QRect(30, 210, 71, 16))
        self.baiduColour_label.setStyleSheet("background: transparent;")
        self.baiduColour_label.setObjectName("baiduColour_label")
        self.tencentColour_label = QtWidgets.QLabel(self.tab_3)
        self.tencentColour_label.setGeometry(QtCore.QRect(30, 250, 71, 16))
        self.tencentColour_label.setStyleSheet("background: transparent;")
        self.tencentColour_label.setObjectName("tencentColour_label")
        self.colour_label_2 = QtWidgets.QLabel(self.tab_3)
        self.colour_label_2.setGeometry(QtCore.QRect(130, 55, 30, 16))
        self.colour_label_2.setStyleSheet("background: transparent;")
        self.colour_label_2.setObjectName("colour_label_2")
        self.colour_label_4 = QtWidgets.QLabel(self.tab_3)
        self.colour_label_4.setGeometry(QtCore.QRect(307, 55, 30, 16))
        self.colour_label_4.setStyleSheet("background: transparent;")
        self.colour_label_4.setObjectName("colour_label_4")
        self.colour_label_3 = QtWidgets.QLabel(self.tab_3)
        self.colour_label_3.setGeometry(QtCore.QRect(200, 55, 30, 16))
        self.colour_label_3.setStyleSheet("background: transparent;")
        self.colour_label_3.setObjectName("colour_label_3")
        self.originalColour_label = QtWidgets.QLabel(self.tab_3)
        self.originalColour_label.setGeometry(QtCore.QRect(30, 290, 61, 16))
        self.originalColour_label.setStyleSheet("background: transparent;")
        self.originalColour_label.setObjectName("originalColour_label")
        
        self.fontComboBox_1 = QtWidgets.QFontComboBox(self.tab_3)
        self.fontComboBox_1.setGeometry(QtCore.QRect(267, 85, 110, 25))
        self.fontComboBox_1.setObjectName("fontComboBox_1")
        ComboBoxFont_1 = QtGui.QFont(self.youdaoFont)
        self.fontComboBox_1.setCurrentFont(ComboBoxFont_1)
        self.fontComboBox_1.activated[str].connect(self.get_font_youdao)

        self.fontComboBox_2 = QtWidgets.QFontComboBox(self.tab_3)
        self.fontComboBox_2.setGeometry(QtCore.QRect(267, 125, 110, 25))
        self.fontComboBox_2.setObjectName("fontComboBox_2")
        ComboBoxFont_2 = QtGui.QFont(self.caiyunFont)
        self.fontComboBox_2.setCurrentFont(ComboBoxFont_2)
        self.fontComboBox_2.activated[str].connect(self.get_font_caiyun)

        self.fontComboBox_3 = QtWidgets.QFontComboBox(self.tab_3)
        self.fontComboBox_3.setGeometry(QtCore.QRect(267, 165, 110, 25))
        self.fontComboBox_3.setObjectName("fontComboBox_3")
        ComboBoxFont_3 = QtGui.QFont(self.caiyunFont)
        self.fontComboBox_3.setCurrentFont(ComboBoxFont_3)
        self.fontComboBox_3.activated[str].connect(self.get_font_jinshan)

        self.fontComboBox_4 = QtWidgets.QFontComboBox(self.tab_3)
        self.fontComboBox_4.setGeometry(QtCore.QRect(267, 205, 110, 25))
        self.fontComboBox_4.setObjectName("fontComboBox_4")
        ComboBoxFont_4 = QtGui.QFont(self.caiyunFont)
        self.fontComboBox_4.setCurrentFont(ComboBoxFont_4)
        self.fontComboBox_4.activated[str].connect(self.get_font_baidu)

        self.fontComboBox_5 = QtWidgets.QFontComboBox(self.tab_3)
        self.fontComboBox_5.setGeometry(QtCore.QRect(267, 245, 110, 25))
        self.fontComboBox_5.setObjectName("fontComboBox_5")
        ComboBoxFont_5 = QtGui.QFont(self.caiyunFont)
        self.fontComboBox_5.setCurrentFont(ComboBoxFont_5)
        self.fontComboBox_5.activated[str].connect(self.get_font_tencent)

        self.fontComboBox_6 = QtWidgets.QFontComboBox(self.tab_3)
        self.fontComboBox_6.setGeometry(QtCore.QRect(267, 285, 110, 25))
        self.fontComboBox_6.setObjectName("fontComboBox_6")
        ComboBoxFont_6 = QtGui.QFont(self.caiyunFont)
        self.fontComboBox_6.setCurrentFont(ComboBoxFont_6)
        self.fontComboBox_6.activated[str].connect(self.get_font_original)
        
        self.youdaoSize_spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.youdaoSize_spinBox.setGeometry(QtCore.QRect(195, 85, 40, 25))
        self.youdaoSize_spinBox.setMinimum(1)
        self.youdaoSize_spinBox.setMaximum(10)
        self.youdaoSize_spinBox.setObjectName("youdaoSize_spinBox")
        self.youdaoSize_spinBox.setValue(self.youdaoSize)

        self.caiyunSize_spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.caiyunSize_spinBox.setGeometry(QtCore.QRect(195, 125, 40, 25))
        self.caiyunSize_spinBox.setMinimum(1)
        self.caiyunSize_spinBox.setMaximum(10)
        self.caiyunSize_spinBox.setObjectName("caiyunSize_spinBox")
        self.caiyunSize_spinBox.setValue(self.caiyunSize)

        self.jinshanSize_spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.jinshanSize_spinBox.setGeometry(QtCore.QRect(195, 165, 40, 25))
        self.jinshanSize_spinBox.setMinimum(1)
        self.jinshanSize_spinBox.setMaximum(10)
        self.jinshanSize_spinBox.setObjectName("jinshanSize_spinBox")
        self.jinshanSize_spinBox.setValue(self.jinshanSize)

        self.baiduSize_spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.baiduSize_spinBox.setGeometry(QtCore.QRect(195, 205, 40, 25))
        self.baiduSize_spinBox.setMinimum(1)
        self.baiduSize_spinBox.setMaximum(10)
        self.baiduSize_spinBox.setObjectName("baiduSize_spinBox")
        self.baiduSize_spinBox.setValue(self.baiduSize)

        self.tencentSize_spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.tencentSize_spinBox.setGeometry(QtCore.QRect(195, 245, 40, 25))
        self.tencentSize_spinBox.setMinimum(1)
        self.tencentSize_spinBox.setMaximum(10)
        self.tencentSize_spinBox.setObjectName("tencentSize_spinBox")
        self.tencentSize_spinBox.setValue(self.tencentSize)

        self.originalSize_spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.originalSize_spinBox.setGeometry(QtCore.QRect(195, 285, 40, 25))
        self.originalSize_spinBox.setMinimum(1)
        self.originalSize_spinBox.setMaximum(10)
        self.originalSize_spinBox.setObjectName("originalSize_spinBox")
        self.originalSize_spinBox.setValue(self.originalSize)

        self.youdaoColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.youdaoColour_toolButton.setGeometry(QtCore.QRect(110, 85, 60, 25))
        self.youdaoColour_toolButton.setAutoFillBackground(False)
        self.youdaoColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.youdaoColor))
        self.youdaoColour_toolButton.setCheckable(False)
        self.youdaoColour_toolButton.setChecked(False)
        self.youdaoColour_toolButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.youdaoColour_toolButton.setAutoRaise(False)
        self.youdaoColour_toolButton.setObjectName("youdaoColour_toolButton")
        self.youdaoColour_toolButton.clicked.connect(lambda:self.get_font_color(1))

        self.caiyunColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.caiyunColour_toolButton.setGeometry(QtCore.QRect(110, 125, 60, 25))
        self.caiyunColour_toolButton.setAutoFillBackground(False)
        self.caiyunColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.caiyunColor))
        self.caiyunColour_toolButton.setCheckable(False)
        self.caiyunColour_toolButton.setChecked(False)
        self.caiyunColour_toolButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.caiyunColour_toolButton.setAutoRaise(False)
        self.caiyunColour_toolButton.setObjectName("caiyunColour_toolButton")
        self.caiyunColour_toolButton.clicked.connect(lambda:self.get_font_color(2))

        self.jinshanColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.jinshanColour_toolButton.setGeometry(QtCore.QRect(110, 165, 60, 25))
        self.jinshanColour_toolButton.setAutoFillBackground(False)
        self.jinshanColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.jinshanColor))
        self.jinshanColour_toolButton.setCheckable(False)
        self.jinshanColour_toolButton.setChecked(False)
        self.jinshanColour_toolButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.jinshanColour_toolButton.setAutoRaise(False)
        self.jinshanColour_toolButton.setObjectName("jinshanColour_toolButton")
        self.jinshanColour_toolButton.clicked.connect(lambda:self.get_font_color(3))

        self.baiduColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.baiduColour_toolButton.setGeometry(QtCore.QRect(110, 205, 60, 25))
        self.baiduColour_toolButton.setAutoFillBackground(False)
        self.baiduColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.baiduColor))
        self.baiduColour_toolButton.setCheckable(False)
        self.baiduColour_toolButton.setChecked(False)
        self.baiduColour_toolButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.baiduColour_toolButton.setAutoRaise(False)
        self.baiduColour_toolButton.setObjectName("baiduColour_toolButton")
        self.baiduColour_toolButton.clicked.connect(lambda:self.get_font_color(4))

        self.tencentColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.tencentColour_toolButton.setGeometry(QtCore.QRect(110, 245, 60, 25))
        self.tencentColour_toolButton.setAutoFillBackground(False)
        self.tencentColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.tencentColor))
        self.tencentColour_toolButton.setCheckable(False)
        self.tencentColour_toolButton.setChecked(False)
        self.tencentColour_toolButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.tencentColour_toolButton.setAutoRaise(False)
        self.tencentColour_toolButton.setObjectName("tencentColour_toolButton")
        self.tencentColour_toolButton.clicked.connect(lambda:self.get_font_color(5))

        self.originalColour_toolButton = QtWidgets.QToolButton(self.tab_3)
        self.originalColour_toolButton.setGeometry(QtCore.QRect(110, 285, 60, 25))
        self.originalColour_toolButton.setAutoFillBackground(False)
        self.originalColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png); color: {};".format(self.originalColor))
        self.originalColour_toolButton.setCheckable(False)
        self.originalColour_toolButton.setChecked(False)
        self.originalColour_toolButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.originalColour_toolButton.setAutoRaise(False)
        self.originalColour_toolButton.setObjectName("originalColour_toolButton")
        self.originalColour_toolButton.clicked.connect(lambda:self.get_font_color(6))

        self.showOriginal_checkBox = QtWidgets.QCheckBox(self.tab_3)
        self.showOriginal_checkBox.setGeometry(QtCore.QRect(30, 325, 101, 20))
        self.showOriginal_checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.showOriginal_checkBox.setStyleSheet("background: transparent;")
        self.showOriginal_checkBox.setObjectName("showOriginal_checkBox")
        self.showOriginal_checkBox.setChecked(self.showOriginal)

        self.spinBox = QtWidgets.QSpinBox(self.tab_3)
        self.spinBox.setGeometry(QtCore.QRect(200, 355, 51, 22))
        self.spinBox.setStyleSheet("background: transparent;")
        self.spinBox.setMinimum(100)
        self.spinBox.setMaximum(300)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setValue(self.screenSize)
        
        self.originalColour_label_2 = QtWidgets.QLabel(self.tab_3)
        self.originalColour_label_2.setGeometry(QtCore.QRect(30, 360, 251, 16))
        self.originalColour_label_2.setStyleSheet("background: transparent;")
        self.originalColour_label_2.setObjectName("originalColour_label_2")
        
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tab4_label_1 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_1.setGeometry(QtCore.QRect(30, 25, 211, 16))
        self.tab4_label_1.setStyleSheet("background: transparent;")
        self.tab4_label_1.setObjectName("tab4_label_1")
        
        self.horizontalSlider = QtWidgets.QSlider(self.tab_4)
        self.horizontalSlider.setGeometry(QtCore.QRect(30, 55, 347, 22))
        self.horizontalSlider.setStyleSheet("background: transparent;")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setValue(self.horizontal)
        self.horizontalSlider.valueChanged.connect(self.get_horizontal)

        self.tab4_label_2 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_2.setGeometry(QtCore.QRect(30, 85, 61, 20))
        self.tab4_label_2.setStyleSheet("background: transparent;")
        self.tab4_label_2.setObjectName("tab4_label_2")
        
        self.tab4_label_3 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_3.setGeometry(QtCore.QRect(310, 85, 71, 20))
        self.tab4_label_3.setStyleSheet("background: transparent;")
        self.tab4_label_3.setObjectName("tab4_label_3")

        self.tab4_label_4 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_4.setGeometry(QtCore.QRect(30, 120, 201, 16))
        self.tab4_label_4.setStyleSheet("background: transparent;")
        self.tab4_label_4.setObjectName("tab4_label_4")
        
        self.Clipboard_checkBox = QtWidgets.QCheckBox(self.tab_4)
        self.Clipboard_checkBox.setGeometry(QtCore.QRect(30, 155, 231, 16))
        self.Clipboard_checkBox.setStyleSheet("background: transparent;")
        self.Clipboard_checkBox.setObjectName("Clipboard_checkBox")
        self.Clipboard_checkBox.setChecked(self.showClipboard)

        self.Clipboard_checkBox_2 = QtWidgets.QCheckBox(self.tab_4)
        self.Clipboard_checkBox_2.setGeometry(QtCore.QRect(30, 190, 171, 16))
        self.Clipboard_checkBox_2.setStyleSheet("background: transparent;")
        self.Clipboard_checkBox_2.setObjectName("Clipboard_checkBox_2")
        self.Clipboard_checkBox_2.setChecked(self.showHotKey)
        
        self.textEdit = QtWidgets.QTextEdit(self.tab_4)
        self.textEdit.setGeometry(QtCore.QRect(200, 185, 51, 21))
        self.textEdit.setStyleSheet("background: transparent;")
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setObjectName("textEdit")

        self.tab4_label_7 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_7.setGeometry(QtCore.QRect(30, 220, 351, 41))
        self.tab4_label_7.setStyleSheet("background: transparent;")
        self.tab4_label_7.setObjectName("tab4_label_7")

        self.tab4_label_5 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_5.setGeometry(QtCore.QRect(30, 280, 261, 16))
        self.tab4_label_5.setStyleSheet("background: transparent;")
        self.tab4_label_5.setObjectName("tab4_label_5")
        
        self.openfileButton = QtWidgets.QPushButton(self.tab_4)
        self.openfileButton.setGeometry(QtCore.QRect(30, 310, 75, 23))
        self.openfileButton.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.openfileButton.setObjectName("openfileButton")
        self.openfileButton.clicked.connect(self.Select_background)
        
        self.openfileText = QtWidgets.QTextBrowser(self.tab_4)
        self.openfileText.setGeometry(QtCore.QRect(120, 310, 251, 21))
        self.openfileText.setStyleSheet("background: transparent;")
        self.openfileText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.openfileText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.openfileText.setObjectName("openfileText")
        
        self.tab4_label_6 = QtWidgets.QLabel(self.tab_4)
        self.tab4_label_6.setGeometry(QtCore.QRect(30, 350, 331, 16))
        self.tab4_label_6.setStyleSheet("background: transparent;")
        self.tab4_label_6.setObjectName("tab4_label_6")
        
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.WechatImage_label = QtWidgets.QLabel(self.tab_5)
        self.WechatImage_label.setGeometry(QtCore.QRect(20, 170, 170, 170))
        self.WechatImage_label.setText("")
        self.WechatImage_label.setTextFormat(QtCore.Qt.AutoText)
        self.WechatImage_label.setObjectName("WechatImage_label")
        self.AlipayImage_label = QtWidgets.QLabel(self.tab_5)
        self.AlipayImage_label.setGeometry(QtCore.QRect(215, 170, 170, 170))
        self.AlipayImage_label.setText("")
        self.AlipayImage_label.setTextFormat(QtCore.Qt.AutoText)
        self.AlipayImage_label.setObjectName("AlipayImage_label")
        self.Wechat_label = QtWidgets.QLabel(self.tab_5)
        self.Wechat_label.setGeometry(QtCore.QRect(60, 350, 81, 16))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Wechat_label.setFont(font)
        self.Wechat_label.setStyleSheet("background: transparent;\n"
"font: 14pt \"华康方圆体W7\";")
        self.Wechat_label.setObjectName("Wechat_label")
        self.Alipay_label = QtWidgets.QLabel(self.tab_5)
        self.Alipay_label.setGeometry(QtCore.QRect(250, 350, 101, 16))
        self.Alipay_label.setStyleSheet("font: 14pt \"华康方圆体W7\";\n"
"background: transparent;")
        self.Alipay_label.setObjectName("Alipay_label")
        self.Mysay_label = QtWidgets.QLabel(self.tab_5)
        self.Mysay_label.setGeometry(QtCore.QRect(40, 10, 281, 141))
        self.Mysay_label.setStyleSheet("background: transparent;")
        self.Mysay_label.setObjectName("Mysay_label")
        self.tabWidget.addTab(self.tab_5, "")
        
        self.SaveButton = QtWidgets.QPushButton(self)
        self.SaveButton.setGeometry(QtCore.QRect(85, 420, 90, 30))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SaveButton.setFont(font)
        self.SaveButton.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.SaveButton.setObjectName("SaveButton")
        self.SaveButton.clicked.connect(lambda:message_thread(self.save_settin))

        self.CancelButton = QtWidgets.QPushButton(self)
        self.CancelButton.setGeometry(QtCore.QRect(232, 420, 90, 30))
        font = QtGui.QFont()
        font.setFamily("华康方圆体W7")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.CancelButton.setFont(font)
        self.CancelButton.setStyleSheet("background-image: url(:/image/Wechat.png);")
        self.CancelButton.setObjectName("CancelButton")

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.OCR_Key_Text, self.OCR_Secret_Text)
        self.setTabOrder(self.OCR_Secret_Text, self.baidu_Key_Text)
        self.setTabOrder(self.baidu_Key_Text, self.baidu_Secret_Text)
        self.setTabOrder(self.baidu_Secret_Text, self.tencent_Key_Text)
        self.setTabOrder(self.tencent_Key_Text, self.tencent_Secret_Text)
        self.setTabOrder(self.tencent_Secret_Text, self.SaveButton)
        self.setTabOrder(self.SaveButton, self.CancelButton)
        self.setTabOrder(self.CancelButton, self.OCRRegister_Button)
        self.setTabOrder(self.OCRRegister_Button, self.baiduRegister_Button)
        self.setTabOrder(self.baiduRegister_Button, self.tencentSelect_Button_2)
        self.setTabOrder(self.tencentSelect_Button_2, self.baiduSelect_Button)
        self.setTabOrder(self.baiduSelect_Button, self.tencentSelect_Button)
        self.setTabOrder(self.tencentSelect_Button, self.tabWidget)
        self.setTabOrder(self.tabWidget, self.youdao_checkBox)
        self.setTabOrder(self.youdao_checkBox, self.caiyun_checkBox)
        self.setTabOrder(self.caiyun_checkBox, self.jinshan_checkBox)
        self.setTabOrder(self.jinshan_checkBox, self.baidu_checkBox)
        self.setTabOrder(self.baidu_checkBox, self.tencent_checkBox)
        self.setTabOrder(self.tencent_checkBox, self.manual_radioButton)
        self.setTabOrder(self.manual_radioButton, self.auto_radioButton)
        self.setTabOrder(self.auto_radioButton, self.autoSpeed_spinBox)
        self.setTabOrder(self.autoSpeed_spinBox, self.fontComboBox_1)
        self.setTabOrder(self.fontComboBox_1, self.fontComboBox_2)
        self.setTabOrder(self.fontComboBox_2, self.fontComboBox_3)
        self.setTabOrder(self.fontComboBox_3, self.fontComboBox_4)
        self.setTabOrder(self.fontComboBox_4, self.fontComboBox_5)
        self.setTabOrder(self.fontComboBox_5, self.fontComboBox_6)
        self.setTabOrder(self.fontComboBox_6, self.youdaoSize_spinBox)
        self.setTabOrder(self.youdaoSize_spinBox, self.youdaoColour_toolButton)
        self.setTabOrder(self.youdaoColour_toolButton, self.caiyunColour_toolButton)
        self.setTabOrder(self.caiyunColour_toolButton, self.jinshanColour_toolButton)
        self.setTabOrder(self.jinshanColour_toolButton, self.tencentColour_toolButton)
        self.setTabOrder(self.tencentColour_toolButton, self.originalColour_toolButton)
        self.setTabOrder(self.originalColour_toolButton, self.baiduColour_toolButton)
        self.setTabOrder(self.baiduColour_toolButton, self.caiyunSize_spinBox)
        self.setTabOrder(self.caiyunSize_spinBox, self.jinshanSize_spinBox)
        self.setTabOrder(self.jinshanSize_spinBox, self.baiduSize_spinBox)
        self.setTabOrder(self.baiduSize_spinBox, self.tencentSize_spinBox)
        self.setTabOrder(self.tencentSize_spinBox, self.originalSize_spinBox)
        self.setTabOrder(self.originalSize_spinBox, self.showOriginal_checkBox)
        self.setTabOrder(self.showOriginal_checkBox, self.horizontalSlider)
        self.setTabOrder(self.horizontalSlider, self.Clipboard_checkBox)

        self.OCR_Key_Text.setPlainText(self.OCR_Key)
        self.OCR_Secret_Text.setPlainText(self.OCR_Secret)
        self.baidu_Key_Text.setPlainText(self.baidu_Key)
        self.baidu_Secret_Text.setPlainText(self.baidu_Secret)
        self.tencent_Key_Text.setPlainText(self.tencent_Key)
        self.tencent_Secret_Text.setPlainText(self.tencent_Secret)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "团子翻译器 Ver3.0 - 设置"))
        self.OCR_Key_Text.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'华康方圆体W7\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
        self.OCR_label_1.setText(_translate("self", "（必填）OCR API：用于识别要翻译的文字"))
        self.OCR_Secret_Text.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'华康方圆体W7\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\';\"><br /></p></body></html>"))
        self.OCR_label_2.setText(_translate("self", "Key："))
        self.OCR_label_3.setText(_translate("self", "Secret Key："))
        self.OCR_label_4.setText(_translate("self", "*"))
        self.OCR_label_5.setText(_translate("self", "*"))
        self.OCRRegister_Button.setText(_translate("self", "注册OCR"))
        self.baiduAPI_label_1.setText(_translate("self", "（选填）百度翻译 API：每月额度200万字符"))
        self.baiduAPI_label_2.setText(_translate("self", "APP ID："))
        self.baiduAPI_label_3.setText(_translate("self", "密钥："))
        self.baidu_Key_Text.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'华康方圆体W7\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
        self.baidu_Secret_Text.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'华康方圆体W7\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
        self.baiduRegister_Button.setText(_translate("self", "注册百度"))
        self.baiduSelect_Button.setText(_translate("self", "额度查询"))
        self.TencentAPI_laber_1.setText(_translate("self", "（选填）腾讯翻译 API：每月额度500万字符"))
        self.TencentAPI_laber_2.setText(_translate("self", "Secretld："))
        self.TencentAPI_laber_3.setText(_translate("self", "SecretKey："))
        self.tencent_Key_Text.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'华康方圆体W7\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
        self.tencent_Secret_Text.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'华康方圆体W7\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt;\"><br /></p></body></html>"))
        self.tencentSelect_Button_2.setText(_translate("self", "注册腾讯"))
        self.tencentSelect_Button.setText(_translate("self", "额度查询"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("self", "API设定"))
        self.translateSource_label_1.setText(_translate("self", "翻译源：选择你想使用的翻译"))
        self.youdao_checkBox.setText(_translate("self", "有道翻译"))
        self.caiyun_checkBox.setText(_translate("self", "彩云小泽"))
        self.jinshan_checkBox.setText(_translate("self", "金山词霸"))
        self.translateSource_label_2.setText(_translate("self", "公共（可直接使用，但可能会失效）"))
        self.translateSource_label_3.setText(_translate("self", "私人API（使用稳定，但需注册后才可使用）"))
        self.baidu_checkBox.setText(_translate("self", "百度翻译"))
        self.tencent_checkBox.setText(_translate("self", "腾讯翻译"))
        self.translateMode_label_1.setText(_translate("self", "翻译模式：选择你喜欢的翻译方式"))
        self.manual_radioButton.setText(_translate("self", "手动翻译（每次翻译需点击翻译键）"))
        self.auto_radioButton.setText(_translate("self", "自动翻译（按照设定的时间自动刷新翻译）"))
        self.translateMode_label_2.setText(_translate("self", "自动模式下每"))
        self.translateMode_label_3.setText(_translate("self", "秒刷新一次翻译"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("self", "翻译方式"))
        self.colour_label_1.setText(_translate("self", "自定义译文字体的颜色、字型、大小"))
        self.youdaoColour_label.setText(_translate("self", "有道翻译："))
        self.caiyunColour_label.setText(_translate("self", "彩云小泽："))
        self.jinshanColour_label.setText(_translate("self", "金山词霸："))
        self.baiduColour_label.setText(_translate("self", "百度翻译："))
        self.tencentColour_label.setText(_translate("self", "腾讯翻译："))
        self.colour_label_2.setText(_translate("self", "颜色"))
        self.colour_label_4.setText(_translate("self", "字型"))
        self.colour_label_3.setText(_translate("self", "大小"))
        self.originalColour_label.setText(_translate("self", "原    文："))
        self.youdaoColour_toolButton.setText(_translate("self", "样 式"))
        self.caiyunColour_toolButton.setText(_translate("self", "样 式"))
        self.jinshanColour_toolButton.setText(_translate("self", "样 式"))
        self.tencentColour_toolButton.setText(_translate("self", "样 式"))
        self.originalColour_toolButton.setText(_translate("self", "样 式"))
        self.baiduColour_toolButton.setText(_translate("self", "样 式"))
        self.showOriginal_checkBox.setText(_translate("self", "是否显示原文"))
        self.originalColour_label_2.setText(_translate("SettinInterface", "我的电脑屏幕显示比例为：         %"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("self", "字体设定"))
        self.tab4_label_1.setText(_translate("self", "翻译框透明度：调节其背景色深度"))
        self.tab4_label_2.setText(_translate("self", "完全透明"))
        self.tab4_label_3.setText(_translate("self", "完全不透明"))
        self.Clipboard_checkBox.setText(_translate("self", "是否启用将原文自动复制到剪贴板"))
        self.tab4_label_4.setText(_translate("self", "其他设定：一些独立的其他设定"))
        self.Clipboard_checkBox_2.setText(_translate("SettinInterface", "是否启用快捷键：alt + "))
        self.textEdit.setHtml(_translate("SettinInterface", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'华康方圆体W7\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%s</p></body></html>"%(self.showHotKeyValue)))
        self.tab4_label_7.setText(_translate("SettinInterface", "<html><head/><body><p>说明：仅支持space、a-z、0-9，alt+所填键按下后生效</p><p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如无效则表示与电脑其他快捷键冲突</p></body></html>"))

        self.tab4_label_5.setText(_translate("self", "自定义背景：设置你喜欢的图片作为背景"))
        self.openfileButton.setText(_translate("self", "浏览文件"))
        self.openfileText.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'华康方圆体W7\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.tab4_label_6.setText(_translate("self", "说明：选择的背景图片以分辨率407 x 475时效果最佳"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("self", "翻译框设定"))
        self.Wechat_label.setText(_translate("self", "微信充电"))
        self.Alipay_label.setText(_translate("self", "支付宝充电"))
        self.Mysay_label.setText(_translate("self", "<html><head/><body><p>大家好，我是胖次团子 ❤</p><p>谢谢大家使用团子翻译器Ver3.0 ~</p><p>软件是免费的，但是若能收到你的充电支持 ~</p><p>我会非常开心的，这会是我后续更新的动力 ~ </p><p>联系方式：QQ 394883561</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("self", "我要充电"))
        self.SaveButton.setText(_translate("self", "保存设置"))
        self.CancelButton.setText(_translate("self", "关 闭"))


    def get_settin(self):  # 获取所有预设值

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)

        # 获取各翻译源颜色预设值
        self.youdaoColor = self.data["fontColor"]["youdao"]
        self.caiyunColor = self.data["fontColor"]["caiyun"]
        self.jinshanColor = self.data["fontColor"]["jinshan"]
        self.baiduColor = self.data["fontColor"]["baidu"]
        self.tencentColor = self.data["fontColor"]["tencent"]
        self.originalColor = self.data["fontColor"]["original"]

        # 获取各翻译源字体大小预设值
        self.youdaoSize = int(self.data["fontSize"]["youdao"])
        self.caiyunSize = int(self.data["fontSize"]["caiyun"])
        self.jinshanSize = int(self.data["fontSize"]["jinshan"])
        self.baiduSize = int(self.data["fontSize"]["baidu"])
        self.tencentSize = int(self.data["fontSize"]["tencent"])
        self.originalSize = int(self.data["fontSize"]["original"])

        # 获取各翻译源字体样式预设值
        self.youdaoFont = self.data["fontType"]["youdao"]
        self.caiyunFont = self.data["fontType"]["caiyun"]
        self.jinshanFont = self.data["fontType"]["jinshan"]
        self.baiduFont = self.data["fontType"]["baidu"]
        self.tencentFont = self.data["fontType"]["tencent"]
        self.originalFont = self.data["fontType"]["original"]

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
        self.showHotKeyValue = self.data["showHotKeyValue"]

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

        # 获取翻译模式预设值
        self.translateMode = self.data["translateMode"]
        if self.translateMode == "auto":
            self.autoMode = True
            self.manualMode = False
        else:
            self.autoMode = False
            self.manualMode = True

        # 获取自动翻译时的刷新间隔预设值
        self.translateSpeed = self.data["translateSpeed"]

        # 获取各API预设值
        self.OCR_Key = self.data["OCR"]["Key"]
        self.OCR_Secret = self.data["OCR"]["Secret"]
        self.baidu_Key = self.data["baiduAPI"]["Key"]
        self.baidu_Secret = self.data["baiduAPI"]["Secret"]
        self.tencent_Key = self.data["tencentAPI"]["Key"]
        self.tencent_Secret = self.data["tencentAPI"]["Secret"]

        # 获取屏幕比例预设值
        self.screenSize = self.data["screenSize"] * 100


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
            self.baiduColor = color.name()
            self.baiduColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["baidu"] = self.baiduColor
        elif sign == 5 :
            self.tencentColor = color.name()
            self.tencentColour_toolButton.setStyleSheet("background-image: url(:/image/Wechat.png);color: {};".format(color.name()))
            self.data["fontColor"]["tencent"] = self.tencentColor
        elif sign == 6 :
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
            self.tabWidget.setStyleSheet("background-image: url(Background.jpg); background-repeat: no-repeat;font: 10pt \"华康方圆体W7\"; border-width:0;")


    def get_font_youdao(self, text):  # 有道字体样式
        
        self.youdaoFont = text
        self.data["fontType"]["youdao"] = self.youdaoFont

    def get_font_caiyun(self, text):  # 彩云字体样式
        
        self.caiyunFont = text
        self.data["fontType"]["caiyun"] = self.caiyunFont

    def get_font_jinshan(self, text):  # 金山字体样式
        
        self.jinshanFont = text
        self.data["fontType"]["jinshan"] = self.jinshanFont

    def get_font_baidu(self, text):   # 百度字体样式
        
        self.baiduFont = text
        self.data["fontType"]["baidu"] = self.baiduFont

    def get_font_tencent(self, text):  # 腾讯字体样式
        
        self.tencentFont = text
        self.data["fontType"]["tencent"] = self.tencentFont

    def get_font_original(self, text):  # 原文字体样式
        
        self.originalFont = text
        self.data["fontType"]["original"] = self.originalFont

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

        if self.Clipboard_checkBox_2.isChecked():
            self.showHotKey = "True"
        else:
            self.showHotKey = "False"
        self.data["showHotKey"] = self.showHotKey
        
        self.showHotKeyValue = self.textEdit.toPlainText().replace(' ','').replace('\n','').replace('\t','')
        char = 'zxcvbnmasdfghjklqwertyuiop1234567890'
        if (self.showHotKeyValue in char) or (self.showHotKeyValue == 'space'):
            self.data["showHotKeyValue"] = self.showHotKeyValue
        else:
            message_thread(message, "无效的快捷键", "你要设定的快捷键无效哦 (〃'▽'〃)")


    def get_horizontal(self):  # 文本框透明度

        self.horizontal = self.horizontalSlider.value()
        self.data["horizontal"] = self.horizontal

    def save_fontSize(self):  # 翻译源字体大小

        self.data["fontSize"]["youdao"] = self.youdaoSize_spinBox.value()
        self.data["fontSize"]["caiyun"] = self.caiyunSize_spinBox.value()
        self.data["fontSize"]["jinshan"] = self.jinshanSize_spinBox.value()
        self.data["fontSize"]["baidu"] = self.baiduSize_spinBox.value()
        self.data["fontSize"]["tencent"] = self.tencentSize_spinBox.value()
        self.data["fontSize"]["original"] = self.originalSize_spinBox.value()

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

    def translateMode_state(self):  # 是否使用腾讯翻译

        if self.manual_radioButton.isChecked():
            self.translateMode = "manual"
        else:
            self.translateMode = "auto"
        self.data["translateMode"] = self.translateMode

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
        self.baiduUse_state()
        self.tencentUse_state()
        self.translateMode_state()
        self.showHotKey_state()
        self.data["translateSpeed"] = self.autoSpeed_spinBox.value()
        self.data["screenSize"] = self.spinBox.value() / 100
        self.saveAPI()

        with open('.\\config\\settin.json','w') as file:
            json.dump(self.data,file)

        get_Access_Token(self)


if __name__ == "__main__":
    
    import sys
    APP = QApplication(sys.argv)
    Settin = SettinInterface()
    Settin.show()
    sys.exit(APP.exec_())
