# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import ui.static.icon
import utils.translater


# 说明界面
class Manga(QWidget) :

    def __init__(self, object) :

        super(Manga, self).__init__()

        self.object = object
        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("漫画翻译")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size, self.font_type))

        # 打开图标
        button = QPushButton(self)
        self.customSetGeometry(button, 15, 10, 50, 20)
        button.setText(" 导入")
        button.setStyleSheet("QPushButton {background: transparent;}"
                             "QPushButton:hover { background-color: #83AAF9; }"
                             "QPushButton:pressed { background-color: #4480F9;")
        button.setIcon(ui.static.icon.OPEN_ICON)
        button.clicked.connect(self.openImageFiles)

        # 横向分割线
        label = QLabel(self)
        self.customSetGeometry(label, 0, 35, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 10
        # 界面尺寸
        self.window_width = int(1200 * self.rate)
        self.window_height = int(700 * self.rate)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 打开图片文件列表
    def openImageFiles(self) :

        options = QFileDialog.Options()
        images, _ = QFileDialog.getOpenFileNames(self,
                                                 "选择要翻译的生肉漫画原图（可多选）",
                                                 "",
                                                 "图片类型(*.png *.jpg *.jpeg);;所有类型 (*)",
                                                 options=options)
        for image_path in images :
            print(image_path)


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.hide()
        self.object.translation_ui.show()
        if self.object.range_ui.show_sign == True:
            self.object.range_ui.show()