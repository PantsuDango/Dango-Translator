# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import qtawesome
import time
import re
import random

import utils.email
import utils.message
import utils.http
import utils.thread


LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"
BG_IMAGE_PATH = "./config/background/register.gif"


# 注册界面
class Register(QWidget) :

    def __init__(self, object) :

        super(Register, self).__init__()
        self.object = object
        self.logger = object.logger
        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

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
        font = QFont()
        font.setFamily(self.font_type)
        font.setPointSize(self.font_size)
        self.setFont(font)

        # 界面样式
        self.setStyleSheet("QLineEdit { background: transparent;"
                                       "border-width:0; "
                                       "border-style:outset; "
                                       "color: %s; "
                                       "font-weight: bold;"
                                       "border-bottom: 2px solid %s; }"
                           "QTextEdit:focus { border-bottom: 2px dashed %s; }"
                           %(self.color, self.color, self.color))

        # 背景图
        label = QLabel(self)
        label.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        gif = QMovie(BG_IMAGE_PATH)
        label.setMovie(gif)
        label.setScaledContents(True)
        gif.start()

        # 此Label用于雾化工具栏1的背景图
        label = QLabel(self)
        label.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 账号输入框
        self.user_text = QLineEdit(self)
        self.customSetGeometry(self.user_text, 30, 10, 300, 30)
        self.user_text.setPlaceholderText("请输入账号:")

        # 密码输入框
        self.password_text = QLineEdit(self)
        self.customSetGeometry(self.password_text, 30, 50, 300, 30)
        self.password_text.setEchoMode(QLineEdit.Password)

        # 是否显示密码
        self.eye_button = QPushButton(qtawesome.icon("fa.eye-slash", color=self.color), "", self)
        self.customSetIconSize(self.eye_button, 25, 25)
        self.customSetGeometry(self.eye_button, 305, 50, 30, 30)
        self.eye_button.setStyleSheet("background: transparent;")
        self.eye_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.eye_button.installEventFilter(self)

        # 邮箱输入框
        self.email_text = QLineEdit(self)
        self.customSetGeometry(self.email_text, 30, 90, 300, 30)
        self.email_text.setPlaceholderText("请输入绑定的邮箱:")

        # 验证码输入框
        self.code_key_text = QLineEdit(self)
        self.customSetGeometry(self.code_key_text, 30, 130, 300, 30)
        self.code_key_text.setPlaceholderText("请输入邮箱验证码:")

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
        self.register_button.setText("确定")
        self.register_button.setStyleSheet("background: rgba(255, 255, 255, 0.5);"
                                           "color: %s;"
                                           "font: 15pt %s;"
                                           % (self.color, self.font_type))

        # 确定注册按钮
        self.modify_password_button = QPushButton(self)
        self.customSetGeometry(self.modify_password_button, 140, 175, 80, 35)
        self.modify_password_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.modify_password_button.setText("确定")
        self.modify_password_button.setStyleSheet("background: rgba(255, 255, 255, 0.5);"
                                           "color: %s;"
                                           "font: 15pt %s;"
                                                  % (self.color, self.font_type))
        self.modify_password_button.hide()

        self.setTabOrder(self.user_text, self.password_text)
        self.setTabOrder(self.password_text, self.email_text)
        self.setTabOrder(self.email_text, self.code_key_text)


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面尺寸
        self.window_width = int(360*self.rate)
        self.window_height = int(231*self.rate)
        # 输入框颜色
        self.color = "#FF79BC"
        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 10
        # 验证码
        self.code_key = ""
        # 当前页面类型
        self.window_type = ""


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

        if object == self.eye_button :
            if event.type() == QEvent.Enter :
                self.eye_button.setIcon(qtawesome.icon('fa.eye', color=self.color))
                self.password_text.setEchoMode(QLineEdit.Normal)

            if event.type() == QEvent.Leave :
                self.eye_button.setIcon(qtawesome.icon('fa.eye-slash', color=self.color))
                self.password_text.setEchoMode(QLineEdit.Password)

            return QWidget.eventFilter(self, object, event)


    # 登录界面点击注册
    def clickRegister(self):

        self.object.login_ui.hide()
        self.window_type = "register"
        self.setWindowTitle("注册账号")
        self.password_text.setPlaceholderText("请输入密码:")
        self.register_button.clicked.connect(self.register)
        self.show()
        self.modify_password_button.hide()
        self.register_button.show()


    # # 登录界面点击修改密码
    def clickForgetPassword(self):

        self.object.login_ui.hide()
        self.window_type = "modify_password"
        self.setWindowTitle("修改密码")
        self.password_text.clear()
        self.password_text.setPlaceholderText("请输入新密码:")
        self.modify_password_button.clicked.connect(self.modifyPassword)
        self.show()
        self.register_button.hide()
        self.modify_password_button.show()


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


    # 显示验证码邮件发送状态
    def showEmailMessage(self, sign, error) :

        if sign :
            utils.message.MessageBox("发送成功",
                                     "验证码邮件已成功发送, 请注意查收~     ")
        else :
            self.signal.emit(True)
            utils.message.MessageBox("发送失败",
                                     "发送验证码邮件失败了!\n%s     "%error)


    # 点击发送验证码按钮
    def sendEmail(self) :

        user = self.user_text.text()
        email = self.email_text.text()

        if not user or re.findall("\s", user):
            utils.message.MessageBox("发送失败",
                                     "用户名为空或含有不合法字符!     ")
            return

        if not self.checkEmailValidity(email) :
            utils.message.MessageBox("发送失败",
                                     "邮箱地址不合法!     ")
            return

        # 冻结验证码按钮
        utils.thread.createThread(self.buttonStatusThread)

        # 发送邮件
        self.code_key = str(random.randint(1001, 9999))
        url = self.object.yaml["dict_info"]["send_key_email"]
        thread = utils.email.SendEmail(url, user, email, self.code_key, self.logger)
        thread.signal.connect(self.showEmailMessage)
        thread.start()
        thread.exec()


    # 注册
    def register(self) :

        user = self.user_text.text()
        password = self.password_text.text()
        email = self.email_text.text()
        code_key = self.code_key_text.text()

        # 校验注册参数合法性
        if not user or re.findall("\s", user) :
            utils.message.MessageBox("注册失败",
                                     "用户名为空或含有不合法字符!     ")
            return
        if not password or re.findall("\s", password) :
            utils.message.MessageBox("注册失败",
                                     "密码为空或含有不合法字符!     ")
            return
        if not self.checkEmailValidity(email) :
            utils.message.MessageBox("注册失败",
                                     "邮箱地址不合法!     ")
            return
        if not code_key or re.findall("\s", code_key) :
            utils.message.MessageBox("修改失败",
                                     "邮箱验证码为空或含有不合法字符!     ")
            return
        if code_key != self.code_key :
            utils.message.MessageBox("注册失败",
                                     "邮箱验证码错误!     ")
            return

        url = self.object.yaml["dict_info"]["dango_register"]
        body = {
            "User": user,
            "Password": password,
            "Email": email
        }

        # 请求服务器
        res = utils.http.post(url, body, self.logger)
        result = res.get("Result", "")

        if result == "User already exists" :
            utils.message.MessageBox("注册失败",
                                     "用户名已存在啦，再想一个吧!     ")

        elif result == "OK" :
            utils.message.MessageBox("注册成功",
                                     "注册成功啦，直接登录吧~     ")
            self.code_key = ""
            self.object.login_ui.user_text.setText(user)
            self.object.login_ui.password_text.setText(password)
            self.close()
            self.object.login_ui.show()

        else :
            utils.message.MessageBox("注册失败",
                                     "出现了出乎意料的情况\n请联系团子解决!     ")


    # 修改密码
    def modifyPassword(self) :

        user = self.user_text.text()
        password = self.password_text.text()
        email = self.email_text.text()
        code_key = self.code_key_text.text()

        # 校验注册参数合法性
        if not user or re.findall("\s", user) :
            utils.message.MessageBox("修改失败",
                                     "用户名为空或含有不合法字符!     ")
            return

        if not password or re.findall("\s", password) :
            utils.message.MessageBox("修改失败",
                                     "密码为空或含有不合法字符!     ")
            return

        if not self.checkEmailValidity(email) :
            utils.message.MessageBox("修改失败",
                                     "邮箱地址不合法!     ")
            return

        if not code_key or re.findall("\s", code_key) :
            utils.message.MessageBox("修改失败",
                                     "邮箱验证码为空或含有不合法字符!     ")
            return

        if code_key != self.code_key :
            utils.message.MessageBox("修改失败",
                                     "邮箱验证码错误!     ")
            return

        url = self.object.yaml["dict_info"]["dango_modify_password"]
        body = {
            "User": user,
            "Password": password,
            "Email": email
        }

        # 请求服务器
        res = utils.http.post(url, body, self.logger)
        result = res.get("Status", "")
        message = res.get("Message", "")

        if result == "Success" :
            utils.message.MessageBox("修改成功",
                                     "修改密码成功啦，直接登录吧~     ")
            self.code_key = ""
            self.object.login_ui.user_text.setText(user)
            self.object.login_ui.password_text.setText(password)
            self.close()
            self.object.login_ui.show()

        else :
            utils.message.MessageBox("修改失败",
                                     "%s     "%message)


    # 检查邮箱线程
    def createBindEmailThread(self) :

        thread = utils.email.BindEmail(self.object)
        thread.signal.connect(self.showBindEmailMessage)
        thread.start()
        thread.exec()


    # 检查邮箱显示消息窗口
    def showBindEmailMessage(self, sign) :

        utils.message.checkEmailMessageBox("邮箱绑定检查",
                                           "检测到您未绑定邮箱, 请先完成邮箱绑定\n"
                                           "邮箱绑定有以下好处:\n"
                                           "1. 忘记密码时用于修改密码;\n"
                                           "2. 购买在线OCR时接收购买凭证;     ",
                                           self.object)


    # 绑定邮箱
    def bindEmail(self) :

        #self.object.translation_ui.hide()
        self.window_type = "bind_email"
        self.setWindowTitle("绑定邮箱")
        self.user_text.setText(self.object.yaml["user"])
        self.password_text.setText(self.object.yaml["password"])
        self.user_text.setEnabled(False)
        self.password_text.setEnabled(False)
        self.email_text.clear()
        self.code_key_text.clear()
        self.show()


    # 热键检测
    def keyPressEvent(self, event) :

        # 如果按下回车键
        if event.key() == 16777220 :
            self.register()


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.close()
        if self.window_type != "bind_email" :
            self.object.login_ui.show()
        else :
            pass
            #self.object.translation_ui.show()