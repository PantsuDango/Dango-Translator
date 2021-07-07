from traceback import print_exc
from playsound import playsound
from threading import Thread

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qtawesome
import requests
import json

from API import MessageBox


def start_music():

    def play():
        try:
            playsound('.\\config\\Dango.mp3')
        except Exception:
            print_exc()

    thread = Thread(target=play)
    thread.setDaemon(True)
    thread.start()


class Login(QWidget):

    def __init__(self, screen_scale_rate, data):

        self.rate = screen_scale_rate
        self.data = data
        if self.rate != 1 and self.rate != 1.25 and self.rate != 1.5 and self.rate != 1.75 :
            self.rate = 1
        super(Login, self).__init__()
        self.ui()


    def ui(self):

        # 窗口尺寸
        self.resize(400*self.rate, 611*self.rate)

        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("./config/图标.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 鼠标样式
        self.pixmap = QPixmap('.\\config\\光标.png')
        self.cursor = QCursor(self.pixmap, 0, 0)
        self.setCursor(self.cursor)

        # 设置字体
        self.setStyleSheet("font: 13pt \"华康方圆体W7\";")

        # 图片
        self.image_label = QLabel(self)
        self.image_label.setGeometry(QRect(0, 0, 400*self.rate, 611*self.rate)) # 长宽比: 1.527272727
        self.image_label.setStyleSheet("border-image: url(./config/登录.png);")

        # 版本号
        self.imageBy_label = QLabel(self)
        self.imageBy_label.setGeometry(QRect(15*self.rate, 385*self.rate, 200*self.rate, 15*self.rate))
        self.imageBy_label.setStyleSheet("color: #1E90FF;"
                                        "background: transparent;"
                                        "font: 10pt \"华康方圆体W7\";"
                                        )
        self.imageBy_label.setText("封面图 pixiv id: 90233998")

        # 矩形框
        self.rect_label = QLabel(self)
        self.rect_label.setGeometry(QRect(0, 400*self.rate, 400*self.rate, 211*self.rate))
        self.rect_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.7);"
                                      "border-width: 5px 5px 5px 5px;"
                                      "border:2px solid #1E90FF;"
                                      "border-radius:15px;")

        # Logo gif
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(QRect(90*self.rate, 400*self.rate, 211*self.rate, 211*self.rate))

        # Logo
        self.logo_Button = QPushButton(self)
        self.logo_Button.setGeometry(QRect(80*self.rate, 410*self.rate, 35*self.rate, 35*self.rate))
        self.logo_Button.setStyleSheet("border-image: url(./config/图标.ico);")
        self.logo_Button.setCursor(QCursor(Qt.PointingHandCursor))
        self.logo_Button.clicked.connect(start_music)

        self.gif = QMovie("./config/动图%s.gif"%int((self.rate*100)))
        self.logo_label.setMovie(self.gif)
        self.gif.start()

        # 标题 #1E90FF蓝 #FF6EB4粉
        self.title_label = QLabel(self)
        self.title_label.setGeometry(QRect(130*self.rate, 415*self.rate, 250*self.rate, 30*self.rate))
        self.title_label.setStyleSheet("color: #1E90FF;"
                                       "background: transparent;"
                                       "font: 20pt \"华康方圆体W7\";"
                                       "font-weight:bold;")
        self.title_label.setText("团子翻译器")

        # 最小化按钮
        self.MinimizeButton = QPushButton(qtawesome.icon("fa.minus", color="#1E90FF"), "", self)
        self.MinimizeButton.setIconSize(QSize(20, 20))
        self.MinimizeButton.setGeometry(QRect(345*self.rate, 405*self.rate, 20*self.rate, 20*self.rate))
        self.MinimizeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.MinimizeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.MinimizeButton.clicked.connect(self.showMinimized)

        # 退出按钮
        self.QuitButton = QPushButton(qtawesome.icon("fa.times", color="#1E90FF"), "", self)
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(QRect(370*self.rate, 405*self.rate, 20*self.rate, 20*self.rate))
        self.QuitButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.clicked.connect(self.close)

        # 账号输入框
        self.user_text = QTextEdit(self)
        self.user_text.setGeometry(QRect(40*self.rate, 455*self.rate, 315*self.rate, 30*self.rate))
        self.user_text.setStyleSheet("QTextEdit {""background: transparent;"
                                           "border-width:0; border-style:outset; color: #1E90FF;"
                                           "border-bottom: 2px solid #1E90FF;""}"
                                           "QTextEdit:focus {""border-bottom: 2px dashed #FF6EB4;""}")
        self.user_text.setPlaceholderText("请输入账号:")
        self.user_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.user_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        user = self.data.get("user", "")
        self.user_text.setPlainText(user)

        # 密码输入框
        self.password_text = QLineEdit(self)
        self.password_text.setGeometry(QRect(40*self.rate, 500*self.rate, 315*self.rate, 30*self.rate))
        self.password_text.setStyleSheet("QLineEdit {""background: transparent;"
                                     "border-width:0; border-style:outset; color: #1E90FF;"
                                     "border-bottom: 2px solid #1E90FF;""}"
                                     "QLineEdit:focus {""border-bottom: 2px dashed #FF6EB4;""}")
        self.password_text.setPlaceholderText("请输入密码:")
        self.password_text.setEchoMode(QLineEdit.Password)
        password = self.data.get("password", "")
        self.password_text.setText(password)

        # 是否显示密码
        self.eyeButton = QPushButton(qtawesome.icon("fa.eye-slash", color="#1E90FF"), "", self)
        self.eyeButton.setIconSize(QSize(25*self.rate, 25*self.rate))
        self.eyeButton.setGeometry(QRect(330*self.rate, 500*self.rate, 30*self.rate, 30*self.rate))
        self.eyeButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.eyeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.eyeButton.installEventFilter(self)

        # 登录按钮
        self.login_Button = QPushButton(self)
        self.login_Button.setGeometry(QRect(130*self.rate, 540*self.rate, 50*self.rate, 35*self.rate))
        self.login_Button.setStyleSheet("background: rgba(255, 255, 255, 0);"
                                        "color: #1E90FF;"
                                        "font: 15pt \"华康方圆体W7\";")
        self.login_Button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_Button.setText("登录")

        # 注册按钮
        self.register_Button = QPushButton(self)
        self.register_Button.setGeometry(QRect(220*self.rate, 540*self.rate, 50*self.rate, 35*self.rate))
        self.register_Button.setStyleSheet("background: rgba(255, 255, 255, 0);"
                                           "color: #1E90FF;"
                                           "font: 15pt \"华康方圆体W7\";")
        self.register_Button.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_Button.clicked.connect(self.register)
        self.register_Button.setText("注册")

        # 版本号
        self.version_label = QLabel(self)
        self.version_label.setGeometry(QRect(20*self.rate, 585*self.rate, 300*self.rate, 15*self.rate))
        self.version_label.setStyleSheet("color: #1E90FF;"
                                         "background: transparent;"
                                         "font: 10pt \"微软雅黑\";"
                                         "font-weight:bold;")
        self.version_label.setText("版本号: Ver 3.6    更新时间: 2021-07-02")

        # 版本号
        self.author_label = QLabel(self)
        self.author_label.setGeometry(QRect(310*self.rate, 585*self.rate, 200*self.rate, 15*self.rate))
        self.author_label.setStyleSheet("color: #1E90FF;"
                                         "background: transparent;"
                                         "font: 10pt \"华康方圆体W7\";"
                                         )
        self.author_label.setText("By 胖次团子")


    # 鼠标移动到眼睛上时对密码的处理
    def eventFilter(self, object, event):

        if object == self.eyeButton :
            if event.type() == QEvent.Enter :
                self.eyeButton.setIcon(qtawesome.icon('fa.eye', color='#1E90FF'))
                self.password_text.setEchoMode(QLineEdit.Normal)
            if event.type() == QEvent.Leave :
                self.eyeButton.setIcon(qtawesome.icon('fa.eye-slash', color='#1E90FF'))
                self.password_text.setEchoMode(QLineEdit.Password)
            return QWidget.eventFilter(self, object, event)


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


    def register(self):
        # 检查用户名和密码是否合法
        user = self.user_text.toPlainText()
        password = self.password_text.text()
        if user == "":
            MessageBox('用户名不合法', '用户名不能为空！   ')
            return
        if password == "":
            MessageBox('密码不合法', '密码不能为空！   ')
            return
        if ' ' in user or '\n' in user or '\t' in user:
            MessageBox('用户名不合法', '用户名含有不合法的字符！   ')
            return
        if ' ' in password or '\n' in password or '\t' in password:
            MessageBox('密码不合法', '密码含有不合法的字符！   ')
            return

        url = "http://120.24.146.175:3000/DangoTranslate/Register"
        formdata = json.dumps({
            "User": user,
            "Password": password
        })
        try:
            res = requests.post(url, data=formdata, timeout=5).json()
            result = res.get("Result", "")
            if result == "User already exists":
                MessageBox('注册失败', '用户名已存在！   ')
            elif result == "OK":
                MessageBox('注册成功', '可以登录啦~   ')
            else :
                MessageBox('登录失败', '请联系团子解决   ')
        except Exception as err:
            MessageBox('注册失败', '原因: %s   '%err)


if __name__ == '__main__':
    import sys
    App = QApplication(sys.argv)
    Init = Login()
    Init.show()
    App.exit(App.exec_())