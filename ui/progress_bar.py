from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ui.static.icon
import utils.thread
import utils.message

import sys
import os
import base64
import requests


# 进度条
class ProgressBar(QWidget) :

    def __init__(self, rate) :

        super().__init__()
        self.rate = rate

        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        # 窗口图标
        icon = QIcon()
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(ui.static.icon.APP_LOGO))
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)
        # 设置字体
        self.setStyleSheet("font: %spt '%s'; background-color: rgb(255, 255, 255);}"%(self.font_size, self.font_type))

        self.progress_bar = QProgressBar(self)
        self.customSetGeometry(self.progress_bar, 20, 10, 260, 10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: rgba(62, 62, 62, 0.2); "
                                        "border-radius: 6px;}"
                                        "QProgressBar::chunk { background-color: %s; border-radius: 5px;}"
                                        %(self.color_2))

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


    # 绘制进度信息
    def paintProgressBar(self, float_val, int_val, str_val) :

        self.progress_label.setText("{:.2f}%".format(float_val))
        self.progress_bar.setValue(int_val)
        self.file_size_label.setText(str_val)


    # 窗口关闭处理
    def closeEvent(self, event) :

        utils.message.MessageBox("这是来自团子的警告~",
                                 "安装进行中, 关闭将会中止操作      ")


# 下载
class Download(QThread) :

    progress_bar_sign = pyqtSignal(float, int, str)

    def __init__(self, url, file_name) :

        super(Download, self).__init__()
        self.url = url
        self.file_name = file_name


    def run(self):

        size = 0
        chunk_size = 1024
        try :
            response = requests.get(self.url, stream=True)
            content_size = int(response.headers["content-length"])
            if response.status_code == 200 :
                # 显示文件大小
                file_size = content_size/chunk_size/1024
                file_size_content = "{:.2f} MB".format(content_size/chunk_size/1024)
                with open(self.file_name, "wb") as file :
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        # 显示当前进度
                        now_size_content = "{:.2f} MB".format(size/content_size*file_size)
                        self.progress_bar_sign.emit(float(size/content_size*100),
                                                    int(size/content_size*100),
                                                    "%s/%s"%(now_size_content, file_size_content))

        except Exception as err :
            os.remove(file_name)


if __name__ == "__main__" :

    app = QApplication(sys.argv)
    obj = ProgressBar(1.5)
    obj.show()
    sys.exit(app.exec_())