from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import qtawesome
import re

import utils.message
import utils.http
import utils.config
import utils.lock


LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"
BACKGROUND_PATH = "./config/background/login.png"
PIXMAP2_PATH = "./config/icon/pixmap2.png"
EDIT_PATH = "./config/icon/edit.png"


# 登录界面
class Login(QWidget) :

    def __init__(self, object) :

        super(Login, self).__init__()
        self.object = object
        self.logger = object.logger
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
        icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        # 鼠标样式, 光标长宽比1.133333
        pixmap = QPixmap(PIXMAP_PATH)
        pixmap = pixmap.scaled(int(20*self.rate),
                               int(20*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 鼠标选中状态图标
        select_pixmap = QPixmap(PIXMAP2_PATH)
        select_pixmap = select_pixmap.scaled(int(20*self.rate),
                                             int(20*self.rate),
                                             Qt.KeepAspectRatio,
                                             Qt.SmoothTransformation)
        select_pixmap = QCursor(select_pixmap, 0, 0)

        # 鼠标编辑状态图标
        edit_pixmap = QPixmap(EDIT_PATH)
        edit_pixmap = edit_pixmap.scaled(int(20*self.rate),
                                         int(25*self.rate),
                                         Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
        edit_pixmap = QCursor(edit_pixmap, 0, 0)


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

        # 背景图片, 长宽比: 1.39
        label = QLabel(self)
        self.customSetGeometry(label, 0, 0, 400, 566)
        label.setStyleSheet("border-image: url(%s);"%BACKGROUND_PATH)

        # 版本号
        label = QLabel(self)
        self.customSetGeometry(label, 15, 340, 200, 15)
        label.setStyleSheet("color: %s;"
                            "background: transparent;"
                            "font: 10pt %s;" % (self.color, self.font_type))
        label.setText("封面图 pixiv id: %s"%self.object.yaml["dict_info"]["cover_pixiv_id"])

        # 矩形框
        label = QLabel(self)
        self.customSetGeometry(label, 0, 355, 400, 211)
        label.setStyleSheet("background-color: rgba(255, 255, 255, 0.7);"
                            "border-width: 5px 5px 5px 5px;"
                            "border:2px solid %s;"
                            "border-radius:15px;"%self.color)

        # Logo
        label = QLabel(self)
        self.customSetGeometry(label, 80, 365, 35, 35)
        label.setStyleSheet("border-image: url(%s);"%LOGO_PATH)

        # 标题
        label = QLabel(self)
        self.customSetGeometry(label, 130, 370, 250, 30)
        label.setText("团子翻译器")
        label.setStyleSheet("color: %s;"
                            "background: transparent;"
                            "font: 20pt %s;"
                            "font-weight:bold;" % (self.color, self.font_type))

        # 最小化按钮
        button = QPushButton(qtawesome.icon("fa.minus", color=self.color), "", self)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 345, 360, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.setCursor(select_pixmap)
        button.clicked.connect(self.showMinimized)

        # 退出按钮
        button = QPushButton(qtawesome.icon("fa.times", color=self.color), "", self)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 370, 360, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.setCursor(select_pixmap)
        button.clicked.connect(self.quit)

        # 账号输入框
        self.user_text = QLineEdit(self)
        self.customSetGeometry(self.user_text, 40, 410, 315, 30)
        self.user_text.setPlaceholderText("请输入账号:")
        self.user_text.setText(self.user)
        self.user_text.setCursor(edit_pixmap)

        # 密码输入框
        self.password_text = QLineEdit(self)
        self.customSetGeometry(self.password_text, 40, 455, 315, 30)
        self.password_text.setPlaceholderText("请输入密码:")
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setText(self.password)
        self.password_text.setCursor(edit_pixmap)

        # 是否显示密码
        self.eye_button = QPushButton(qtawesome.icon("fa.eye-slash", color=self.color), "", self)
        self.customSetIconSize(self.eye_button, 25, 25)
        self.customSetGeometry(self.eye_button, 330, 455, 30, 30)
        self.eye_button.setStyleSheet("background: transparent;")
        self.eye_button.setCursor(select_pixmap)
        self.eye_button.clicked.connect(self.clickEyeButton)

        # 登录按钮
        self.login_button = QPushButton(self)
        self.customSetGeometry(self.login_button, 130, 495, 50, 35)
        self.login_button.setCursor(select_pixmap)
        self.login_button.setText("登录")
        self.login_button.setStyleSheet("background: transparent;"
                                        "color: %s;"
                                        "font: 15pt %s;"
                                        % (self.color, self.font_type))

        # 注册按钮
        self.register_button = QPushButton(self)
        self.customSetGeometry(self.register_button, 220, 495, 50, 35)
        self.register_button.setCursor(select_pixmap)
        self.register_button.setText("注册")
        self.register_button.setStyleSheet("background: transparent;"
                                           "color: %s;"
                                           "font: 15pt %s;"
                                           % (self.color, self.font_type))

        # 忘记密码按钮
        self.forget_password_button = QPushButton(self)
        self.customSetGeometry(self.forget_password_button, 305, 490, 60, 15)
        self.forget_password_button.setCursor(select_pixmap)
        self.forget_password_button.setText("忘记密码")
        self.forget_password_button.setStyleSheet("background: transparent;"
                                                  "color: %s;"
                                                  "font: 8pt %s;"
                                                  % (self.color, self.font_type))

        # 版本号
        label = QLabel(self)
        self.customSetGeometry(label, 20, 540, 380, 15)
        label.setText("版本号: %s  更新时间: 2022-02-24  By: 胖次团子"%self.object.yaml["version"])
        label.setStyleSheet("color: %s;"
                            "background: transparent;"
                            "font-weight:bold;"
                            "font: 10pt %s;"
                            %(self.color, self.font_type))

        self.setTabOrder(self.user_text, self.password_text)


    # 初始化配置
    def getInitConfig(self) :

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 13
        # 界面颜色
        self.color = "#FF79BC"
        # 用户名
        self.user = str(self.object.yaml["user"])
        # 密码
        self.password = str(self.object.yaml["password"])


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
    def mouseMoveEvent(self, e: QMouseEvent) :

        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)


    # 鼠标按下事件
    def mousePressEvent(self, e: QMouseEvent) :

        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())


    # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent) :

        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


    # 点击眼睛
    def clickEyeButton(self) :

        if self.password_text.echoMode() == QLineEdit.Password :
            self.eye_button.setIcon(qtawesome.icon('fa.eye', color=self.color))
            self.password_text.setEchoMode(QLineEdit.Normal)
        else :
            self.eye_button.setIcon(qtawesome.icon('fa.eye-slash', color=self.color))
            self.password_text.setEchoMode(QLineEdit.Password)


    # 检查登录参数
    def checkLogin(self) :

        self.user = self.user_text.text()
        self.password = self.password_text.text()

        # 检查用户名是否合法
        if not self.user or re.findall("\s", self.user):
            utils.message.MessageBox("登录失败",
                                     "用户名为空或含有不合法字符!     ")
            return False

        # 检查密码是否合法
        if not self.password or re.findall("\s", self.password):
            utils.message.MessageBox("登录失败",
                                     "密码为空或含有不合法字符!     ")
            return False

        return True


    # 登录请求
    def postLogin(self) :

        # 请求服务器
        url = self.object.yaml["dict_info"]["dango_login"]
        body = {
            "User": self.user,
            "Password": self.password
        }
        res = utils.http.post(url=url, body=body, logger=self.logger)
        result = res.get("Result", "")

        if result == "User dose not exist":
            utils.message.MessageBox("登录失败",
                                     "用户名不存在, 请先注册!     ")
            return False

        elif result == "Password error":
            utils.message.MessageBox("登录失败",
                                     "密码输错啦!     ")
            return False

        elif result == "User is black list":
            utils.message.MessageBox("登录失败",
                                     "已被纳入黑名单!     ")
            return False

        elif result == "OK":
            # 保存配置
            self.object.yaml["user"] = self.user
            self.object.yaml["password"] = self.password
            utils.config.saveConfig(self.object.yaml, self.logger)
            return True

        else:
            utils.message.MessageBox("登录失败",
                                     "出现了出乎意料的情况\n请联系团子解决!     ")
            return False


    # 登录
    def login(self) :

        # 检查登录参数
        if not self.checkLogin() :
            return False

        # 登录请求
        if not self.postLogin() :
            return False

        return True


    # 热键检测
    def keyPressEvent(self, event) :

        # 如果按下回车键
        if event.key() == 16777220 :
            self.object.login()


    # 退出程序
    def quit(self) :

        # 退出
        QCoreApplication.instance().quit()