# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import qtawesome

import json
from Translate import translate
from switch import SwitchBtn

from traceback import print_exc
import time
from pyperclip import copy
from threading import Thread

from ScreenRate import get_screen_rate
from playVoice import Voice


class Runthread(QThread):

    _signal = pyqtSignal(dict)
 
    def __init__(self, window, mode):
        
        self.window = window
        self.mode = mode
        super(Runthread, self).__init__()

    def run(self):

        with open('.\\config\\settin.json') as file:
            data = json.load(file)
        
        if not self.mode :
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
                    self.window.StartButton.setIcon(qtawesome.icon('fa.pause', color='white'))

                while True:

                    with open('.\\config\\settin.json') as file:
                        data = json.load(file)

                    if data["sign"] % 2 == 0:
                        try:
                            result = translate(self.window, data)
                            self._signal.emit(result)
                            sec = data["translateSpeed"] - 0.9
                            time.sleep(sec)

                        except Exception:
                            print_exc()
                            break
                    else:
                        self.window.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
                        break

            except Exception:
                print_exc()


class MainInterface(QMainWindow):

    sig_keyhot = pyqtSignal(str)
    
    def __init__(self, screen_scale_rate):

        super(MainInterface, self).__init__()
        
        if 1.01 <= screen_scale_rate <= 1.49:
            self.rate = 1.25
        else:
            self.rate = 1
        
        self.get_settin()
        self.init_ui()


    def init_ui(self):
       
        # 窗口尺寸
        self.resize(800*self.rate, 120*self.rate)

        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("./config/图标.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 鼠标样式
        self.pixmap = QPixmap('.\\config\\光标.png')
        self.cursor = QCursor(self.pixmap, 0, 0)
        self.setCursor(self.cursor)

        # 工具栏标签
        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(0, 0, 800*self.rate, 30*self.rate)
        self.titleLabel.setStyleSheet("background-color:rgba(62, 62, 62, 0.01)")

        self.Font = QFont()
        self.Font.setFamily("华康方圆体W7")
        self.Font.setPointSize(15)

        # 翻译框
        self.translateText = QTextBrowser(self)
        self.translateText.setGeometry(0, 30*self.rate, 800*self.rate, 4000*self.rate)
        self.translateText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.translateText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.translateText.setStyleSheet("border-width:0;\
                                          border-style:outset;\
                                          border-top:0px solid #e8f3f9;\
                                          color:white;\
                                          font-weight: bold;\
                                          background-color:rgba(62, 62, 62, %s)"
                                          %(self.horizontal))
        self.translateText.setFont(self.Font)

        # 翻译框加入描边文字
        self.format = QTextCharFormat()
        self.format.setTextOutline(QPen(QColor('#FF69B4'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.translateText.mergeCurrentCharFormat(self.format)
        self.translateText.append("团子翻译器 ver3.3 --- By：胖次团子   更新时间：2020-05-07")
        self.translateText.append("交流群：1050705995   加群可获取最新版本并解惑翻译器一切问题")
        self.translateText.append("喜欢这个软件可以点击上方的电池按钮给团子个充电支持吗 ❤")
        self.translateText.append("团子会努力保持更新让大家用上更好的团子翻译器哒！")

        # 此Label用于当鼠标进入界面时给出颜色反应
        self.dragLabel = QLabel(self)
        self.dragLabel.setObjectName("dragLabel")
        self.dragLabel.setGeometry(0, 0, 4000*self.rate, 2000*self.rate)

        # 翻译按钮
        self.StartButton = QPushButton(qtawesome.icon('fa.play', color='white'), "", self)
        self.StartButton.setIconSize(QSize(20, 20))
        self.StartButton.setGeometry(QRect(213*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.StartButton.setToolTip('<b>翻译 Translate</b><br>点击翻译（手动）<br>开始/停止（自动）')
        self.StartButton.setStyleSheet("background: transparent")
        self.StartButton.clicked.connect(self.start_login)
        self.StartButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.StartButton.hide()

        # 设置按钮
        self.SettinButton = QPushButton(qtawesome.icon('fa.cog', color='white'), "", self)
        self.SettinButton.setIconSize(QSize(20, 20))
        self.SettinButton.setGeometry(QRect(253*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.SettinButton.setToolTip('<b>设置 Settin</b>')
        self.SettinButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.SettinButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.SettinButton.hide()
       
        # 范围按钮
        self.RangeButton = QPushButton(qtawesome.icon('fa.crop', color='white'), "", self)
        self.RangeButton.setIconSize(QSize(20, 20))
        self.RangeButton.setGeometry(QRect(293*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.RangeButton.setToolTip('<b>范围 Range</b><br>框选要翻译的区域<br>需从左上到右下拖动')
        self.RangeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.RangeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.RangeButton.hide()

        # 复制按钮
        self.CopyButton = QPushButton(qtawesome.icon('fa.copy', color='white'), "", self)
        self.CopyButton.setIconSize(QSize(20, 20))
        self.CopyButton.setGeometry(QRect(333*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.CopyButton.setToolTip('<b>复制 Copy</b><br>将当前识别到的文本<br>复制至剪贴板')
        self.CopyButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.CopyButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.CopyButton.clicked.connect(lambda:copy(self.original))
        self.CopyButton.hide()

        # 翻译模式按钮
        self.switchBtn = SwitchBtn(self)
        self.switchBtn.setGeometry(373*self.rate, 5*self.rate, 50*self.rate, 20*self.rate)
        self.switchBtn.setToolTip('<b>模式 Mode</b><br>手动翻译/自动翻译')
        self.switchBtn.checkedChanged.connect(self.getState)
        self.switchBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.switchBtn.hide()

        # 朗读原文按钮
        self.playVoiceButton = QPushButton(qtawesome.icon('fa.music', color='white'), "", self)
        self.playVoiceButton.setIconSize(QSize(20, 20))
        self.playVoiceButton.setGeometry(QRect(443*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.playVoiceButton.setGeometry(QRect(443*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.playVoiceButton.setToolTip('<b>朗读原文 Play Voice</b><br>朗读识别到的原文')
        self.playVoiceButton.setStyleSheet("background: transparent")
        self.playVoiceButton.clicked.connect(self.play_voice)
        self.playVoiceButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.playVoiceButton.hide()

        # 充电按钮
        self.BatteryButton = QPushButton(qtawesome.icon('fa.battery-half', color='white'), "", self)
        self.BatteryButton.setIconSize(QSize(24, 20))
        self.BatteryButton.setGeometry(QRect(483*self.rate, 5*self.rate, 24*self.rate, 20*self.rate))
        self.BatteryButton.setToolTip('<b>充电入口 Support author</b><br>我要给团子充电支持！')
        self.BatteryButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.BatteryButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.BatteryButton.hide()

        # 最小化按钮
        self.MinimizeButton = QPushButton(qtawesome.icon('fa.minus', color='white'), "", self)
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(QRect(527*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.MinimizeButton.setToolTip('<b>最小化 Minimize</b>')
        self.MinimizeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.MinimizeButton.hide()

        # 退出按钮
        self.QuitButton = QPushButton(qtawesome.icon('fa.times', color='white'), "", self)
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(QRect(567*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.QuitButton.setToolTip('<b>退出程序 Quit</b>')
        self.QuitButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.hide()

        # 右下角用于拉伸界面的控件
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)


    # 判断翻译模式键状态
    def getState(self, checked):

        if checked:
            self.mode = True
        else:
            self.mode = False
            
            with open('.\\config\\settin.json') as file:
                data = json.load(file)
                data["sign"] = 1
            with open('.\\config\\settin.json','w') as file:
                json.dump(data, file)
            self.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))


    # 鼠标移动事件
    def mouseMoveEvent(self, e: QMouseEvent):
        
        try:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except Exception:
            pass


    # 鼠标按下事件    
    def mousePressEvent(self, e: QMouseEvent):
        
        try:
            if e.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(e.x(), e.y())
        except Exception:
            print_exc()


    # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent):
        
        try:
            if e.button() == Qt.LeftButton:
                self._isTracking = False
                self._startPos = None
                self._endPos = None
        except Exception:
            print_exc()


    # 鼠标进入控件事件
    def enterEvent(self, QEvent):

        try:
            # 显示所有顶部工具栏控件
            self.switchBtn.show()
            self.StartButton.show()
            self.SettinButton.show()
            self.RangeButton.show()
            self.CopyButton.show()
            self.QuitButton.show()
            self.MinimizeButton.show()
            self.BatteryButton.show()
            self.playVoiceButton.show()

            self.setStyleSheet('QLabel#dragLabel {background-color:rgba(62, 62, 62, 0.3)}')
        
        except Exception:
            print_exc()

    # 鼠标离开控件事件
    def leaveEvent(self, QEvent):
        
        try:
            # 重置所有控件的位置和大小
            width = (self.width() * 213) / 800
            self.StartButton.setGeometry(QRect(width, 5*self.rate, 20*self.rate, 20*self.rate))
            self.SettinButton.setGeometry(QRect(width+40*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.RangeButton.setGeometry(QRect(width+80*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.CopyButton.setGeometry(QRect(width+120*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.switchBtn.setGeometry(QRect(width+160*self.rate, 5*self.rate, 50*self.rate, 20*self.rate))
            self.playVoiceButton.setGeometry(QRect(width+230*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.BatteryButton.setGeometry(QRect(width+270*self.rate, 5*self.rate, 24*self.rate, 20*self.rate))
            self.MinimizeButton.setGeometry(QRect(width+314*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.QuitButton.setGeometry(QRect(width+354*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.translateText.setGeometry(0, 30*self.rate, self.width(), 4000*self.rate)

            # 隐藏所有顶部工具栏控件
            self.switchBtn.hide()
            self.StartButton.hide()
            self.SettinButton.hide()
            self.RangeButton.hide()
            self.CopyButton.hide()
            self.QuitButton.hide()
            self.MinimizeButton.hide()
            self.BatteryButton.hide()
            self.playVoiceButton.hide()

            self.setStyleSheet('QLabel#dragLabel {background-color:none}')

        except Exception:
            print_exc()
  

    # 获取界面预设参数
    def get_settin(self):

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)

        # 翻译模式预设
        self.mode = False
        # 原文预设值
        self.original = ''
        
        # 透明度预设
        self.horizontal = (self.data["horizontal"]) / 100
        if self.horizontal == 0:
            self.horizontal = 0.01

    def start_login(self):

        with open('.\\config\\settin.json') as file:
            data = json.load(file)
        
        if data["sign"] % 2 == 0:
            data["sign"] += 1
            with open('.\\config\\settin.json','w') as file:
                json.dump(data, file)

            self.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
        else:
            try:
                self.thread = Runthread(self, self.mode)
                self.thread._signal.connect(self.call_backlog)
                self.thread.start()
            except Exception:
                print_exc()


    def send_key_event(self, i_str):
        
        self.start_login()


    # 将获得的翻译结果打印至翻译界面
    def call_backlog(self, result):

        with open('.\\config\\settin.json') as file:
            data = json.load(file)

        self.Font.setFamily(data["fontType"])
        self.Font.setPointSize(data["fontSize"])
        self.translateText.setFont(self.Font)

        if result["original"] and result["sign"]:
            self.original = result["original"]
            self.translateText.clear()

            if data["showOriginal"] == "True":
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["original"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["original"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["original"], result["original"]))

            if result["caiyunPrivate"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["caiyunPrivate"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["caiyunPrivate"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["caiyunPrivate"], result["caiyunPrivate"]))

            if result["tencent"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["tencent"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["tencent"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["tencent"], result["tencent"]))

            if result["baidu"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["baidu"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["baidu"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["baidu"], result["baidu"]))

            if result["Bing"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["Bing"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["Bing"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["Bing"], result["Bing"]))

            if result["google"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["google"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["google"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["google"], result["google"])) 

            if result["tencentweb"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["tencentweb"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["tencentweb"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["tencentweb"], result["tencentweb"])) 

            if result["baiduweb"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["baiduweb"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["baiduweb"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["baiduweb"], result["baiduweb"]))

            if result["alapi"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["ALAPI"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["alapi"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["ALAPI"], result["alapi"]))

            if result["yeekit"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["yeekit"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["yeekit"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["yeekit"], result["yeekit"]))

            if result["jinshan"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["jinshan"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["jinshan"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["jinshan"], result["jinshan"]))

            if result["caiyun"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["caiyun"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["caiyun"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["caiyun"], result["caiyun"]))

            if result["youdao"]:
                if data["showColorType"] == "False":
                    self.format.setTextOutline(QPen(QColor(data["fontColor"]["youdao"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(result["youdao"])
                else:
                    self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["youdao"], result["youdao"]))
       
        # 如果OCR出错，则打印错误信息
        elif result["original"] and not result["sign"]:
            self.translateText.clear()

            if data["showColorType"] == "False":
                self.format.setTextOutline(QPen(QColor(data["fontColor"]["original"]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result["original"])
            else:
                self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"]["original"], result["original"]))


    # 语音朗读
    def play_voice(self):

        try:
            thread = Thread(target=Voice, args=(self.original,)) 
            thread.setDaemon(True) 
            thread.start()
        except Exception:
            print_exc()


if __name__ == '__main__':
    
    import sys
    screen_scale_rate = get_screen_rate()
    App = QApplication(sys.argv)
    Init = MainInterface(screen_scale_rate)
    Init.show()
    App.exit(App.exec_())