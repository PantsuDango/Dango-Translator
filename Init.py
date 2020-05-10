# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

import json
from Translate import translate

from traceback import print_exc
import time
from system_hotkey import SystemHotkey


class Runthread(QThread):

    _signal = pyqtSignal(tuple)
 
    def __init__(self, window):
        
        self.window = window
        super(Runthread, self).__init__()

    def run(self):

        with open('.\\config\\settin.json') as file:
            data = json.load(file)
        translateMode = data["translateMode"]
        
        if translateMode == 'manual':
            try:
                result = translate(self.window, data)
                self._signal.emit(result)
            except Exception:
                print_exc()
        else:
            data["sign"] += 1
            with open('.\\config\\settin.json','w') as file:
                json.dump(data, file)
            try:
                if data["sign"] % 2 == 0:
                    self.window.StartButton.setText("停止")

                while True:
                    with open('.\\config\\settin.json') as file:
                        data = json.load(file)

                    if data["sign"] % 2 == 0:
                        try:
                            result = translate(self.window, data)
                            self._signal.emit(result)
                            sec = data["translateSpeed"] - 1.5
                            time.sleep(sec)
                        except Exception:
                            print_exc()
                            break
                    else:
                        break
            except Exception:
                print_exc()


class MainInterface(QMainWindow):

    sig_keyhot = pyqtSignal(str)
    
    def __init__(self):
        
        _startPos = None
        _endPos = None
        _isTracking = False
        super(MainInterface, self).__init__()
        self.init_ui()


    def init_ui(self):
        
        self.get_settin()

        self.resize(800, 95)
        self.setMinimumSize(QSize(800, 0))
        self.setMaximumSize(QSize(800, 1000))
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | 
                            Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        if self.showHotKey == "True":
            self.hk_start = SystemHotkey()
            self.hk_start.register(('alt', self.showHotKeyValue), callback=lambda x:self.send_key_event("start"))

        icon = QIcon()
        icon.addPixmap(QPixmap(":/image/图标.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        self.dragLabel = QLabel(self)
        self.dragLabel.setObjectName("dragLabel")
        self.dragLabel.setGeometry(0, 0, 800, 25)

        self.ButtonFont = QFont()
        self.ButtonFont.setFamily("华康方圆体W7")
        self.ButtonFont.setPointSize(10)

        self.StartButton = QPushButton(self)
        self.StartButton.setGeometry(QRect(0, 0, 70, 25))
        self.StartButton.setFont(self.ButtonFont)
        self.StartButton.setStyleSheet("QPushButton{border-width:0;border-style:outset;border-top:0px solid #e8f3f9;background: transparent;}")
        if self.translateMode == "auto":
            self.StartButton.setText("开始")
        else:
            self.StartButton.setText("翻译")

        self.StartButton.clicked.connect(self.start_login)

        self.SettinButton = QPushButton("设置", self)
        self.SettinButton.setGeometry(QRect(70, 0, 70, 25))
        self.SettinButton.setFont(self.ButtonFont)
        self.SettinButton.setStyleSheet("QPushButton{border-width:0;border-style:outset;border-top:0px solid #e8f3f9;background: transparent;}")
        
        self.RangeButton = QPushButton("范围", self)
        self.RangeButton.setGeometry(QRect(140, 0, 70, 25))
        self.RangeButton.setFont(self.ButtonFont)
        self.RangeButton.setStyleSheet("QPushButton{border-width:0;border-style:outset;border-top:0px solid #e8f3f9;background: transparent;}")

        self.QuitButton = QPushButton("退出", self)
        self.QuitButton.setGeometry(QRect(730, 0, 70, 25))
        self.QuitButton.setFont(self.ButtonFont)
        self.QuitButton.setStyleSheet("QPushButton{border-width:0;border-style:outset;border-top:0px solid #e8f3f9;background: transparent;}")
        self.QuitButton.clicked.connect(self.close)

        self.MinimizeButton = QPushButton("最小化", self)
        self.MinimizeButton.setGeometry(QRect(660, 0, 70, 25))
        self.MinimizeButton.setFont(self.ButtonFont)
        self.MinimizeButton.setStyleSheet("QPushButton{border-width:0;border-style:outset;border-top:0px solid #e8f3f9;background: transparent;}")
        self.MinimizeButton.clicked.connect(self.showMinimized)

        self.TextFont = QFont()
        self.TextFont.setFamily("华康方圆体W7")
        self.TextFont.setPointSize(15)

        self.translateText = QTextBrowser(self)
        self.translateText.setEnabled(True)
        self.translateText.setGeometry(0, 25, 800, 5000)
        self.translateText.setStyleSheet("border-width:0;border-style:outset;border-top:0px solid #e8f3f9;background-color:rgba(62, 62, 62, {}); color:#FF69B4".format(self.horizontal))
        self.translateText.setFont(self.TextFont)
        self.translateText.append("团子翻译器 ver3.0 --- By：胖次团子   更新时间：2020-02-26")
        self.translateText.append("交流群：①群779594427  ②群1038904947  ③群1048646110  ④群939840254")
        self.translateText.append("        ④群939840254  ⑤群905382640（可加）")

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)


    def mouseMoveEvent(self, e: QMouseEvent):
        
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)


    def mousePressEvent(self, e: QMouseEvent):
        
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

 
    def mouseReleaseEvent(self, e: QMouseEvent):
        
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


    def enterEvent(self,QEvent):
        self.setStyleSheet('QLabel#dragLabel {background-color:rgba(62, 62, 62, 0.8)}')


    def leaveEvent(self,QEvent):
        self.setStyleSheet('QLabel#dragLabel {background-color:none}')


    def get_settin(self):

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)

        self.horizontal = (self.data["horizontal"]) / 100
        self.translateMode = self.data["translateMode"]
        self.showHotKeyValue = self.data["showHotKeyValue"]
        self.showHotKey = self.data["showHotKey"]


    def start_login(self):

        with open('.\\config\\settin.json') as file:
            data = json.load(file)
        
        if self.StartButton.text() == '停止':
            data["sign"] += 1
            with open('.\\config\\settin.json','w') as file:
                json.dump(data, file)

            self.StartButton.setText("开始")
        else:
            try:
                self.thread = Runthread(self)
                self.thread._signal.connect(self.call_backlog)
                self.thread.start()
            except Exception:
                print_exc()

    def send_key_event(self,i_str):
        
        self.start_login()


    def call_backlog(self, result):
        
        with open('.\\config\\settin.json') as file:
            data = json.load(file)

        youdaoColor = data["fontColor"]["youdao"]
        caiyunColor = data["fontColor"]["caiyun"]
        jinshanColor = data["fontColor"]["jinshan"]
        baiduColor = data["fontColor"]["baidu"]
        tencentColor = data["fontColor"]["tencent"]
        originalColor = data["fontColor"]["original"]

        youdaoSize = data["fontSize"]["youdao"]
        caiyunSize = data["fontSize"]["caiyun"]
        jinshanSize = data["fontSize"]["jinshan"]
        baiduSize = data["fontSize"]["baidu"]
        tencentSize = data["fontSize"]["tencent"]
        originalSize = data["fontSize"]["original"]
            
        youdaoFont = data["fontType"]["youdao"]
        caiyunFont = data["fontType"]["caiyun"]
        jinshanFont = data["fontType"]["jinshan"]
        baiduFont = data["fontType"]["baidu"]
        tencentFont = data["fontType"]["tencent"]
        originalFont = data["fontType"]["original"]


        if (not result[0]) and (not result[1]) and (not result[2]) and (not result[3]) and (not result[4]) and (not result[5]):
            pass
        else:
            self.translateText.setHtml("<font color=%s size=%s face=%s>%s</font>\
                                        <font color=%s size=%s face=%s>%s</font>\
                                        <font color=%s size=%s face=%s>%s</font>\
                                        <font color=%s size=%s face=%s>%s</font>\
                                        <font color=%s size=%s face=%s>%s</font>\
                                        <font color=%s size=%s face=%s>%s</font>"
                                        %(youdaoColor, youdaoSize, youdaoFont, result[0],
                                            caiyunColor, caiyunSize, caiyunFont, result[1],
                                            jinshanColor, jinshanSize, jinshanFont, result[2],
                                            baiduColor, baiduSize, baiduFont, result[3],
                                            tencentColor, tencentSize, tencentFont, result[4],
                                            originalColor, originalSize, originalFont, result[5]))


if __name__ == '__main__':
    
    import sys
    App = QApplication(sys.argv)
    Init = MainInterface()
    Init.show()
    App.exit(App.exec_())