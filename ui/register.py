# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"
BG_IMAGE_PATH = "./config/background/register.gif"


class Register(QWidget) :

    def __init__(self, config) :

        super(Register, self).__init__()

        self.config = config
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
        self.password_text = QTextEdit(self)
        self.customSetGeometry(self.password_text, 30, 50, 300, 30)
        self.password_text.setPlaceholderText("请输入密码:")
        self.password_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.password_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.password_text.setStyleSheet("QTextEdit {""background: transparent;"
                                      "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                      "border-bottom: 2px solid %s;""}"
                                      "QTextEdit:focus {""border-bottom: 2px dashed %s;""}"
                                      % (self.color, self.color, self.color))

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
        self.key_code_text = QTextEdit(self)
        self.customSetGeometry(self.key_code_text, 30, 130, 300, 30)
        self.key_code_text.setPlaceholderText("请输入邮箱验证码:")
        self.key_code_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.key_code_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.key_code_text.setStyleSheet("QTextEdit {""background: transparent;"
                                         "border-width:0; border-style:outset; color: %s; font-weight: bold;"
                                         "border-bottom: 2px solid %s;""}"
                                         "QTextEdit:focus {""border-bottom: 2px dashed %s;""}"
                                         %(self.color, self.color, self.color))

        # 获取验证码按钮
        self.send_email_button = QPushButton(self)
        self.customSetGeometry(self.send_email_button, 250, 125, 80, 25)
        self.send_email_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.send_email_button.setText("获取验证码")
        self.send_email_button.setStyleSheet("background: rgba(255, 255, 255, 0.5); color: %s"%(self.color))

        # 确定注册按钮
        self.register_button = QPushButton(self)
        self.customSetGeometry(self.register_button, 140, 175, 80, 35)
        self.register_button.setCursor(QCursor(Qt.PointingHandCursor))
        #self.register_button.clicked.connect(self.openRegister)
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


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))