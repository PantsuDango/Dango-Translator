# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import ui.static.icon
import utils.translater


# 说明界面
class Edit(QWidget) :

    def __init__(self, object) :

        super(Edit, self).__init__()

        self.object = object
        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("修改原文并重新翻译")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size, self.font_type))

        # 编辑框
        self.edit_text = QTextBrowser(self)
        self.customSetGeometry(self.edit_text, 0, 0, self.window_width, 220)
        #self.edit_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.edit_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.edit_text.setStyleSheet("QTextBrowser { border-width: 0;"
                                                    "border-style: outset;"
                                                    "border-top:0px solid #e8f3f9;"
                                                    "color: #5B8FF9;"
                                                    "background: rgba(255, 255, 255, 0.7); }")
        self.edit_text.setCursor(ui.static.icon.PIXMAP_CURSOR)
        self.edit_text.setReadOnly(False)

        # 公共翻译测试可用性按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 200, 240, 100, 50)
        button.setText("重新翻译")
        button.clicked.connect(self.flushTranslate)
        button.setCursor(ui.static.icon.SELECT_CURSOR)


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 15
        # 界面尺寸
        self.window_width = int(500 * self.rate)
        self.window_height = int(300 * self.rate)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 刷新翻译
    def flushTranslate(self) :

        thread = utils.translater.Translater(self.object)
        thread.clear_text_sign.connect(self.object.translation_ui.clearText)
        thread.hide_range_ui_sign.connect(self.object.range_ui.hideUI)
        thread.flushTranslate(self.edit_text.toPlainText())