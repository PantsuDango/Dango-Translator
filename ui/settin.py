from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from traceback import format_exc
import qtawesome
import webbrowser
import os
import re

import utils.thread
import utils.config
import utils.message
import utils.port
import utils.test
import utils.http

from ui import image
import ui.hotkey
import ui.switch
import ui.desc
import ui.key

import translator.ocr.baidu


LOGO_ICON_PATH = "./config/icon/logo.ico"
PIXMAP_ICON_PATH = "./config/icon/pixmap.png"
PIXMAP2_PATH = "./config/icon/pixmap2.png"
QUESTION_PATH = "./config/icon/question.png"
OCR_ICON_PATH = "./config/icon/ocr.png"
ABOUT_ICON_PATH = "./config/icon/about.png"
STYPE_ICON_PATH = "./config/icon/stype.png"
TRANSLATE_ICON_PATH = "./config/icon/translate.png"
GOOD_ICON_PATH = "./config/icon/good.png"
HOLLOW_IMG_PATH = "./config/other/描边.png"
SOLID_IMG_PATH = "./config/other/实心.png"
BG_IMAGE_PATH = "./config/background/settin.jpg"
QQ_GROUP_PATH = "./config/other/交流群.png"
GITHUB_ICON_PATH = "./config/icon/github.png"
TUTORIAL_ICON_PATH = "./config/icon/tutorial.png"
BILIBILI_ICON_PATH = "./config/icon/bilibili.png"
GROUP_PATH = "./config/icon/group.png"
BILIBILI_VIDEO_PATH = "./config/icon/video.png"
BLOG_PATH = "./config/icon/blog.png"
HOME_ICON_PATH = "./config/icon/home.png"
SLIDER_ICON_PATH = "./config/icon/slider.png"
FUNCTION_ICON_PATH = "./config/icon/function.png"
OPEN_STATUSBAR_IMG_PATH = "./config/other/显示消息栏.png"
CLOSE_STATUSBAR_IMG_PATH = "./config/other/屏蔽消息栏.png"


# 重构QTabWidget使其竖直选项卡文字水平
class TabBar(QTabBar):

    def tabSizeHint(self, index):

        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s


    def paintEvent(self, event) :

        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()) :
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


# 重构QTabWidget使其竖直选项卡文字水平
class TabWidget(QTabWidget) :

    def __init__(self, *args, **kwargs):

        QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))


class Settin(QMainWindow) :

    def __init__(self, object):

        super(Settin, self).__init__()

        self.object = object
        self.logger = object.logger
        self.getInitConfig()
        self.ui()

        # 初始化界面
        self.key_ui = ui.key.Key(self.object)
        self.desc_ui = ui.desc.Desc(self.object)
        self.hotkey_ui = ui.hotkey.HotKey(self.object)


    def ui(self):

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        # 窗口置顶及关闭窗口最小化最大化
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("团子翻译器 Ver%s - 设置"%self.object.yaml["version"])

        # 窗口图标
        icon = QIcon()
        icon.addPixmap(QPixmap(LOGO_ICON_PATH), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        # 鼠标样式
        pixmap = QPixmap(PIXMAP_ICON_PATH)
        pixmap = pixmap.scaled(int(20*self.rate),
                               int(20*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 鼠标选中状态图标
        self.select_pixmap = QPixmap(PIXMAP2_PATH)
        self.select_pixmap = self.select_pixmap.scaled(int(20*self.rate),
                                                       int(20*self.rate),
                                                       Qt.KeepAspectRatio,
                                                       Qt.SmoothTransformation)
        self.select_pixmap = QCursor(self.select_pixmap, 0, 0)

        # 鼠标问号图标
        self.question_pixmap = QPixmap(QUESTION_PATH)
        self.question_pixmap = self.question_pixmap.scaled(int(20 * self.rate),
                                                       int(20 * self.rate),
                                                       Qt.KeepAspectRatio,
                                                       Qt.SmoothTransformation)
        self.question_pixmap = QCursor(self.question_pixmap, 0, 0)

        # 设置字体
        self.setStyleSheet("font: %spt '华康方圆体W7'; color: %s"
                           %(self.font_size, self.color_1))

        # 顶部工具栏
        self.tab_widget = TabWidget(self)
        self.tab_widget.setGeometry(QRect(0, -1, self.window_width+5, self.window_height+5))
        self.tab_widget.setTabPosition(QTabWidget.West)
        # 工具栏样式
        self.tab_widget.setStyleSheet("QTabBar:tab { min-width: %dpx;"
                                                   "background: rgba(255, 255, 255, 1); }"
                                     "QTabBar:tab:selected { background: rgba(62, 62, 62, 0.01); }"
                                     "QTabWidget::pane { border-image: url(%s); }"
                                     "QPushButton { background: %s;"
                                                   "border-radius: %spx;"
                                                   "color: rgb(255, 255, 255); }"
                                     "QPushButton:hover { background-color: #83AAF9; }"
                                     "QPushButton:pressed { background-color: #4480F9;"
                                                           "padding-left: 3px;"
                                                           "padding-top: 3px; }"
                                     "QTextEdit { background: transparent;"
                                                 "border-width: 0;"
                                                 "border-style: outset;"
                                                 "border-bottom: 2px solid %s; }"
                                     "QTextEdit:focus { border-bottom: 2px;"
                                                       "dashed %s; }"
                                     "QSlider:groove:horizontal { height: %spx;"
                                                                 "border-radius: %spx;"
                                                                 "margin-left: %spx;"
                                                                 "margin-right: %spx;"
                                                                 "background: rgba(89, 89, 89, 0.3); }"
                                     "QSlider:handle:horizontal { width: %spx;"
                                                                  "height: %spx;"
                                                                  "margin-top: %spx;"
                                                                  "margin-left: %spx;"
                                                                  "margin-bottom: %spx;"
                                                                  "margin-right: %spx;"
                                                                  "border-image: url(./config/icon/slider.png); }"
                                     "QSlider::sub-page:horizontal { height: %spx;"
                                                                    "border-radius: %spx;"
                                                                    "margin-left: %spx;"
                                                                    "background: %s; }"
                                     "QSpinBox { background: rgba(255, 255, 255, 0.3); }"
                                     "QFontComboBox { background: rgba(255, 255, 255, 0.3); }"
                                     "QDoubleSpinBox { background: rgba(255, 255, 255, 0.3); }"
                                      % (67*self.rate, BG_IMAGE_PATH, self.color_2, 6.66*self.rate, self.color_2,
                                       self.color_2, 8.66*self.rate, 4*self.rate, 13.33*self.rate, 13.33*self.rate,
                                       33.33*self.rate, 33.33*self.rate, -13.33*self.rate, -13.33*self.rate,
                                       -13.33*self.rate, -13.33*self.rate, 8.66*self.rate, 4*self.rate,
                                       10*self.rate, self.color_2
                                       ))

        # 选项卡
        self.setTabOne()
        self.setTabTwo()
        self.setTabThree()
        self.setTabFour()
        self.setTabFive()
        self.setTabSix()

        # 背景图pixiv标签
        label = QLabel(self)
        self.customSetGeometry(label, 630, 380, 200, 15)
        label.setText("背景图 pixiv id: %s"%self.object.yaml["dict_info"]["bg_pixiv_id"])
        label.setStyleSheet("font-size: 9pt; color: %s"%self.color_2)


    # OCR设定标签页
    def setTabOne(self) :

        # 选项卡界面
        self.tab_1 = QWidget()
        self.customSetGeometry(self.tab_1, 0, 0, self.window_width, self.window_height)
        self.tab_widget.addTab(self.tab_1, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_1), "OCR设定")

        # 分割线
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 0, 0, 1, 400)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 选项卡图标
        icon = QIcon()
        pixmap = QPixmap(OCR_ICON_PATH)
        pixmap = pixmap.scaled(int(15*self.rate),
                               int(15*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_1), icon)

        # 此Label用于雾化工具栏1的背景图
        label = QLabel(self.tab_1)
        label.setGeometry(QRect(0, -1, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # OCR说明
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 400, 25, 65, 20)
        button.setStyleSheet("color: %s;"
                             "background: transparent;"%self.color_2)
        button.setText("什么是OCR")
        button.clicked.connect(lambda: self.showDesc("OCR"))
        button.setCursor(self.question_pixmap)

        # OCR说明?号
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_1)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 465, 25, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("OCR"))
        button.setCursor(self.question_pixmap)

        # 本地OCR标签
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 20, 25, 60, 20)
        label.setText("本地OCR")

        # 本地OCR说明按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 80, 25, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;"%self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("offlineOCR"))
        button.setCursor(self.question_pixmap)

        # 本地OCR说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_1)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 105, 25, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("offlineOCR"))
        button.setCursor(self.question_pixmap)

        # 本地OCR备注
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 145, 25, 300, 20)
        label.setText("如果安装失败建议直接使用在线OCR")
        label.setStyleSheet("color: %s" % self.color_2)

        # 本地OCR状态开关
        self.offline_ocr_switch = ui.switch.OfflineSwitch(self.tab_1, sign=self.offline_ocr_use, startX=(65-20)*self.rate, object=self.object)
        self.customSetGeometry(self.offline_ocr_switch, 20, 60, 65, 20)
        self.offline_ocr_switch.checkedChanged.connect(self.changeOfflineSwitch)
        self.offline_ocr_switch.setCursor(self.select_pixmap)

        # 本地OCR运行按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 105, 60, 60, 20)
        button.setText("运行")
        button.clicked.connect(self.runOfflineOCR)
        button.setCursor(self.select_pixmap)

        # 本地OCR测试按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 185, 60, 60, 20)
        button.setText("测试")
        button.clicked.connect(self.testOfflineOCR)
        button.setCursor(self.select_pixmap)

        # 本地OCR教程按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 265, 60, 60, 20)
        button.setText("教程")
        button.clicked.connect(self.openOfflineOCRTutorial)
        button.setCursor(self.select_pixmap)

        # 在线OCR标签
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 20, 120, 60, 20)
        label.setText("在线OCR")

        # 在线OCR说明按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 80, 120, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;"%self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("onlineOCR"))
        button.setCursor(self.question_pixmap)

        # 在线OCR说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_1)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 105, 120, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("onlineOCR"))
        button.setCursor(self.question_pixmap)

        # 在线OCR备注
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 145, 120, 300, 20)
        label.setText("精度高, 无限调用次数, 建议使用")
        label.setStyleSheet("color: %s" % self.color_2)

        # 在线OCR状态开关
        self.online_ocr_switch = ui.switch.SwitchOCR(self.tab_1, self.online_ocr_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.online_ocr_switch, 20, 155, 65, 20)
        self.online_ocr_switch.checkedChanged.connect(self.changeOnlineSwitch)
        self.online_ocr_switch.setCursor(self.select_pixmap)

        # 在线OCR购买按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 105, 155, 60, 20)
        button.setText("购买")
        button.clicked.connect(self.openDangoBuyPage)
        button.setCursor(self.select_pixmap)

        # 在线OCR测试按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 185, 155, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testOnlineOCR(self.object))
        button.setCursor(self.select_pixmap)

        # 在线OCR教程按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 265, 155, 60, 20)
        button.setText("教程")
        button.clicked.connect(self.openOnlineOCRTutorials)
        button.setCursor(self.select_pixmap)

        # 节点下拉框
        self.node_info_comboBox = QComboBox(self.tab_1)
        self.customSetGeometry(self.node_info_comboBox, 345, 155, 150, 20)
        self.node_info_comboBox.setStyleSheet("QComboBox{color: %s}"%self.color_2)
        self.node_info_comboBox.setCursor(self.select_pixmap)
        # 获取节点信息
        utils.thread.createThread(self.getNodeInfo)

        # 百度OCR标签
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 20, 215, 60, 20)
        label.setText("百度OCR")

        # 百度OCR说明标签
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 80, 215, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;"%self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("baiduOCR"))
        button.setCursor(self.question_pixmap)

        # 百度OCR说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_1)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 105, 215, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("baiduOCR"))
        button.setCursor(self.question_pixmap)

        # 百度OCR备注
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 145, 215, 300, 20)
        label.setText("老用户专用, 精度虽高但价格昂贵")
        label.setStyleSheet("color: %s" % self.color_2)

        # 百度OCR状态开关
        self.baidu_ocr_switch = ui.switch.BaiduSwitchOCR(self.tab_1, self.baidu_ocr_use, startX=(65-20)*self.rate, object=self.object)
        self.customSetGeometry(self.baidu_ocr_switch, 20, 250, 65, 20)
        self.baidu_ocr_switch.checkedChanged.connect(self.changeBaiduSwitch)
        self.baidu_ocr_switch.setCursor(self.select_pixmap)

        # 百度OCR密钥按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 105, 250, 60, 20)
        button.setText("密钥")
        button.clicked.connect(lambda: self.showKey("baiduOCR"))
        button.setCursor(self.select_pixmap)

        # 百度OCR测试按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 185, 250, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testBaiduOCR(self.object))
        button.setCursor(self.select_pixmap)

        # 百度OCR教程按钮
        button = QPushButton(self.tab_1)
        self.customSetGeometry(button, 265, 250, 60, 20)
        button.setText("教程")
        button.clicked.connect(self.openBaiduOCRTutorials)
        button.setCursor(self.select_pixmap)

        # OCR识别语种标签
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 20, 310, 150, 20)
        label.setText("选择要翻译的原语种:")

        # OCR识别语种comboBox
        self.language_comboBox = QComboBox(self.tab_1)
        self.customSetGeometry(self.language_comboBox, 160, 310, 130, 20)
        self.language_comboBox.addItem("")
        self.language_comboBox.addItem("")
        self.language_comboBox.addItem("")
        self.language_comboBox.setItemText(0, "日语（Japanese）")
        self.language_comboBox.setItemText(1, "英语（English）")
        self.language_comboBox.setItemText(2, "韩语（Korean）")
        self.language_comboBox.setStyleSheet("QComboBox{color: %s}"%self.color_2)
        self.language_comboBox.setCursor(self.select_pixmap)
        if self.object.config["language"] == "ENG":
            self.language_comboBox.setCurrentIndex(1)
        elif self.object.config["language"] == "KOR":
            self.language_comboBox.setCurrentIndex(2)
        else:
            self.language_comboBox.setCurrentIndex(0)


    # 翻译设定标签栏
    def setTabTwo(self) :

        # 选项卡界面
        self.tab_2 = QWidget()
        self.tab_widget.addTab(self.tab_2, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_2), " 翻译设定")

        # 分割线
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 0, 0, 1, 400)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.2);")

        # 选项卡图标
        icon = QIcon()
        pixmap = QPixmap(TRANSLATE_ICON_PATH)
        pixmap = pixmap.scaled(int(20*self.rate),
                               int(20*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_2), icon)

        # 此Label用于雾化工具栏2的背景图
        imageLabel = QLabel(self.tab_2)
        imageLabel.setGeometry(QRect(0, -1, self.window_width+5, self.window_height+5))
        imageLabel.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 公共翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 20, 25, 70, 20)
        label.setText("公共翻译")

        # 公共翻译说明按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 90, 25, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;"%self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("publicTranslate"))
        button.setCursor(self.question_pixmap)

        # 公共翻译说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_2)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 115, 25, 20, 20)
        button.clicked.connect(lambda: self.showDesc("publicTranslate"))
        button.setCursor(self.question_pixmap)
        button.setStyleSheet("background: transparent;")

        # 公共翻译备注
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 155, 25, 300, 20)
        label.setText("可直接使用, 但不稳定可能会抽风")
        label.setStyleSheet("color: %s"%self.color_2)

        # 公共翻译教程按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 380, 25, 60, 20)
        button.setText("教程")
        button.clicked.connect(self.openPublicTransTutorial)
        button.setCursor(self.select_pixmap)

        # 有道翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 20, 70, 35, 20)
        label.setText("有道:")

        # 有道翻译开关
        self.youdao_switch = ui.switch.SwitchOCR(self.tab_2, sign=self.youdao_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.youdao_switch, 65, 70, 65, 20)
        self.youdao_switch.checkedChanged.connect(self.changeYoudaoSwitch)
        self.youdao_switch.setCursor(self.select_pixmap)

        # 有道翻译颜色选择
        self.youdao_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.youdao_color), "", self.tab_2)
        self.customSetIconSize(self.youdao_color_button, 20, 20)
        self.customSetGeometry(self.youdao_color_button, 140, 70, 20, 20)
        self.youdao_color_button.setStyleSheet("background: transparent;")
        self.youdao_color_button.clicked.connect(lambda: self.ChangeTranslateColor("youdao", self.youdao_color))
        self.youdao_color_button.setCursor(self.select_pixmap)

        # 百度翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 200, 70, 35, 20)
        label.setText("百度:")

        # 百度翻译开关
        self.baidu_switch = ui.switch.SwitchOCR(self.tab_2, sign=self.baidu_web_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.baidu_switch, 245, 70, 65, 20)
        self.baidu_switch.checkedChanged.connect(self.changeBaiduWebSwitch)
        self.baidu_switch.setCursor(self.select_pixmap)

        # 百度翻译颜色选择
        self.baidu_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.baidu_web_color), "", self.tab_2)
        self.customSetIconSize(self.baidu_color_button, 20, 20)
        self.customSetGeometry(self.baidu_color_button, 320, 70, 20, 20)
        self.baidu_color_button.setStyleSheet("background: transparent;")
        self.baidu_color_button.clicked.connect(lambda: self.ChangeTranslateColor("baidu", self.baidu_web_color))
        self.baidu_color_button.setCursor(self.select_pixmap)

        # 腾讯翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 380, 70, 35, 20)
        label.setText("腾讯:")

        # 腾讯翻译开关
        self.tencent_switch = ui.switch.SwitchOCR(self.tab_2, sign=self.tencent_web_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.tencent_switch, 425, 70, 65, 20)
        self.tencent_switch.checkedChanged.connect(self.changeTencentWebSwitch)
        self.tencent_switch.setCursor(self.select_pixmap)

        # 腾讯翻译颜色选择
        self.tencent_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.tencent_web_color), "", self.tab_2)
        self.customSetIconSize(self.tencent_color_button, 20, 20)
        self.customSetGeometry(self.tencent_color_button, 500, 70, 20, 20)
        self.tencent_color_button.setStyleSheet("background: transparent;")
        self.tencent_color_button.clicked.connect(lambda: self.ChangeTranslateColor("tencent", self.tencent_web_color))
        self.tencent_color_button.setCursor(self.select_pixmap)

        # DeepL翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 20, 120, 40, 20)
        label.setText("DeepL:")

        # DeepL翻译开关
        self.deepl_switch = ui.switch.SwitchOCR(self.tab_2, sign=self.deepl_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.deepl_switch, 65, 120, 65, 20)
        self.deepl_switch.checkedChanged.connect(self.changeDeepLSwitch)
        self.deepl_switch.setCursor(self.select_pixmap)

        # DeepL翻译颜色选择
        self.deepl_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.deepl_color), "", self.tab_2)
        self.customSetIconSize(self.deepl_color_button, 20, 20)
        self.customSetGeometry(self.deepl_color_button, 140, 120, 20, 20)
        self.deepl_color_button.setStyleSheet("background: transparent;")
        self.deepl_color_button.clicked.connect(lambda: self.ChangeTranslateColor("deepl", self.deepl_color))
        self.deepl_color_button.setCursor(self.select_pixmap)

        # 谷歌翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 200, 120, 35, 20)
        label.setText("谷歌:")

        # 谷歌翻译开关
        self.google_switch = ui.switch.SwitchOCR(self.tab_2, sign=self.google_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.google_switch, 245, 120, 65, 20)
        self.google_switch.checkedChanged.connect(self.changeGoogleSwitch)
        self.google_switch.setCursor(self.select_pixmap)

        # 谷歌翻译颜色选择
        self.google_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.google_color), "", self.tab_2)
        self.customSetIconSize(self.google_color_button, 20, 20)
        self.customSetGeometry(self.google_color_button, 320, 120, 20, 20)
        self.google_color_button.setStyleSheet("background: transparent;")
        self.google_color_button.clicked.connect(lambda: self.ChangeTranslateColor("google", self.google_color))
        self.google_color_button.setCursor(self.select_pixmap)

        # 彩云翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 380, 120, 35, 20)
        label.setText("彩云:")

        # 彩云翻译开关
        self.caiyun_switch = ui.switch.SwitchOCR(self.tab_2, sign=self.caiyun_web_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.caiyun_switch, 425, 120, 65, 20)
        self.caiyun_switch.checkedChanged.connect(self.changeCaiyunWebSwitch)
        self.caiyun_switch.setCursor(self.select_pixmap)

        # 彩云翻译颜色选择
        self.caiyun_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.caiyun_web_color), "", self.tab_2)
        self.customSetIconSize(self.caiyun_color_button, 20, 20)
        self.customSetGeometry(self.caiyun_color_button, 500, 120, 20, 20)
        self.caiyun_color_button.setStyleSheet("background: transparent;")
        self.caiyun_color_button.clicked.connect(lambda: self.ChangeTranslateColor("caiyun", self.caiyun_web_color))
        self.caiyun_color_button.setCursor(self.select_pixmap)

        # 私人翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 20, 185, 70, 20)
        label.setText("私人翻译")

        # 私人翻译说明按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 90, 185, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;"%self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("privateTranslate"))
        button.setCursor(self.question_pixmap)

        # 私人翻译说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_2)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 115, 185, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("privateTranslate"))
        button.setCursor(self.question_pixmap)

        # 私人翻译备注
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 155, 185, 300, 20)
        label.setText("需注册, 但稳定效果好, 建议使用")
        label.setStyleSheet("color: %s" % self.color_2)

        # 私人腾讯翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 20, 230, 35, 20)
        label.setText("腾讯:")

        # 私人腾讯翻译开关
        self.tencent_private_switch = ui.switch.SwitchOCR(self.tab_2, sign=self.tencent_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.tencent_private_switch, 65, 230, 65, 20)
        self.tencent_private_switch.checkedChanged.connect(self.changeTencentSwitch)
        self.tencent_private_switch.setCursor(self.select_pixmap)

        # 私人腾讯翻译颜色选择
        self.tencent_private_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.tencent_color), "", self.tab_2)
        self.customSetIconSize(self.tencent_private_color_button, 20, 20)
        self.customSetGeometry(self.tencent_private_color_button, 140, 230, 20, 20)
        self.tencent_private_color_button.setStyleSheet("background: transparent;")
        self.tencent_private_color_button.clicked.connect(lambda: self.ChangeTranslateColor("tencent_private", self.tencent_use))
        self.tencent_private_color_button.setCursor(self.select_pixmap)

        # 私人腾讯翻译密钥按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 180, 230, 60, 20)
        button.setText("密钥")
        button.clicked.connect(lambda: self.showKey("tencentTranslate"))
        button.setCursor(self.select_pixmap)

        # 私人腾讯翻译测试按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 260, 230, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testTencent(self.object))
        button.setCursor(self.select_pixmap)

        # 私人腾讯翻译教程按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 340, 230, 60, 20)
        button.setText("教程")
        button.clicked.connect(self.openTencentTutorial)
        button.setCursor(self.select_pixmap)

        # 私人百度翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 20, 280, 35, 20)
        label.setText("百度:")

        # 私人百度翻译开关
        self.baidu_private_switch = ui.switch.SwitchOCR(self.tab_2, sign=self.baidu_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.baidu_private_switch, 65, 280, 65, 20)
        self.baidu_private_switch.checkedChanged.connect(self.changeBaiduTranslaterSwitch)
        self.baidu_private_switch.setCursor(self.select_pixmap)

        # 私人百度翻译颜色选择
        self.baidu_private_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.baidu_color), "", self.tab_2)
        self.customSetIconSize(self.baidu_private_color_button, 20, 20)
        self.customSetGeometry(self.baidu_private_color_button, 140, 280, 20, 20)
        self.baidu_private_color_button.setStyleSheet("background: transparent;")
        self.baidu_private_color_button.clicked.connect(lambda: self.ChangeTranslateColor("baidu_private", self.baidu_color))
        self.baidu_private_color_button.setCursor(self.select_pixmap)

        # 私人百度翻译密钥按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 180, 280, 60, 20)
        button.setText("密钥")
        button.clicked.connect(lambda: self.showKey("baiduTranslate"))
        button.setCursor(self.select_pixmap)

        # 私人百度翻译测试按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 260, 280, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testBaidu(self.object))
        button.setCursor(self.select_pixmap)

        # 私人百度翻译教程按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 340, 280, 60, 20)
        button.setText("教程")
        button.clicked.connect(self.openBaiduTutorial)
        button.setCursor(self.select_pixmap)

        # 私人彩云翻译标签
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 20, 330, 35, 20)
        label.setText("彩云:")

        # 私人彩云翻译开关
        self.caiyun_private_switch = ui.switch.SwitchOCR(self.tab_2, sign=self.caiyun_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.caiyun_private_switch, 65, 330, 65, 20)
        self.caiyun_private_switch.checkedChanged.connect(self.changeCaiyunSwitch)
        self.caiyun_private_switch.setCursor(self.select_pixmap)

        # 私人彩云翻译颜色选择
        self.caiyun_private_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.caiyun_color), "", self.tab_2)
        self.customSetIconSize(self.caiyun_private_color_button, 20, 20)
        self.customSetGeometry(self.caiyun_private_color_button, 140, 330, 20, 20)
        self.caiyun_private_color_button.setStyleSheet("background: transparent;")
        self.caiyun_private_color_button.clicked.connect(lambda: self.ChangeTranslateColor("caiyun_private", self.caiyun_color))
        self.caiyun_private_color_button.setCursor(self.select_pixmap)

        # 私人彩云翻译密钥按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 180, 330, 60, 20)
        button.setText("密钥")
        button.clicked.connect(lambda: self.showKey("caiyunTranslate"))
        button.setCursor(self.select_pixmap)

        # 私人彩云翻译测试按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 260, 330, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testCaiyun(self.object))
        button.setCursor(self.select_pixmap)

        # 私人彩云翻译教程按钮
        button = QPushButton(self.tab_2)
        self.customSetGeometry(button, 340, 330, 60, 20)
        button.setText("教程")
        button.clicked.connect(self.openCaiyunTutorial)
        button.setCursor(self.select_pixmap)


    # 显示设定标签页
    def setTabThree(self) :

        # 选项卡界面
        self.tab_3 = QWidget()
        self.tab_widget.addTab(self.tab_3, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_3), " 显示设定")

        # 分割线
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 0, 0, 1, 400)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.2);")

        # 选项卡图标
        icon = QIcon()
        pixmap = QPixmap(STYPE_ICON_PATH)
        pixmap = pixmap.scaled(int(20*self.rate),
                               int(20*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_3), icon)

        # 此Label用于雾化工具栏1的背景图
        imageLabel = QLabel(self.tab_3)
        imageLabel.setGeometry(QRect(0, -1, self.window_width + 5, self.window_height + 5))
        imageLabel.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 翻译框透明度设定标签
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 20, 20, 90, 20)
        label.setText("翻译框透明度:")

        # 翻译框透明度设定
        self.horizontal_slider = QSlider(self.tab_3)
        self.customSetGeometry(self.horizontal_slider, 120, 18, 320, 25)
        self.horizontal_slider.setMaximum(100)
        self.horizontal_slider.setOrientation(Qt.Horizontal)
        self.horizontal_slider.setValue(0)
        self.horizontal_slider.setValue(self.horizontal)
        self.horizontal_slider.valueChanged.connect(self.changeHorizontal)
        self.horizontal_slider.installEventFilter(self)
        self.horizontal_slider.setCursor(self.select_pixmap)

        # 翻译框透明度数值标签
        self.horizontal_slider_label = QLabel(self.tab_3)
        self.customSetGeometry(self.horizontal_slider_label, 450, 20, 30, 20)
        self.horizontal_slider_label.setText("{}%".format(self.horizontal))

        # 翻译框透明度说明标签
        button = QPushButton(self.tab_3)
        self.customSetGeometry(button, 490, 20, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;" % self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("horizontalSlider"))
        button.setCursor(self.question_pixmap)

        # 翻译框透明度说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_3)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 515, 20, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("horizontalSlider"))
        button.setCursor(self.question_pixmap)

        # 翻译字体大小设定标签
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 20, 70, 145, 16)
        label.setText("字体大小:")

        # 翻译字体大小设定
        self.fontSize_spinBox = QSpinBox(self.tab_3)
        self.customSetGeometry(self.fontSize_spinBox, 95, 65, 40, 25)
        self.fontSize_spinBox.setMinimum(10)
        self.fontSize_spinBox.setMaximum(30)
        self.fontSize_spinBox.setValue(self.fontSize)
        self.fontSize_spinBox.setCursor(self.select_pixmap)

        # 翻译字体类型设定标签
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 275, 70, 145, 20)
        label.setText("字体类型:")

        # 翻译字体类型设定
        self.font_comboBox = QFontComboBox(self.tab_3)
        self.customSetGeometry(self.font_comboBox, 350, 65, 185, 25)
        self.font_comboBox.activated[str].connect(self.getFontType)
        self.comboBox_font = QFont(self.font_type)
        self.font_comboBox.setCurrentFont(self.comboBox_font)
        self.font_comboBox.setCursor(self.select_pixmap)
        self.font_comboBox.setStyleSheet("QComboBox{color: %s}" % self.color_2)

        # 字体样式设定标签
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 20, 120, 60, 20)
        label.setText("字体样式:")

        # 字体样式设定开关
        self.font_type_switch = ui.switch.SwitchFontType(self.tab_3, sign=self.font_color_type, startX=(65-20)*self.rate)
        self.customSetGeometry(self.font_type_switch, 95, 120, 65, 20)
        self.font_type_switch.checkedChanged.connect(self.changeFontColorTypeSwitch)
        self.font_type_switch.setCursor(self.select_pixmap)

        # 字体样式设定说明标签
        button = QPushButton(self.tab_3)
        self.customSetGeometry(button, 175, 120, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;" % self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("fontType"))
        button.setCursor(self.question_pixmap)

        # 字体样式设定说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_3)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 200, 120, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("fontType"))
        button.setCursor(self.question_pixmap)

        # 显示原文标签
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 275, 120, 60, 20)
        label.setText("显示原文:")

        # 显示原文标签开关
        self.show_original_switch = ui.switch.ShowSwitch(self.tab_3, sign=self.show_original_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.show_original_switch, 350, 120, 65, 20)
        self.show_original_switch.checkedChanged.connect(self.changeShowOriginalSwitch)
        self.show_original_switch.setCursor(self.select_pixmap)

        # 显示原文说明标签
        button = QPushButton(self.tab_3)
        self.customSetGeometry(button, 430, 120, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;"%self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("showOriginal"))
        button.setCursor(self.question_pixmap)

        # 显示原文说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_3)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 455, 120, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("showOriginal"))
        button.setCursor(self.question_pixmap)

        # 显示消息栏标签
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 20, 170, 60, 20)
        label.setText("翻译时间:")

        # 显示消息栏开关
        self.show_statusbar_switch = ui.switch.ShowSwitch(self.tab_3, sign=self.show_statusbar_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.show_statusbar_switch, 95, 170, 65, 20)
        self.show_statusbar_switch.checkedChanged.connect(self.changeShowStatusbarSwitch)
        self.show_statusbar_switch.setCursor(self.select_pixmap)

        # 显示消息栏说明标签
        button = QPushButton(self.tab_3)
        self.customSetGeometry(button, 175, 170, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;" % self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("showStatusbar"))
        button.setCursor(self.question_pixmap)

        # 显示消息栏说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_3)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 200, 170, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("showStatusbar"))
        button.setCursor(self.question_pixmap)

        # 原文颜色标签
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 275, 170, 60, 20)
        label.setText("原文颜色:")

        # 原文颜色选择
        self.original_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.original_color), "", self.tab_3)
        self.customSetIconSize(self.original_color_button, 20, 20)
        self.customSetGeometry(self.original_color_button, 350, 170, 20, 20)
        self.original_color_button.setStyleSheet("background: transparent;")
        self.original_color_button.clicked.connect(lambda: self.ChangeTranslateColor("original", self.original_color))
        self.original_color_button.setCursor(self.select_pixmap)

        # 原文颜色说明标签
        button = QPushButton(self.tab_3)
        self.customSetGeometry(button, 430, 170, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;" % self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("originalColor"))
        button.setCursor(self.question_pixmap)

        # 原文颜色说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_3)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 455, 170, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("originalColor"))
        button.setCursor(self.question_pixmap)

        # 是否全屏下置顶
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 20, 220, 150, 20)
        label.setText("是否全屏下置顶:")

        # 是否全屏下置顶开关
        self.set_top_switch = ui.switch.SwitchOCR(self.tab_4,
                                                  self.set_top_use,
                                                  startX=(65-20) * self.rate)
        self.customSetGeometry(self.set_top_switch, 140, 270, 65, 20)
        self.set_top_switch.checkedChanged.connect(self.changeSetTopSwitch)
        self.set_top_switch.setCursor(self.select_pixmap)

        # 是否全屏下置顶说明标签
        button = QPushButton(self.tab_4)
        self.customSetGeometry(button, 220, 220, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;"%self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("setTop"))
        button.setCursor(self.question_pixmap)

        # 是否全屏下置顶说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_4)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 245, 220, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("setTop"))
        button.setCursor(self.question_pixmap)




    # 功能设定标签页
    def setTabFour(self) :

        # 选项卡界面
        self.tab_4 = QWidget()
        self.tab_widget.addTab(self.tab_4, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_4), " 功能设定")

        # 分割线
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 0, 0, 1, 400)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.2);")

        # 选项卡图标
        icon = QIcon()
        pixmap = QPixmap(FUNCTION_ICON_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_4), icon)

        # 此Label用于雾化工具栏1的背景图
        imageLabel = QLabel(self.tab_4)
        imageLabel.setGeometry(QRect(0, -1, self.window_width + 5, self.window_height + 5))
        imageLabel.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 原文自动复制到剪贴板标签
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 20, 20, 150, 20)
        label.setText("原文自动复制到剪贴板:")

        # 原文自动复制到剪贴板开关
        self.auto_copy_original_switch = ui.switch.SwitchOCR(self.tab_4, sign=self.auto_clipboard_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.auto_copy_original_switch, 430-255, 20, 65, 20)
        self.auto_copy_original_switch.checkedChanged.connect(self.changeAutoCopyOriginalSwitch)
        self.auto_copy_original_switch.setCursor(self.select_pixmap)

        # 自动翻译间隔标签
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 275, 20, 150, 20)
        label.setText("自动模式刷新间隔(秒):")

        # 自动模式速率设定
        self.auto_speed_spinBox = QDoubleSpinBox(self.tab_4)
        self.customSetGeometry(self.auto_speed_spinBox, 430, 15, 45, 25)
        self.auto_speed_spinBox.setDecimals(1)
        self.auto_speed_spinBox.setMinimum(0.5)
        self.auto_speed_spinBox.setMaximum(10.0)
        self.auto_speed_spinBox.setSingleStep(0.1)
        self.auto_speed_spinBox.setValue(self.translate_speed)
        self.auto_speed_spinBox.setCursor(self.select_pixmap)

        # 自动模式速率设定说明标签
        button = QPushButton(self.tab_4)
        self.customSetGeometry(button, 490, 20, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;" % self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("autoSpeed"))
        button.setCursor(self.question_pixmap)

        # 自动模式速率设定说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_4)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 515, 20, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("autoSpeed"))
        button.setCursor(self.question_pixmap)

        # 文字方向标签
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 20, 70, 80, 20)
        label.setText("文字方向:")

        # 文字方向开关
        self.text_direction_switch = ui.switch.SwitchDirection(self.tab_4, sign=self.text_direction_use, startX=(65-20)*self.rate, object=self.object)
        self.customSetGeometry(self.text_direction_switch, 95, 70, 65, 20)
        self.text_direction_switch.checkedChanged.connect(self.changeTextDirectionSwitch)
        self.text_direction_switch.setCursor(self.select_pixmap)

        # 文字方向说明标签
        button = QPushButton(self.tab_4)
        self.customSetGeometry(button, 175, 70, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;"%self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("textDirection"))
        button.setCursor(self.question_pixmap)

        # 文字方向说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_4)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 200, 70, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("textDirection"))
        button.setCursor(self.question_pixmap)

        # 文字换行标签
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 275, 70, 80, 20)
        label.setText("文字换行:")

        # 文字换行开关
        self.branch_line_switch = ui.switch.SwitchBranchLine(self.tab_4, sign=self.branch_line_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.branch_line_switch, 350, 70, 65, 20)
        self.branch_line_switch.checkedChanged.connect(self.changeBranchLineSwitch)
        self.branch_line_switch.setCursor(self.select_pixmap)

        # 文字换行说明标签
        button = QPushButton(self.tab_4)
        self.customSetGeometry(button, 430, 70, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;"%self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("branchLine"))
        button.setCursor(self.question_pixmap)

        # 文字换行说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_4)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 455, 70, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("branchLine"))
        button.setCursor(self.question_pixmap)

        # 翻译快捷键标签
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 20, 120, 80, 20)
        label.setText("翻译热键:")

        # 翻译快捷键开关
        self.translate_hotkey_switch = ui.switch.SwitchOCR(self.tab_4, sign=self.translate_hotkey_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.translate_hotkey_switch, 95, 120, 65, 20)
        self.translate_hotkey_switch.checkedChanged.connect(self.changeTranslateHotkeySwitch)
        self.translate_hotkey_switch.setCursor(self.select_pixmap)

        # 翻译快捷键设定按钮
        self.translate_hotkey_button = QPushButton(self.tab_4)
        self.customSetGeometry(self.translate_hotkey_button, 175, 120, 60, 20)
        self.translate_hotkey_button.setText(self.object.config["translateHotkeyValue1"] + "+" + self.object.config["translateHotkeyValue2"])
        self.translate_hotkey_button.clicked.connect(lambda: self.setHotKey("translate"))
        self.translate_hotkey_button.setCursor(self.select_pixmap)

        # 范围快捷键标签
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 275, 120, 80, 20)
        label.setText("范围热键:")

        # 范围快捷键开关
        self.range_hotkey_switch = ui.switch.SwitchOCR(self.tab_4, sign=self.range_hotkey_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.range_hotkey_switch, 350, 120, 65, 20)
        self.range_hotkey_switch.checkedChanged.connect(self.changeRangeHotkeySwitch)
        self.range_hotkey_switch.setCursor(self.select_pixmap)

        # 范围快捷键设定按钮
        self.range_hotkey_button = QPushButton(self.tab_4)
        self.customSetGeometry(self.range_hotkey_button, 430, 120, 60, 20)
        self.range_hotkey_button.setText(
            self.object.config["rangeHotkeyValue1"] + "+" + self.object.config["rangeHotkeyValue2"])
        self.range_hotkey_button.clicked.connect(lambda: self.setHotKey("range"))
        self.range_hotkey_button.setCursor(self.select_pixmap)

        # 图像相似度标签
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 20, 170, 150, 20)
        label.setText("图像相似度(%):")

        # 图像相似度设定
        self.image_refresh_spinBox = QDoubleSpinBox(self.tab_4)
        self.customSetGeometry(self.image_refresh_spinBox, 130, 167, 45, 25)
        self.image_refresh_spinBox.setDecimals(0)
        self.image_refresh_spinBox.setMinimum(80)
        self.image_refresh_spinBox.setMaximum(100)
        self.image_refresh_spinBox.setSingleStep(1)
        self.image_refresh_spinBox.setValue(self.image_refresh_score)
        self.image_refresh_spinBox.setCursor(self.select_pixmap)

        # 图像相似度说明标签
        button = QPushButton(self.tab_4)
        self.customSetGeometry(button, 190, 170, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;" % self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("imageRefresh"))
        button.setCursor(self.question_pixmap)

        # 图像相似度说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_4)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 215, 170, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("imageRefresh"))
        button.setCursor(self.question_pixmap)

        # 文字相似度标签
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 275, 170, 150, 20)
        label.setText("文字相似度(%):")

        # 文字相似度设定
        self.text_refresh_spinBox = QDoubleSpinBox(self.tab_4)
        self.customSetGeometry(self.text_refresh_spinBox, 385, 167, 45, 25)
        self.text_refresh_spinBox.setDecimals(0)
        self.text_refresh_spinBox.setMinimum(80)
        self.text_refresh_spinBox.setMaximum(100)
        self.text_refresh_spinBox.setSingleStep(1)
        self.text_refresh_spinBox.setValue(self.text_refresh_score)
        self.text_refresh_spinBox.setCursor(self.select_pixmap)

        # 文字相似度说明标签
        button = QPushButton(self.tab_4)
        self.customSetGeometry(button, 445, 170, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;" % self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("textRefresh"))
        button.setCursor(self.question_pixmap)

        # 文字相似度说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_4)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 470, 170, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("textRefresh"))
        button.setCursor(self.question_pixmap)

        # 自动登录标签
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 20, 220, 80, 20)
        label.setText("自动登录:")

        # 自动登录开关
        self.auto_login_switch = ui.switch.SwitchOCR(self.tab_4,
                                                     sign=self.auto_login_use,
                                                     startX=(65-20) * self.rate)
        self.customSetGeometry(self.auto_login_switch, 95, 220, 65, 20)
        self.auto_login_switch.checkedChanged.connect(self.changeAutoLoginSwitch)
        self.auto_login_switch.setCursor(self.select_pixmap)

        # 百度OCR高精度模式备注
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 275, 220, 150, 20)
        label.setText("百度OCR高精度:")

        # 百度OCR高精度模式开关
        self.baidu_ocr_high_precision_switch = ui.switch.SwitchOCR(self.tab_4,
                                                                   self.baidu_ocr_high_precision_use,
                                                                   startX=(65-20) * self.rate)
        self.customSetGeometry(self.baidu_ocr_high_precision_switch, 390, 220, 65, 20)
        self.baidu_ocr_high_precision_switch.checkedChanged.connect(self.changeBaiduOcrHighPrecisionSwitch)
        self.baidu_ocr_high_precision_switch.setCursor(self.select_pixmap)


        # 贴字翻译标签
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 20, 220, 60, 20)
        label.setText("贴字翻译:")

        # 贴字翻译开关
        self.draw_image_switch = ui.switch.DrawSwitchOCR(self.tab_3, sign=self.draw_image_use, startX=(65-20)*self.rate, object=self.object)
        self.customSetGeometry(self.draw_image_switch, 95, 220, 65, 20)
        self.draw_image_switch.checkedChanged.connect(self.changeDrawImageSwitch)
        self.draw_image_switch.setCursor(self.select_pixmap)

        # 贴字翻译说明标签
        button = QPushButton(self.tab_3)
        self.customSetGeometry(button, 175, 220, 25, 20)
        button.setStyleSheet("color: %s; font-size: 9pt; background: transparent;" % self.color_2)
        button.setText("说明")
        button.clicked.connect(lambda: self.showDesc("drawImage"))
        button.setCursor(self.question_pixmap)

        # 贴字翻译说明?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self.tab_3)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 200, 220, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("drawImage"))
        button.setCursor(self.question_pixmap)

        # 隐藏范围快捷键标签
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 275, 220, 100, 20)
        label.setText("隐藏范围热键:")

        # 隐藏快捷键开关
        self.hide_range_hotkey_switch = ui.switch.SwitchOCR(self.tab_3, sign=self.hide_range_hotkey_use,
                                                             startX=(65-20) * self.rate)
        self.customSetGeometry(self.hide_range_hotkey_switch, 380, 220, 65, 20)
        self.hide_range_hotkey_switch.checkedChanged.connect(self.changeHideRangeHotkeySwitch)
        self.hide_range_hotkey_switch.setCursor(self.select_pixmap)

        # 隐藏快捷键设定按钮
        self.hide_range_hotkey_button = QPushButton(self.tab_3)
        self.customSetGeometry(self.hide_range_hotkey_button, 460, 220, 60, 20)
        self.hide_range_hotkey_button.setText(self.object.config["hideRangeHotkeyValue1"] + "+" + self.object.config["hideRangeHotkeyValue2"])
        self.hide_range_hotkey_button.clicked.connect(lambda: self.setHotKey("hideRange"))
        self.hide_range_hotkey_button.setCursor(self.select_pixmap)

    # 关于标签页
    def setTabFive(self) :

        # 选项卡界面
        self.tab_5 = QWidget()
        self.tab_widget.addTab(self.tab_5, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_5), "关于   ")

        # 分割线
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 0, 0, 1, 400)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.2);")

        # 选项卡图标
        icon = QIcon()
        pixmap = QPixmap(ABOUT_ICON_PATH)
        pixmap = pixmap.scaled(int(20*self.rate),
                               int(20*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_5), icon)

        # 此Label用于雾化工具栏1的背景图
        imageLabel = QLabel(self.tab_5)
        imageLabel.setGeometry(QRect(0, -1, self.window_width + 5, self.window_height + 5))
        imageLabel.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 官方网站标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 20, 300, 20)
        label.setText("团子翻译器的官网哦 (欢迎来玩)")

        # 官方网站按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 20, 90, 20)
        button.setText("官方网站")
        button.clicked.connect(self.openHomePage)
        button.setCursor(self.select_pixmap)

        # 项目地址图标
        icon = QIcon()
        pixmap = QPixmap(HOME_ICON_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        button.setIcon(icon)

        # 项目地址标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 65, 300, 20)
        label.setText("本软件已在github开源 (欢迎来点小星星)")

        # 项目地址按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 65, 90, 20)
        button.setText("项目地址")
        button.clicked.connect(self.openGithubproject)
        button.setCursor(self.select_pixmap)

        # 项目地址图标
        github_icon = QIcon()
        pixmap = QPixmap(GITHUB_ICON_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        github_icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        button.setIcon(github_icon)

        # 在线教程标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 110, 300, 20)
        label.setText("软件完整使用教程 (要好好阅读哦)")

        # 在线教程按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 110, 90, 20)
        button.setText("在线文档")
        button.clicked.connect(self.openTutorial)
        button.setCursor(self.select_pixmap)

        # 在线教程图标
        icon = QIcon()
        pixmap = QPixmap(TUTORIAL_ICON_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        button.setIcon(icon)

        # 教程视频标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 150, 300, 20)
        label.setText("软件b站教程视频 (不想看文档就看这个吧)")

        # 教程视频按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 150, 90, 20)
        button.setText("教程视频")
        button.clicked.connect(self.openBilibiliVideo)
        button.setCursor(self.select_pixmap)

        # b站教程视频图标
        icon = QIcon()
        pixmap = QPixmap(BILIBILI_VIDEO_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        button.setIcon(icon)

        # 关注作者标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 195, 300, 20)
        label.setText("发布公告的地方 (不关注团子吗)")

        # 关注作者按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 195, 90, 20)
        button.setText("关注团子")
        button.clicked.connect(self.oepnBilibili)
        button.setCursor(self.select_pixmap)

        # QQ图标
        icon = QIcon()
        pixmap = QPixmap(BILIBILI_ICON_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        button.setIcon(icon)

        # 添加交流群标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 240, 300, 20)
        label.setText("加入交流群 (QQ群申请)")

        # 添加交流群按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 240, 90, 20)
        button.setText("群聊交流")
        button.clicked.connect(lambda: self.showDesc("qqGroup"))
        button.setCursor(self.select_pixmap)

        # QQ群图标
        icon = QIcon()
        pixmap = QPixmap(GROUP_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        button.setIcon(icon)

        # 特别鸣谢标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 20, 290, 300, 20)
        label.setText("特别鸣谢 (本软件受到以下人员和项目的帮助)")

        # PaddleOCR主页按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 330, 90, 20)
        button.setText("PaddleOCR‭")
        button.clicked.connect(self.openPaddleOCR)
        button.setIcon(github_icon)
        button.setCursor(self.select_pixmap)

        # GT-Zhang主页按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 130, 330, 90, 20)
        button.setText("GT-Zhang")
        button.clicked.connect(self.openGT)
        button.setIcon(github_icon)
        button.setCursor(self.select_pixmap)

        # 博客图标
        icon = QIcon()
        pixmap = QPixmap(BLOG_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)

        # C4a15Wh主页按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 240, 330, 90, 20)
        button.setText("C4a15Wh")
        button.clicked.connect(self.openC44)
        button.setIcon(icon)
        button.setCursor(self.select_pixmap)

        # cypas‭主页按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 350, 330, 90, 20)
        button.setText("Cypas‭")
        button.clicked.connect(self.openCy)
        button.setIcon(icon)
        button.setCursor(self.select_pixmap)


    # 支持作者标签页
    def setTabSix(self) :

        # 选项卡界面
        self.tab_6 = QWidget()
        self.tab_widget.addTab(self.tab_6, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_6), " 支持作者")

        # 分割线
        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 0, 0, 1, 400)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.2);")

        # 选项卡图标
        icon = QIcon()
        pixmap = QPixmap(GOOD_ICON_PATH)
        pixmap = pixmap.scaled(int(20*self.rate),
                               int(20*self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_6), icon)

        # 此Label用于雾化工具栏1的背景图
        imageLabel = QLabel(self.tab_6)
        imageLabel.setGeometry(QRect(0, -1, self.window_width+5, self.window_height+5))
        imageLabel.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 充电独白标签
        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 30, 20, 400, 145)
        label.setText("<html><head/><body><p>你好呀, 这里是胖次团子 ❤\
                       </p><p>不知不觉软件已经更新到Ver%s了, 谢谢下载使用~!\
                       </p><p>然后感谢你也成为团子用户的一员 ~\
                       </p><p>软件是免费的, 希望你没有被第三方渠道坑到 ~\
                       </p><p>欢迎你的投喂 ~ 团子会非常开心的! \
                       </p><p>这会是团子不断更新优化的动力 ~</p></body></html>"%self.object.yaml["version"])

        # 放置微信收款图片
        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 20, 180, 150, 150)
        label.setStyleSheet("border-image: url(:/image/weixin.jpg);")

        # 放置支付宝收款图片
        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 180, 180, 150, 150)
        label.setStyleSheet("border-image: url(:/image/zhifubao.jpg);")

        # 微信充电标签
        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 65, 330, 80, 20)
        label.setStyleSheet("font: 12pt")
        label.setText("微信充电")

        # 支付宝充电标签
        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 215, 330, 80, 20)
        label.setStyleSheet("font: 12pt")
        label.setText("支付宝充电")


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面尺寸
        self.window_width = int(800*self.rate)
        self.window_height = int(400*self.rate)
        # 所使用的颜色
        self.color_1 = "#595959"  # 灰色
        self.color_2 = "#5B8FF9"  # 蓝色
        # 界面字体大小
        self.font_size = 10
        # 存被开启的翻译源
        self.translate_list = []

        # OCR各开关
        self.offline_ocr_use = self.object.config["offlineOCR"]
        self.online_ocr_use = self.object.config["onlineOCR"]
        self.baidu_ocr_use = self.object.config["baiduOCR"]
        self.baidu_ocr_high_precision_use = self.object.config["OCR"]["highPrecision"]

        # 公共有道翻译开关
        self.youdao_use = eval(self.object.config["youdaoUse"])
        if self.youdao_use :
            self.translate_list.append("youdao")
        # 公共百度翻译开关
        self.baidu_web_use = eval(self.object.config["baiduwebUse"])
        if self.baidu_web_use :
            self.translate_list.append("baidu")
        # 公共腾讯翻译开关
        self.tencent_web_use = eval(self.object.config["tencentwebUse"])
        if self.tencent_web_use :
            self.translate_list.append("tencent")
        # 公共DeepL翻译开关
        self.deepl_use = eval(self.object.config["deeplUse"])
        if self.deepl_use :
            self.translate_list.append("deepl")
        # 公共谷歌翻译开关
        self.google_use = eval(self.object.config["googleUse"])
        if self.google_use :
            self.translate_list.append("google")
        # 公共彩云翻译开关
        self.caiyun_web_use = eval(self.object.config["caiyunUse"])
        if self.caiyun_web_use :
            self.translate_list.append("caiyun")
        # 私人腾讯翻译开关
        self.tencent_use = eval(self.object.config["tencentUse"])
        if self.tencent_use :
            self.translate_list.append("tencent_private")
        # 私人百度翻译开关
        self.baidu_use = eval(self.object.config["baiduUse"])
        if self.baidu_use :
            self.translate_list.append("baidu_private")
        # 私人彩云翻译开关
        self.caiyun_use = eval(self.object.config["caiyunPrivateUse"])
        if self.caiyun_use :
            self.translate_list.append("caiyun_private")

        # 字体颜色 公共有道
        self.youdao_color = self.object.config["fontColor"]["youdao"]
        # 字体颜色 公共百度
        self.baidu_web_color = self.object.config["fontColor"]["baiduweb"]
        # 字体颜色 公共腾讯
        self.tencent_web_color = self.object.config["fontColor"]["tencentweb"]
        # 字体颜色 公共DeepL
        self.deepl_color = self.object.config["fontColor"]["deepl"]
        # 字体颜色 公共谷歌
        self.google_color = self.object.config["fontColor"]["google"]
        # 字体颜色 公共彩云
        self.caiyun_web_color = self.object.config["fontColor"]["caiyun"]
        # 字体颜色 私人腾讯
        self.tencent_color = self.object.config["fontColor"]["tencent"]
        # 字体颜色 私人百度
        self.baidu_color = self.object.config["fontColor"]["baidu"]
        # 字体颜色 私人彩云
        self.caiyun_color = self.object.config["fontColor"]["caiyunPrivate"]
        # 原文颜色
        self.original_color = self.object.config["fontColor"]["original"]

        # 翻译界面透明度
        self.horizontal = self.object.config["horizontal"]
        # 翻译字体大小
        self.fontSize = self.object.config["fontSize"]
        # 翻译字体类型
        self.font_type = self.object.config["fontType"]
        # 字体样式开关
        self.font_color_type = eval(self.object.config["showColorType"])
        # 自动翻译间隔设定
        self.translate_speed = self.object.config["translateSpeed"]
        # 显示原文开关
        self.show_original_use = eval(self.object.config["showOriginal"])
        # 原文自动复制到剪贴板开关
        self.auto_clipboard_use = eval(self.object.config["showClipboard"])
        # 文字方向开关
        self.text_direction_use = eval(self.object.config["showTranslateRow"])
        # 文字换行开关
        self.branch_line_use = self.object.config["BranchLineUse"]
        # 翻译快捷键开关
        self.translate_hotkey_use = eval(self.object.config["showHotKey1"])
        # 范围快捷键开关
        self.range_hotkey_use = eval(self.object.config["showHotKey2"])
        # 自动登录开关
        self.auto_login_use = self.object.yaml["auto_login"]
        # 自动翻译图片刷新相似度
        self.image_refresh_score = self.object.config["imageSimilarity"]
        # 自动翻译文字刷新相似度
        self.text_refresh_score = self.object.config["textSimilarity"]

        # 团子翻译器开源地址
        self.dango_translator_url = "https://github.com/PantsuDango/Dango-Translator"
        # 团子b站个人主页
        self.dango_bilibili_url = "https://space.bilibili.com/227927/dynamic"
        # 在线教程地址
        self.tutorial_url = self.object.yaml["dict_info"]["tutorial_url"]
        # GT-Zhang个人主页
        self.gt_github_url = "https://github.com/GT-ZhangAcer"
        # C4a15Wh个人主页
        self.c44_github_url = "https://c4a15wh.cn/"
        # Cypas_Nya‭个人主页
        self.cy_github_url = "https://blog.ayano.top"
        # PaddleOCR项目主页
        self.PaddleOCR_github_url = "https://github.com/PaddlePaddle/PaddleOCR"
        # 更新日志
        self.bilibili_video_url = self.object.yaml["dict_info"]["bilibili_video"]
        # 显示消息栏
        self.show_statusbar_use = self.object.config["showStatusbarUse"]
        # 贴字翻译开关
        self.draw_image_use = self.object.config["drawImageUse"]
        # 隐藏范围快捷键开关
        self.hide_range_hotkey_use = self.object.config["showHotKey3"]
        # 是否全屏下置顶开关
        self.set_top_use = self.object.config["setTop"]


    # 获取节点信息
    def getNodeInfo(self) :

        # 重置
        self.node_info_comboBox.clear()
        # 展开全部节点信息
        self.node_info = eval(self.object.yaml["dict_info"]["ocr_node"])
        self.node_info_comboBox.setMaxVisibleItems(len(self.node_info)+1)

        # 自动模式
        url = self.object.yaml["dict_info"]["ocr_server"]
        sign, time_diff = utils.http.getOCR(url)
        model = self.node_info_comboBox.model()
        if sign :
            entry = QStandardItem("自动模式  {}ms".format(time_diff))
            entry.setForeground(QColor(Qt.green))
        else :
            entry = QStandardItem("自动模式  不可用")
            entry.setForeground(QColor(Qt.red))
        model.appendRow(entry)
        # 默认选中
        self.node_info_comboBox.setCurrentIndex(0)

        # 手动节点
        try:
            if type(self.node_info) != dict:
                self.node_info = {}
        except Exception:
            self.node_info = {}

        node_ip = re.findall(r"//(.+?)/", self.object.config["nodeURL"])[0]
        for node_name in self.node_info.keys() :
            url = re.sub(r"//.+?/", "//%s/"%self.node_info[node_name], url)
            # 校验节点有效性
            sign, time_diff = utils.http.getOCR(url)
            model = self.node_info_comboBox.model()

            if sign :
                text = "{}  {}ms".format(node_name, time_diff)
                entry = QStandardItem(text)
                entry.setForeground(QColor(Qt.green))
            else :
                text = "{}  不可用".format(node_name)
                entry = QStandardItem(text)
                entry.setForeground(QColor(Qt.red))
            model.appendRow(entry)

            if self.node_info[node_name] == node_ip :
                self.node_info_comboBox.setCurrentText(text)

        if not self.node_info.keys() :
            self.object.config["nodeURL"] = self.object.yaml["dict_info"]["ocr_server"]
        self.node_info_comboBox.currentIndexChanged.connect(self.changeNodeInfo)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x*self.rate),
                                 int(y*self.rate), int(w*self.rate),
                                 int(h*self.rate)))


    # 根据分辨率定义图标位置尺寸
    def customSetIconSize(self, object, w, h) :

        object.setIconSize(QSize(int(w * self.rate),
                                 int(h * self.rate)))


    # 控件加入阴影
    def setShadow(self, object, color) :

        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(5, 5)
        shadow.setBlurRadius(50)
        shadow.setColor(color)
        object.setGraphicsEffect(shadow)


    # 在线OCR选择节点
    def chooseOcrNode(self) :

        self.choose_ocr_node_ui.show()


    # 改变本地OCR开关状态
    def changeOfflineSwitch(self, checked) :

        if checked :
            if self.online_ocr_use == True :
                self.resetSwitch("onlineOCR")
            if self.baidu_ocr_use == True :
                self.resetSwitch("baiduOCR")
            self.offline_ocr_use = True
        else:
            self.offline_ocr_use = False


    # 改变在线OCR开关状态
    def changeOnlineSwitch(self, checked) :

        if checked :
            if self.offline_ocr_use == True :
                self.resetSwitch("offlineOCR")
            if self.baidu_ocr_use == True :
                self.resetSwitch("baiduOCR")
            self.online_ocr_use = True
        else:
            self.online_ocr_use = False


    # 改变百度OCR开关状态
    def changeBaiduSwitch(self, checked) :

        if checked :
            if self.offline_ocr_use == True :
                self.resetSwitch("offlineOCR")
            if self.online_ocr_use == True :
                self.resetSwitch("onlineOCR")
            self.baidu_ocr_use = True
        else :
            self.baidu_ocr_use = False


    # 改变百度OCR高精度开关状态
    def changeBaiduOcrHighPrecisionSwitch(self, checked):

        if checked :
            self.baidu_ocr_high_precision_use = True
        else:
            self.baidu_ocr_high_precision_use = False


    # 改变是否全屏下置顶开关状态
    def changeSetTopSwitch(self, checked):

        if checked:
            self.set_top_use = True
            utils.thread.createThread(self.object.hwndObj.run)
        else:
            self.set_top_use = False


    # 改变公共有道翻译开关状态
    def changeYoudaoSwitch(self, checked) :

        if checked :
            self.youdao_use = True
            self.translate_list.append("youdao")
            self.checkTranslaterUse()
        else:
            self.youdao_use = False
            self.translate_list.remove("youdao")


    # 改变公共百度翻译开关状态
    def changeBaiduWebSwitch(self, checked) :

        if checked :
            self.baidu_web_use = True
            self.translate_list.append("baidu")
            self.checkTranslaterUse()
        else:
            self.baidu_web_use = False
            self.translate_list.remove("baidu")


    # 改变公共腾讯翻译开关状态
    def changeTencentWebSwitch(self, checked) :

        if checked :
            self.tencent_web_use = True
            self.translate_list.append("tencent")
            self.checkTranslaterUse()
        else:
            self.tencent_web_use = False
            self.translate_list.remove("tencent")


    # 改变公共DeepL翻译开关状态
    def changeDeepLSwitch(self, checked) :

        if checked :
            self.deepl_use = True
            self.translate_list.append("deepl")
            self.checkTranslaterUse()
        else:
            self.deepl_use = False
            self.translate_list.remove("deepl")


    # 改变公共Google翻译开关状态
    def changeGoogleSwitch(self, checked) :

        if checked :
            self.google_use = True
            self.translate_list.append("google")
            self.checkTranslaterUse()
        else:
            self.google_use = False
            self.translate_list.remove("google")


    # 改变公共彩云翻译开关状态
    def changeCaiyunWebSwitch(self, checked) :

        if checked :
            self.caiyun_web_use = True
            self.translate_list.append("caiyun")
            self.checkTranslaterUse()
        else:
            self.caiyun_web_use = False
            self.translate_list.remove("caiyun")


    # 改变私人腾讯翻译开关状态
    def changeTencentSwitch(self, checked) :

        if checked :
            self.tencent_use = True
            self.translate_list.append("tencent_private")
            self.checkTranslaterUse()
        else:
            self.tencent_use = False
            self.translate_list.remove("tencent_private")


    # 改变私人百度翻译开关状态
    def changeBaiduTranslaterSwitch(self, checked) :

        if checked :
            self.baidu_use = True
            self.translate_list.append("baidu_private")
            self.checkTranslaterUse()
        else:
            self.baidu_use = False
            self.translate_list.remove("baidu_private")


    # 改变私人彩云翻译开关状态
    def changeCaiyunSwitch(self, checked) :

        if checked :
            self.caiyun_use = True
            self.translate_list.append("caiyun_private")
            self.checkTranslaterUse()
        else:
            self.caiyun_use = False
            self.translate_list.remove("caiyun_private")


    # 改变字体样式开关状态
    def changeFontColorTypeSwitch(self, checked) :

        if checked :
            self.font_color_type = True
        else:
            self.font_color_type = False


    # 改变显示原文开关状态
    def changeShowOriginalSwitch(self, checked) :

        if checked :
            self.show_original_use = True
        else:
            self.show_original_use = False


    # 改变贴字翻译开关状态
    def changeDrawImageSwitch(self, checked) :

        if checked :
            self.draw_image_use = True
        else:
            self.draw_image_use = False


    # 改变显示消息栏开关状态
    def changeShowStatusbarSwitch(self, checked):

        if checked:
            self.show_statusbar_use = True
            self.object.translation_ui.statusbar_sign = True
            self.object.translation_ui.statusbar.show()
            self.object.translation_ui.textAreaChanged()
        else:
            self.show_statusbar_use = False
            self.object.translation_ui.statusbar_sign = False
            self.object.translation_ui.statusbar.hide()
            self.object.translation_ui.textAreaChanged()


    # 改变自动复制剪贴板开关状态
    def changeAutoCopyOriginalSwitch(self, checked) :

        if checked :
            self.auto_clipboard_use = True
        else:
            self.auto_clipboard_use = False


    # 改变文字换行开关状态
    def changeBranchLineSwitch(self, checked):

        if checked :
            self.branch_line_use = True
        else:
            self.branch_line_use = False


    # 改变文字方向开关状态
    def changeTextDirectionSwitch(self, checked) :

        if checked :
            self.text_direction_use = True
        else:
            self.text_direction_use = False


    # 改变翻译热键开关状态
    def changeTranslateHotkeySwitch(self, checked) :

        if checked :
            self.translate_hotkey_use = True
        else:
            self.translate_hotkey_use = False


    # 改变范围热键开关状态
    def changeRangeHotkeySwitch(self, checked) :

        if checked :
            self.range_hotkey_use = True
        else:
            self.range_hotkey_use = False


    # 改变隐藏范围热键开关状态
    def changeHideRangeHotkeySwitch(self, checked):

        if checked:
            self.hide_range_hotkey_use = True
        else:
            self.hide_range_hotkey_use = False


    # 改变自动登录开关状态
    def changeAutoLoginSwitch(self, checked) :

        if checked :
            self.auto_login_use = True
        else:
            self.auto_login_use = False


    # 重置开关状态
    def resetSwitch(self, switch_type) :

        if switch_type == "offlineOCR" :
            self.offline_ocr_switch.mousePressEvent(1)
            self.offline_ocr_switch.updateValue()
        elif switch_type == "onlineOCR" :
            self.online_ocr_switch.mousePressEvent(1)
            self.online_ocr_switch.updateValue()
        elif switch_type == "baiduOCR" :
            self.baidu_ocr_switch.mousePressEvent(1)
            self.baidu_ocr_switch.updateValue()


    # 运行本地OCR
    def runOfflineOCR(self) :

        # 检查端口是否被占用
        if utils.port.detectPort(self.object.yaml["port"]) :
            utils.message.MessageBox("运行失败",
                                     "本地OCR已启动, 请不要重复运行!     ")
        else :
            try :
                # 启动本地OCR
                os.startfile(self.object.yaml["ocr_cmd_path"])
            except Exception :
                self.logger.error(format_exc())
                utils.message.MessageBox("运行失败",
                                         "本地OCR运行失败, 原因:\n%s     "%format_exc())


    # 测试本地OCR
    def testOfflineOCR(self) :

        # 检查端口是否被占用
        if not utils.port.detectPort(self.object.yaml["port"]) :
            utils.message.MessageBox("测试失败",
                                     "本地OCR还没运行成功，不可以进行测试     \n"
                                     "请先启动本地OCR, 并保证其运行正常")
        else :
            utils.test.testOfflineOCR(self.object)


    # 打开私人腾讯翻译教程
    def openTencentTutorial(self):

        try :
            url = self.object.yaml["dict_info"]["tencent_tutorial"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开公共翻译教程
    def openPublicTransTutorial(self):

        try:
            url = self.object.yaml["dict_info"]["tutorial_public_trans"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())


    # 打开私人百度翻译教程
    def openBaiduTutorial(self):

        try:
            url = self.object.yaml["dict_info"]["baidu_tutorial"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())


    # 打开私人彩云翻译教程
    def openCaiyunTutorial(self):

        try:
            url = self.object.yaml["dict_info"]["caiyun_tutorial"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())


    # 打开本地OCR教程
    def openOfflineOCRTutorial(self) :

        try :
            url = self.object.yaml["dict_info"]["tutorials_offline_ocr"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开guihub项目地址
    def openGithubproject(self):

        try :
            webbrowser.open(self.dango_translator_url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开软件首页
    def openHomePage(self):

        try :
            url = self.object.yaml["dict_info"]["dango_home_page"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开在线教程地址
    def openTutorial(self):

        try :
            webbrowser.open(self.tutorial_url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开添加作者地址
    def oepnBilibili(self):

        try :
            webbrowser.open(self.dango_bilibili_url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开更新日志地址
    def openBilibiliVideo(self):

        try :
            webbrowser.open(self.bilibili_video_url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开PaddleOCR项目地址
    def openPaddleOCR(self):

        try :
            webbrowser.open(self.PaddleOCR_github_url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开Gt-Zhang项目地址
    def openGT(self):

        try :
            webbrowser.open(self.gt_github_url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开c44项目地址
    def openC44(self):

        try :
            webbrowser.open(self.c44_github_url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开Cy项目地址
    def openCy(self):

        try :
            webbrowser.open(self.cy_github_url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 打开在线OCR教程地址
    def openOnlineOCRTutorials(self) :

        try :
            url = self.object.yaml["dict_info"]["tutorials_online_ocr"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())


    # 打开百度OCR教程地址
    def openBaiduOCRTutorials(self):

        try:
            url = self.object.yaml["dict_info"]["tutorials_baidu_ocr"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())


    # 打开团子在线OCR购买
    def openDangoBuyPage(self):

        try :
            ocr_login_html = self.object.yaml["dict_info"]["ocr_login_html"]
            token = self.object.config["DangoToken"]
            ocr_buy_html_base64 = self.object.yaml["dict_info"]["ocr_buy_html_base64"]

            url = "%s?token=%s&jump=%s"%(ocr_login_html, token, ocr_buy_html_base64)
            webbrowser.open(url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())


    # 翻译源字体颜色
    def ChangeTranslateColor(self, translate_type, color_str) :

        color = QColorDialog.getColor(QColor(color_str), None, "设定所选翻译显示时的颜色")
        if not color.isValid() :
            return

        if translate_type == "youdao" :
            self.youdao_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.youdao_color = color.name()
        elif translate_type == "baidu" :
            self.baidu_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.baidu_web_color = color.name()
        elif translate_type == "tencent" :
            self.tencent_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.tencent_web_color = color.name()
        elif translate_type == "deepl" :
            self.deepl_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.deepl_color = color.name()
        elif translate_type == "google" :
            self.google_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.google_color = color.name()
        elif translate_type == "caiyun" :
            self.caiyun_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.caiyun_web_color = color.name()
        elif translate_type == "tencent_private" :
            self.tencent_private_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.tencent_color = color.name()
        elif translate_type == "baidu_private" :
            self.baidu_private_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.baidu_color = color.name()
        elif translate_type == "caiyun_private" :
            self.caiyun_private_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.caiyun_color = color.name()
        elif translate_type == "original" :
            self.original_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.original_color = color.name()


    # 说明窗口
    def showDesc(self, message_type) :

        self.desc_ui = ui.desc.Desc(self.object)

        # OCR说明
        if message_type == "OCR" :
            self.desc_ui.setWindowTitle("OCR说明")
            self.desc_ui.desc_text.append("\n首先区别OCR和翻译是两个模块。")
            self.desc_ui.desc_text.append("\nOCR即为文字识别技术, 用于提取图片内要翻译的文字.")
            self.desc_ui.desc_text.append("\n翻译器通过对所框选的范围进行截图, 然后利用OCR将截图内要翻译的文字识别出来, 再发送给翻译模块翻译。")

        # 本地OCR说明
        elif message_type == "offlineOCR" :
            self.desc_ui.setWindowTitle("本地OCR说明")
            self.desc_ui.desc_text.append("\n特性: \n依赖自身CPU性能, CPU性能越高，识别速度越快.")
            self.desc_ui.desc_text.append("识别精度一般.")
            self.desc_ui.desc_text.append("\n优点:\n1. 无额度限制, 完全免费, 可无限次使用;")
            self.desc_ui.desc_text.append("\n缺点:\n1. 对电脑配置较低的用户不友好, 可能会导致电脑很卡;")
            self.desc_ui.desc_text.append("2. 可能会因为环境配置问题导致安装失败, 不支持10年以前发行的CPU;")
            self.desc_ui.desc_text.append("\n详细使用方式见教程.")

        # 在线OCR说明
        elif message_type == "onlineOCR":
            self.desc_ui.setWindowTitle("在线OCR说明")
            self.desc_ui.desc_text.append("\n特性: \n团子在大佬们的帮助下自行搭建的OCR在线服务.")
            self.desc_ui.desc_text.append("识别精度较好.")
            self.desc_ui.desc_text.append("\n优点:\n1. 不消耗电脑配置, 仅需联网;")
            self.desc_ui.desc_text.append("2. 性价比高, 服务期内无使用次数限制;")
            self.desc_ui.desc_text.append("\n缺点:\n1. 不免费, 需要氪点金金;")
            self.desc_ui.desc_text.append("\n详细使用方式见教程.")

        # 百度OCR说明
        elif message_type == "baiduOCR":
            self.desc_ui.setWindowTitle("百度OCR说明")
            self.desc_ui.desc_text.append("\n特性: \n百度智能云的OCR服务.")
            self.desc_ui.desc_text.append("识别精度优秀.")
            self.desc_ui.desc_text.append("\n优点:\n1. 不消耗电脑配置, 仅需联网;")
            self.desc_ui.desc_text.append("\n缺点:\n1. 使用次数有限制;")
            self.desc_ui.desc_text.append("2. 不免费, 且价格较贵;")
            self.desc_ui.desc_text.append("\n详细使用方式见教程.")

        # 公共翻译说明
        elif message_type == "publicTranslate" :
            self.desc_ui.setWindowTitle("公共翻译说明")
            self.desc_ui.desc_text.append("\n没有次数限制, 不需要注册, 可直接使用, 但不保证使用稳定性, 可能会抽风.")
            self.desc_ui.desc_text.append('\n使用需要电脑装有"最新版本的" Chorem(谷歌)浏览器、Firefox(火狐)浏览器、Edga(微软)浏览器 至少一款.')
            self.desc_ui.desc_text.append('\n翻译器原理上, 是通过后台启动相应的浏览器, 自动打开翻译网站去实现翻译.')
            self.desc_ui.desc_text.append("\n详细使用方式见教程.")

        # 私人翻译说明
        elif message_type == "privateTranslate" :
            self.desc_ui.setWindowTitle("私人翻译说明")
            self.desc_ui.desc_text.append("\n有次数限制, 使用前需要注册, 但使用稳定性, 基本上不会抽风.")
            self.desc_ui.desc_text.append("\n翻译器原理上, 是通过请求相应的云API接口去获取翻译结果")
            self.desc_ui.desc_text.append("\n详细使用方式见教程.")

        # 翻译框透明度说明
        elif message_type == "horizontalSlider" :
            self.desc_ui.setWindowTitle("翻译框透明度说明")
            self.desc_ui.desc_text.append("\n用于调节显示翻译结果的翻译框透明度.")
            self.desc_ui.desc_text.append("数值0为全透明")
            self.desc_ui.desc_text.append("数值100为完全不透明")

        # 字体样式设定说明
        elif message_type == "fontType" :
            self.desc_ui.setWindowTitle("字体样式设定说明")
            self.desc_ui.desc_text.append("描边字体为字体中间镂空白底, 描边带颜色:\n")
            self.desc_ui.desc_text.insertHtml('<img src={} width="{}" >'.format(HOLLOW_IMG_PATH, 245*self.rate))
            self.desc_ui.desc_text.append("\n实心字体为纯色字体:\n")
            self.desc_ui.desc_text.insertHtml('<img src="{}" width="{}" >'.format(SOLID_IMG_PATH, 245*self.rate))
            self.desc_ui.desc_text.append("\n顺便一提团子喜欢描边字体~")

        # 自动翻译设定说明
        elif message_type == "autoSpeed" :
            self.desc_ui.setWindowTitle("自动翻译设定说明")
            self.desc_ui.desc_text.append("\n自动翻译模式下, 每隔该设定时间, 便会检测一次所框的范围内图像是否发生变化, 若发生变化则识别并刷新翻译")

        # 显示原文说明
        elif message_type == "showOriginal" :
            self.desc_ui.setWindowTitle("显示原文说明")
            self.desc_ui.desc_text.append("\n开启后, 会将OCR识别到的原文显示在翻译框.")

        # 文字方向说明
        elif message_type == "textDirection":
            self.desc_ui.setWindowTitle("文字方向说明")
            self.desc_ui.desc_text.append("\n正常都是横向的呢, 竖向多用于漫画翻译的情况.")

        # 图像相似度说明
        elif message_type == "imageRefresh":
            self.desc_ui.setWindowTitle("图像相似度说明")
            self.setTextColor(self.desc_ui.desc_text, "#FF0000", "如果看不懂请不要轻易修改此参数, 建议值为98.")
            self.desc_ui.desc_text.append("\n自动翻译模式下, 每隔设定的时间间隔, 会重新检测范围区域的图像. "
                                          "只有当当前图像, 与前一次图像比较的相似度小于该设定的值时, 才会重新调取OCR识别该图像.")
            self.desc_ui.desc_text.append("\n如果觉得OCR频繁重复识别, 翻译框出现了'闪烁'的话, 可以调低此参数.")

        # 文字相似度说明
        elif message_type == "textRefresh":
            self.desc_ui.setWindowTitle("文字相似度说明")
            self.setTextColor(self.desc_ui.desc_text, "#FF0000", "如果看不懂请不要轻易修改此参数, 建议值为90.")
            self.desc_ui.desc_text.append("\n自动翻译模式下, 每隔设定的时间间隔, OCR识别结果刷新后. "
                                          "如果当前OCR识别出的原文, 与前一次识别的原文比较, 其相似度小于该设定的值时, "
                                          "才会重新调取翻译并刷新至翻译界面.")
            self.desc_ui.desc_text.append("\n如果觉得频繁重复翻译, 翻译框出现了'闪烁'的话, 可以调低此参数.")

        # QQ交流群
        elif message_type == "qqGroup":
            self.desc_ui.setWindowTitle("加入交流群")
            self.desc_ui.desc_text.insertHtml('<img src="{}" width="{}" height="{}">'.format(QQ_GROUP_PATH, 245*self.rate, 295*self.rate))

        # 文字换行
        elif message_type == "branchLine" :
            self.desc_ui.setWindowTitle("文字换行说明")
            self.setTextColor(self.desc_ui.desc_text, "#FF0000", "如果看不懂请不要打开此开关.")
            self.desc_ui.desc_text.append("\n会将识别到的原文换行后再翻译, 可能会出现断句错误情况")

        # 原文颜色
        elif message_type == "originalColor" :
            self.desc_ui.setWindowTitle("原文颜色说明")
            self.desc_ui.desc_text.append("\n控制翻译界面显示的原文, 和一切错误说明, 通知信息的文字颜色")

        # 显示消息栏说明
        elif message_type == "showStatusbar" :
            self.desc_ui.setWindowTitle("翻译时间说明")
            self.desc_ui.desc_text.append("控制翻译界面底部消息栏是否显示\n")
            self.desc_ui.desc_text.append("若显示\n")
            self.desc_ui.desc_text.insertHtml('<img src={} width="{}" >'.format(OPEN_STATUSBAR_IMG_PATH, 245*self.rate))
            self.desc_ui.desc_text.append("\n若屏蔽:\n")
            self.desc_ui.desc_text.insertHtml('<img src="{}" width="{}" >'.format(CLOSE_STATUSBAR_IMG_PATH, 245*self.rate))

        # 贴字翻译
        elif message_type == "drawImage":
            self.desc_ui.setWindowTitle("贴字翻译说明")
            self.desc_ui.desc_text.append("\n开启后会将翻译结果直接贴在截图区域上, 目前仅支持于在线OCR")

        # 贴字翻译
        elif message_type == "setTop":
            self.desc_ui.setWindowTitle("全屏下置顶说明")
            self.desc_ui.desc_text.append("\n如果需要游玩全屏游戏, 则打开此开关, 否则平时请保持关闭")

        self.desc_ui.show()


    # 设置QText插入文字的颜色
    def setTextColor(self, object, color, text) :

        object.setTextColor(QColor(color))
        object.append(text)
        object.setTextColor(QColor(self.color_2))


    # 密钥窗口
    def showKey(self, key_type) :

        # 百度OCR
        if key_type == "baiduOCR" :
            self.key_ui.setWindowTitle("百度OCR - 密钥编辑")
            self.key_ui.baidu_ocr_key_textEdit.show()
            self.key_ui.baidu_ocr_secret_textEdit.show()

        # 私人腾讯翻译
        elif key_type == "tencentTranslate" :
            self.key_ui.setWindowTitle("私人腾讯翻译 - 密钥编辑")
            self.key_ui.tencent_private_key_textEdit.show()
            self.key_ui.tencent_private_secret_textEdit.show()

        # 私人腾讯翻译
        elif key_type == "baiduTranslate" :
            self.key_ui.setWindowTitle("私人百度翻译 - 密钥编辑")
            self.key_ui.baidu_private_key_textEdit.show()
            self.key_ui.baidu_private_secret_textEdit.show()

        # 私人彩云翻译
        elif key_type == "caiyunTranslate" :
            self.key_ui.setWindowTitle("私人彩云翻译 - 密钥编辑")
            self.key_ui.caiyun_private_key_textEdit.show()

        self.key_ui.show()


    # 翻译框透明度
    def changeHorizontal(self) :

        self.horizontal = self.horizontal_slider.value()
        self.object.translation_ui.horizontal = self.horizontal
        self.horizontal_slider_label.setText("{}%".format(self.horizontal))
        if self.horizontal == 0 :
            self.horizontal = 1
        # 重置翻译界面
        self.object.translation_ui.translate_text.setStyleSheet("border-width:0;\
                                                                 border-style:outset;\
                                                                 border-top:0px solid #e8f3f9;\
                                                                 color:white;\
                                                                 font-weight: bold;\
                                                                 background-color:rgba(62, 62, 62, %s)"
                                                                %(self.horizontal/100))
        self.object.translation_ui.temp_text.setStyleSheet("border-width:0;\
                                                            border-style:outset;\
                                                            border-top:0px solid #e8f3f9;\
                                                            color:white;\
                                                            font-weight: bold;\
                                                            background-color:rgba(62, 62, 62, %s)"
                                                           %(self.horizontal/100))
        # 重置状态栏界面
        self.object.translation_ui.statusbar.setStyleSheet("font: 10pt '华康方圆体W7';"
                                                           "color: white;"
                                                           "background-color: rgba(62, 62, 62, 0.1)")


    # 翻译框透明度调整时同屏显示透明框
    def eventFilter(self, object, event):

        if object == self.horizontal_slider :
            if event.type() == QEvent.Enter :
                self.object.translation_ui.show()

            if event.type() == QEvent.Leave :
                self.object.translation_ui.hide()

            return QWidget.eventFilter(self, object, event)


    # 设定字体样式
    def getFontType(self, text) :

        self.font_type = text


    # 设定快捷键
    def setHotKey(self, key_type) :

        # 快捷键界面
        self.hotkey_ui = ui.hotkey.HotKey(self.object)

        if key_type == "translate" :
            self.hotkey_ui.setWindowTitle("设定翻译快捷键")
            self.hotkey_ui.comboBox_1.setCurrentText(self.object.config["translateHotkeyValue1"])
            self.hotkey_ui.comboBox_2.setCurrentText(self.object.config["translateHotkeyValue2"])
            self.hotkey_ui.sure_button.clicked.connect(lambda: self.hotkey_ui.sure(key_type))

        if key_type == "range" :
            self.hotkey_ui.setWindowTitle("设定范围快捷键")
            self.hotkey_ui.comboBox_1.setCurrentText(self.object.config["rangeHotkeyValue1"])
            self.hotkey_ui.comboBox_2.setCurrentText(self.object.config["rangeHotkeyValue2"])
            self.hotkey_ui.sure_button.clicked.connect(lambda: self.hotkey_ui.sure(key_type))

        if key_type == "hideRange" :
            self.hotkey_ui.setWindowTitle("设定隐藏范围快捷键")
            self.hotkey_ui.comboBox_1.setCurrentText(self.object.config["hideRangeHotkeyValue1"])
            self.hotkey_ui.comboBox_2.setCurrentText(self.object.config["hideRangeHotkeyValue2"])
            self.hotkey_ui.sure_button.clicked.connect(lambda: self.hotkey_ui.sure(key_type))

        self.hotkey_ui.show()


    # 校验翻译开关状态
    def checkTranslaterUse(self) :

        if len(self.translate_list) <= 3 :
            return

        for val in self.translate_list :
            if val == "baidu" :
                self.baidu_switch.mousePressEvent(1)
                self.baidu_switch.updateValue()

            elif val == "tencent" :
                self.tencent_switch.mousePressEvent(1)
                self.tencent_switch.updateValue()

            elif val == "caiyun" :
                self.caiyun_switch.mousePressEvent(1)
                self.caiyun_switch.updateValue()

            elif val == "deepl" :
                self.deepl_switch.mousePressEvent(1)
                self.deepl_switch.updateValue()

            elif val == "google" :
                self.google_switch.mousePressEvent(1)
                self.google_switch.updateValue()

            elif val == "youdao" :
                self.youdao_switch.mousePressEvent(1)
                self.youdao_switch.updateValue()

            elif val == "tencent_private" :
                self.tencent_private_switch.mousePressEvent(1)
                self.tencent_private_switch.updateValue()

            elif val == "baidu_private" :
                self.baidu_private_switch.mousePressEvent(1)
                self.baidu_private_switch.updateValue()

            elif val == "caiyun_private" :
                self.caiyun_private_switch.mousePressEvent(1)
                self.caiyun_private_switch.updateValue()

            if len(self.translate_list) <= 3 :
                break


    # 重置翻译引擎
    def resetWebdriver(self) :

        # 重置语音模块
        utils.thread.createThread(self.object.translation_ui.sound.refreshWeb)

        # 重置开关
        self.object.translation_ui.webdriver1.web_type = ""
        self.object.translation_ui.webdriver2.web_type = ""
        self.object.translation_ui.webdriver3.web_type = ""
        self.object.translation_ui.webdriver1.open_sign = False
        self.object.translation_ui.webdriver2.open_sign = False
        self.object.translation_ui.webdriver3.open_sign = False

        # 刷新翻译
        translater_list = ["youdaoUse", "baiduwebUse", "tencentwebUse", "deeplUse", "googleUse", "caiyunUse"]
        for val in translater_list :
            if self.object.config[val] == "False" :
                continue
            web_type = val.replace("Use", "").replace("web", "")
            # 刷新翻译引擎1
            if not self.object.translation_ui.webdriver1.web_type :
                self.object.translation_ui.webdriver1.web_type = web_type
                utils.thread.createThread(self.object.translation_ui.webdriver1.openWeb, web_type)

            # 刷新翻译引擎2
            elif not self.object.translation_ui.webdriver2.web_type :
                self.object.translation_ui.webdriver2.web_type = web_type
                utils.thread.createThread(self.object.translation_ui.webdriver2.openWeb, web_type)

            # 刷新翻译引擎3
            elif not self.object.translation_ui.webdriver3.web_type :
                self.object.translation_ui.webdriver3.web_type = web_type
                utils.thread.createThread(self.object.translation_ui.webdriver3.openWeb, web_type)


    # 改变节点
    def changeNodeInfo(self) :

        node_name = self.node_info_comboBox.currentText().split("  ")[0]
        if node_name == "自动模式":
            node_url = self.object.yaml["dict_info"]["ocr_server"]
        else:
            node_url = re.sub(r"//.+?/", "//%s/" % self.node_info[node_name], self.object.yaml["dict_info"]["ocr_server"])
        self.object.config["nodeURL"] = node_url


    # 退出前保存设置
    def saveConfig(self) :

        # OCR开关
        self.object.config["offlineOCR"] = self.offline_ocr_use
        self.object.config["onlineOCR"] = self.online_ocr_use
        self.object.config["baiduOCR"] = self.baidu_ocr_use

        # 翻译语种
        if self.language_comboBox.currentIndex() == 1 :
            self.object.config["language"] = "ENG"
        elif self.language_comboBox.currentIndex() == 2 :
            self.object.config["language"] = "KOR"
        else:
            self.object.config["language"] = "JAP"

        # 公共有道翻译开关
        self.object.config["youdaoUse"] = str(self.youdao_use)
        # 公共百度翻译开关
        self.object.config["baiduwebUse"] = str(self.baidu_web_use)
        # 公共腾讯翻译开关
        self.object.config["tencentwebUse"] = str(self.tencent_web_use)
        # 公共DeepL翻译开关
        self.object.config["deeplUse"] = str(self.deepl_use)
        # 公共谷歌翻译开关
        self.object.config["googleUse"] = str(self.google_use)
        # 公共彩云翻译开关
        self.object.config["caiyunUse"] = str(self.caiyun_web_use)
        # 私人腾讯翻译开关
        self.object.config["tencentUse"] = str(self.tencent_use)
        # 私人百度翻译开关
        self.object.config["baiduUse"] = str(self.baidu_use)
        # 私人彩云翻译开关
        self.object.config["caiyunPrivateUse"] = str(self.caiyun_use)

        # 字体颜色 公共有道
        self.object.config["fontColor"]["youdao"] = self.youdao_color
        # 字体颜色 公共百度
        self.object.config["fontColor"]["baiduweb"] = self.baidu_web_color
        # 字体颜色 公共腾讯
        self.object.config["fontColor"]["tencentweb"] = self.tencent_web_color
        # 字体颜色 公共DeepL
        self.object.config["fontColor"]["deepl"] = self.deepl_color
        # 字体颜色 公共谷歌
        self.object.config["fontColor"]["google"] = self.google_color
        # 字体颜色 公共彩云
        self.object.config["fontColor"]["caiyun"] = self.caiyun_web_color
        # 字体颜色 私人腾讯
        self.object.config["fontColor"]["tencent"] = self.tencent_color
        # 字体颜色 私人百度
        self.object.config["fontColor"]["baidu"] = self.baidu_color
        # 字体颜色 私人彩云
        self.object.config["fontColor"]["caiyunPrivate"] = self.caiyun_color
        # 原文颜色
        self.object.config["fontColor"]["original"] = self.original_color

        # 翻译框透明度
        self.object.config["horizontal"] = self.horizontal
        if self.horizontal == 0 :
            self.horizontal = 1
        # 翻译字体大小
        self.object.config["fontSize"] = self.fontSize_spinBox.value()
        # 翻译字体类型
        self.object.config["fontType"] = self.font_type
        # 字体样式开关
        self.object.config["showColorType"] = str(self.font_color_type)
        # 自动翻译间隔
        self.object.config["translateSpeed"] = self.auto_speed_spinBox.value()
        # 显示原文开关
        self.object.config["showOriginal"] = str(self.show_original_use)
        # 原文自动复制到剪贴板开关
        self.object.config["showClipboard"] = str(self.auto_clipboard_use)
        # 文字方向
        self.object.config["showTranslateRow"] = str(self.text_direction_use)
        # 文字换行
        self.object.config["BranchLineUse"] = self.branch_line_use
        # 翻译快捷键开关
        self.object.config["showHotKey1"] = str(self.translate_hotkey_use)
        # 范围快捷键开关
        self.object.config["showHotKey2"] = str(self.range_hotkey_use)
        # 自动翻译图片刷新相似度
        self.object.config["imageSimilarity"] = self.image_refresh_spinBox.value()
        # 自动翻译文字刷新相似度
        self.object.config["textSimilarity"] = self.text_refresh_spinBox.value()
        # 自动登录开关
        self.object.yaml["auto_login"] = self.auto_login_use
        # 百度OCR高精度开关
        self.object.config["OCR"]["highPrecision"] = self.baidu_ocr_high_precision_use
        # 显示消息栏
        self.object.config["showStatusbarUse"] = self.show_statusbar_use
        # 贴字翻译开关
        self.object.config["drawImageUse"] = self.draw_image_use
        if not self.draw_image_use or not self.online_ocr_use :
            self.object.range_ui.draw_label.hide()
        # 隐藏范围快捷键开关
        self.object.config["showHotKey3"] = str(self.hide_range_hotkey_use)
        # 是否全屏下置顶开关
        self.object.config["setTop"] = self.set_top_use


    # 注册新快捷键
    def registerHotKey(self) :

        hotkey_map = {
            "ctrl": "control",
            "win": "super"
        }
        self.object.translation_ui.translate_hotkey_value1 = hotkey_map.get(self.object.config["translateHotkeyValue1"], self.object.config["translateHotkeyValue1"])
        self.object.translation_ui.translate_hotkey_value2 = hotkey_map.get(self.object.config["translateHotkeyValue2"], self.object.config["translateHotkeyValue2"])
        self.object.translation_ui.range_hotkey_value1 = hotkey_map.get(self.object.config["rangeHotkeyValue1"], self.object.config["rangeHotkeyValue1"])
        self.object.translation_ui.range_hotkey_value2 = hotkey_map.get(self.object.config["rangeHotkeyValue2"], self.object.config["rangeHotkeyValue2"])
        self.object.translation_ui.hide_range_hotkey_value1 = hotkey_map.get(self.object.config["hideRangeHotkeyValue1"], self.object.config["hideRangeHotkeyValue1"])
        self.object.translation_ui.hide_range_hotkey_value2 = hotkey_map.get(self.object.config["hideRangeHotkeyValue2"], self.object.config["hideRangeHotkeyValue2"])

        # 注册新翻译快捷键
        if self.translate_hotkey_use :
            self.object.translation_ui.translate_hotkey.register((self.object.translation_ui.translate_hotkey_value1,
                                                                  self.object.translation_ui.translate_hotkey_value2),
                                                                  callback=lambda x: utils.thread.createThread(self.object.translation_ui.startTranslater))

        # 注册新范围快捷键
        if self.range_hotkey_use :
            self.object.translation_ui.range_hotkey.register((self.object.translation_ui.range_hotkey_value1,
                                                              self.object.translation_ui.range_hotkey_value2),
                                                              callback=lambda x: self.object.translation_ui.range_hotkey_sign.emit(True))

        # 注册新隐藏范围快捷键
        if self.hide_range_hotkey_use :
            self.object.translation_ui.hide_range_hotkey.register((self.object.translation_ui.hide_range_hotkey_value1,
                                                                   self.object.translation_ui.hide_range_hotkey_value2),
                                                                   callback=lambda x: self.object.translation_ui.hide_range_sign.emit(True))

    # 窗口显示信号
    def showEvent(self, e):

        # 如果处于自动模式下则暂停
        if self.object.translation_ui.translate_mode :
            self.object.translation_ui.stop_sign = True


    # 窗口关闭处理
    def closeEvent(self, event) :

        # 保存设置
        self.saveConfig()
        # 保存本地配置
        utils.config.saveConfig(self.object.yaml, self.logger)
        # 注册新快捷键
        utils.thread.createThread(self.registerHotKey)
        # 重置翻译引擎
        self.resetWebdriver()
        # 刷新百度OCR的AccessToken
        if self.baidu_ocr_use :
            translator.ocr.baidu.getAccessToken(self.object)
        # 设置上传云端
        utils.thread.createThread(utils.config.postSaveSettin, self.object)

        self.hide()
        self.object.translation_ui.show()
        if self.object.range_ui.show_sign == True :
            self.object.range_ui.show()