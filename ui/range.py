from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import re
import utils


# 选择范围
class WScreenShot(QWidget):

    def __init__(self, Init, chooseRange, parent=None):

        super(WScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.6)
        desktopRect = QDesktopWidget().screenGeometry()
        self.setGeometry(desktopRect)
        self.setCursor(Qt.CrossCursor)
        self.blackMask = QBitmap(desktopRect.size())
        self.blackMask.fill(Qt.black)
        self.mask = self.blackMask.copy()
        self.isDrawing = False
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.Init = Init
        self.chooseRange = chooseRange


    def paintEvent(self, event):

        try:
            if self.isDrawing:
                self.mask = self.blackMask.copy()
                pp = QPainter(self.mask)
                pen = QPen()
                pen.setStyle(Qt.NoPen)
                pp.setPen(pen)
                brush = QBrush(Qt.white)
                pp.setBrush(brush)
                pp.drawRect(QRect(self.startPoint, self.endPoint))
                self.setMask(QBitmap(self.mask))
        except Exception:
            pass


    def mousePressEvent(self, event) :

        try:
            if event.button() == Qt.LeftButton:
                self.startPoint = event.pos()
                self.endPoint = self.startPoint
                self.isDrawing = True
        except Exception:
            pass


    def mouseMoveEvent(self, event) :

        try:
            if self.isDrawing:
                self.endPoint = event.pos()
                self.update()
        except Exception:
            pass


    def getRange(self) :

        start = re.findall(r'(\d+), (\d+)', str(self.startPoint))[0]
        end = re.findall(r'\d+, \d+', str(self.endPoint))[0]
        end = end.split(', ')

        X1 = int(start[0])
        Y1 = int(start[1])
        X2 = int(end[0])
        Y2 = int(end[1])

        if X1 > X2:
            tmp = X1
            X1 = X2
            X2 = tmp

        if Y1 > Y2:
            tmp = Y1
            Y1 = Y2
            Y2 = tmp

        self.Init.config["range"]["X1"] = X1
        self.Init.config["range"]["Y1"] = Y1
        self.Init.config["range"]["X2"] = X2
        self.Init.config["range"]["Y2"] = Y2

        # 显示范围框
        self.chooseRange.setGeometry(X1, Y1, X2 - X1, Y2 - Y1)
        self.chooseRange.Label.setGeometry(0, 0, X2 - X1, Y2 - Y1)
        self.chooseRange.show()

        # 如果是自动模式下, 则解除暂停
        if self.Init.translateMode :
            self.Init.stop_sign = False


    def mouseReleaseEvent(self, event):

        try:
            if event.button() == Qt.LeftButton:
                self.endPoint = event.pos()
                self.getRange()

                self.close()
                # 如果处于手动模式下则刷新一次翻译
                if not self.Init.translateMode :
                    self.Init.startTranslater()
        except Exception :
            pass


# 范围框
class Range(QMainWindow):

    def __init__(self, X1, Y1, X2, Y2, ScreenScaleRate, window):

        super(Range, self).__init__()

        self.rate = ScreenScaleRate
        self.window = window
        self.setGeometry(X1, Y1, X2-X1, Y2-Y1)

        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 鼠标样式
        pixmap = QPixmap("./config/icon/pixmap.png")
        pixmap = pixmap.scaled(int(30*self.rate),
                               int(34*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        self.Label = QLabel(self)
        self.Label.setObjectName("dragLabel")
        self.Label.setGeometry(0, 0, X2-X1, Y2-Y1)
        self.Label.setStyleSheet("border-width:1;\
                                  border:2px dashed #1E90FF;\
                                  background-color:rgba(62, 62, 62, 0.01)")

        # 此Label用于当鼠标进入界面时给出颜色反应
        self.dragLabel = QLabel(self)
        self.dragLabel.setObjectName("dragLabel")
        self.dragLabel.setGeometry(0, 0, 4000, 2000)

        self.Font = QFont()
        self.Font.setFamily("华康方圆体W7")
        self.Font.setPointSize(12)

        # 隐藏按钮
        self.Button = QPushButton(self)
        self.Button.setGeometry(QRect(int(X2-X1-40*self.rate),
                                      0,
                                      int(40*self.rate),
                                      int(30*self.rate)))
        self.Button.setStyleSheet("background-color:rgba(62, 62, 62, 0.3);"
                                  "color:#1E90FF")
        self.Button.setFont(self.Font)
        self.Button.setText("隐藏")
        self.Button.setCursor(QCursor(Qt.PointingHandCursor))
        self.Button.clicked.connect(self.close)
        self.Button.hide()

        # 右下角用于拉伸界面的控件
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)


    # 鼠标移动事件
    def mouseMoveEvent(self, e: QMouseEvent):
        try :
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except Exception :
            pass


    # 鼠标按下事件
    def mousePressEvent(self, e: QMouseEvent):
        try :
            if e.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(e.x(), e.y())
        except Exception :
            pass


    # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent):
        try :
            if e.button() == Qt.LeftButton:
                self._isTracking = False
                self._startPos = None
                self._endPos = None
        except Exception :
            pass


    # 鼠标进入控件事件
    def enterEvent(self, QEvent):

        rect = self.geometry()
        X1 = rect.left()
        X2 = rect.left() + rect.width()
        self.Button.setGeometry(QRect(int(X2-X1-40*self.rate),
                                      0,
                                      int(40*self.rate),
                                      int(30*self.rate)))
        self.Button.show()
        self.dragLabel.setStyleSheet("background-color:rgba(62, 62, 62, 0.1)")


    # 鼠标离开控件事件
    def leaveEvent(self, QEvent):

        self.dragLabel.setStyleSheet("background-color:none")
        self.Label.setGeometry(0, 0, self.width(), self.height())
        self.Button.hide()

        rect = self.geometry()
        X1 = rect.left()
        Y1 = rect.top()
        X2 = rect.left() + rect.width()
        Y2 = rect.top() + rect.height()

        self.window.config["range"]["X1"] = X1
        self.window.config["range"]["Y1"] = Y1
        self.window.config["range"]["X2"] = X2
        self.window.config["range"]["Y2"] = Y2