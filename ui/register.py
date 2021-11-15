# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils import MessageBox, createSendEmailThread

import qtawesome
import threading
import time
import re
import random


LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"
BG_IMAGE_PATH = "./config/background/register.gif"


class Register(QWidget) :

    def __init__(self, config, logger) :

        super(Register, self).__init__()

        self.config = config
        self.logger = logger
        self.getInitConfig()

        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("注册")

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 鼠标样式
        pixmap = QPixmap(PIXMAP_PATH)
        pixmap = pixmap.scaled(int(30*self.rate),
                               int(34*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 设置字体
        self.setStyleSheet("font: 10pt '华康方圆体W7';")

        # 背景图
        image_label = QLabel(self)
        image_label.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        gif = QMovie(BG_IMAGE_PATH)
        image_label.setMovie(gif)
        image_label.setScaledContents(True)
        gif.start()

        # 此Label用于雾化工具栏1的背景图
        label = QLabel(self)
        label.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 账号输入框
        self.user_text = QTextEdit(self)
        self.customSetGeometry(self.user_text, 30, 10, 300, 30)
        self.user_text.setPlaceholderText("请输入账号:")
        self.user_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.user_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.user_text.setStyleSheet("QTextEdit {""background: transparent;"
                                     "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                     "border-bottom: 2px solid %s;""}"
                                     "QTextEdit:focus {""border-bottom: 2px dashed %s;""}"
                                     %(self.color, self.color, self.color))

        # 密码输入框
        self.password_text = QLineEdit(self)
        self.customSetGeometry(self.password_text, 30, 50, 300, 30)
        self.password_text.setPlaceholderText("请输入密码:")
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setStyleSheet("QLineEdit {""background: transparent;"
                                        "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                        "border-bottom: 2px solid %s;""}"
                                        "QLineEdit:focus {""border-bottom: 2px dashed %s;""}"
                                         % (self.color, self.color, self.color))

        # 是否显示密码
        self.eye_button = QPushButton(qtawesome.icon("fa.eye-slash", color=self.color), "", self)
        self.customSetIconSize(self.eye_button, 25, 25)
        self.customSetGeometry(self.eye_button, 305, 50, 30, 30)
        self.eye_button.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.eye_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.eye_button.installEventFilter(self)

        # 邮箱输入框
        self.email_text = QTextEdit(self)
        self.customSetGeometry(self.email_text, 30, 90, 300, 30)
        self.email_text.setPlaceholderText("请输入绑定的邮箱:")
        self.email_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.email_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.email_text.setStyleSheet("QTextEdit {""background: transparent;"
                                      "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                      "border-bottom: 2px solid %s;""}"
                                      "QTextEdit:focus {""border-bottom: 2px dashed %s;""}"
                                      %(self.color, self.color, self.color))

        # 验证码输入框
        self.code_key_text = QTextEdit(self)
        self.customSetGeometry(self.code_key_text, 30, 130, 300, 30)
        self.code_key_text.setPlaceholderText("请输入邮箱验证码:")
        self.code_key_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.code_key_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.code_key_text.setStyleSheet("QTextEdit {""background: transparent;"
                                         "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                         "border-bottom: 2px solid %s;""}"
                                         "QTextEdit:focus {""border-bottom: 2px dashed %s;""}"
                                         % (self.color, self.color, self.color))

        # 获取验证码按钮
        self.send_email_button = QPushButton(self)
        self.customSetGeometry(self.send_email_button, 205, 125, 125, 25)
        self.send_email_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.send_email_button.setText("获取验证码")
        self.send_email_button.setStyleSheet("background: rgba(255, 255, 255, 0.5); color: %s"%(self.color))
        self.send_email_button.clicked.connect(self.sendEmail)

        # 确定注册按钮
        self.register_button = QPushButton(self)
        self.customSetGeometry(self.register_button, 140, 175, 80, 35)
        self.register_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_button.clicked.connect(self.register)
        self.register_button.setText("确定")
        self.register_button.setStyleSheet('background: rgba(255, 255, 255, 0.5);'
                                           'color: %s;'
                                           'font: 15pt %s;'%(self.color, self.font))


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.config["screenScaleRate"]
        # 界面尺寸
        self.window_width = int(360 * self.rate)
        self.window_height = int(231 * self.rate)
        # 输入框颜色
        self.color = "#FF79BC"
        # 界面字体
        self.font = "华康方圆体W7"
        # 验证码
        self.code_key = ""


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 根据分辨率定义图标位置尺寸
    def customSetIconSize(self, object, w, h) :

        object.setIconSize(QSize(int(w * self.rate),
                                 int(h * self.rate)))


    # 鼠标移动到眼睛上时对密码的处理
    def eventFilter(self, object, event) :

        if object == self.eye_button:
            if event.type() == QEvent.Enter:
                self.eye_button.setIcon(qtawesome.icon('fa.eye', color=self.color))
                self.password_text.setEchoMode(QLineEdit.Normal)

            if event.type() == QEvent.Leave:
                self.eye_button.setIcon(qtawesome.icon('fa.eye-slash', color=self.color))
                self.password_text.setEchoMode(QLineEdit.Password)

            return QWidget.eventFilter(self, object, event)


    # 获取验证码按钮状态控制线程
    def buttonStatusThread(self) :

        self.send_email_button.setEnabled(False)
        for count in range(60, 0, -1) :
            self.send_email_button.setText("%d秒后可再次获取"%count)
            time.sleep(1)
        self.send_email_button.setText("获取验证码")
        self.send_email_button.setEnabled(True)


    # 验证邮箱地址有效性
    def checkEmailValidity(self, email) :

        regex = r'''^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'''
        return re.match(regex, email)


    # 点击发送验证码按钮
    def sendEmail(self) :

        user = self.user_text.toPlainText()
        email = self.email_text.toPlainText()

        if not user or re.findall("\s", user):
            MessageBox("注册失败", "用户名为空或含有不合法字符!     ")
            return
        if not self.checkEmailValidity(email) :
            MessageBox("发送失败", "邮箱地址不合法!     ")
            return

        thread = threading.Thread(target=self.buttonStatusThread)
        thread.setDaemon(True)
        thread.start()

        # 发送邮件
        self.code_key = str(random.randint(1001, 9999))
        createSendEmailThread(self.config, user, email, self.code_key, self.logger)


    # 注册
    def register(self) :

        user = self.user_text.toPlainText()
        password = self.password_text.text()
        email = self.email_text.toPlainText()
        code_key = self.code_key_text.toPlainText()

        if not user or re.findall("\s", user) :
            MessageBox("注册失败", "用户名为空或含有不合法字符!     ")
            return
        if not password or re.findall("\s", password) :
            MessageBox("注册失败", "密码为空或含有不合法字符!     ")
            return
        if not self.checkEmailValidity(email) :
            MessageBox("注册失败", "邮箱地址不合法!     ")
            return
        if code_key != self.code_key :
            MessageBox("注册失败", "邮箱验证码错误!     ")
            return

        MessageBox("注册成功", "注册成功啦，直接登录吧(〃'▽'〃)     ")