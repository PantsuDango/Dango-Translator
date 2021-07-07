# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qtawesome

import json
from Translate import TranslateThread
from switch import SwitchBtn

from traceback import print_exc
from pyperclip import copy
from threading import Thread
import requests

from ScreenRate import get_screen_rate
from playVoice import Voice

from API import youdao, caiyun, jinshan, yeekit, ALAPI, baidu, tencent, caiyunAPI
from baidufanyi import BaiduTranslator
from Tencent import TencentTrans
from Google import GoogleTranslate
from Bing import BingTranslate


class UseTranslateThread(QObject):

    use_translate_signal = pyqtSignal(str, dict, str)
 
    def __init__(self, fun, original, data, translate_type):
        
        self.fun = fun  # 要执行的翻译函数
        self.original = original  # 识别到的原文
        self.data = data  # 配置信息
        self.translate_type = translate_type  # 翻译源
        super(UseTranslateThread, self).__init__()


    # 过滤屏蔽词
    def filter_words(self, content):

        with open('.\\config\\settin.json') as file:
            data = json.load(file)
        filter = data.get("filter", [])

        for old_word, new_word in filter:
            content = content.replace(old_word, new_word)

        return content


    def run(self):

        if self.translate_type == "yeekit"  or self.translate_type == "baidu" or self.translate_type == "tencent" or self.translate_type == "caiyunPrivate":
            result = self.fun(self.original, self.data)
        
        elif self.translate_type == "baiduweb":
            baiduweb = self.fun()
            result = baiduweb.run(self.original)
        
        elif self.translate_type == "tencentweb":
            tencentweb = self.fun()
            result = tencentweb.get_trans_result(self.original)
        
        elif self.translate_type == "google":
            google = self.fun()
            result = google.translate(self.original)
        
        elif self.translate_type == "Bing":
            bing = self.fun()
            result = bing.translate(self.original, self.data)

        elif self.translate_type == "original":
            result = self.original
        
        else:
            result = self.fun(self.original)

        # 屏蔽词过滤
        if self.translate_type != "original" :
            result = self.filter_words(result)

        self.use_translate_signal.emit(result, self.data, self.translate_type)


class MainInterface(QMainWindow):
  
    def __init__(self, screen_scale_rate, user):

        super(MainInterface, self).__init__()

        self.rate = screen_scale_rate  # 屏幕缩放比例
        self.lock_sign = 0
        self.user = user
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

        # 系统托盘
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.icon)
        self.tray.activated.connect(self.show)
        self.tray.show()


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
        self.translateText.setGeometry(0, 30*self.rate, 1500*self.rate, 90*self.rate)
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
        sign = self.getinform()
        if sign == 0 :
            self.format.setTextOutline(QPen(QColor('#1E90FF'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.translateText.mergeCurrentCharFormat(self.format)
            self.translateText.append("欢迎你 ~ %s 么么哒 ~"%self.user)
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
        self.dragLabel.setGeometry(0, 0, 4000*self.rate, 2000*self.rate)

        # 翻译按钮
        self.StartButton = QPushButton(qtawesome.icon('fa.play', color='white'), "", self)
        self.StartButton.setIconSize(QSize(20, 20))
        self.StartButton.setGeometry(QRect(173*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.StartButton.setToolTip('<b>翻译 Translate</b><br>点击翻译（手动）<br>开始/停止（自动）')
        self.StartButton.setStyleSheet("background: transparent")
        self.StartButton.clicked.connect(self.start_login)
        self.StartButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.StartButton.hide()

        # 设置按钮
        self.SettinButton = QPushButton(qtawesome.icon('fa.cog', color='white'), "", self)
        self.SettinButton.setIconSize(QSize(20, 20))
        self.SettinButton.setGeometry(QRect(213*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.SettinButton.setToolTip('<b>设置 Settin</b>')
        self.SettinButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.SettinButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.SettinButton.hide()
       
        # 范围按钮
        self.RangeButton = QPushButton(qtawesome.icon('fa.crop', color='white'), "", self)
        self.RangeButton.setIconSize(QSize(20, 20))
        self.RangeButton.setGeometry(QRect(253*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.RangeButton.setToolTip('<b>范围 Range</b><br>框选要翻译的区域<br>需从左上到右下拖动')
        self.RangeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.RangeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.RangeButton.hide()

        # 复制按钮
        self.CopyButton = QPushButton(qtawesome.icon('fa.copy', color='white'), "", self)
        self.CopyButton.setIconSize(QSize(20, 20))
        self.CopyButton.setGeometry(QRect(293*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.CopyButton.setToolTip('<b>复制 Copy</b><br>将当前识别到的文本<br>复制至剪贴板')
        self.CopyButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.CopyButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.CopyButton.clicked.connect(lambda:copy(self.original))
        self.CopyButton.hide()

        # 屏蔽词按钮
        self.FilterWordButton = QPushButton(qtawesome.icon('fa.ban', color='white'), "", self)
        self.FilterWordButton.setIconSize(QSize(20, 20))
        self.FilterWordButton.setGeometry(QRect(333*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.FilterWordButton.setToolTip('<b>屏蔽字符 Filter</b><br>将特定翻译错误的词<br>屏蔽不显示')
        self.FilterWordButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.FilterWordButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.FilterWordButton.hide()

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

        # 锁按钮
        self.LockButton = QPushButton(qtawesome.icon('fa.lock', color='white'), "", self)
        self.LockButton.setIconSize(QSize(20, 20))
        self.LockButton.setGeometry(QRect(527 * self.rate, 5 * self.rate, 20 * self.rate, 20 * self.rate))
        self.LockButton.setToolTip('<b>锁定翻译界面 Lock</b>')
        self.LockButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.LockButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.LockButton.clicked.connect(self.lock)
        self.LockButton.hide()

        # 最小化按钮
        self.MinimizeButton = QPushButton(qtawesome.icon('fa.minus', color='white'), "", self)
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(QRect(567*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.MinimizeButton.setToolTip('<b>最小化 Minimize</b>')
        self.MinimizeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.hide)
        self.MinimizeButton.hide()

        # 退出按钮
        self.QuitButton = QPushButton(qtawesome.icon('fa.times', color='white'), "", self)
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(QRect(607*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
        self.QuitButton.setToolTip('<b>退出程序 Quit</b>')
        self.QuitButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.hide()

        # 右下角用于拉伸界面的控件
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)


    # 锁定界面
    def lock(self):

        try :
            if self.lock_sign == 0 :
                self.LockButton.setIcon(qtawesome.icon('fa.unlock', color='white'))
                self.dragLabel.hide()
                self.lock_sign = 1

                if self.horizontal == 0.01 :
                    self.horizontal = 0
            else :
                self.LockButton.setIcon(qtawesome.icon('fa.lock', color='white'))
                self.LockButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
                self.dragLabel.show()
                self.lock_sign = 0

                if self.horizontal == 0 :
                    self.horizontal = 0.01

            self.translateText.setStyleSheet("border-width:0;\
                                              border-style:outset;\
                                              border-top:0px solid #e8f3f9;\
                                              color:white;\
                                              font-weight: bold;\
                                              background-color:rgba(62, 62, 62, %s)"
                                              %(self.horizontal))
        except Exception:
            print_exc()


    # 当翻译内容改变时界面自适应窗口大小
    def textAreaChanged(self):
        
        newHeight = self.document.size().height()
        width = self.width()
        self.resize(width, newHeight+30*self.rate)
        self.translateText.setGeometry(0, 30*self.rate, width, newHeight)


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

        if self.lock_sign == 1 :
            return
        
        try:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except Exception:
            pass


    # 鼠标按下事件    
    def mousePressEvent(self, e: QMouseEvent):

        if self.lock_sign == 1 :
            return
        
        try:
            if e.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(e.x(), e.y())
        except Exception:
            print_exc()


    # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent):

        if self.lock_sign == 1 :
            return
        
        try:
            if e.button() == Qt.LeftButton:
                self._isTracking = False
                self._startPos = None
                self._endPos = None
        except Exception:
            print_exc()


    # 鼠标进入控件事件
    def enterEvent(self, QEvent):

        if self.lock_sign == 1 :
            self.LockButton.show()
            self.LockButton.setStyleSheet("background-color:rgba(62, 62, 62, 0.7);")
            return

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
            self.LockButton.show()
            self.FilterWordButton.show()

            self.setStyleSheet('QLabel#dragLabel {background-color:rgba(62, 62, 62, 0.3)}')
        
        except Exception:
            print_exc()


    # 鼠标离开控件事件
    def leaveEvent(self, QEvent):

        try:
            # 重置所有控件的位置和大小
            width = (self.width()-454*self.rate) / 2
            height = self.height()-30*self.rate
            self.StartButton.setGeometry(QRect(width, 5*self.rate, 20*self.rate, 20*self.rate))
            self.SettinButton.setGeometry(QRect(width+40*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.RangeButton.setGeometry(QRect(width+80*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.CopyButton.setGeometry(QRect(width+120*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.FilterWordButton.setGeometry(QRect(width+160*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))

            self.switchBtn.setGeometry(QRect(width+200*self.rate, 5*self.rate, 50*self.rate, 20*self.rate))
            self.playVoiceButton.setGeometry(QRect(width+270*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.BatteryButton.setGeometry(QRect(width+314*self.rate, 5*self.rate, 24*self.rate, 20*self.rate))
            self.LockButton.setGeometry(QRect(width+358*self.rate, 5*self.rate, 24*self.rate, 20*self.rate))
            self.MinimizeButton.setGeometry(QRect(width+398*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))
            self.QuitButton.setGeometry(QRect(width+438*self.rate, 5*self.rate, 20*self.rate, 20*self.rate))

            self.translateText.setGeometry(0, 30*self.rate, self.width(), height*self.rate)


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
            self.LockButton.hide()
            self.FilterWordButton.hide()

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

        # 各翻译源线程状态标志
        self.thread_state = 0

        # 记录翻译失败的状态
        self.is_fail = False


    def start_login(self):

        with open('.\\config\\settin.json') as file:
            data = json.load(file)
        
        if data["sign"] % 2 == 0:
            data["sign"] += 1
            with open('.\\config\\settin.json','w') as file:
                json.dump(data, file)

            self.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
        else:
            thread = TranslateThread(self, self.mode)
            thread.use_translate_signal.connect(self.use_translate)
            thread.start()
            thread.exec()


    # 创造翻译线程
    def creat_thread(self, fun, original, data, translate_type):

        self.thread_state += 1  # 线程开始，增加线程数
        translation_source = UseTranslateThread(fun, original, data, translate_type)
        thread = Thread(target=translation_source.run)
        thread.setDaemon(True) 
        translation_source.use_translate_signal.connect(self.display_text)
        thread.start()


    # 并发执行所有翻译源
    def use_translate(self, signal_list, original, data):

        # 翻译界面清屏
        self.translateText.clear()
        # 设定翻译时的字体类型和大小
        self.Font.setFamily(data["fontType"])
        self.Font.setPointSize(data["fontSize"])
        self.translateText.setFont(self.Font)

        if "original" in signal_list or "error" in signal_list:
            self.creat_thread(None, original, data, "original")
        
        if "youdao" in signal_list:
            self.creat_thread(youdao, original, data, "youdao")
        
        if "caiyun" in signal_list:
            self.creat_thread(caiyun, original, data, "caiyun")
        
        if "jinshan" in signal_list:
            self.creat_thread(jinshan, original, data, "jinshan")
        
        if "yeekit" in signal_list:
            self.creat_thread(yeekit, original, data, "yeekit")
        
        if "ALAPI" in signal_list:
            self.creat_thread(ALAPI, original, data, "ALAPI")
        
        if "baiduweb" in signal_list:
            self.creat_thread(BaiduTranslator, original, data, "baiduweb")
        
        if "tencentweb" in signal_list:
            self.creat_thread(TencentTrans, original, data, "tencentweb")
        
        if "google" in signal_list:
            self.creat_thread(GoogleTranslate, original, data, "google")
        
        if "Bing" in signal_list:
            self.creat_thread(BingTranslate, original, data, "Bing")

        if "baidu" in signal_list:
            self.creat_thread(baidu, original, data, "baidu")
        
        if "tencent" in signal_list:
            self.creat_thread(tencent, original, data, "tencent")
        
        if "caiyunPrivate" in signal_list:
            self.creat_thread(caiyunAPI, original, data, "caiyunPrivate")

    
    # 将翻译结果打印
    def display_text(self, result, data, translate_type):

        try :
            if data["showColorType"] == "False":
                self.format.setTextOutline(QPen(QColor(data["fontColor"][translate_type]), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.translateText.mergeCurrentCharFormat(self.format)
                self.translateText.append(result)
            else:
                self.translateText.append("<font color=%s>%s</font>"%(data["fontColor"][translate_type], result))

            # 保存译文
            self.save_text(result, translate_type)
            self.thread_state -= 1  #  线程结束，减少线程数

        except Exception :
            print_exc()


    # 语音朗读
    def play_voice(self):

        if not self.original:
            return
        try:
            thread = Thread(target=Voice, args=(self.original,)) 
            thread.setDaemon(True) 
            thread.start()
        except Exception:
            print_exc()


    def save_text(self, text, translate_type):

        if translate_type == "youdao" :
            content = "\n[有道翻译]\n%s"%text
        elif translate_type == "caiyun" :
            content = "\n[公共彩云翻译]\n%s"%text
        elif translate_type == "jinshan" :
            content = "\n[金山翻译]\n%s"%text
        elif translate_type == "yeekit" :
            content = "\n[yeekit翻译]\n%s"%text
        elif translate_type == "ALAPI" :
            content = "\n[ALAPI翻译]\n%s"%text
        elif translate_type == "baiduweb" :
            content = "\n[网页百度翻译]\n%s"%text
        elif translate_type == "tencentweb" :
            content = "\n[网页腾讯翻译]\n%s"%text
        elif translate_type == "google" :
            content = "\n[谷歌翻译]\n%s"%text
        elif translate_type == "Bing" :
            content = "\n[Bing翻译]\n%s"%text
        elif translate_type == "baidu" :
            content = "\n[私人百度翻译]\n%s"%text
        elif translate_type == "tencent" :
            content = "\n[私人腾讯翻译]\n%s"%text
        elif translate_type == "caiyunPrivate" :
            content = "\n[私人翻译]\n%s"%text
        else:
            content = ""

        with open(".\\config\\翻译历史.txt", "a+", encoding="utf-8") as file:
            file.write(content)


    def getinform(self):

        url = "http://120.24.146.175:3000/DangoTranslate/Getinform"
        formdata = json.dumps({
            "version": "3.6"
        })
        try :
            res = requests.post(url, data=formdata).json()
            result = res.get("Result", "")
            if result != "" and result != "No" :
                for content in result.split("\\n") :
                    self.format.setTextOutline(QPen(QColor('#1E90FF'), 0.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    self.translateText.mergeCurrentCharFormat(self.format)
                    self.translateText.append(content)
                return 1
        except Exception :
            print_exc()
        return 0



if __name__ == '__main__':
    
    import sys
    screen_scale_rate = get_screen_rate()
    App = QApplication(sys.argv)
    Init = MainInterface(screen_scale_rate)
    Init.show()
    App.exit(App.exec_())