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
import ui.static.icon


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
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)

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
        self.user_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 密码输入框
        self.password_text = QLineEdit(self)
        self.customSetGeometry(self.password_text, 30, 50, 300, 30)
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 是否显示密码
        self.eye_button = QPushButton(qtawesome.icon("fa.eye-slash", color=self.color), "", self)
        self.customSetIconSize(self.eye_button, 25, 25)
        self.customSetGeometry(self.eye_button, 305, 50, 30, 30)
        self.eye_button.setStyleSheet("background: transparent;")
        self.eye_button.setCursor(ui.static.icon.SELECT_CURSOR)
        self.eye_button.clicked.connect(self.clickEyeButton)

        # 邮箱输入框
        self.email_text = QLineEdit(self)
        self.customSetGeometry(self.email_text, 30, 90, 300, 30)
        self.email_text.setPlaceholderText("请输入绑定的邮箱:")
        self.email_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 验证码输入框
        self.code_key_text = QLineEdit(self)
        self.customSetGeometry(self.code_key_text, 30, 130, 300, 30)
        self.code_key_text.setPlaceholderText("请输入邮箱验证码:")
        self.code_key_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 获取验证码按钮
        self.send_email_button = QPushButton(self)
        self.customSetGeometry(self.send_email_button, 205, 125, 125, 25)
        self.send_email_button.setCursor(ui.static.icon.SELECT_CURSOR)
        self.send_email_button.setText("获取验证码")
        self.send_email_button.setStyleSheet("background: rgba(255, 255, 255, 0.5); color: %s"%(self.color))
        self.send_email_button.clicked.connect(self.sendEmail)

        # 确定注册按钮
        self.sure_button = QPushButton(self)
        self.customSetGeometry(self.sure_button, 140, 175, 80, 35)
        self.sure_button.setCursor(ui.static.icon.SELECT_CURSOR)
        self.sure_button.setText("确定")
        self.sure_button.setStyleSheet("background: rgba(255, 255, 255, 0.5);"
                                           "color: %s;"
                                           "font: 15pt %s;"
                                       % (self.color, self.font_type))

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


    # 点击眼睛
    def clickEyeButton(self):

        if self.password_text.echoMode() == QLineEdit.Password:
            self.eye_button.setIcon(qtawesome.icon('fa.eye', color=self.color))
            self.password_text.setEchoMode(QLineEdit.Normal)
        else:
            self.eye_button.setIcon(qtawesome.icon('fa.eye-slash', color=self.color))
            self.password_text.setEchoMode(QLineEdit.Password)


    # 登录界面点击注册
    def clickRegister(self):

        self.window_type = "register"
        self.setWindowTitle("注册账号")
        self.password_text.setPlaceholderText("请输入密码:")

        self.user_text.clear()
        self.user_text.setEnabled(True)
        self.password_text.clear()
        self.password_text.setEnabled(True)
        self.email_text.clear()
        self.email_text.setEnabled(True)
        self.code_key_text.clear()
        self.code_key_text.setEnabled(True)
        self.code_key = ""

        self.buttonUnbind(self.sure_button)
        self.sure_button.clicked.connect(self.register)

        self.object.login_ui.hide()
        self.show()


    # 登录界面点击修改密码
    def clickForgetPassword(self):

        user = self.object.login_ui.user_text.text()
        email = utils.email.bindEmail(self.object, user)
        if not email :
            utils.message.MessageBox("修改失败",
                                     "用户未绑定邮箱, 请先完成绑定再修改密码     ")
            return

        self.window_type = "modify_password"
        self.setWindowTitle("修改密码")
        self.user_text.setText(user)
        self.user_text.setEnabled(False)
        self.password_text.clear()
        self.password_text.setPlaceholderText("请输入新密码:")
        self.email_text.setText(email)
        self.email_text.setEnabled(False)
        self.code_key_text.clear()
        self.code_key_text.setEnabled(True)
        self.code_key = ""

        self.buttonUnbind(self.sure_button)
        self.sure_button.clicked.connect(self.modifyPassword)

        self.object.login_ui.hide()
        self.show()

    # 绑定邮箱窗口
    def clickBindEmail(self) :

        self.window_type = "bind_email"
        self.setWindowTitle("绑定邮箱")

        self.user_text.setText(self.object.yaml["user"])
        self.user_text.setEnabled(False)
        self.password_text.setText(self.object.yaml["password"])
        self.password_text.setEnabled(False)
        self.email_text.clear()
        self.email_text.setEnabled(True)
        self.code_key_text.clear()
        self.code_key_text.setEnabled(True)
        self.code_key = ""

        self.buttonUnbind(self.sure_button)
        self.sure_button.clicked.connect(self.bindEmail)

        self.object.translation_ui.hide()
        self.show()


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
            self.super_code = 99999
            utils.message.MessageBox("发送失败",
                                     "发送验证码邮件失败了!\n%s     \n请直接联系团子解决"%error)


    # 点击发送验证码按钮
    def sendEmail(self) :

        user = self.user_text.text()
        email = self.email_text.text().strip()
        self.email_text.setText(email)

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
        url = self.object.yaml["dict_info"]["dango_send_email"]
        thread = utils.email.SendEmail(url, user, email, self.code_key, self.logger)
        thread.signal.connect(self.showEmailMessage)
        thread.start()
        thread.exec()


    # 注册
    def register(self) :

        user = self.user_text.text().strip()
        self.user_text.setText(user)
        password = self.password_text.text().strip()
        self.password_text.setText(password)
        email = self.email_text.text().strip()
        self.email_text.setText(email)
        code_key = self.code_key_text.text().strip()
        self.code_key_text.setText(code_key)

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

        if code_key != "99999" :
            if  code_key != self.code_key :
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
        if not res:
            url = "https://trans.dango.cloud/DangoTranslate/Register"
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
        email = self.email_text.text().strip()
        self.email_text.setText(email)
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

        if code_key != "99999":
            if code_key != self.code_key:
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
        if not res:
            url = "https://trans.dango.cloud/DangoTranslate/ModifyPassword"
            res = utils.http.post(url, body, self.logger)
        result = res.get("Status", "")
        message = res.get("Error", "")

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


    # 显示检查邮箱失败信息
    def showBindEmailMessage(self) :

        utils.message.checkEmailMessageBox("邮箱绑定检查",
                                           "检测到您未绑定邮箱, 请先完成邮箱绑定     \n"
                                           "邮箱绑定有以下好处:\n"
                                           "1. 忘记密码时用于修改密码;\n"
                                           "2. 购买在线OCR时接收购买凭证;",
                                           self.object)


    # 按键信号解绑
    def buttonUnbind(self, button) :

        try :
            button.clicked.disconnect()
        except Exception :
            pass


    # 绑定邮箱确定键
    def bindEmail(self) :

        email = self.email_text.text().strip()
        self.email_text.setText(email)
        code_key = self.code_key_text.text()

        if not self.checkEmailValidity(email) :
            utils.message.MessageBox("绑定失败",
                                     "邮箱地址不合法!     ")
            return

        if not code_key or re.findall("\s", code_key) :
            utils.message.MessageBox("绑定失败",
                                     "邮箱验证码为空或含有不合法字符!     ")
            return

        if code_key != "99999":
            if code_key != self.code_key:
                utils.message.MessageBox("绑定失败",
                                         "邮箱验证码错误!     ")
                return

        url = self.object.yaml["dict_info"]["dango_modify_email"]
        body = {
            "User": self.object.yaml["user"],
            "Email": email
        }

        # 请求服务器
        res = utils.http.post(url, body, self.logger)
        if not res:
            url = "https://trans.dango.cloud/DangoTranslate/ModifyEmail"
            res = utils.http.post(url, body, self.logger)
        result = res.get("Status", "")
        message = res.get("Error", "")
        if result == "Success" :
            utils.message.MessageBox("绑定成功",
                                     "你已经成功绑定邮箱啦~     ")
        else :
            utils.message.MessageBox("绑定失败",
                                     "%s!     "%message)
        self.close()
        self.object.translation_ui.show()


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
            self.object.translation_ui.show()