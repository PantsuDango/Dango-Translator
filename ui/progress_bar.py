from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ui.static.icon
import utils.thread
import utils.message


# 进度条
class ProgressBar(QWidget) :

    def __init__(self, rate, use_type) :

        super(ProgressBar, self).__init__()
        self.rate = rate
        self.use_type = use_type
        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 设置字体
        self.setStyleSheet("font: %spt '%s'; background-color: rgb(255, 255, 255);}"%(self.font_size, self.font_type))

        self.progress_bar = QProgressBar(self)
        self.customSetGeometry(self.progress_bar, 20, 10, 260, 10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: rgba(62, 62, 62, 0.2); "
                                        "border-radius: 6px;}"
                                        "QProgressBar::chunk { background-color: %s; border-radius: 5px;}"
                                        %(self.color_2))
        self.progress_bar.setValue(0)

        self.progress_label = QLabel(self)
        self.customSetGeometry(self.progress_label, 240, 25, 150, 20)
        self.progress_label.setStyleSheet("color: %s"%self.color_2)

        self.file_size_label = QLabel(self)
        self.customSetGeometry(self.file_size_label, 20, 25, 150, 20)
        self.file_size_label.setStyleSheet("color: %s" % self.color_2)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate),
                                 int(w * self.rate),
                                 int(h * self.rate)))


    # 初始化配置
    def getInitConfig(self):

        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 10
        # 灰色
        self.color_1 = "#595959"
        # 蓝色
        self.color_2 = "#5B8FF9"
        # 界面尺寸
        self.window_width = int(300 * self.rate)
        self.window_height = int(50 * self.rate)
        # 结束信号
        self.finish_sign = False
        # 中止信号
        self.stop_sign = False


    # 绘制进度信息
    def paintProgressBar(self, float_val, int_val, str_val) :

        self.progress_label.setText("{:.2f}%".format(float_val))
        self.progress_bar.setValue(int_val)
        self.file_size_label.setText(str_val)


    # 修改窗口标题
    def modifyTitle(self, title) :

        self.setWindowTitle(title)


    # 停止任务
    def stopProcess(self) :

        self.stop_sign = True


    # 窗口关闭处理
    def closeEvent(self, event) :

        if self.finish_sign :
            return
        if self.use_type == "offline_ocr" :
            utils.message.closeProcessBarMessageBox("停止安装",
                                                    "本地OCR安装进行中\n确定要中止操作吗     ",
                                                    self)
        elif self.use_type == "input_images" :
            utils.message.closeProcessBarMessageBox("停止导入",
                                                    "图片导入进行中\n确定要中止操作吗     ",
                                                    self)
        if not self.stop_sign :
            event.ignore()