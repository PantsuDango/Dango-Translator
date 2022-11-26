from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import system_hotkey
from traceback import format_exc

import re
import utils.thread
import ui.static.icon
import ui.switch
import utils.message
import translator.sound


DRAW_PATH = "./config/draw.jpg"


# 选择范围
class WScreenShot(QWidget) :

    multi_range_sign = pyqtSignal(int, tuple)

    def __init__(self, object, index=0, parent=None) :

        super(WScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet("background-color:black;")
        self.setWindowOpacity(0.6)

        desktop_widget = QDesktopWidget()
        screen_count = desktop_widget.screenCount()
        max_width, max_height = 0, 0
        for i in range(screen_count):
            temp_screen = desktop_widget.screenGeometry(i)
            if max_height == 0:
                max_height = temp_screen.height()
            max_width += temp_screen.width()
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
        self.index = index


    # 绘制事情
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


    # 鼠标按下事件
    def mousePressEvent(self, event) :

        try:
            if event.button() == Qt.LeftButton:
                self.start_point = event.pos()
                self.end_point = self.start_point
                self.is_drawing = True
        except Exception:
            pass


    # 鼠标移动事件
    def mouseMoveEvent(self, event) :

        try:
            if self.is_drawing:
                self.end_point = event.pos()
                self.update()
        except Exception:
            pass


    # 获取鼠标起始点坐标
    def getRange(self) :

        # 计算范围
        x = self.start_point.x()
        if self.start_point.x() > self.end_point.x() :
            x = self.end_point.x()
        y = self.start_point.y()
        if self.start_point.y() > self.end_point.y() :
            y = self.end_point.y()
        w = abs(self.end_point.x() - self.start_point.x())
        h = abs(self.end_point.y() - self.start_point.y())

        # 选择使用的范围
        if self.index == 0 :
            for index in range(1, 5):
                if self.object.config["switch{}Use".format(index)]:
                    self.object.yaml["range{}".format(index)]["x"] = x
                    self.object.yaml["range{}".format(index)]["y"] = y
                    self.object.yaml["range{}".format(index)]["w"] = w
                    self.object.yaml["range{}".format(index)]["h"] = h

            # 显示范围框
            self.object.range_ui.setGeometry(x, y, w, h)
            self.object.range_ui.label.setGeometry(0, 0, w, h)
            self.object.range_ui.show_sign = True
            self.object.range_ui.show()

            # 如果是自动模式下, 则解除暂停
            if self.object.translation_ui.translate_mode :
                self.object.translation_ui.stop_sign = False
        else :
            # 多范围选择范围信号槽
            self.multi_range_sign.emit(self.index, (x, y, w, h))


    # 鼠标松开事件
    def mouseReleaseEvent(self, event):

        try:
            if event.button() == Qt.LeftButton:
                self.end_point = event.pos()
                self.getRange()
                self.close()
                if self.index == 0 :
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
        self.ui()


    def ui(self) :

        x, y, w, h = 0, 0, 0, 0
        # 选择使用的范围
        for index in range(1, 5):
            if self.object.config["switch{}Use".format(index)]:
                x = self.object.yaml["range{}".format(index)]["x"]
                y = self.object.yaml["range{}".format(index)]["y"]
                w = self.object.yaml["range{}".format(index)]["w"]
                h = self.object.yaml["range{}".format(index)]["h"]

        # 窗口大小
        self.setGeometry(x, y, w, h)
        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, w, h)
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
        self.hide_button.setGeometry(QRect(int(w-40*self.rate), 0, int(40*self.rate), int(30*self.rate)))
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

        self.hide_button.setGeometry(QRect(int(self.width()-40*self.rate), 0, int(40*self.rate), int(30*self.rate)))
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

        # 选择使用的范围
        for index in range(1, 5):
            if self.object.config["switch{}Use".format(index)]:
                self.object.yaml["range{}".format(index)]["x"] = self.x()
                self.object.yaml["range{}".format(index)]["y"] = self.y()
                self.object.yaml["range{}".format(index)]["w"] = self.width()
                self.object.yaml["range{}".format(index)]["h"] = self.height()
        self.object.multi_range_ui.updateLabelRectText()

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

        if self.isHidden():
            self.show()
        else:
            self.hide()


    # 隐藏/显示窗体信号
    def hideRangeUI(self, hotkey_sign=False) :

        if hotkey_sign :
            if self.object.translation_ui.isHidden() and self.object.multi_range_ui.isHidden() :
                return
            #self.object.translation_ui.sound.playButtonSound()

        if self.isHidden() :
            self.show()
        else :
            self.hide()


    # 退出信号
    def quit(self) :

        self.show_sign = False
        self.close()


# 多范围参数页面
class MultiRange(QWidget):

    # 切换范围快捷键信号
    choice_range_hotkey_sign_1 = pyqtSignal(int)
    choice_range_hotkey_sign_2 = pyqtSignal(int)
    choice_range_hotkey_sign_3 = pyqtSignal(int)
    choice_range_hotkey_sign_4 = pyqtSignal(int)

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
        self.choice_range_hotkey_use = object.config["choiceRangeHotKeyUse"]
        # 快捷键映射关系
        self.hotkey_map = {
            "ctrl": "control",
            "win": "super"
        }
        # 范围快捷键
        self.choice_range_hotkey_1 = system_hotkey.SystemHotkey()
        self.choice_range_hotkey_2 = system_hotkey.SystemHotkey()
        self.choice_range_hotkey_3 = system_hotkey.SystemHotkey()
        self.choice_range_hotkey_4 = system_hotkey.SystemHotkey()

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

        self.switch_1 = ui.switch.SwitchOCR(self, sign=self.switch_1_use, startX=(60-20)*self.rate)
        self.customSetGeometry(self.switch_1, 15, 35, 60, 20)
        self.switch_1.checkedChanged.connect(self.changeRangeSwitch1)
        self.switch_1.setCursor(ui.static.icon.SELECT_CURSOR)

        self.choice_button_1 = QPushButton(self)
        self.customSetGeometry(self.choice_button_1, 100, 35, 60, 20)
        self.choice_button_1.setText("框选范围")
        self.choice_button_1.clicked.connect(lambda: self.cutRange(1))

        # 范围二
        self.label_2 = QLabel(self)
        self.customSetGeometry(self.label_2, 15, 70, self.window_width, 20)

        self.switch_2 = ui.switch.SwitchOCR(self, sign=self.switch_2_use, startX=(60-20)*self.rate)
        self.customSetGeometry(self.switch_2, 15, 95, 60, 20)
        self.switch_2.checkedChanged.connect(self.changeRangeSwitch2)
        self.switch_2.setCursor(ui.static.icon.SELECT_CURSOR)

        self.choice_button_2 = QPushButton(self)
        self.customSetGeometry(self.choice_button_2, 100, 95, 60, 20)
        self.choice_button_2.setText("框选范围")
        self.choice_button_2.clicked.connect(lambda: self.cutRange(2))

        # 范围三
        self.label_3 = QLabel(self)
        self.customSetGeometry(self.label_3, 15, 130, self.window_width, 20)

        self.switch_3 = ui.switch.SwitchOCR(self, sign=self.switch_3_use, startX=(60-20)*self.rate)
        self.customSetGeometry(self.switch_3, 15, 155, 60, 20)
        self.switch_3.checkedChanged.connect(self.changeRangeSwitch3)
        self.switch_3.setCursor(ui.static.icon.SELECT_CURSOR)

        self.choice_button_3 = QPushButton(self)
        self.customSetGeometry(self.choice_button_3, 100, 155, 60, 20)
        self.choice_button_3.setText("框选范围")
        self.choice_button_3.clicked.connect(lambda: self.cutRange(3))

        # 范围四
        self.label_4 = QLabel(self)
        self.customSetGeometry(self.label_4, 15, 190, self.window_width, 20)

        self.switch_4 = ui.switch.SwitchOCR(self, sign=self.switch_4_use, startX=(60-20)*self.rate)
        self.customSetGeometry(self.switch_4, 15, 215, 60, 20)
        self.switch_4.checkedChanged.connect(self.changeRangeSwitch4)
        self.switch_4.setCursor(ui.static.icon.SELECT_CURSOR)

        self.choice_button_4 = QPushButton(self)
        self.customSetGeometry(self.choice_button_4, 100, 215, 60, 20)
        self.choice_button_4.setText("框选范围")
        self.choice_button_4.clicked.connect(lambda: self.cutRange(4))

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
            self.object.config["choiceRangeHotkeyValue"] + " + " + "f1-f4")
        self.choice_range_hotkey_button.clicked.connect(lambda: self.object.settin_ui.setHotKey("choiceRange"))
        self.choice_range_hotkey_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 注册切换范围快捷键
        if self.choice_range_hotkey_use:
            self.RegisterChoiceRangeHotkey()
        self.choice_range_hotkey_sign_1.connect(self.choiceRangeHotkeyFunc)
        self.choice_range_hotkey_sign_2.connect(self.choiceRangeHotkeyFunc)
        self.choice_range_hotkey_sign_3.connect(self.choiceRangeHotkeyFunc)
        self.choice_range_hotkey_sign_4.connect(self.choiceRangeHotkeyFunc)


    # 框选范围按钮信号槽
    def cutRange(self, index) :

        self.screen_shot_ui = WScreenShot(self.object, index)
        self.screen_shot_ui.multi_range_sign.connect(self.changeRange)
        self.screen_shot_ui.show()


    # 改变范围信号槽
    def changeRange(self, index, rect) :

        self.object.yaml["range{}".format(index)]["x"] = rect[0]
        self.object.yaml["range{}".format(index)]["y"] = rect[1]
        self.object.yaml["range{}".format(index)]["w"] = rect[2]
        self.object.yaml["range{}".format(index)]["h"] = rect[3]
        self.updateLabelRectText()

        if (index == 1 and self.switch_1_use) \
                or (index == 2 and self.switch_2_use) \
                or (index == 3 and self.switch_3_use) \
                or (index == 4 and self.switch_4_use) :
            self.object.range_ui.setGeometry(rect[0], rect[1], rect[2], rect[3])
            self.object.range_ui.label.setGeometry(0, 0, rect[2], rect[3])


    # 切换范围快捷键信号槽
    def choiceRangeHotkeyFunc(self, sign):

        # 快捷键只允许在多范围界面或翻译界面活动的情况下使用
        if self.isHidden() and self.object.translation_ui.isHidden() :
            return

        if sign == 1 and not self.switch_1_use:
            #self.object.translation_ui.sound.playButtonSound()
            self.switch_1.mousePressEvent(1)
            self.switch_1.updateValue()
        if sign == 2 and not self.switch_2_use:
            #self.object.translation_ui.sound.playButtonSound()
            self.switch_2.mousePressEvent(1)
            self.switch_2.updateValue()
        if sign == 3 and not self.switch_3_use:
            #self.object.translation_ui.sound.playButtonSound()
            self.switch_3.mousePressEvent(1)
            self.switch_3.updateValue()
        if sign == 4 and not self.switch_4_use:
            #self.object.translation_ui.sound.playButtonSound()
            self.switch_4.mousePressEvent(1)
            self.switch_4.updateValue()


    # 注册切换范围快捷键
    def RegisterChoiceRangeHotkey(self):

        hotkey = self.object.config["choiceRangeHotkeyValue"]
        if hotkey in self.hotkey_map:
            hotkey = self.hotkey_map[hotkey]

        try :
            self.choice_range_hotkey_1.register((hotkey, "f1"), overwrite=True,
                                                callback=lambda x: self.choice_range_hotkey_sign_1.emit(1))
            self.choice_range_hotkey_2.register((hotkey, "f2"), overwrite=True,
                                                callback=lambda x: self.choice_range_hotkey_sign_2.emit(2))
            self.choice_range_hotkey_3.register((hotkey, "f3"), overwrite=True,
                                                callback=lambda x: self.choice_range_hotkey_sign_3.emit(3))
            self.choice_range_hotkey_4.register((hotkey, "f4"), overwrite=True,
                                                callback=lambda x: self.choice_range_hotkey_sign_4.emit(4))
        except Exception :
            self.object.logger.error(format_exc())


    # 修改切换范围快捷键
    def modifyChoiceRangeHotkey(self):

        hotkey = self.object.config["choiceRangeHotkeyValue"]
        if hotkey in self.hotkey_map:
            hotkey = self.hotkey_map[hotkey]

        self.choice_range_hotkey_1.order_hotkey((hotkey, "f1"))
        self.choice_range_hotkey_2.order_hotkey((hotkey, "f2"))
        self.choice_range_hotkey_3.order_hotkey((hotkey, "f3"))
        self.choice_range_hotkey_4.order_hotkey((hotkey, "f4"))


    # 注销切换范围快捷键
    def UnRegisterChoiceRangeHotkey(self):

        hotkey = self.object.config["choiceRangeHotkeyValue"]
        if hotkey in self.hotkey_map:
            hotkey = self.hotkey_map[hotkey]

        self.choice_range_hotkey_1.unregister((hotkey, "f1"))
        self.choice_range_hotkey_2.unregister((hotkey, "f2"))
        self.choice_range_hotkey_3.unregister((hotkey, "f3"))
        self.choice_range_hotkey_4.unregister((hotkey, "f4"))


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
            # 改变范围框的坐标
            self.updateRangeUIRect(1)
        else:
            self.switch_1_use = False
            self.object.range_ui.hide()
        self.object.config["switch1Use"] = checked


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
            # 改变范围框的坐标
            self.updateRangeUIRect(2)
        else:
            self.switch_2_use = False
            self.object.range_ui.hide()
        self.object.config["switch2Use"] = checked


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
            # 改变范围框的坐标
            self.updateRangeUIRect(3)
        else:
            self.switch_3_use = False
            self.object.range_ui.hide()
        self.object.config["switch3Use"] = checked


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
            # 改变范围框的坐标
            self.updateRangeUIRect(4)
        else:
            self.switch_4_use = False
            self.object.range_ui.hide()
        self.object.config["switch4Use"] = checked


    # 改变范围框的坐标
    def updateRangeUIRect(self, index):
        self.object.range_ui.setGeometry(self.object.yaml["range{}".format(index)]["x"],
                                         self.object.yaml["range{}".format(index)]["y"],
                                         self.object.yaml["range{}".format(index)]["w"],
                                         self.object.yaml["range{}".format(index)]["h"])
        self.object.range_ui.label.setGeometry(0,
                                               0,
                                               self.object.yaml["range{}".format(index)]["w"],
                                               self.object.yaml["range{}".format(index)]["h"])
        self.object.range_ui.show()


    # 改变切换范围快键键开关状态
    def changeChoiceRangeHotkeySwitch(self, checked):

        if checked:
            self.choice_range_hotkey_use = True
            self.object.config["choiceRangeHotKeyUse"] = True
            self.RegisterChoiceRangeHotkey()
        else:
            self.choice_range_hotkey_use = False
            self.object.config["choiceRangeHotKeyUse"] = False
            self.UnRegisterChoiceRangeHotkey()


    # 更新显示的坐标文本
    def updateLabelRectText(self) :
        self.label_1.setText("区域一 (x:{} y:{} w:{} h:{})".format(
            self.object.yaml["range1"]["x"],
            self.object.yaml["range1"]["y"],
            self.object.yaml["range1"]["w"],
            self.object.yaml["range1"]["h"],
        ))
        self.label_2.setText("区域二 (x:{} y:{} w:{} h:{})".format(
            self.object.yaml["range2"]["x"],
            self.object.yaml["range2"]["y"],
            self.object.yaml["range2"]["w"],
            self.object.yaml["range2"]["h"],
        ))
        self.label_3.setText("区域三 (x:{} y:{} w:{} h:{})".format(
            self.object.yaml["range3"]["x"],
            self.object.yaml["range3"]["y"],
            self.object.yaml["range3"]["w"],
            self.object.yaml["range3"]["h"],
        ))
        self.label_4.setText("区域四 (x:{} y:{} w:{} h:{})".format(
            self.object.yaml["range4"]["x"],
            self.object.yaml["range4"]["y"],
            self.object.yaml["range4"]["w"],
            self.object.yaml["range4"]["h"],
        ))


    # 窗口显示信号
    def showEvent(self, e):

        # 如果处于自动模式下则暂停
        if self.object.translation_ui.translate_mode:
            self.object.translation_ui.stop_sign = True
        # 更新显示的坐标文本
        self.updateLabelRectText()


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

        if not self.object.range_ui.show_sign :
            self.object.range_ui.hide()

        # 如果处于自动模式下则开始
        if self.object.translation_ui.translate_mode:
            self.object.translation_ui.stop_sign = False