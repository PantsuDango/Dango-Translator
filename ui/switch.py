from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils.port import detectPort
from utils.message import MessageBox
import utils.check_chrome


# 只有翻译界面用
class SwitchButton(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=30):

        super(QWidget, self).__init__(parent)

        self.checked = sign
        self.bgColorOff = QColor(255, 255, 255)

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#ffcef9"))
        self.bgColorOn.setColorAt(1, QColor("#ff7cbc"))


        self.sliderColorOff = QColor('#dedede')
        self.sliderColorOn = QColor('#fefefe')

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "手动"
        self.textOn = "自动"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        if self.checked :
            self.startX = startX

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event):

        self.checked = not self.checked
        # 发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())

        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()


# 只有本地OCR用
class OfflineSwitch(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=45, object=None):

        super(QWidget, self).__init__(parent)

        self.object = object
        self.checked = sign
        self.bgColorOff = QColor("#f0f0f0")

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#83AAF9"))
        self.bgColorOn.setColorAt(1, QColor("#5B8FF9"))


        self.sliderColorOff = QColor("#fefefe")
        self.sliderColorOn = QColor("#fefefe")

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "关闭"
        self.textOn = "使用"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        if self.checked :
            self.startX = startX

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event) :

        # 通过检查端口占用校验本地OCR是否运行成功
        sign = detectPort(self.object.yaml["port"])
        if not self.checked and not sign :
            MessageBox("本地OCR使用失败", "请先点击 运行 按钮, 并保证其运行正常, 再打开此开关      \n"
                                         "若启动时间较长或运行失败, 可通过交流群联系客服\n"
                                         "使用期间可以缩小黑窗, 但不可以关闭它")
            return

        if not self.checked and self.object.settin_ui.text_direction_use :
            MessageBox("竖向翻译开启失败", "检测到已开启[竖向翻译], [本地OCR]不支持[竖向翻译]\n"
                                         "请在[功能设定]里将[文字方向]开关改为横向, 再开启[本地OCR]      \n"
                                         "若想使用[竖向翻译], 也可改用其他OCR")
            return

        self.checked = not self.checked
        # 发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()


class SwitchOCR(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=45):

        super(QWidget, self).__init__(parent)

        self.checked = sign
        self.bgColorOff = QColor("#f0f0f0")

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#83AAF9"))
        self.bgColorOn.setColorAt(1, QColor("#5B8FF9"))


        self.sliderColorOff = QColor("#fefefe")
        self.sliderColorOn = QColor("#fefefe")

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "关闭"
        self.textOn = "开启"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        if self.checked :
            self.startX = startX

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event) :

        self.checked = not self.checked
        # 发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()


class PublictranslationSwitch(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=45):

        super(QWidget, self).__init__(parent)

        self.checked = sign
        self.bgColorOff = QColor("#f0f0f0")

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#83AAF9"))
        self.bgColorOn.setColorAt(1, QColor("#5B8FF9"))


        self.sliderColorOff = QColor("#fefefe")
        self.sliderColorOn = QColor("#fefefe")

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "关闭"
        self.textOn = "开启"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        if self.checked :
            self.startX = startX

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event) :

        try :
            if not utils.check_chrome.checkChrome() :
                self.timer.stop()
                utils.check_chrome.openChromeDownloadMessageBox()
                return
        except Exception :
            pass

        self.checked = not self.checked
        # 发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()

class BaiduSwitchOCR(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=45, object=None):

        super(QWidget, self).__init__(parent)

        self.object = object
        self.checked = sign
        self.bgColorOff = QColor("#f0f0f0")

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#83AAF9"))
        self.bgColorOn.setColorAt(1, QColor("#5B8FF9"))


        self.sliderColorOff = QColor("#fefefe")
        self.sliderColorOn = QColor("#fefefe")

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "关闭"
        self.textOn = "开启"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        if self.checked :
            self.startX = startX

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event) :

        if not self.checked and self.object.settin_ui.draw_image_use:
            MessageBox("贴字翻译开启失败", "检测到已开启[贴字翻译], [百度OCR]不支持[贴字翻译]\n"
                                         "请在[功能设定]里将[贴字翻译]开关改为关闭, 再开启[百度OCR]      \n"
                                         "若想使用[贴字翻译], 也可改用其他OCR")
            return

        self.checked = not self.checked
        # 发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()


class DrawSwitchOCR(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=45, object=None):

        super(QWidget, self).__init__(parent)

        self.object = object
        self.checked = sign
        self.bgColorOff = QColor("#f0f0f0")

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#83AAF9"))
        self.bgColorOn.setColorAt(1, QColor("#5B8FF9"))


        self.sliderColorOff = QColor("#fefefe")
        self.sliderColorOn = QColor("#fefefe")

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "关闭"
        self.textOn = "开启"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        if self.checked :
            self.startX = startX

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event) :

        if not self.checked and self.object.settin_ui.baidu_ocr_use:
            MessageBox("贴字翻译开启失败", "检测到当前正在使用[百度OCR], [百度OCR]不支持[贴字翻译]      \n"
                                         "请在[OCR设定]中选择其他OCR源再开启[贴字翻译]")
            return

        self.checked = not self.checked
        # 发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()


# 字体样式用
class SwitchFontType(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=45):

        super(QWidget, self).__init__(parent)


        self.checked = sign
        self.bgColorOff = QColor("#f0f0f0")

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#83AAF9"))
        self.bgColorOn.setColorAt(1, QColor("#5B8FF9"))


        self.sliderColorOff = QColor("#fefefe")
        self.sliderColorOn = QColor("#fefefe")

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "描边"
        self.textOn = "实心"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        if self.checked :
            self.startX = startX

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event) :

        self.checked = not self.checked
        # 发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()


class ShowSwitch(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=45):

        super(QWidget, self).__init__(parent)


        self.checked = sign
        self.bgColorOff = QColor("#f0f0f0")

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#83AAF9"))
        self.bgColorOn.setColorAt(1, QColor("#5B8FF9"))


        self.sliderColorOff = QColor("#fefefe")
        self.sliderColorOn = QColor("#fefefe")

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "屏蔽"
        self.textOn = "显示"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        if self.checked:
            self.startX = startX

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event) :

        self.checked = not self.checked
        # 射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()


class SwitchDirection(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=45, object=None):

        super(QWidget, self).__init__(parent)

        self.object = object
        self.checked = sign
        self.bgColorOff = QColor("#f0f0f0")

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#83AAF9"))
        self.bgColorOn.setColorAt(1, QColor("#5B8FF9"))


        self.sliderColorOff = QColor("#fefefe")
        self.sliderColorOn = QColor("#fefefe")

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "横向"
        self.textOn = "竖向"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        if self.checked :
            self.startX = startX

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event) :

        if not self.checked and self.object.settin_ui.offline_ocr_use :
            MessageBox("竖向翻译开启失败", "检测到当前正在使用[本地OCR], [本地OCR]不支持竖向翻译      \n"
                                         "请在[OCR设定]中选择其他OCR源再开启[竖向翻译]")
            return

        self.checked = not self.checked
        # 发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()



class SwitchBranchLine(QWidget) :

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None, sign=False, startX=45):

        super(QWidget, self).__init__(parent)


        self.checked = sign
        self.bgColorOff = QColor("#f0f0f0")

        # 渐变色背景
        self.bgColorOn =  QLinearGradient(0, 0, self.width(), self.height())
        self.bgColorOn.setColorAt(0, QColor("#83AAF9"))
        self.bgColorOn.setColorAt(1, QColor("#5B8FF9"))


        self.sliderColorOff = QColor("#fefefe")
        self.sliderColorOn = QColor("#fefefe")

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "拼接"
        self.textOn = "换行"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        if self.checked :
            self.startX = startX

        # 初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("华康方圆体W7", 9))


    def updateValue(self):

        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self, event) :

        self.checked = not self.checked
        # 发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        # 状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)


    def paintEvent(self, evt):

        # 绘制准备工作, 启用反锯齿
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        self.drawBg(evt, painter)
        # 绘制滑块
        self.drawSlider(evt, painter)
        # 绘制文字
        self.drawText(evt, painter)

        painter.end()


    def drawText(self, event, painter):

        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(self.space, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2 - self.space * 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):

        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        # 半径为高度的一半
        radius = rect.height() / 2
        # 圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()


    def drawSlider(self, event, painter):

        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(sliderRect)

        painter.restore()