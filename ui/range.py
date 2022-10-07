from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re

import utils.thread
import ui.static.icon


DRAW_PATH = "./config/draw.jpg"


# 选择范围
class WScreenShot(QWidget) :

    def __init__(self, object, parent=None) :

        super(WScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.6)
        desktop_rect = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, desktop_rect.width()-1, desktop_rect.height()-1)
        self.setCursor(Qt.CrossCursor)
        self.black_mask = QBitmap(QSize(desktop_rect.width()-1, desktop_rect.height()-1))
        self.black_mask.fill(Qt.black)
        self.mask = self.black_mask.copy()
        self.is_drawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.object = object


    def paintEvent(self, event):

        try:
            if self.is_drawing:
                self.mask = self.black_mask.copy()
                pp = QPainter(self.mask)
                pen = QPen()
                pen.setStyle(Qt.NoPen)
                pp.setPen(pen)
                brush = QBrush(Qt.white)
                pp.setBrush(brush)
                pp.drawRect(QRect(self.start_point, self.end_point))
                self.setMask(QBitmap(self.mask))
        except Exception:
            pass


    def mousePressEvent(self, event) :

        try:
            if event.button() == Qt.LeftButton:
                self.start_point = event.pos()
                self.end_point = self.start_point
                self.is_drawing = True
        except Exception:
            pass


    def mouseMoveEvent(self, event) :

        try:
            if self.is_drawing:
                self.end_point = event.pos()
                self.update()
        except Exception:
            pass


    def getRange(self) :

        start = re.findall(r'(\d+), (\d+)', str(self.start_point))[0]
        end = re.findall(r'\d+, \d+', str(self.end_point))[0]
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

        self.object.yaml["range"]["X1"] = X1
        self.object.yaml["range"]["Y1"] = Y1
        self.object.yaml["range"]["X2"] = X2
        self.object.yaml["range"]["Y2"] = Y2

        # 显示范围框
        self.object.range_ui.setGeometry(X1, Y1, X2-X1, Y2-Y1)
        self.object.range_ui.label.setGeometry(0, 0, X2-X1, Y2-Y1)
        self.object.range_ui.show_sign = True
        self.object.range_ui.show()

        # 如果是自动模式下, 则解除暂停
        if self.object.translation_ui.translate_mode :
            self.object.translation_ui.stop_sign = False


    def mouseReleaseEvent(self, event):

        try:
            if event.button() == Qt.LeftButton:
                self.end_point = event.pos()
                self.getRange()
                self.close()
                self.object.translation_ui.checkOverlap()
                # 如果处于手动模式下则刷新一次翻译
                if not self.object.translation_ui.translate_mode :
                    utils.thread.createThread(self.object.translation_ui.startTranslater)
        except Exception :
            pass


# 范围框
class Range(QMainWindow) :

    def __init__(self, object):

        super(Range, self).__init__()

        self.object = object
        self.rate = object.yaml["screen_scale_rate"]
        self.font_type = "华康方圆体W7"
        self.color = "#1E90FF"
        self.font_size = 12
        self.show_sign = False
        self.object.show_range_ui_sign = False
        self.ui()


    def ui(self) :

        X1 = self.object.yaml["range"]["X1"]
        Y1 = self.object.yaml["range"]["Y1"]
        X2 = self.object.yaml["range"]["X2"]
        Y2 = self.object.yaml["range"]["Y2"]

        # 窗口大小
        self.setGeometry(X1, Y1, X2-X1, Y2-Y1)
        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, X2 - X1, Y2 - Y1)
        self.label.setStyleSheet("border-width:1;\
                                  border:2px dashed #1E90FF;\
                                  background-color:rgba(62, 62, 62, 0.01)")

        # 此Label用于当鼠标进入界面时给出颜色反应
        self.drag_label = QLabel(self)
        self.drag_label.setGeometry(0, 0, 4000, 2000)

        # 字体
        self.font = QFont()
        self.font.setFamily(self.font_type)
        self.font.setPointSize(self.font_size)

        # 显示翻译结果
        self.draw_label = QLabel(self)

        # 隐藏按钮
        self.hide_button = QPushButton(self)
        self.hide_button.setGeometry(QRect(int(X2-X1-40*self.rate), 0, int(40*self.rate), int(30*self.rate)))
        self.hide_button.setStyleSheet("background-color:rgba(62, 62, 62, 0.3);"
                                       "color: %s;"%self.color)
        self.hide_button.setFont(self.font)
        self.hide_button.setText("隐藏")
        self.hide_button.setCursor(ui.static.icon.SELECT_CURSOR)
        self.hide_button.clicked.connect(self.quit)
        self.hide_button.hide()

        # 右下角用于拉伸界面的控件
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)


    # 鼠标移动事件
    def mouseMoveEvent(self, e: QMouseEvent) :

        try :
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
        except Exception :
            pass

        # 判断是否和翻译框碰撞
        self.object.translation_ui.checkOverlap()


    # 鼠标按下事件
    def mousePressEvent(self, e: QMouseEvent) :

        try :
            if e.button() == Qt.LeftButton :
                self._isTracking = True
                self._startPos = QPoint(e.x(), e.y())
        except Exception :
            pass


    # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent) :

        try :
            if e.button() == Qt.LeftButton:
                self._isTracking = False
                self._startPos = None
                self._endPos = None
        except Exception :
            pass


    # 鼠标进入控件事件
    def enterEvent(self, QEvent) :

        rect = self.geometry()
        X1 = rect.left()
        X2 = rect.left() + rect.width()
        self.hide_button.setGeometry(QRect(int(X2-X1-40*self.rate), 0, int(40*self.rate), int(30*self.rate)))
        self.hide_button.show()
        self.drag_label.setStyleSheet("background-color:rgba(62, 62, 62, 0.1)")

        # 如果处于自动模式下则暂停
        if self.object.translation_ui.translate_mode :
            self.object.translation_ui.stop_sign = True


    # 鼠标离开控件事件
    def leaveEvent(self, QEvent):

        self.drag_label.setStyleSheet("background-color:none")
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.hide_button.hide()

        rect = self.geometry()
        X1 = rect.left()
        Y1 = rect.top()
        X2 = rect.left() + rect.width()
        Y2 = rect.top() + rect.height()

        self.object.yaml["range"]["X1"] = X1
        self.object.yaml["range"]["Y1"] = Y1
        self.object.yaml["range"]["X2"] = X2
        self.object.yaml["range"]["Y2"] = Y2

        # 如果是自动模式下, 则解除暂停
        if self.object.translation_ui.translate_mode :
            self.object.translation_ui.stop_sign = False


    # 将翻译结果显示在原图上
    def drawImage(self) :

        rect = self.geometry()
        self.draw_label.setGeometry(0, 0, rect.width(), rect.height())
        gif = QMovie(DRAW_PATH)
        self.draw_label.setMovie(gif)
        self.draw_label.setScaledContents(True)
        gif.start()
        self.object.range_ui.draw_label.show()
        self.show()


    # 接收隐藏窗体信号
    def hideUI(self, sign) :

        if sign :
            self.show()
        else :
            self.hide()


    # 隐藏/显示窗体信号
    def hideRangeUI(self) :

        if self.object.show_range_ui_sign :
            self.hide()
        else :
            self.show()


    # 窗口隐藏信号
    def hideEvent(self, e):

        self.object.show_range_ui_sign = False


    # 窗口显示信号
    def showEvent(self, e):

        self.object.show_range_ui_sign = True


    def quit(self) :

        self.show_sign = False
        self.close()