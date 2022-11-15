from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re

import utils.thread
import ui.static.icon
import ui.switch
import utils.message


DRAW_PATH = "./config/draw.jpg"


# 选择范围
class WScreenShot(QWidget) :

    def __init__(self, object, parent=None) :

        super(WScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet("background-color:black;")
        self.setWindowOpacity(0.6)

        desktop_rect = QDesktopWidget().screenGeometry()
        desktop_widget = QDesktopWidget()
        screen_count = desktop_widget.screenCount()
        max_width, max_height = 0, 0
        for i in range(screen_count):
            temp_screen = desktop_widget.screenGeometry(i)
            max_width += temp_screen.width()
            if temp_screen.height() > max_height :
                max_height = temp_screen.height()
        desktop_rect = QRect(0, 0, max_width, max_height)

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
        self.label.setGeometry(0, 0, X2-X1, Y2-Y1)
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


# 多范围参数页面
class MultiRange(QWidget):

    def __init__(self, object):

        super(MultiRange, self).__init__()
        self.object = object

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 9
        # 所使用的颜色
        self.color_1 = "#595959"  # 灰色
        self.color_2 = "#5B8FF9"  # 蓝色
        # 界面尺寸
        self.window_width = int(250*self.rate)
        self.window_height = int(320*self.rate)
        # 范围状态开关
        self.switch_1_use = self.object.config["switch1Use"]
        self.switch_2_use = self.object.config["switch2Use"]
        self.switch_3_use = self.object.config["switch3Use"]
        self.switch_4_use = self.object.config["switch4Use"]
        # 切换范围快捷键开关
        self.choice_range_hotkey_use = object.config["choiceRangeHotKey"]

        self.ui()


    def ui(self):

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        # 窗口标题
        self.setWindowTitle("多识别范围设置")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("QLabel { font: %spt '华康方圆体W7'; color: %s;}"
                           "QPushButton { background: %s;"
                                         "border-radius: %spx;"
                                         "color: rgb(255, 255, 255); "
                                         "font: %spt '华康方圆体W7';}"
                           "QPushButton:hover { background-color: #83AAF9; }"
                           "QPushButton:pressed { background-color: #4480F9;"
                                                "padding-left: 3px;"
                                                "padding-top: 3px; }"
                           %(self.font_size, self.color_2, self.color_2, 6.66*self.rate, self.font_size))

        # 背景, 长宽比1.424
        label = QLabel(self)
        label.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        label.setStyleSheet("background: rgb(255, 255, 255);")

        # 范围一
        self.label_1 = QLabel(self)
        self.customSetGeometry(self.label_1, 15, 10, self.window_width, 20)
        self.label_1.setText("区域一 (X1:{} Y1:{} X2:{} Y2:{})".format(
            self.object.yaml["range1"]["X1"],
            self.object.yaml["range1"]["Y1"],
            self.object.yaml["range1"]["X2"],
            self.object.yaml["range1"]["Y2"],
        ))

        self.switch_1 = ui.switch.SwitchOCR(self, sign=self.switch_1_use, startX=(60-20)*self.rate)
        self.customSetGeometry(self.switch_1, 15, 35, 60, 20)
        self.switch_1.checkedChanged.connect(self.changeRangeSwitch1)
        self.switch_1.setCursor(ui.static.icon.SELECT_CURSOR)

        self.show_button_1 = QPushButton(self)
        self.customSetGeometry(self.show_button_1, 90, 35, 60, 20)
        self.show_button_1.setText("查看范围")

        self.choice_button_1 = QPushButton(self)
        self.customSetGeometry(self.choice_button_1, 165, 35, 60, 20)
        self.choice_button_1.setText("框选范围")

        # 范围二
        self.label_2 = QLabel(self)
        self.customSetGeometry(self.label_2, 15, 70, self.window_width, 20)
        self.label_2.setText("区域二 (X1:{} Y1:{} X2:{} Y2:{})".format(
            self.object.yaml["range2"]["X1"],
            self.object.yaml["range2"]["Y1"],
            self.object.yaml["range2"]["X2"],
            self.object.yaml["range2"]["Y2"],
        ))

        self.switch_2 = ui.switch.SwitchOCR(self, sign=self.switch_2_use, startX=(60-20)*self.rate)
        self.customSetGeometry(self.switch_2, 15, 95, 60, 20)
        self.switch_2.checkedChanged.connect(self.changeRangeSwitch2)
        self.switch_2.setCursor(ui.static.icon.SELECT_CURSOR)

        self.show_button_2 = QPushButton(self)
        self.customSetGeometry(self.show_button_2, 90, 95, 60, 20)
        self.show_button_2.setText("查看范围")

        self.choice_button_2 = QPushButton(self)
        self.customSetGeometry(self.choice_button_2, 165, 95, 60, 20)
        self.choice_button_2.setText("框选范围")

        # 范围三
        self.label_3 = QLabel(self)
        self.customSetGeometry(self.label_3, 15, 130, self.window_width, 20)
        self.label_3.setText("区域三 (X1:{} Y1:{} X2:{} Y2:{})".format(
            self.object.yaml["range3"]["X1"],
            self.object.yaml["range3"]["Y1"],
            self.object.yaml["range3"]["X2"],
            self.object.yaml["range3"]["Y2"],
        ))

        self.switch_3 = ui.switch.SwitchOCR(self, sign=self.switch_3_use, startX=(60-20)*self.rate)
        self.customSetGeometry(self.switch_3, 15, 155, 60, 20)
        self.switch_3.checkedChanged.connect(self.changeRangeSwitch3)
        self.switch_3.setCursor(ui.static.icon.SELECT_CURSOR)

        self.show_button_3 = QPushButton(self)
        self.customSetGeometry(self.show_button_3, 90, 155, 60, 20)
        self.show_button_3.setText("查看范围")

        self.choice_button_3 = QPushButton(self)
        self.customSetGeometry(self.choice_button_3, 165, 155, 60, 20)
        self.choice_button_3.setText("框选范围")

        # 范围四
        self.label_4 = QLabel(self)
        self.customSetGeometry(self.label_4, 15, 190, self.window_width, 20)
        self.label_4.setText("区域四 (X1:{} Y1:{} X2:{} Y2:{})".format(
            self.object.yaml["range4"]["X1"],
            self.object.yaml["range4"]["Y1"],
            self.object.yaml["range4"]["X2"],
            self.object.yaml["range4"]["Y2"],
        ))

        self.switch_4 = ui.switch.SwitchOCR(self, sign=self.switch_4_use, startX=(60-20)*self.rate)
        self.customSetGeometry(self.switch_4, 15, 215, 60, 20)
        self.switch_4.checkedChanged.connect(self.changeRangeSwitch4)
        self.switch_4.setCursor(ui.static.icon.SELECT_CURSOR)

        self.show_button_4 = QPushButton(self)
        self.customSetGeometry(self.show_button_4, 90, 215, 60, 20)
        self.show_button_4.setText("查看范围")

        self.choice_button_4 = QPushButton(self)
        self.customSetGeometry(self.choice_button_4, 165, 215, 60, 20)
        self.choice_button_4.setText("框选范围")

        # 切换范围快捷键开关
        label = QLabel(self)
        self.customSetGeometry(label, 15, 250, self.window_width, 20)
        label.setText("切换范围1-4区域的快捷键")

        self.choice_range_hotkey_switch = ui.switch.SwitchOCR(self, sign=self.choice_range_hotkey_use, startX=(60-20)*self.rate)
        self.customSetGeometry(self.choice_range_hotkey_switch, 15, 275, 60, 20)
        self.choice_range_hotkey_switch.checkedChanged.connect(self.changeChoiceRangeHotkeySwitch)
        self.choice_range_hotkey_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # 切换范围快捷键设定按钮
        self.choice_range_hotkey_button = QPushButton(self)
        self.customSetGeometry(self.choice_range_hotkey_button, 100, 275, 100, 20)
        self.choice_range_hotkey_button.setText(
            self.object.config["choiceRangeHotkeyValue"] + " + " + "F1-F4")
        self.choice_range_hotkey_button.clicked.connect(lambda: self.object.settin_ui.setHotKey("choiceRange"))
        self.choice_range_hotkey_button.setCursor(ui.static.icon.SELECT_CURSOR)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 改变范围一开关状态
    def changeRangeSwitch1(self, checked):

        if checked:
            if self.switch_2_use :
                self.switch_2.mousePressEvent(1)
                self.switch_2.updateValue()
            if self.switch_3_use :
                self.switch_3.mousePressEvent(1)
                self.switch_3.updateValue()
            if self.switch_4_use :
                self.switch_4.mousePressEvent(1)
                self.switch_4.updateValue()
            self.switch_1_use = True
        else:
            self.switch_1_use = False


    # 改变范围二开关状态
    def changeRangeSwitch2(self, checked):

        if checked:
            if self.switch_1_use:
                self.switch_1.mousePressEvent(1)
                self.switch_1.updateValue()
            if self.switch_3_use:
                self.switch_3.mousePressEvent(1)
                self.switch_3.updateValue()
            if self.switch_4_use:
                self.switch_4.mousePressEvent(1)
                self.switch_4.updateValue()
            self.switch_2_use = True
        else:
            self.switch_2_use = False


    # 改变范围三开关状态
    def changeRangeSwitch3(self, checked):

        if checked:
            if self.switch_1_use:
                self.switch_1.mousePressEvent(1)
                self.switch_1.updateValue()
            if self.switch_2_use:
                self.switch_2.mousePressEvent(1)
                self.switch_2.updateValue()
            if self.switch_4_use:
                self.switch_4.mousePressEvent(1)
                self.switch_4.updateValue()
            self.switch_3_use = True
        else:
            self.switch_3_use = False


    # 改变范围四开关状态
    def changeRangeSwitch4(self, checked):

        if checked:
            if self.switch_1_use:
                self.switch_1.mousePressEvent(1)
                self.switch_1.updateValue()
            if self.switch_2_use:
                self.switch_2.mousePressEvent(1)
                self.switch_2.updateValue()
            if self.switch_3_use:
                self.switch_3.mousePressEvent(1)
                self.switch_3.updateValue()
            self.switch_4_use = True
        else:
            self.switch_4_use = False


    # 改变切换范围快键键开关状态
    def changeChoiceRangeHotkeySwitch(self, checked):

        if checked:
            self.choice_range_hotkey_use = True
            self.object.config["choiceRangeHotKey"] = True
        else:
            self.choice_range_hotkey_use = False
            self.object.config["choiceRangeHotKey"] = False


    # 窗口关闭处理
    def closeEvent(self, event):

        if not self.switch_1_use and not self.switch_2_use and not self.switch_3_use and not self.switch_4_use :
            utils.message.MessageBox("这是来自团子的警告", "未使用任一范围\n必须要开启一处范围才可使用      ",
                                     self.object.yaml["screen_scale_rate"])
            event.ignore()
            return

        # 范围状态开关
        self.object.config["switch1Use"] = self.switch_1_use
        self.object.config["switch2Use"] = self.switch_2_use
        self.object.config["switch3Use"] = self.switch_3_use
        self.object.config["switch4Use"] = self.switch_4_use
        self.object.translation_ui.show()