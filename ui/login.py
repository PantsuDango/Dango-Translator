from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils import MessageBox
from traceback import format_exc

import qtawesome
import requests
import json
from utils import http
import threading


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
        label = QLabel(self)
        self.customSetGeometry(label, 80, 365, 35, 35)
        label.setStyleSheet("border-image: url(./config/icon/logo.ico);")

        # 标题
        label = QLabel(self)
        self.customSetGeometry(label, 130, 370, 250, 30)
        label.setText("团子翻译器")
        label.setStyleSheet("color: %s;"
                            "background: transparent;"
                            "font: 20pt %s;"
                            "font-weight:bold;"%(self.color, self.font))

        # 最小化按钮
        self.minimize_button = QPushButton(qtawesome.icon("fa.minus", color=self.color), "", self)
        self.customSetIconSize(self.minimize_button, 20, 20)
        self.customSetGeometry(self.minimize_button, 345, 360, 20, 20)
        self.minimize_button.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.minimize_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.minimize_button.clicked.connect(self.showMinimized)

        # 退出按钮
        self.quit_button = QPushButton(qtawesome.icon("fa.times", color=self.color), "", self)
        self.customSetIconSize(self.quit_button, 20, 20)
        self.customSetGeometry(self.quit_button, 370, 360, 20, 20)
        self.quit_button.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.quit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.quit_button.clicked.connect(QCoreApplication.instance().quit)

        # 账号输入框
        self.user_text = QTextEdit(self)
        self.customSetGeometry(self.user_text, 40, 410, 315, 30)
        self.user_text.setPlaceholderText("请输入账号:")
        self.user_text.setText(self.username)
        self.user_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.user_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.user_text.setStyleSheet("QTextEdit {""background: transparent;"
                                    "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                    "border-bottom: 2px solid %s;""}"
                                    "QTextEdit:focus {""border-bottom: 2px dashed %s;""}"
                                     % (self.color, self.color, self.color))

        # 密码输入框
        self.password_text = QLineEdit(self)
        self.customSetGeometry(self.password_text, 40, 455, 315, 30)
        self.password_text.setPlaceholderText("请输入密码:")
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setText(self.password)
        self.password_text.setStyleSheet("QLineEdit {""background: transparent;"
                                         "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                         "border-bottom: 2px solid %s;""}"
                                         "QLineEdit:focus {""border-bottom: 2px dashed %s;""}"
                                         % (self.color, self.color, self.color))

        # 是否显示密码
        self.eye_button = QPushButton(qtawesome.icon("fa.eye-slash", color=self.color), "", self)
        self.customSetIconSize(self.eye_button, 25, 25)
        self.customSetGeometry(self.eye_button, 330, 455, 30, 30)
        self.eye_button.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.eye_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.eye_button.installEventFilter(self)

        # 登录按钮
        self.login_button = QPushButton(self)
        self.customSetGeometry(self.login_button, 130, 495, 50, 35)
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_button.setText("登录")
        self.login_button.setStyleSheet('background: rgba(255, 255, 255, 0);'
                                       'color: %s;'
                                       'font: 15pt %s;' % (self.color, self.font))

        # 注册按钮
        self.register_button = QPushButton(self)
        self.customSetGeometry(self.register_button, 220, 495, 50, 35)
        self.register_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_button.setText("注册")
        self.register_button.setStyleSheet('background: rgba(255, 255, 255, 0);'
                                          'color: %s;'
                                          'font: 15pt %s;' % (self.color, self.font))

        # 忘记密码按钮
        self.forget_password_button = QPushButton(self)
        self.customSetGeometry(self.forget_password_button, 305, 490, 60, 15)
        self.forget_password_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.forget_password_button.setText("忘记密码")
        self.forget_password_button.setStyleSheet('background: rgba(255, 255, 255, 0);'
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

        if object == self.eye_button :
            if event.type() == QEvent.Enter:
                self.eye_button.setIcon(qtawesome.icon('fa.eye', color=self.color))
                self.password_text.setEchoMode(QLineEdit.Normal)

            if event.type() == QEvent.Leave:
                self.eye_button.setIcon(qtawesome.icon('fa.eye-slash', color=self.color))
                self.password_text.setEchoMode(QLineEdit.Password)

            return QWidget.eventFilter(self, object, event)


    # 登录
    def login(self) :

        # 检查用户名和密码是否合法
        self.user = self.user_text.toPlainText()
        self.password = self.password_text.text()

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