from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.switch import SwitchButton
from translator import sound
import utils

from traceback import format_exc, print_exc
import qtawesome
import requests
import json
import threading
import os
import pyperclip


class Translation(QMainWindow):

    def __init__(self, config, logger):

        super(Translation, self).__init__()

        self.config = config
        self.logger = logger
        self.getInitConfig()
        self.ui()
        self.stratSoundThread(logger)


    # 开启音乐朗读线程
    def stratSoundThread(self, logger) :

        soundThread = threading.Thread(target=sound.createSound, args=(self, logger))
        soundThread.setDaemon(True)
        soundThread.start()


    def ui(self) :

        # 窗口尺寸
        self.resize(int(800*self.rate), int(120*self.rate))

        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 窗口图标
        icon = QIcon()
        icon.addPixmap(QPixmap("./config/icon/logo.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        # 鼠标样式
        pixmap = QPixmap("./config/icon/pixmap.png")
        pixmap = pixmap.scaled(int(30 * self.rate),
                               int(34 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 工具栏标签
        self.titleLabel = QLabel(self)
        self.customSetGeometry(self.titleLabel, 0, 0, 800, 30)
        self.titleLabel.setStyleSheet("background-color:rgba(62, 62, 62, 0.01)")

        self.font = QFont()
        self.font.setFamily("华康方圆体W7")
        self.font.setPointSize(15)

        # 翻译框
        self.translateText = QTextBrowser(self)
        self.customSetGeometry(self.translateText, 0, 30, 1500, 90)
        self.translateText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.translateText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.translateText.setStyleSheet("border-width:0;\
                                          border-style:outset;\
                                          border-top:0px solid #e8f3f9;\
                                          color:white;\
                                          font-weight: bold;\
                                          background-color:rgba(62, 62, 62, %s)"
                                         %(self.horizontal))
        self.translateText.setFont(self.font)

        # 翻译框加入描边文字
        self.format = QTextCharFormat()
        inform = self.getInform()
        if not inform :
            self.format.setTextOutline(QPen(QColor('#1E90FF'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.translateText.mergeCurrentCharFormat(self.format)
            self.translateText.append("欢迎你 ~ %s 么么哒 ~" % self.user)
            self.format.setTextOutline(QPen(QColor('#FF69B4'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.translateText.mergeCurrentCharFormat(self.format)
            self.translateText.append("b站关注 团子翻译器 查看动态可了解翻译器最新情况 ~")
            self.format.setTextOutline(QPen(QColor('#1E90FF'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.translateText.mergeCurrentCharFormat(self.format)
            self.translateText.append("团子一个人开发不易，这个软件真的花了很大很大的精力 _(:з」∠)_")
            self.format.setTextOutline(QPen(QColor('#FF69B4'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.translateText.mergeCurrentCharFormat(self.format)
            self.translateText.append("喜欢的话能不能点击上方的电池图标支持一下团子，真心感谢你❤")

        # 翻译框根据内容自适应大小
        self.document = self.translateText.document()
        self.document.contentsChanged.connect(self.textAreaChanged)

        # 此Label用于当鼠标进入界面时给出颜色反应
        self.dragLabel = QLabel(self)
        self.dragLabel.setObjectName("dragLabel")
        self.customSetGeometry(self.dragLabel, 0, 0, 4000, 2000)

        # 翻译按钮
        self.startButton = QPushButton(qtawesome.icon('fa.play', color='white'), "", self)
        self.customSetIconSize(self.startButton, 20, 20)
        self.customSetGeometry(self.startButton, 173, 5, 20, 20)
        self.startButton.setToolTip("<b>翻译键 Translate</b><br>点击后翻译（手动模式）")
        self.startButton.setStyleSheet("background: transparent")
        #self.startButton.clicked.connect(self.start_login)
        self.startButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.startButton.hide()

        # 设置按钮
        self.settinButton = QPushButton(qtawesome.icon('fa.cog', color='white'), "", self)
        self.customSetIconSize(self.settinButton, 20, 20)
        self.customSetGeometry(self.settinButton, 213, 5, 20, 20)
        self.settinButton.setToolTip("<b>设置键 Settin</b><br>翻译器的详细设置")
        self.settinButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.settinButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.settinButton.hide()

        # 范围按钮
        self.rangeButton = QPushButton(qtawesome.icon('fa.crop', color='white'), "", self)
        self.customSetIconSize(self.rangeButton, 20, 20)
        self.customSetGeometry(self.rangeButton, 253, 5, 20, 20)
        self.rangeButton.setToolTip('<b>范围 Range</b><br>框选要翻译的区域<br>需从左上到右下拖动')
        self.rangeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.rangeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.rangeButton.hide()

        # 复制按钮
        self.copyButton = QPushButton(qtawesome.icon('fa.copy', color='white'), "", self)
        self.customSetIconSize(self.copyButton, 20, 20)
        self.customSetGeometry(self.copyButton, 293, 5, 20, 20)
        self.copyButton.setToolTip('<b>复制 Copy</b><br>将当前识别到的文本<br>复制至剪贴板')
        self.copyButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.copyButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.copyButton.clicked.connect(lambda: pyperclip.copy(self.original))
        self.copyButton.hide()

        # 屏蔽词按钮
        self.filterWordButton = QPushButton(qtawesome.icon('fa.ban', color='white'), "", self)
        self.customSetIconSize(self.filterWordButton, 20, 20)
        self.customSetGeometry(self.filterWordButton, 333, 5, 20, 20)
        self.filterWordButton.setToolTip('<b>屏蔽字符 Filter</b><br>将特定翻译错误的词<br>屏蔽不显示')
        self.filterWordButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.filterWordButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.filterWordButton.hide()

        # 翻译模式按钮
        self.switchBtn = SwitchButton(self, sign=self.translateMode, startX=(50-20)*self.rate)
        self.customSetGeometry(self.switchBtn, 373, 5, 50, 20)
        self.switchBtn.setToolTip('<b>模式 Mode</b><br>手动翻译/自动翻译')
        self.switchBtn.checkedChanged.connect(self.changeTranslateMode)
        self.switchBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.switchBtn.hide()

        # 朗读原文按钮
        self.playVoiceButton = QPushButton(qtawesome.icon('fa.music', color='white'), "", self)
        self.customSetIconSize(self.playVoiceButton, 20, 20)
        self.customSetGeometry(self.playVoiceButton, 443, 5, 20, 20)
        self.playVoiceButton.setToolTip('<b>朗读原文 Play Voice</b><br>朗读识别到的原文')
        self.playVoiceButton.setStyleSheet("background: transparent")
        self.playVoiceButton.clicked.connect(self.playSound)
        self.playVoiceButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.playVoiceButton.hide()

        # 充电按钮
        self.batteryButton = QPushButton(qtawesome.icon('fa.battery-half', color='white'), "", self)
        self.customSetIconSize(self.batteryButton, 24, 20)
        self.customSetGeometry(self.batteryButton, 483, 5, 24, 20)
        self.batteryButton.setToolTip('<b>充电入口 Support author</b><br>我要给团子充电支持！')
        self.batteryButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.batteryButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.batteryButton.hide()

        # 锁按钮
        self.lockButton = QPushButton(qtawesome.icon('fa.lock', color='white'), "", self)
        self.customSetIconSize(self.lockButton, 20, 20)
        self.customSetGeometry(self.lockButton, 527, 5, 20, 20)
        self.lockButton.setToolTip('<b>锁定翻译界面 Lock</b>')
        self.lockButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.lockButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.lockButton.clicked.connect(self.lock)
        self.lockButton.hide()

        # 最小化按钮
        self.minimizeButton = QPushButton(qtawesome.icon('fa.minus', color='white'), "", self)
        self.customSetIconSize(self.minimizeButton, 20, 20)
        self.customSetGeometry(self.minimizeButton, 567, 5, 20, 20)
        self.minimizeButton.setToolTip('<b>最小化 Minimize</b>')
        self.minimizeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.minimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.minimizeButton.hide()

        # 退出按钮
        self.quitButton = QPushButton(qtawesome.icon('fa.times', color='white'), "", self)
        self.customSetIconSize(self.quitButton, 20, 20)
        self.customSetGeometry(self.quitButton, 607, 5, 20, 20)
        self.quitButton.setToolTip('<b>退出程序 Quit</b>')
        self.quitButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.quitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.quitButton.clicked.connect(self.quit)
        self.quitButton.hide()

        # 右下角用于拉伸界面的控件
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.config["screenScaleRate"]
        # 界面透明度
        self.horizontal = self.config["horizontal"]
        # 当前登录的用户
        self.user = self.config["user"]
        # 版本广播信息请求地址
        self.getInformURL = "http://120.24.146.175:3000/DangoTranslate/Getinform"
        # 界面锁
        self.lockSign = False
        # 翻译模式
        self.translateMode = False
        # 原文
        self.original = "ところで今日の最高気温、何度だと思う？37度だぜ、37度。夏にしても暑すぎる。これじゃオーブンだ。37度っていえば一人でじっとしてるより女の子と抱き合ってた方が涼しいくらいの温度だ。"


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 根据分辨率定义图标位置尺寸
    def customSetIconSize(self, object, w, h):

        object.setIconSize(QSize(int(w*self.rate),
                                 int(h*self.rate)))


    # 鼠标移动事件
    def mouseMoveEvent(self, e: QMouseEvent) :

        if self.lockSign == True :
            return

        try:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except Exception:
            pass


    # 鼠标按下事件
    def mousePressEvent(self, e: QMouseEvent) :

        if self.lockSign == True :
            return

        try:
            if e.button() == Qt.LeftButton :
                self._isTracking = True
                self._startPos = QPoint(e.x(), e.y())
        except Exception:
            pass


    # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent) :

        if self.lockSign == True :
            return

        try:
            if e.button() == Qt.LeftButton :
                self._isTracking = False
                self._startPos = None
                self._endPos = None
        except Exception:
            pass


    # 鼠标进入控件事件
    def enterEvent(self, QEvent) :

        if self.lockSign == True :
            self.lockButton.show()
            self.lockButton.setStyleSheet("background-color:rgba(62, 62, 62, 0.1);")
            self.statusbar.hide()
            return

        # 显示所有顶部工具栏控件
        self.switchBtn.show()
        self.startButton.show()
        self.settinButton.show()
        self.rangeButton.show()
        self.copyButton.show()
        self.quitButton.show()
        self.minimizeButton.show()
        self.batteryButton.show()
        self.playVoiceButton.show()
        self.lockButton.show()
        self.filterWordButton.show()

        self.setStyleSheet('QLabel#dragLabel {background-color:rgba(62, 62, 62, 0.1)}')


    # 鼠标离开控件事件
    def leaveEvent(self, QEvent) :

        if self.lockSign == False :
            self.statusbar.show()

        # 重置所有控件的位置和大小
        width = round((self.width()- 454*self.rate) / 2)
        height = self.height() - 30*self.rate

        self.startButton.setGeometry(QRect(width, 5*self.rate, 20*self.rate, 20*self.rate))
        self.settinButton.setGeometry(QRect(width + 40*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.rangeButton.setGeometry(QRect(width + 80*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.copyButton.setGeometry(QRect(width + 120*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.filterWordButton.setGeometry(QRect(width + 160*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.switchBtn.setGeometry(QRect(width + 200*self.rate, 5*self.rate, 50*self.rate, 20*self.rate))
        self.playVoiceButton.setGeometry(QRect(width + 270*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.batteryButton.setGeometry(QRect(width + 314*self.rate, 5*self.rate, 24*self.rate, 20*self.rate))
        self.lockButton.setGeometry(QRect(width + 358*self.rate, 5*self.rate, 24*self.rate, 20*self.rate))
        self.minimizeButton.setGeometry(QRect(width + 398*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.quitButton.setGeometry(QRect(width + 438*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.translateText.setGeometry(0, 30*self.rate, self.width(), height*self.rate)

        # 隐藏所有顶部工具栏控件
        self.switchBtn.hide()
        self.startButton.hide()
        self.settinButton.hide()
        self.rangeButton.hide()
        self.copyButton.hide()
        self.quitButton.hide()
        self.minimizeButton.hide()
        self.batteryButton.hide()
        self.playVoiceButton.hide()
        self.lockButton.hide()
        self.filterWordButton.hide()

        self.setStyleSheet('QLabel#dragLabel {background-color:none}')
        self.textAreaChanged()


    # 获取通知信息
    def getInform(self) :

        params = json.dumps({"version": "4.0"})
        try :
            res = requests.post(self.getInformURL, data=params, timeout=10)
            res.encoding = "utf-8"
            result = res.json().get("Result", "")

            if result != "" and result != "No" :
                for content in result.split(r"\n") :
                    self.format.setTextOutline(QPen(QColor('#1E90FF'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(content)
                return result

        except Exception :
            self.logger.error(format_exc())

        return False


    # 当翻译内容改变时界面自适应窗口大小
    def textAreaChanged(self) :

        newHeight = self.document.size().height()
        width = self.width()
        self.resize(width, newHeight + 30*self.rate)
        self.translateText.setGeometry(0, 30*self.rate, width, newHeight)


    # 锁定界面
    def lock(self) :

        # 上锁
        if not self.lockSign :
            self.lockButton.setIcon(qtawesome.icon("fa.unlock", color="white"))
            self.dragLabel.hide()
            self.lockSign = True

            if self.horizontal == 0.01 :
                self.horizontal = 0
        # 解锁
        else:
            self.lockButton.setIcon(qtawesome.icon("fa.lock", color="white"))
            self.lockButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
            self.dragLabel.show()
            self.lockSign = False

            if self.horizontal == 0 :
                self.horizontal = 0.01

        self.translateText.setStyleSheet("border-width:0;\
                                          border-style:outset;\
                                          border-top:0px solid #e8f3f9;\
                                          color:white;\
                                          font-weight: bold;\
                                          background-color:rgba(62, 62, 62, %s)"
                                         %(self.horizontal))


    # 改变翻译模式
    def changeTranslateMode(self, checked) :

        if checked :
            self.translateMode = True
        else:
            self.translateMode = False


    # 朗读原文
    def playSound(self) :

        try :
            playSoundThread = threading.Thread(target=self.sound.playSound, args=(self.original, self.config["language"]))
            playSoundThread.setDaemon(True)
            playSoundThread.start()
        except Exception :
            self.logger.error(format_exc())


    # 退出程序
    def quit(self) :

        # 关闭音乐模块
        try :
            self.sound.close()
        except Exception :
            self.logger.error(format_exc())
        finally :
            # 关闭selenuim的driver引擎
            os.system("taskkill /im chromedriver.exe /F")
            os.system("taskkill /im geckodriver.exe /F")

        # 退出程序前保存设置
        utils.postSaveSettin(self.config, self.logger)
        self.close()