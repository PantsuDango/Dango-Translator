from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.register import Register

from utils import MessageBox
from traceback import format_exc

import qtawesome
import requests
import json
import re


# 登录界面
class Login(QWidget):

    def __init__(self, config, logger):

        super(Login, self).__init__()

        self.config = config
        self.logger = logger
        self.getInitConfig()

        self.ui()


    def ui(self):

        # 窗口尺寸
        self.resize(int(400*self.rate), int(566*self.rate))

        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 窗口图标
        icon = QIcon()
        icon.addPixmap(QPixmap("./config/icon/logo.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        # 鼠标样式, 光标长宽比1.133333
        pixmap = QPixmap("./config/icon/pixmap.png")
        pixmap = pixmap.scaled(int(30*self.rate),
                               int(34*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)

        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 设置字体
        self.setStyleSheet("font: 13pt %s;"%self.font)

        # 背景图片, 长宽比: 1.39
        self.background = QLabel(self)
        self.customSetGeometry(self.background, 0, 0, 400, 566)
        self.background.setStyleSheet("border-image: url(./config/background/login.png);")

        # 版本号
        self.pixivIDLabel = QLabel(self)
        self.customSetGeometry(self.pixivIDLabel, 15, 340, 200, 15)
        self.pixivIDLabel.setStyleSheet("color: %s;"
                                        "background: transparent;"
                                        "font: 10pt %s;"%(self.color, self.font))
        self.pixivIDLabel.setText("封面图 pixiv id: 80124193")

        # 矩形
        self.pixivIDLabel = QLabel(self)
        self.customSetGeometry(self.pixivIDLabel, 0, 355, 400, 211)
        self.pixivIDLabel.setStyleSheet("background-color: rgba(255, 255, 255, 0.7);"
                                        "border-width: 5px 5px 5px 5px;"
                                        "border:2px solid %s;"
                                        "border-radius:15px;"%self.color)

        # Logo
        self.logoButton = QPushButton(self)
        self.customSetGeometry(self.logoButton, 80, 365, 35, 35)
        self.logoButton.setStyleSheet("border-image: url(./config/icon/logo.ico);")
        self.logoButton.setCursor(QCursor(Qt.PointingHandCursor))

        # 标题
        self.titleLabel = QLabel(self)
        self.customSetGeometry(self.titleLabel, 130, 370, 250, 30)
        self.titleLabel.setText("团子翻译器")
        self.titleLabel.setStyleSheet("color: %s;"
                                      "background: transparent;"
                                      "font: 20pt %s;"
                                      "font-weight:bold;"%(self.color, self.font))

        # 最小化按钮
        self.minimizeButton = QPushButton(qtawesome.icon("fa.minus", color=self.color), "", self)
        self.customSetIconSize(self.minimizeButton, 20, 20)
        self.customSetGeometry(self.minimizeButton, 345, 360, 20, 20)
        self.minimizeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.minimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.minimizeButton.clicked.connect(self.showMinimized)

        # 退出按钮
        self.quitButton = QPushButton(qtawesome.icon("fa.times", color=self.color), "", self)
        self.customSetIconSize(self.quitButton, 20, 20)
        self.customSetGeometry(self.quitButton, 370, 360, 20, 20)
        self.quitButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.quitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.quitButton.clicked.connect(QCoreApplication.instance().quit)

        # 账号输入框
        self.userEdit = QTextEdit(self)
        self.customSetGeometry(self.userEdit, 40, 410, 315, 30)
        self.userEdit.setPlaceholderText("请输入账号:")
        self.userEdit.setText(self.username)
        self.userEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.userEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.userEdit.setStyleSheet("QTextEdit {""background: transparent;"
                                    "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                    "border-bottom: 2px solid %s;""}"
                                    "QTextEdit:focus {""border-bottom: 2px dashed %s;""}"
                                    %(self.color, self.color, self.color))

        # 密码输入框
        self.passwordEdit = QLineEdit(self)
        self.customSetGeometry(self.passwordEdit, 40, 455, 315, 30)
        self.passwordEdit.setPlaceholderText("请输入密码:")
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit.setText(self.password)
        self.passwordEdit.setStyleSheet("QLineEdit {""background: transparent;"
                                         "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                         "border-bottom: 2px solid %s;""}"
                                         "QLineEdit:focus {""border-bottom: 2px dashed %s;""}"
                                        %(self.color, self.color, self.color))

        # 是否显示密码
        self.eyeButton = QPushButton(qtawesome.icon("fa.eye-slash", color=self.color), "", self)
        self.customSetIconSize(self.eyeButton, 25, 25)
        self.customSetGeometry(self.eyeButton, 330, 455, 30, 30)
        self.eyeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.eyeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.eyeButton.installEventFilter(self)

        # 登录按钮
        self.loginButton = QPushButton(self)
        self.customSetGeometry(self.loginButton, 130, 495, 50, 35)
        self.loginButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.loginButton.setText("登录")
        self.loginButton.setStyleSheet('background: rgba(255, 255, 255, 0);'
                                       'color: %s;'
                                       'font: 15pt %s;'%(self.color, self.font))

        # 注册按钮
        self.registerButton = QPushButton(self)
        self.customSetGeometry(self.registerButton, 220, 495, 50, 35)
        self.registerButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.registerButton.clicked.connect(self.openRegister)
        self.registerButton.setText("注册")
        self.registerButton.setStyleSheet('background: rgba(255, 255, 255, 0);'
                                          'color: %s;'
                                          'font: 15pt %s;'%(self.color, self.font))

        # 忘记密码按钮
        self.registerButton = QPushButton(self)
        self.customSetGeometry(self.registerButton, 305, 490, 60, 15)
        self.registerButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.registerButton.clicked.connect(self.register)
        self.registerButton.setText("忘记密码")
        self.registerButton.setStyleSheet('background: rgba(255, 255, 255, 0);'
                                          'color: %s;'
                                          'font: 8pt %s;' % (self.color, self.font))

        # 版本号
        self.versionLabel = QLabel(self)
        self.customSetGeometry(self.versionLabel, 20, 540, 400, 15)
        self.versionLabel.setText("版本号: Ver 4.0    更新时间: 2021-11-01    By: 胖次团子")
        self.versionLabel.setStyleSheet('color: %s;'
                                        'background: transparent;'
                                        'font-weight:bold;'
                                        'font: 10pt %s;'%(self.color, self.font))


    # 初始化配置
    def getInitConfig(self) :

        # 界面颜色
        self.color = "#FF79BC"
        # 界面字体
        self.font = "华康方圆体W7"
        # 界面缩放比例
        self.rate = self.config["screenScaleRate"]
        # 登录历史用户名
        self.username = str(self.config.get("user", ""))
        # 登录历史密码
        self.password = str(self.config.get("password", ""))
        # 注册接口地址
        self.registerURL = "http://120.24.146.175:3000/DangoTranslate/Register"
        # 登录接口地址
        self.loginURL = "http://120.24.146.175:3000/DangoTranslate/Login"


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 根据分辨率定义图标位置尺寸
    def customSetIconSize(self, object, w, h) :

        object.setIconSize(QSize(int(w*self.rate),
                                 int(h*self.rate)))


    # 鼠标移动事件
    def mouseMoveEvent(self, e: QMouseEvent):

        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)


    # 鼠标按下事件
    def mousePressEvent(self, e: QMouseEvent):

        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())


    # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent):

        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


    # 鼠标移动到眼睛上时对密码的处理
    def eventFilter(self, object, event):

        if object == self.eyeButton :
            if event.type() == QEvent.Enter:
                self.eyeButton.setIcon(qtawesome.icon('fa.eye', color=self.color))
                self.passwordEdit.setEchoMode(QLineEdit.Normal)

            if event.type() == QEvent.Leave:
                self.eyeButton.setIcon(qtawesome.icon('fa.eye-slash', color=self.color))
                self.passwordEdit.setEchoMode(QLineEdit.Password)

            return QWidget.eventFilter(self, object, event)


    def openRegister(self) :

        self.Register = Register(self.config)
        self.Register.show()


    # 注册
    def register(self):

        # 检查用户名和密码是否合法
        user = self.userEdit.toPlainText()
        password = self.passwordEdit.text()

        if user == "" :
            MessageBox("注册失败", "用户名不能为空ヽ(`Д´)ﾉ     ")
            return
        if password == "" :
            MessageBox("注册失败", "密码不能为空ヽ(`Д´)ﾉ     ")
            return
        if re.findall("\s", user) :
            MessageBox("注册失败", "用户名含有不合法的字符ヽ(`Д´)ﾉ     ")
            return
        if re.findall("\s", password):
            MessageBox("注册失败", "密码含有不合法的字符ヽ(`Д´)ﾉ     ")
            return
        if len(user) < 6 or len(user) > 18 :
            MessageBox("注册失败", "用户名长度不合法ヽ(`Д´)ﾉ     \n需大于6位，小于18位")
            return
        if len(password) < 6 or len(password) > 18 :
            MessageBox("注册失败", "密码长度不合法ヽ(`Д´)ﾉ     \n需大于6位，小于18位")
            return

        # 请求服务器
        params = json.dumps({"User": user, "Password": password})
        proxies = {"http": None, "https": None}

        try:
            res = requests.post(self.registerURL, data=params, proxies=proxies, timeout=10)
            res.encoding = "utf-8"
            result = json.loads(res.text).get("Result", "")

            if result == "User already exists" :
                MessageBox("注册失败", "用户名已存在啦，再想一个吧(〃'▽'〃)     ")

            elif result == "OK" :
                MessageBox("注册成功", "注册成功啦，直接登录吧(〃'▽'〃)     ")

            else :
                self.logger.error(format_exc())
                MessageBox("注册失败", "啊咧，出现了出乎意料的情况\n请联系团子解决!!!∑(ﾟДﾟノ)ノ\n\n%s"%format_exc())

        except Exception :
            self.logger.error(format_exc())
            MessageBox("注册失败", "啊咧，出现了出乎意料的情况\n请联系团子解决!!!∑(ﾟДﾟノ)ノ\n\n%s"%format_exc())


    def login(self) :

        # 检查用户名和密码是否合法
        self.user = self.userEdit.toPlainText()
        self.password = self.passwordEdit.text()

        if self.user == "" :
            MessageBox("登录失败", "用户名不能为空ヽ(`Д´)ﾉ     ")
            return
        if self.password == "" :
            MessageBox("登录失败", "密码不能为空ヽ(`Д´)ﾉ     ")
            return

        # 请求服务器
        params = json.dumps({"User": self.user, "Password": self.password})
        proxies = {"http": None, "https": None}
        try:
            res = requests.post(self.loginURL, data=params, proxies=proxies, timeout=10)
            res.encoding = "utf-8"
            result = res.json().get("Result", "")

            if result == "User dose not exist" :
                MessageBox("登录失败", "用户名不存在，请先注册哦ヽ(`Д´)ﾉ     ")
                return

            elif result == "Password error" :
                MessageBox("登录失败", "密码输错啦ヽ(`Д´)ﾉ     ")
                return

            elif result == "User is black list" :
                MessageBox("登录失败", "你已经被团子纳入黑名单了ヽ(`Д´)ﾉ     ")
                return

            elif result == "OK" :
                return True

            else:
                self.logger.error(format_exc())
                MessageBox("登录失败", "啊咧，出现了出乎意料的情况\n请联系团子解决!!!∑(ﾟДﾟノ)ノ\n\n%s" % format_exc())
                return

        except Exception :
            self.logger.error(format_exc())
            MessageBox("登录失败", "啊咧，出现了出乎意料的情况\n请联系团子解决!!!∑(ﾟДﾟノ)ノ\n\n%s"%format_exc())
            return