from traceback import print_exc
from playsound import playsound
from threading import Thread

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qtawesome

from login import start_music


def start_music():

    def play():
        try:
            playsound('.\\config\\Dango.mp3')
        except Exception:
            print_exc()

    thread = Thread(target=play)
    thread.setDaemon(True)
    thread.start()


class DangoUI(QWidget):

    def __init__(self):

        super(DangoUI, self).__init__()
        self.ui()


    def ui(self):

        # 获取显示器分辨率大小
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        # 窗口尺寸
        self.resize(150, 150)
        self.move(self.width-160, self.height-170)

        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("./config/图标.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 鼠标样式
        self.pixmap = QPixmap('.\\config\\光标.png')
        self.cursor = QCursor(self.pixmap, 0, 0)
        self.setCursor(self.cursor)

        # Logo gif
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(QRect(0, 0, 150, 150))
        self.logo_label.setStyleSheet("background-color:rgba(62, 62, 62, 0.01);")

        self.gif = QMovie("./config/动图2.gif")
        self.logo_label.setMovie(self.gif)
        self.gif.start()

        # 退出按钮
        self.QuitButton = QPushButton(qtawesome.icon("fa.times", color="#FF6EB4"), "", self)
        self.QuitButton.setIconSize(QSize(20, 20))
        self.QuitButton.setGeometry(QRect(130, 0, 20, 20))
        self.QuitButton.setStyleSheet("background-color:rgba(62, 62, 62, 0);")
        self.QuitButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QuitButton.clicked.connect(self.close)
        self.QuitButton.hide()



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
                start_music()
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


    # 鼠标进入控件事件
    def enterEvent(self, QEvent):

        try:
            self.QuitButton.show()
        except Exception:
            print_exc()


    # 鼠标离开控件事件
    def leaveEvent(self, QEvent):

        try:
            self.QuitButton.hide()
        except Exception:
            print_exc()



if __name__ == '__main__':
    import sys
    App = QApplication(sys.argv)
    Init = DangoUI()
    Init.show()
    App.exit(App.exec_())