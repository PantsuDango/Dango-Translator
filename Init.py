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
from system_hotkey import SystemHotkey
from pyperclip import copy


class Runthread(QThread):

    _signal = pyqtSignal(tuple)
 
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
                            sec = data["translateSpeed"] - 1
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
    
    def __init__(self):

        super(MainInterface, self).__init__()
        self.get_settin()
        self.init_ui()


    def init_ui(self):
        
        # 窗口尺寸
        self.resize(800, 100)

        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(":/image/图标.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 鼠标样式
        self.pixmap = QPixmap('.\\config\\光标.png')
        self.cursor = QCursor(self.pixmap, 0, 0)
        self.setCursor(self.cursor)

        # 工具栏标签
        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(0, 0, 800, 30)
        self.titleLabel.setStyleSheet("background-color:rgba(62, 62, 62, 0.01)")

        self.Font = QFont()
        self.Font.setFamily("华康方圆体W7")
        self.Font.setPointSize(15)

        # 翻译框
        self.translateText = QTextBrowser(self)
        self.translateText.setGeometry(0, 30, 800, 4000)
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
        self.translateText.append("团子翻译器 ver3.1 --- By：胖次团子   更新时间：2020-03-22")
        self.translateText.append("喜欢这个软件可以点击上方的电池按钮给我个充电支持吗 ❤")
        self.translateText.append("我会努力保持更新让大家用上更好的团子翻译器哒！")

        # 此Label用于当鼠标进入界面时给出颜色反应
        self.dragLabel = QLabel(self)
        self.dragLabel.setObjectName("dragLabel")
        self.dragLabel.setGeometry(0, 0, 4000, 2000)

        # 翻译按钮
        self.StartButton = QPushButton(qtawesome.icon('fa.play', color='white'), "", self)
        self.StartButton.setIconSize(QSize(20, 20))
        self.StartButton.setGeometry(QRect(233, 5, 20, 20))
        self.StartButton.setToolTip('<b>翻译 Translate</b><br>点击翻译（手动）<br>开始/停止（自动）')
        self.StartButton.setStyleSheet("background: transparent")
        self.StartButton.clicked.connect(self.start_login)
        self.StartButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.StartButton.hide()

        # 设置按钮
        self.SettinButton = QPushButton(qtawesome.icon('fa.cog', color='white'), "", self)
        self.SettinButton.setIconSize(QSize(20, 20))
        self.SettinButton.setGeometry(QRect(273, 5, 20, 20))
        self.SettinButton.setToolTip('<b>设置 Settin</b>')
        self.SettinButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.SettinButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.SettinButton.hide()
       
        # 范围按钮
        self.RangeButton = QPushButton(qtawesome.icon('fa.crop', color='white'), "", self)
        self.RangeButton.setIconSize(QSize(20, 20))
        self.RangeButton.setGeometry(QRect(313, 5, 20, 20))
        self.RangeButton.setToolTip('<b>范围 Range</b><br>框选要翻译的区域<br>需从左上到右下拖动')
        self.RangeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.RangeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.RangeButton.hide()

        # 复制按钮
        self.CopyButton = QPushButton(qtawesome.icon('fa.copy', color='white'), "", self)
        self.CopyButton.setIconSize(QSize(20, 20))
        self.CopyButton.setGeometry(QRect(353, 5, 20, 20))
        self.CopyButton.setToolTip('<b>复制 Copy</b><br>将当前识别到的文本<br>复制至剪贴板')
        self.CopyButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.CopyButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.CopyButton.clicked.connect(lambda:copy(self.original))
        self.CopyButton.hide()

        # 翻译模式按钮
        self.switchBtn = SwitchBtn(self)
        self.switchBtn.setGeometry(393, 5, 50, 20)
        self.switchBtn.setToolTip('<b>模式 Mode</b><br>手动翻译/自动翻译')
        self.switchBtn.checkedChanged.connect(self.getState)
        self.switchBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.switchBtn.hide()

        # 充电按钮
        self.BatteryButton = QPushButton(qtawesome.icon('fa.battery-half', color='white'), "", self)
        self.BatteryButton.setIconSize(QSize(24, 20))
        self.BatteryButton.setGeometry(QRect(463, 5, 24, 20))
        self.BatteryButton.setToolTip('<b>充电入口 Support author</b><br>我要给团子充电支持！')
        self.BatteryButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.BatteryButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.BatteryButton.hide()

        # 最小化按钮
        self.MinimizeButton = QPushButton(qtawesome.icon('fa.minus', color='white'), "", self)
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(QRect(507, 5, 20, 20))
        self.MinimizeButton.setToolTip('<b>最小化 Minimize</b>')
        self.MinimizeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.MinimizeButton.hide()

        # 退出按钮
        self.QuitButton = QPushButton(qtawesome.icon('fa.times', color='white'), "", self)
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(QRect(547, 5, 20, 20))
        self.QuitButton.setToolTip('<b>退出程序 Quit</b>')
        self.QuitButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.clicked.connect(self.close)
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

            self.setStyleSheet('QLabel#dragLabel {background-color:rgba(62, 62, 62, 0.3)}')
        except Exception:
            print_exc()

    # 鼠标离开控件事件
    def leaveEvent(self, QEvent):
        
        try:
            # 重置所有控件的位置和大小
            width = (self.width() * 233) / 800
            self.StartButton.setGeometry(QRect(width, 5, 20, 20))
            self.SettinButton.setGeometry(QRect(width+40, 5, 20, 20))
            self.RangeButton.setGeometry(QRect(width+80, 5, 20, 20))
            self.CopyButton.setGeometry(QRect(width+120, 5, 20, 20))
            self.switchBtn.setGeometry(QRect(width+160, 5, 50, 20))
            self.BatteryButton.setGeometry(QRect(width+220, 5, 50, 20))
            self.MinimizeButton.setGeometry(QRect(width+274, 5, 24, 20))
            self.QuitButton.setGeometry(QRect(width+314, 5, 20, 20))
            self.translateText.setGeometry(0, 30, self.width(), 4000)

            # 隐藏所有顶部工具栏控件
            self.switchBtn.hide()
            self.StartButton.hide()
            self.SettinButton.hide()
            self.RangeButton.hide()
            self.CopyButton.hide()
            self.QuitButton.hide()
            self.MinimizeButton.hide()
            self.BatteryButton.hide()

            self.setStyleSheet('QLabel#dragLabel {background-color:none}')
        except Exception:
            print_exc()


    # 获取界面预设参数
    def get_settin(self):

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)

        # 翻译模式预设
        self.mode = False
        
        # 透明度预设
        self.horizontal = (self.data["horizontal"]) / 100
        if self.horizontal == 0:
            self.horizontal = 0.01

        # 获得快捷键预设并注册成全局热键
        self.showHotKeyValue1 = self.data["showHotKeyValue1"]
        self.showHotKeyValue2 = self.data["showHotKeyValue2"]
        self.showHotKey = self.data["showHotKey"]
        if self.showHotKey == "True":
            try:
                self.hk_start = SystemHotkey()
                self.hk_start.register((self.showHotKeyValue1, self.showHotKeyValue2), callback=lambda x:self.send_key_event("start"))
            except Exception:
                print_exc()


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


    def send_key_event(self,i_str):
        
        self.start_login()


    def call_backlog(self, result):
        
        if result[8]:
            self.original = result[8]

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)

        # 各翻译源颜色
        self.jinshanColor = self.data["fontColor"]["jinshan"]
        self.yeekitColor = self.data["fontColor"]["yeekit"]
        self.originalColor = self.data["fontColor"]["original"]
        self.caiyunColor = self.data["fontColor"]["caiyun"]
        self.tencentColor = self.data["fontColor"]["tencent"]
        self.baiduwebColor = self.data["fontColor"]["baiduweb"]
        self.baiduColor = self.data["fontColor"]["baidu"]
        self.youdaoColor = self.data["fontColor"]["youdao"]
        self.ALAPIColor = self.data["fontColor"]["ALAPI"]

        # 字体大小
        self.fontSize = self.data["fontSize"]
        # 字体样式
        self.fontType = self.data["fontType"]
        # 是否显示原文
        self.showOriginal = self.data["showOriginal"]

        self.Font = QFont()
        self.Font.setFamily(self.fontType)
        self.Font.setPointSize(self.fontSize)
        self.translateText.setFont(self.Font)


        if (not result[0]) and (not result[1]) and (not result[2]) and (not result[3]) and (not result[4]) and (not result[5]) and (not result[6]) and (not result[7]) and (not result[8]):
            pass
        else:
            self.translateText.clear()
            if result[0]:
                self.format.setTextOutline(QPen(QColor(self.youdaoColor), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result[0])
            if result[1]:
                self.format.setTextOutline(QPen(QColor(self.caiyunColor), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result[1])
            if result[2]:
                self.format.setTextOutline(QPen(QColor(self.jinshanColor), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result[2])
            if result[3]:
                self.format.setTextOutline(QPen(QColor(self.yeekitColor), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result[3])
            if result[4]:
                self.format.setTextOutline(QPen(QColor(self.ALAPIColor), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result[4])
            if result[5]:
                self.format.setTextOutline(QPen(QColor(self.baiduwebColor), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result[5])
            if result[6]:
                self.format.setTextOutline(QPen(QColor(self.baiduColor), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result[6])
            if result[7]:
                self.format.setTextOutline(QPen(QColor(self.tencentColor), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result[7])
            if result[8] and self.showOriginal == "True":
                self.format.setTextOutline(QPen(QColor(self.originalColor), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result[8])


if __name__ == '__main__':
    
    import sys
    App = QApplication(sys.argv)
    Init = MainInterface()
    Init.show()
    App.exit(App.exec_())