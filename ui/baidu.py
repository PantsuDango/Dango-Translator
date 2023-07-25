# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ui.static.icon
import utils.test
import webbrowser


# 私人百度设置界面
class BaiduSetting(QWidget) :

    def __init__(self, object) :

        super(BaiduSetting, self).__init__()
        self.object = object
        self.logger = object.logger
        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("私人百度翻译设置 - 退出会自动保存")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 界面样式
        self.setStyleSheet("QWidget { font: 9pt '华康方圆体W7';"
                                     "color: %s;"
                                     "background: rgba(255, 255, 255, 1); }"
                           "QLineEdit { background: transparent;"
                                       "border-width:0;"
                                       "border-style:outset;"
                                       "border-bottom: 2px solid %s; }"
                          "QLineEdit:focus { border-bottom: 2px "
                                            "dashed %s; }"
                          "QLabel {color: %s;}"
                          "QPushButton { background: %s; border-radius: %spx; color: rgb(255, 255, 255); }"
                          "QPushButton:hover { background-color: #83AAF9; }"
                          "QPushButton:pressed { background-color: #4480F9; padding-left: 3px; padding-top: 3px; }"
                           %(self.color, self.color, self.color, self.color, self.color, 6.66*self.rate))

        # secret_id 输入框
        label = QLabel(self)
        self.customSetGeometry(label, 20, 20, 330, 20)
        label.setText("APP ID: ")
        self.secret_id_text = QLineEdit(self)
        self.customSetGeometry(self.secret_id_text, 20, 40, 330, 25)
        self.secret_id_text.setText(self.object.config["baiduAPI"]["Key"])
        self.secret_id_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # secret_key 输入框
        label = QLabel(self)
        self.customSetGeometry(label, 20, 80, 330, 20)
        label.setText("密钥: ")
        self.secret_key_text = QLineEdit(self)
        self.customSetGeometry(self.secret_key_text, 20, 100, 330, 25)
        self.secret_key_text.setText(self.object.config["baiduAPI"]["Secret"])
        self.secret_key_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 测试按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 65, 150, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testBaidu(
            self.object, self.filterNullWord(self.secret_id_text), self.filterNullWord(self.secret_key_text)))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 注册按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 155, 150, 60, 20)
        button.setText("注册")
        button.clicked.connect(self.openTutorial)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 查额度按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 245, 150, 60, 20)
        button.setText("查额度")
        button.clicked.connect(self.openQueryQuota)
        button.setCursor(ui.static.icon.SELECT_CURSOR)


    # 初始化配置
    def getInitConfig(self) :

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面尺寸
        self.window_width = int(370 * self.rate)
        self.window_height = int(200 * self.rate)
        # 颜色
        self.color = "#5B8FF9"


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 过滤空字符
    def filterNullWord(self, obj) :

        text = obj.text().strip()
        obj.setText(text)
        return text


    # 打开注册教程
    def openTutorial(self) :

        try :
            url = self.object.yaml["dict_info"]["baidu_tutorial"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())
            utils.message.MessageBox("私人百度注册",
                                     "请尝试手动打开此地址:\n%s     " % url)


    # 打开查询额度地址
    def openQueryQuota(self):

        url = "https://fanyi-api.baidu.com/api/trans/product/desktop"
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())
            utils.message.MessageBox("私人百度额度查询",
                                     "打开地址失败, 请尝试手动打开此网页下载\n%s     " % url)


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.object.config["baiduAPI"]["Key"] = self.filterNullWord(self.secret_id_text)
        self.object.config["baiduAPI"]["Secret"] = self.filterNullWord(self.secret_key_text)