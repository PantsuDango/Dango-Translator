import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from traceback import format_exc
import qtawesome
import webbrowser
import base64
import os
import re

import utils.thread
import utils.config
import utils.message
import utils.port
import utils.test
import utils.http
import utils.offline_ocr

from ui import image
import ui.static.icon
import ui.static.background
import ui.hotkey
import ui.switch
import ui.desc
import ui.key
import ui.progress_bar
import translator.ocr.baidu
import translator.all


BG_IMAGE_PATH = "./config/background/settin.jpg"


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
        self.setWindowTitle("团子翻译器 Ver%s - 设置         当前登录用户: %s"%(
            self.object.yaml["version"], self.object.yaml["user"]))
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)

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
                                      %(70*self.rate, BG_IMAGE_PATH, self.color_2, 6.66*self.rate, self.color_2,
                                       self.color_2, 8.66*self.rate, 4*self.rate, 13.33*self.rate, 13.33*self.rate,
                                       33.33*self.rate, 33.33*self.rate, -13.33*self.rate, -13.33*self.rate,
                                       -13.33*self.rate, -13.33*self.rate, 8.66*self.rate, 4*self.rate,
                                       10*self.rate, self.color_2))

        # 选项卡
        self.setTabOne()
        self.setTabTwo()
        self.setTabThree()
        self.setTabFour()
        self.setTabFive()
        self.setTabSix()

        # 背景图pixiv标签
        label = QLabel(self)
        self.customSetGeometry(label, 630, 400, 200, 15)
        label.setText("背景图 pixiv id: %s"%self.object.yaml["dict_info"]["bg_pixiv_id"])
        label.setStyleSheet("font-size: 9pt; color: %s"%self.color_2)


    # OCR设定标签页
    def setTabOne(self) :

        # 选项卡界面
        self.tab_1 = QWidget()
        self.tab_widget.addTab(self.tab_1, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_1), " 识别设定")

        # 此Label用于雾化顶部工具栏的背景图
        label = QLabel(self.tab_1)
        label.setGeometry(QRect(0, 0, self.window_width, 35*self.rate))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 选项卡图标
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_1), ui.static.icon.OCR_ICON)

        # 顶部工具栏
        self.ocr_tab_widget = QTabWidget(self.tab_1)
        self.ocr_tab_widget.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        self.ocr_tab_widget.setTabPosition(QTabWidget.North)
        self.ocr_tab_widget.setStyleSheet("QTabBar:tab { min-height: %dpx; min-width: %dpx;"
                                                        "background: rgba(255, 255, 255, 1);}"
                                                        "QTabBar:tab:selected { background: rgba(62, 62, 62, 0.07); }"
                                                        "QTabWidget::pane { border-image: none; }"
                                                        %(35*self.rate, 120*self.rate))

        # 竖向分割线
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 0, 0, 1, 420)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.1);")

        # 在线OCR页签
        online_OCR_tab = QWidget()
        self.ocr_tab_widget.addTab(online_OCR_tab, "")
        self.ocr_tab_widget.setTabText(self.ocr_tab_widget.indexOf(online_OCR_tab), "在线OCR")

        # 在线OCR页签图标
        self.ocr_tab_widget.setTabIcon(self.ocr_tab_widget.indexOf(online_OCR_tab), ui.static.icon.ONLINE_OCR_ICON)

        # 横向分割线
        label = QLabel(online_OCR_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 此Label用于雾化在线OCR页签的背景图
        label = QLabel(online_OCR_tab)
        label.setGeometry(QRect(0, 0, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 本地OCR页签
        offline_OCR_tab = QWidget()
        self.ocr_tab_widget.addTab(offline_OCR_tab, "")
        self.ocr_tab_widget.setTabText(self.ocr_tab_widget.indexOf(offline_OCR_tab), "本地OCR")

        # 本地OCR页签图标
        self.ocr_tab_widget.setTabIcon(self.ocr_tab_widget.indexOf(offline_OCR_tab), ui.static.icon.OFFLINE_OCR_ICON)

        # 横向分割线
        label = QLabel(offline_OCR_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 此Label用于本地OCR页签的背景图
        label = QLabel(offline_OCR_tab)
        label.setGeometry(QRect(0, 0, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 百度OCR页签
        baidu_OCR_tab = QWidget()
        self.ocr_tab_widget.addTab(baidu_OCR_tab, "")
        self.ocr_tab_widget.setTabText(self.ocr_tab_widget.indexOf(baidu_OCR_tab), "百度OCR")

        # 百度OCR页签图标
        self.ocr_tab_widget.setTabIcon(self.ocr_tab_widget.indexOf(baidu_OCR_tab), ui.static.icon.BAIDU_OCR_ICON)

        # 横向分割线
        label = QLabel(baidu_OCR_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 此Label用于雾化百度OCR页签的背景图
        label = QLabel(baidu_OCR_tab)
        label.setGeometry(QRect(0, 0, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # OCR标签
        self.ocr_label = QLabel(self.tab_1)
        self.customSetGeometry(self.ocr_label, 370, 10, 300, 20)
        if self.online_ocr_use :
            self.ocr_label.setText("当前正在使用【在线OCR】")
        elif self.offline_ocr_use :
            self.ocr_label.setText("当前正在使用【本地OCR】")
        elif self.baidu_ocr_use :
            self.ocr_label.setText("当前正在使用【百度OCR】")
        elif self.online_ocr_probation_use :
            self.ocr_label.setText("当前正在使用【在线OCR试用】")
        else :
            self.ocr_label.setText("请选择开启一种OCR开关, 否则翻译将无法使用")
        self.ocr_label.setStyleSheet("color: %s"%self.color_2)

        # 在线OCR标签
        label = QLabel(online_OCR_tab)
        self.customSetGeometry(label, 20, 20, 400, 20)
        label.setText("需购买, 无限调用次数且识别精度高, 建议使用")
        label.setStyleSheet("color: %s"%self.color_2)

        # 在线OCR教程按钮
        button = QPushButton(online_OCR_tab)
        self.customSetGeometry(button, 550, 20, 100, 20)
        button.setText("详细教程")
        button.clicked.connect(self.openOnlineOCRTutorials)
        button.setCursor(ui.static.icon.QUESTION_CURSOR)

        # 在线OCR状态开关
        self.online_ocr_switch = ui.switch.SwitchOCR(online_OCR_tab, self.online_ocr_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.online_ocr_switch, 20, 70, 65, 20)
        self.online_ocr_switch.checkedChanged.connect(self.changeOnlineSwitch)
        self.online_ocr_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 在线OCR标签
        label = QLabel(online_OCR_tab)
        self.customSetGeometry(label, 105, 70, 400, 20)
        label.setText("使用在线OCR")

        # 在线OCR试用状态开关
        self.online_ocr_probation_switch = ui.switch.SwitchOCR(online_OCR_tab, self.online_ocr_probation_use, startX=(65-20) * self.rate)
        self.customSetGeometry(self.online_ocr_probation_switch, 220, 70, 65, 20)
        self.online_ocr_probation_switch.checkedChanged.connect(self.changeProbationSwitch)
        self.online_ocr_probation_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 在线OCR试用标签
        self.online_ocr_probation_label = QLabel(online_OCR_tab)
        self.customSetGeometry(self.online_ocr_probation_label, 305, 70, 400, 20)
        self.online_ocr_probation_label.setText("试用在线OCR")
        utils.thread.createThread(utils.http.ocrProbationReadCount, self.object)

        # 在线OCR购买按钮
        button = QPushButton(online_OCR_tab)
        self.customSetGeometry(button, 20, 120, 60, 20)
        button.setText("购买")
        button.clicked.connect(self.openDangoBuyPage)
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 在线OCR测试按钮
        button = QPushButton(online_OCR_tab)
        self.customSetGeometry(button, 100, 120, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testOnlineOCR(self.object))
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 在线OCR标签
        label = QLabel(online_OCR_tab)
        self.customSetGeometry(label, 180, 120, 400, 20)
        label.setText("购买在线OCR, 支持团子")

        # 节点下拉框
        self.node_info_comboBox = QComboBox(online_OCR_tab)
        self.customSetGeometry(self.node_info_comboBox, 20, 170, 140, 20)
        self.node_info_comboBox.setStyleSheet("QComboBox{color: %s}"%self.color_2)
        self.node_info_comboBox.setCursor(ui.static.icon.SELECT_CURSOR)
        # 获取节点信息
        utils.thread.createThread(self.getNodeInfo)
        # 在线OCR刷新按钮
        button = QPushButton(qtawesome.icon("fa.refresh", color=self.color_2), "", online_OCR_tab)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 170, 170, 20, 20)
        button.setStyleSheet("QPushButton { background: transparent;}"
                             "QPushButton:hover { background-color: rgba(62, 62, 62, 0.2); }"
                             "QPushButton:pressed { background-color: rgba(62, 62, 62, 0.4);"
                             "padding-left: 3px; padding-top: 3px;}")
        button.clicked.connect(lambda: utils.thread.createThread(self.getNodeInfo))
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 在线OCR标签
        label = QLabel(online_OCR_tab)
        self.customSetGeometry(label, 200, 170, 400, 20)
        label.setText("翻译慢可以切换延迟低的节点")

        # 在线OCR查额度按钮
        button = QPushButton(online_OCR_tab)
        self.customSetGeometry(button, 20, 220, 60, 20)
        button.setText("查额度")
        button.clicked.connect(lambda: self.showDesc("onlineOCRQueryQuota"))
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 在线OCR备注
        label = QLabel(online_OCR_tab)
        self.customSetGeometry(label, 100, 220, 400, 20)
        label.setText("查询在线OCR有效期")

        # 本地OCR标签
        label = QLabel(offline_OCR_tab)
        self.customSetGeometry(label, 20, 20, 400, 20)
        label.setText("免费使用, 识别精度一般, 依赖自身电脑性能")
        label.setStyleSheet("color: %s"%self.color_2)
        # 本地OCR教程按钮
        button = QPushButton(offline_OCR_tab)
        self.customSetGeometry(button, 550, 20, 100, 20)
        button.setText("详细教程")
        button.clicked.connect(self.openOfflineOCRTutorial)
        button.setCursor(ui.static.icon.QUESTION_CURSOR)

        # 本地OCR状态开关
        self.offline_ocr_switch = ui.switch.OfflineSwitch(offline_OCR_tab, sign=self.offline_ocr_use, startX=(65-20)*self.rate, object=self.object)
        self.customSetGeometry(self.offline_ocr_switch, 20, 70, 65, 20)
        self.offline_ocr_switch.checkedChanged.connect(self.changeOfflineSwitch)
        self.offline_ocr_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 本地OCR标签
        label = QLabel(offline_OCR_tab)
        self.customSetGeometry(label, 105, 70, 400, 20)
        label.setText("使用本地OCR, 使用前需先运行")

        # 本地OCR运行按钮
        button = QPushButton(offline_OCR_tab)
        self.customSetGeometry(button, 20, 120, 60, 20)
        button.setText("运行")
        button.clicked.connect(self.runOfflineOCR)
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 本地OCR测试按钮
        button = QPushButton(offline_OCR_tab)
        self.customSetGeometry(button, 100, 120, 60, 20)
        button.setText("测试")
        button.clicked.connect(self.testOfflineOCR)
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 本地OCR备注
        label = QLabel(offline_OCR_tab)
        self.customSetGeometry(label, 180, 120, 400, 20)
        label.setText("运行本地OCR, 使用过程中切勿关闭黑窗")

        # 本地OCR安装按钮
        button = QPushButton(offline_OCR_tab)
        self.customSetGeometry(button, 20, 170, 60, 20)
        button.setText("安装")
        button.clicked.connect(lambda: utils.offline_ocr.install_offline_ocr(self.object))
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        self.progress_bar = ui.progress_bar.ProgressBar(self.object.yaml["screen_scale_rate"])
        # 本地OCR卸载按钮
        button = QPushButton(offline_OCR_tab)
        self.customSetGeometry(button, 100, 170, 60, 20)
        button.setText("卸载")
        button.clicked.connect(lambda: utils.offline_ocr.whether_uninstall_offline_ocr(self.object))
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 本地OCR标签
        label = QLabel(offline_OCR_tab)
        self.customSetGeometry(label, 180, 170, 400, 20)
        label.setText("首次使用请先安装, 不使用可卸载节省空间")

        # 百度OCR标签
        label = QLabel(baidu_OCR_tab)
        self.customSetGeometry(label, 20, 20, 400, 20)
        label.setText("老用户专用, 精度虽高但价格昂贵, 新用户忽略")
        label.setStyleSheet("color: %s"%self.color_2)
        # 百度OCR教程按钮
        button = QPushButton(baidu_OCR_tab)
        self.customSetGeometry(button, 550, 20, 100, 20)
        button.setText("详细教程")
        button.clicked.connect(self.openBaiduOCRTutorials)
        button.setCursor(ui.static.icon.QUESTION_CURSOR)

        # 百度OCR状态开关
        self.baidu_ocr_switch = ui.switch.BaiduSwitchOCR(baidu_OCR_tab, self.baidu_ocr_use, startX=(65-20)*self.rate, object=self.object)
        self.customSetGeometry(self.baidu_ocr_switch, 20, 70, 65, 20)
        self.baidu_ocr_switch.checkedChanged.connect(self.changeBaiduSwitch)
        self.baidu_ocr_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 百度OCR标签
        label = QLabel(baidu_OCR_tab)
        self.customSetGeometry(label, 105, 70, 400, 20)
        label.setText("使用百度OCR, 使用前请确认是否有额度")

        # 百度OCR密钥按钮
        button = QPushButton(baidu_OCR_tab)
        self.customSetGeometry(button, 20, 120, 60, 20)
        button.setText("密钥")
        button.clicked.connect(lambda: self.showKey("baiduOCR"))
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 百度OCR测试按钮
        button = QPushButton(baidu_OCR_tab)
        self.customSetGeometry(button, 100, 120, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testBaiduOCR(self.object))
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 百度OCR备注
        label = QLabel(baidu_OCR_tab)
        self.customSetGeometry(label, 180, 120, 400, 20)
        label.setText("使用前请填入有额度的密钥")

        # 百度OCR高精度模式开关
        self.baidu_ocr_high_precision_switch = ui.switch.SwitchOCR(baidu_OCR_tab, self.baidu_ocr_high_precision_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.baidu_ocr_high_precision_switch, 20, 170, 65, 20)
        self.baidu_ocr_high_precision_switch.checkedChanged.connect(self.changeBaiduOcrHighPrecisionSwitch)
        self.baidu_ocr_high_precision_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 百度OCR高精度模式备注
        label = QLabel(baidu_OCR_tab)
        self.customSetGeometry(label, 105, 170, 300, 20)
        label.setText("开启高精度模式, 开启前请确认额度")

        # 百度OCR密查额度按钮
        button = QPushButton(baidu_OCR_tab)
        self.customSetGeometry(button, 20, 220, 60, 20)
        button.setText("查额度")
        button.clicked.connect(self.openBaiduOCRQueryQuota)
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 百度OCR备注
        label = QLabel(baidu_OCR_tab)
        self.customSetGeometry(label, 100, 220, 400, 20)
        label.setText("查询百度OCR密钥额度")

        # OCR识别语种comboBox
        self.language_comboBox = QComboBox(self.tab_1)
        self.customSetGeometry(self.language_comboBox, 20, 310, 120, 20)
        language_list = ["日语(Japanese)", "英语(English)", "韩语(Korean)", "俄语(Russian)"]
        for index, language in enumerate(language_list) :
            self.language_comboBox.addItem("")
            self.language_comboBox.setItemText(index, language)
        self.language_comboBox.setStyleSheet("QComboBox{color: %s}"%self.color_2)
        self.language_comboBox.setCursor(ui.static.icon.SELECT_CURSOR)
        if self.object.config["language"] == "ENG":
            self.language_comboBox.setCurrentIndex(1)
        elif self.object.config["language"] == "KOR":
            self.language_comboBox.setCurrentIndex(2)
        elif self.object.config["language"] == "RU":
            self.language_comboBox.setCurrentIndex(3)
        else:
            self.language_comboBox.setCurrentIndex(0)
        # OCR识别语种标签
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 160, 310, 150, 20)
        label.setText("选择要翻译的原文语种")

        # 显示原文标签开关
        self.show_original_switch = ui.switch.ShowSwitch(self.tab_1, sign=self.show_original_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.show_original_switch, 340, 310, 65, 20)
        self.show_original_switch.checkedChanged.connect(self.changeShowOriginalSwitch)
        self.show_original_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 原文颜色选择
        self.original_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.original_color), "", self.tab_1)
        self.customSetIconSize(self.original_color_button, 20, 20)
        self.customSetGeometry(self.original_color_button, 415, 310, 20, 20)
        self.original_color_button.setStyleSheet("background: transparent;")
        self.original_color_button.clicked.connect(lambda: self.ChangeTranslateColor("original", self.original_color))
        self.original_color_button.setCursor(ui.static.icon.EDIT_CURSOR)
        # 显示原文备注
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 450, 310, 300, 20)
        label.setText("是否显示识别到的原文")

        # 文字方向开关
        self.text_direction_switch = ui.switch.SwitchDirection(self.tab_1, sign=self.text_direction_use, startX=(65-20)*self.rate, object=self.object)
        self.customSetGeometry(self.text_direction_switch, 20, 360, 65, 20)
        self.text_direction_switch.checkedChanged.connect(self.changeTextDirectionSwitch)
        self.text_direction_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 文字方向标签
        self.text_direction_label = QLabel(self.tab_1)
        self.customSetGeometry(self.text_direction_label, 105, 360, 300, 20)
        self.text_direction_label.setText("识别的原文阅读方向")

        # 文字换行开关
        self.branch_line_switch = ui.switch.SwitchBranchLine(self.tab_1, sign=self.branch_line_use, startX=(65-20) * self.rate)
        self.customSetGeometry(self.branch_line_switch, 340, 360, 65, 20)
        self.branch_line_switch.checkedChanged.connect(self.changeBranchLineSwitch)
        self.branch_line_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 文字换行标签
        label = QLabel(self.tab_1)
        self.customSetGeometry(label, 425, 360, 300, 20)
        label.setText("开启会对原文换行后再翻译")


    # 翻译设定标签栏
    def setTabTwo(self) :

        # 选项卡界面
        self.tab_2 = QWidget()
        self.tab_widget.addTab(self.tab_2, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_2), " 翻译设定")

        # 此Label用于雾化顶部工具栏的背景图
        label = QLabel(self.tab_2)
        label.setGeometry(QRect(0, 0, self.window_width, 35*self.rate))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 选项卡图标
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_2), ui.static.icon.TRANSLATE_ICON)

        # 顶部工具栏
        tab_widget = QTabWidget(self.tab_2)
        tab_widget.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        tab_widget.setTabPosition(QTabWidget.North)
        tab_widget.setStyleSheet("QTabBar:tab { min-height: %dpx; min-width: %dpx;"
                                               "background: rgba(255, 255, 255, 1);}"
                                 "QTabBar:tab:selected { background: rgba(62, 62, 62, 0.07); }"
                                 "QTabWidget::pane { border-image: none; }"
                                 %(35*self.rate, 120*self.rate))

        # 竖向分割线
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 0, 0, 1, 420)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.1);")

        # 私人翻译页签
        private_translater_tab = QWidget()
        tab_widget.addTab(private_translater_tab, "")
        tab_widget.setTabText(tab_widget.indexOf(private_translater_tab), "私人翻译")

        # 私人翻译页签图标
        tab_widget.setTabIcon(tab_widget.indexOf(private_translater_tab), ui.static.icon.PRIVATE_TRANSLATER_ICON)

        # 横向分割线
        label = QLabel(private_translater_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 此Label用于雾化私人翻译页签的背景图
        label = QLabel(private_translater_tab)
        label.setGeometry(QRect(0, 0, self.window_width + 5, self.window_height + 5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 公共翻译页签
        public_translater_tab = QWidget()
        tab_widget.addTab(public_translater_tab, "")
        tab_widget.setTabText(tab_widget.indexOf(public_translater_tab), "公共翻译")

        # 公共翻译页签图标
        tab_widget.setTabIcon(tab_widget.indexOf(public_translater_tab), ui.static.icon.PUBLIC_TRANSLATER_ICON)

        # 横向分割线
        label = QLabel(public_translater_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 此Label用于雾化公共翻译页签的背景图
        label = QLabel(public_translater_tab)
        label.setGeometry(QRect(0, 0, self.window_width + 5, self.window_height + 5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 显示正在使用的翻译源类型
        self.translate_list_label = QLabel(self.tab_2)
        self.customSetGeometry(self.translate_list_label, 250, 10, 400, 20)
        self.translate_list_label.setStyleSheet("color: %s"%self.color_2)
        self.setTransLabelMessage()

        # 私人翻译备注
        label = QLabel(private_translater_tab)
        self.customSetGeometry(label, 20, 20, 400, 20)
        label.setText("免费, 使用前需先注册, 稳定且效果好, 建议使用")
        label.setStyleSheet("color: %s" % self.color_2)

        # 私人翻译教程按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 550, 20, 100, 20)
        button.setText("详细教程")
        button.clicked.connect(self.openPublicTransTutorial)
        button.setCursor(ui.static.icon.QUESTION_CURSOR)

        # 私人腾讯翻译标签
        label = QLabel(private_translater_tab)
        self.customSetGeometry(label, 20, 70, 35, 20)
        label.setText("腾讯:")

        # 私人腾讯翻译开关
        self.tencent_private_switch = ui.switch.SwitchOCR(private_translater_tab, sign=self.tencent_use, startX=(65-20) * self.rate)
        self.customSetGeometry(self.tencent_private_switch, 90, 70, 65, 20)
        self.tencent_private_switch.checkedChanged.connect(self.changeTencentSwitch)
        self.tencent_private_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 私人腾讯翻译颜色选择
        self.tencent_private_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.tencent_color), "", private_translater_tab)
        self.customSetIconSize(self.tencent_private_color_button, 20, 20)
        self.customSetGeometry(self.tencent_private_color_button, 165, 70, 20, 20)
        self.tencent_private_color_button.setStyleSheet("background: transparent;")
        self.tencent_private_color_button.clicked.connect(lambda: self.ChangeTranslateColor("tencent_private", self.tencent_use))
        self.tencent_private_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人腾讯翻译密钥按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 205, 70, 60, 20)
        button.setText("密钥")
        button.clicked.connect(lambda: self.showKey("tencentTranslate"))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人腾讯翻译测试按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 285, 70, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testTencent(self.object))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人腾讯翻译教程按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 365, 70, 60, 20)
        button.setText("注册")
        button.clicked.connect(self.openTencentTutorial)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人腾讯查额度按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 445, 70, 60, 20)
        button.setText("查额度")
        button.clicked.connect(self.openTencentQueryQuota)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人百度翻译标签
        label = QLabel(private_translater_tab)
        self.customSetGeometry(label, 20, 120, 35, 20)
        label.setText("百度:")

        # 私人百度翻译开关
        self.baidu_private_switch = ui.switch.SwitchOCR(private_translater_tab, sign=self.baidu_use, startX=(65-20) * self.rate)
        self.customSetGeometry(self.baidu_private_switch, 90, 120, 65, 20)
        self.baidu_private_switch.checkedChanged.connect(self.changeBaiduTranslaterSwitch)
        self.baidu_private_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人百度翻译颜色选择
        self.baidu_private_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.baidu_color), "", private_translater_tab)
        self.customSetIconSize(self.baidu_private_color_button, 20, 20)
        self.customSetGeometry(self.baidu_private_color_button, 165, 120, 20, 20)
        self.baidu_private_color_button.setStyleSheet("background: transparent;")
        self.baidu_private_color_button.clicked.connect(lambda: self.ChangeTranslateColor("baidu_private", self.baidu_color))
        self.baidu_private_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人百度翻译密钥按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 205, 120, 60, 20)
        button.setText("密钥")
        button.clicked.connect(lambda: self.showKey("baiduTranslate"))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人百度翻译测试按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 285, 120, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testBaidu(self.object))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人百度翻译教程按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 365, 120, 60, 20)
        button.setText("注册")
        button.clicked.connect(self.openBaiduTutorial)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人百度查额度按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 445, 120, 60, 20)
        button.setText("查额度")
        button.clicked.connect(self.openBaiduQueryQuota)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人彩云翻译标签
        label = QLabel(private_translater_tab)
        self.customSetGeometry(label, 20, 170, 35, 20)
        label.setText("彩云:")

        # 私人彩云翻译开关
        self.caiyun_private_switch = ui.switch.SwitchOCR(private_translater_tab, sign=self.caiyun_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.caiyun_private_switch, 90, 170, 65, 20)
        self.caiyun_private_switch.checkedChanged.connect(self.changeCaiyunSwitch)
        self.caiyun_private_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人彩云翻译颜色选择
        self.caiyun_private_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.caiyun_color), "", private_translater_tab)
        self.customSetIconSize(self.caiyun_private_color_button, 20, 20)
        self.customSetGeometry(self.caiyun_private_color_button, 165, 170, 20, 20)
        self.caiyun_private_color_button.setStyleSheet("background: transparent;")
        self.caiyun_private_color_button.clicked.connect(
            lambda: self.ChangeTranslateColor("caiyun_private", self.caiyun_color))
        self.caiyun_private_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人彩云翻译密钥按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 205, 170, 60, 20)
        button.setText("密钥")
        button.clicked.connect(lambda: self.showKey("caiyunTranslate"))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人彩云翻译测试按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 285, 170, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testCaiyun(self.object))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人彩云翻译教程按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 365, 170, 60, 20)
        button.setText("注册")
        button.clicked.connect(self.openCaiyunTutorial)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人彩云查额度按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 445, 170, 60, 20)
        button.setText("查额度")
        button.clicked.connect(self.openCaiyunQueryQuota)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人ChatGPT翻译标签
        label = QLabel(private_translater_tab)
        self.customSetGeometry(label, 20, 220, 60, 20)
        label.setText("ChatGPT:")

        # 私人ChatGPT翻译开关
        self.chatgpt_private_switch = ui.switch.SwitchOCR(private_translater_tab, sign=self.chatgpt_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.chatgpt_private_switch, 90, 220, 65, 20)
        self.chatgpt_private_switch.checkedChanged.connect(self.changeChatGPTSwitch)
        self.chatgpt_private_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人ChatGPT翻译颜色选择
        self.chatgpt_private_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.chatgpt_color), "", private_translater_tab)
        self.customSetIconSize(self.chatgpt_private_color_button, 20, 20)
        self.customSetGeometry(self.chatgpt_private_color_button, 215, 220, 20, 20)
        self.chatgpt_private_color_button.setStyleSheet("background: transparent;")
        self.chatgpt_private_color_button.clicked.connect(lambda: self.ChangeTranslateColor("chatgpt_private", self.chatgpt_color))
        self.chatgpt_private_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人ChatGPT翻译密钥按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 205, 220, 60, 20)
        button.setText("密钥")
        button.clicked.connect(lambda: self.showKey("chatgptTranslate"))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人ChatGPT翻译测试按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 285, 220, 60, 20)
        button.setText("测试")
        #button.clicked.connect(lambda: utils.test.testChatGPT(self.object))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人ChatGPT翻译注册按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 365, 220, 60, 20)
        button.setText("注册")
        button.clicked.connect(self.openChatGPTTutorial)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 私人ChatGPT查额度按钮
        button = QPushButton(private_translater_tab)
        self.customSetGeometry(button, 445, 220, 60, 20)
        button.setText("查额度")
        button.clicked.connect(self.openChatGPTQueryQuota)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 公共翻译备注
        label = QLabel(public_translater_tab)
        self.customSetGeometry(label, 20, 20, 420, 20)
        label.setText("免费, 无需注册, 安装Chrome浏览器后可直接使用, 但不保证其稳定性")
        label.setStyleSheet("color: %s"%self.color_2)

        # 公共翻译教程按钮
        button = QPushButton(public_translater_tab)
        self.customSetGeometry(button, 550, 20, 100, 20)
        button.setText("详细教程")
        button.clicked.connect(self.openPublicTransTutorial)
        button.setCursor(ui.static.icon.QUESTION_CURSOR)

        # 有道翻译标签
        label = QLabel(public_translater_tab)
        self.customSetGeometry(label, 20, 70, 35, 20)
        label.setText("有道:")
        # 有道翻译开关
        self.youdao_switch = ui.switch.PublicTranslationSwitch(public_translater_tab, sign=self.youdao_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.youdao_switch, 65, 70, 65, 20)
        self.youdao_switch.checkedChanged.connect(self.changeYoudaoSwitch)
        self.youdao_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # 有道翻译颜色选择
        self.youdao_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.youdao_color), "", public_translater_tab)
        self.customSetIconSize(self.youdao_color_button, 20, 20)
        self.customSetGeometry(self.youdao_color_button, 140, 70, 20, 20)
        self.youdao_color_button.setStyleSheet("background: transparent;")
        self.youdao_color_button.clicked.connect(lambda: self.ChangeTranslateColor("youdao", self.youdao_color))
        self.youdao_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 百度翻译标签
        label = QLabel(public_translater_tab)
        self.customSetGeometry(label, 200, 70, 35, 20)
        label.setText("百度:")

        # 百度翻译开关
        self.baidu_switch = ui.switch.PublicTranslationSwitch(public_translater_tab, sign=self.baidu_web_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.baidu_switch, 245, 70, 65, 20)
        self.baidu_switch.checkedChanged.connect(self.changeBaiduWebSwitch)
        self.baidu_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # 百度翻译颜色选择
        self.baidu_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.baidu_web_color), "", public_translater_tab)
        self.customSetIconSize(self.baidu_color_button, 20, 20)
        self.customSetGeometry(self.baidu_color_button, 320, 70, 20, 20)
        self.baidu_color_button.setStyleSheet("background: transparent;")
        self.baidu_color_button.clicked.connect(lambda: self.ChangeTranslateColor("baidu", self.baidu_web_color))
        self.baidu_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 腾讯翻译标签
        label = QLabel(public_translater_tab)
        self.customSetGeometry(label, 380, 70, 35, 20)
        label.setText("腾讯:")

        # 腾讯翻译开关
        self.tencent_switch = ui.switch.PublicTranslationSwitch(public_translater_tab, sign=self.tencent_web_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.tencent_switch, 425, 70, 65, 20)
        self.tencent_switch.checkedChanged.connect(self.changeTencentWebSwitch)
        self.tencent_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # 腾讯翻译颜色选择
        self.tencent_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.tencent_web_color), "", public_translater_tab)
        self.customSetIconSize(self.tencent_color_button, 20, 20)
        self.customSetGeometry(self.tencent_color_button, 500, 70, 20, 20)
        self.tencent_color_button.setStyleSheet("background: transparent;")
        self.tencent_color_button.clicked.connect(lambda: self.ChangeTranslateColor("tencent", self.tencent_web_color))
        self.tencent_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # DeepL翻译标签
        label = QLabel(public_translater_tab)
        self.customSetGeometry(label, 20, 120, 40, 20)
        label.setText("DeepL:")

        # DeepL翻译开关
        self.deepl_switch = ui.switch.PublicTranslationSwitch(public_translater_tab, sign=self.deepl_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.deepl_switch, 65, 120, 65, 20)
        self.deepl_switch.checkedChanged.connect(self.changeDeepLSwitch)
        self.deepl_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # DeepL翻译颜色选择
        self.deepl_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.deepl_color), "", public_translater_tab)
        self.customSetIconSize(self.deepl_color_button, 20, 20)
        self.customSetGeometry(self.deepl_color_button, 140, 120, 20, 20)
        self.deepl_color_button.setStyleSheet("background: transparent;")
        self.deepl_color_button.clicked.connect(lambda: self.ChangeTranslateColor("deepl", self.deepl_color))
        self.deepl_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # Bing翻译标签
        label = QLabel(public_translater_tab)
        self.customSetGeometry(label, 200, 120, 35, 20)
        label.setText("Bing:")

        # Bing翻译开关
        self.bing_switch = ui.switch.PublicTranslationSwitch(public_translater_tab, sign=self.bing_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.bing_switch, 245, 120, 65, 20)
        self.bing_switch.checkedChanged.connect(self.changeBingSwitch)
        self.bing_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # Bing翻译颜色选择
        self.bing_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.bing_color), "", public_translater_tab)
        self.customSetIconSize(self.bing_color_button, 20, 20)
        self.customSetGeometry(self.bing_color_button, 320, 120, 20, 20)
        self.bing_color_button.setStyleSheet("background: transparent;")
        self.bing_color_button.clicked.connect(lambda: self.ChangeTranslateColor("bing", self.bing_color))
        self.bing_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 彩云翻译标签
        label = QLabel(public_translater_tab)
        self.customSetGeometry(label, 380, 120, 35, 20)
        label.setText("彩云:")

        # 彩云翻译开关
        self.caiyun_switch = ui.switch.PublicTranslationSwitch(public_translater_tab, sign=self.caiyun_web_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.caiyun_switch, 425, 120, 65, 20)
        self.caiyun_switch.checkedChanged.connect(self.changeCaiyunWebSwitch)
        self.caiyun_switch.setCursor(ui.static.icon.SELECT_CURSOR)

        # 彩云翻译颜色选择
        self.caiyun_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.caiyun_web_color), "", public_translater_tab)
        self.customSetIconSize(self.caiyun_color_button, 20, 20)
        self.customSetGeometry(self.caiyun_color_button, 500, 120, 20, 20)
        self.caiyun_color_button.setStyleSheet("background: transparent;")
        self.caiyun_color_button.clicked.connect(lambda: self.ChangeTranslateColor("caiyun", self.caiyun_web_color))
        self.caiyun_color_button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 公共翻译测试可用性按钮
        button = QPushButton(public_translater_tab)
        self.customSetGeometry(button, 20, 170, 100, 20)
        button.setText("测试可用性")
        button.clicked.connect(self.testPublicTrans)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 公共翻译安装谷歌浏览器按钮
        button = QPushButton(public_translater_tab)
        self.customSetGeometry(button, 140, 170, 100, 20)
        button.setText("安装Chrome")
        button.clicked.connect(self.openInstallChrome)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        label = QLabel(public_translater_tab)
        self.customSetGeometry(label, 260, 170, 300, 20)
        label.setText("首次安装Chrome浏览器后需重启翻译器")

        # 翻译备注
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 20, 305, 250, 20)
        label.setText("点击每种翻译源对应的")
        # 颜色说明
        button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.color_2), "", self.tab_2)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 170, 305, 20, 20)
        button.setStyleSheet("background: transparent;")
        # 公共翻译备注
        label = QLabel(self.tab_2)
        self.customSetGeometry(label, 200, 305, 500, 20)
        label.setText("图标, 可以修改其翻译后显示的文字颜色")


    # 显示设定标签页
    def setTabThree(self) :

        # 选项卡界面
        self.tab_3 = QWidget()
        self.tab_widget.addTab(self.tab_3, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_3), " 显示设定")

        # 此Label用于雾化顶部工具栏的背景图
        label = QLabel(self.tab_3)
        label.setGeometry(QRect(0, 0, self.window_width, 35 * self.rate))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 选项卡图标
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_3), ui.static.icon.STYLE_ICON)

        # 顶部工具栏
        tab_widget = QTabWidget(self.tab_3)
        tab_widget.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        tab_widget.setTabPosition(QTabWidget.North)
        tab_widget.setStyleSheet("QTabBar:tab { min-height: %dpx; min-width: %dpx;"
                                 "background: rgba(255, 255, 255, 1);}"
                                 "QTabBar:tab:selected { background: rgba(62, 62, 62, 0.07); }"
                                 "QTabWidget::pane { border-image: none; }"
                                 % (35 * self.rate, 120 * self.rate))

        # 竖向分割线
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 0, 0, 1, 420)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.1);")

        # 翻译框页签
        translation_frame_tab = QWidget()
        tab_widget.addTab(translation_frame_tab, "")
        tab_widget.setTabText(tab_widget.indexOf(translation_frame_tab), "翻译框")
        # 翻译框页签图标
        tab_widget.setTabIcon(tab_widget.indexOf(translation_frame_tab), ui.static.icon.TRANSLATION_FRAME_ICON)

        # 横向分割线
        label = QLabel(translation_frame_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 此Label用于雾化翻译框页签的背景图
        label = QLabel(translation_frame_tab)
        label.setGeometry(QRect(0, 0, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 字体样式页签
        font_tab = QWidget()
        tab_widget.addTab(font_tab, "")
        tab_widget.setTabText(tab_widget.indexOf(font_tab), "字体样式")

        # 字体样式页签图标
        tab_widget.setTabIcon(tab_widget.indexOf(font_tab), ui.static.icon.FONT_ICON)

        # 横向分割线
        label = QLabel(font_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 此Label用于雾化字体样式页签的背景图
        label = QLabel(font_tab)
        label.setGeometry(QRect(0, 0, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 翻译框透明度设定
        self.horizontal_slider = QSlider(translation_frame_tab)
        self.customSetGeometry(self.horizontal_slider, 20, 28, 320, 25)
        self.horizontal_slider.setMaximum(100)
        self.horizontal_slider.setOrientation(Qt.Horizontal)
        self.horizontal_slider.setValue(0)
        self.horizontal_slider.setValue(self.horizontal)
        self.horizontal_slider.valueChanged.connect(self.changeHorizontal)
        self.horizontal_slider.installEventFilter(self)
        self.horizontal_slider.setCursor(ui.static.icon.SELECT_CURSOR)
        # 翻译框透明度数值标签
        self.horizontal_slider_label = QLabel(translation_frame_tab)
        self.customSetGeometry(self.horizontal_slider_label, 350, 30, 30, 20)
        self.horizontal_slider_label.setText("{}%".format(self.horizontal))
        # 翻译框透明度设定标签
        label = QLabel(translation_frame_tab)
        self.customSetGeometry(label, 400, 30, 200, 20)
        label.setText("调整翻译框的透明度")

        # 显示翻译时间开关
        self.show_statusbar_switch = ui.switch.ShowSwitch(translation_frame_tab, sign=self.show_statusbar_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.show_statusbar_switch, 20, 80, 65, 20)
        self.show_statusbar_switch.checkedChanged.connect(self.changeShowStatusbarSwitch)
        self.show_statusbar_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 显示翻译时间标签
        label = QLabel(translation_frame_tab)
        self.customSetGeometry(label, 105, 80, 300, 20)
        label.setText("是否在翻译框上显示翻译耗时")

        # 翻译字体大小设定
        self.fontSize_spinBox = QSpinBox(font_tab)
        self.customSetGeometry(self.fontSize_spinBox, 30, 25, 40, 25)
        self.fontSize_spinBox.setMinimum(10)
        self.fontSize_spinBox.setMaximum(30)
        self.fontSize_spinBox.setValue(self.fontSize)
        self.fontSize_spinBox.setCursor(ui.static.icon.SELECT_CURSOR)
        # 翻译字体大小设定标签
        label = QLabel(font_tab)
        self.customSetGeometry(label, 90, 30, 300, 16)
        label.setText("翻译框上显示的字体大小")

        # 翻译字体类型设定
        self.font_comboBox = QFontComboBox(font_tab)
        self.customSetGeometry(self.font_comboBox, 20, 75, 185, 25)
        self.font_comboBox.activated[str].connect(self.getFontType)
        self.comboBox_font = QFont(self.font_type)
        self.font_comboBox.setCurrentFont(self.comboBox_font)
        self.font_comboBox.setCursor(ui.static.icon.SELECT_CURSOR)
        self.font_comboBox.setStyleSheet("QComboBox{color: %s}"%self.color_2)
        # 翻译字体类型设定标签
        label = QLabel(font_tab)
        self.customSetGeometry(label, 225, 80, 300, 20)
        label.setText("翻译框上显示的字体类型")

        # 字体样式设定开关
        self.font_type_switch = ui.switch.SwitchFontType(font_tab, sign=self.font_color_type, startX=(65-20)*self.rate)
        self.customSetGeometry(self.font_type_switch, 20, 130, 65, 20)
        self.font_type_switch.checkedChanged.connect(self.changeFontColorTypeSwitch)
        self.font_type_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 字体样式设定标签
        label = QLabel(font_tab)
        self.customSetGeometry(label, 105, 130, 300, 20)
        label.setText("翻译框上显示字体样式, 建议使用描边样式")


    # 功能设定标签页
    def setTabFour(self) :

        # 选项卡界面
        self.tab_4 = QWidget()
        self.tab_widget.addTab(self.tab_4, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_4), " 功能设定")

        # 此Label用于雾化工具栏1的背景图
        label = QLabel(self.tab_4)
        label.setGeometry(QRect(0, 0, self.window_width, 35*self.rate))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 选项卡图标
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_4), ui.static.icon.FUNCTION_ICON)

        # 顶部工具栏
        tab_widget = QTabWidget(self.tab_4)
        tab_widget.setGeometry(QRect(0, 0, self.window_width, self.window_height))
        tab_widget.setTabPosition(QTabWidget.North)
        tab_widget.setStyleSheet("QTabBar:tab { min-height: %dpx; min-width: %dpx;"
                                 "background: rgba(255, 255, 255, 1);}"
                                 "QTabBar:tab:selected { background: rgba(62, 62, 62, 0.07); }"
                                 "QTabWidget::pane { border-image: none; }"
                                 %(35*self.rate, 120*self.rate))

        # 竖向分割线
        label = QLabel(self.tab_4)
        self.customSetGeometry(label, 0, 0, 1, 420)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.1);")

        # 自动模式页签
        auto_mode_tab = QWidget(self.tab_4)
        tab_widget.addTab(auto_mode_tab, "")
        tab_widget.setTabText(tab_widget.indexOf(auto_mode_tab), "自动模式")
        tab_widget.setTabIcon(tab_widget.indexOf(auto_mode_tab), ui.static.icon.AUTO_MODE_ICON)

        # 横向分割线
        label = QLabel(auto_mode_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 雾化页签的背景图
        label = QLabel(auto_mode_tab)
        label.setGeometry(QRect(0, 0, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 快捷键页签
        shortcut_key_tab = QWidget()
        tab_widget.addTab(shortcut_key_tab, "")
        tab_widget.setTabText(tab_widget.indexOf(shortcut_key_tab), "快捷键")
        tab_widget.setTabIcon(tab_widget.indexOf(shortcut_key_tab), ui.static.icon.SHORTCUT_KEY_ICON)

        # 横向分割线
        label = QLabel(shortcut_key_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 雾化页签的背景图
        label = QLabel(shortcut_key_tab)
        label.setGeometry(QRect(0, 0, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 其他页签
        other_tab = QWidget()
        tab_widget.addTab(other_tab, "")
        tab_widget.setTabText(tab_widget.indexOf(other_tab), "其他")
        tab_widget.setTabIcon(tab_widget.indexOf(other_tab), ui.static.icon.OTHER_ICON)

        # 横向分割线
        label = QLabel(other_tab)
        self.customSetGeometry(label, 0, 0, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 雾化页签的背景图
        label = QLabel(other_tab)
        label.setGeometry(QRect(0, 0, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 自动模式速率设定
        self.auto_speed_spinBox = QDoubleSpinBox(auto_mode_tab)
        self.customSetGeometry(self.auto_speed_spinBox, 20, 30, 45, 25)
        self.auto_speed_spinBox.setDecimals(1)
        self.auto_speed_spinBox.setMinimum(0.5)
        self.auto_speed_spinBox.setMaximum(10.0)
        self.auto_speed_spinBox.setSingleStep(0.1)
        self.auto_speed_spinBox.setValue(self.translate_speed)
        self.auto_speed_spinBox.setCursor(ui.static.icon.EDIT_CURSOR)
        # 自动翻译间隔标签
        label = QLabel(auto_mode_tab)
        self.customSetGeometry(label, 85, 35, 600, 20)
        label.setText("自动模式下刷新翻译的时间间隔(0.5-10.0秒), 建议1")

        # 图像相似度设定
        self.image_refresh_spinBox = QDoubleSpinBox(auto_mode_tab)
        self.customSetGeometry(self.image_refresh_spinBox, 20, 80, 45, 25)
        self.image_refresh_spinBox.setDecimals(0)
        self.image_refresh_spinBox.setMinimum(80)
        self.image_refresh_spinBox.setMaximum(100)
        self.image_refresh_spinBox.setSingleStep(1)
        self.image_refresh_spinBox.setValue(self.image_refresh_score)
        self.image_refresh_spinBox.setCursor(ui.static.icon.SELECT_CURSOR)
        # 图像相似度标签
        label = QLabel(auto_mode_tab)
        self.customSetGeometry(label, 85, 80, 600, 20)
        label.setText("自动模式下的图像相似度(80-100%), 数值越高越频繁刷新OCR识别结果, 建议98")

        # 文字相似度设定
        self.text_refresh_spinBox = QDoubleSpinBox(auto_mode_tab)
        self.customSetGeometry(self.text_refresh_spinBox, 20, 130, 45, 25)
        self.text_refresh_spinBox.setDecimals(0)
        self.text_refresh_spinBox.setMinimum(80)
        self.text_refresh_spinBox.setMaximum(100)
        self.text_refresh_spinBox.setSingleStep(1)
        self.text_refresh_spinBox.setValue(self.text_refresh_score)
        self.text_refresh_spinBox.setCursor(ui.static.icon.SELECT_CURSOR)
        # 文字相似度标签
        label = QLabel(auto_mode_tab)
        self.customSetGeometry(label, 85, 130, 600, 20)
        label.setText("自动模式下的文字相似度(80-100%), 数值越高越频繁刷新翻译结果, 建议90")

        # 翻译快捷键开关
        self.translate_hotkey_switch = ui.switch.SwitchOCR(shortcut_key_tab, sign=self.translate_hotkey_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.translate_hotkey_switch, 20, 30, 65, 20)
        self.translate_hotkey_switch.checkedChanged.connect(self.changeTranslateHotkeySwitch)
        self.translate_hotkey_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 翻译快捷键设定按钮
        self.translate_hotkey_button = QPushButton(shortcut_key_tab)
        self.customSetGeometry(self.translate_hotkey_button, 100, 30, 60, 20)
        self.translate_hotkey_button.setText(self.object.config["translateHotkeyValue1"]+"+"+self.object.config["translateHotkeyValue2"])
        self.translate_hotkey_button.clicked.connect(lambda: self.setHotKey("translate"))
        self.translate_hotkey_button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 翻译快捷键标签
        label = QLabel(shortcut_key_tab)
        self.customSetGeometry(label, 180, 30, 500, 20)
        label.setText("手动模式下刷新翻译的快捷键")

        # 范围快捷键开关
        self.range_hotkey_switch = ui.switch.SwitchOCR(shortcut_key_tab, sign=self.range_hotkey_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.range_hotkey_switch, 20, 80, 65, 20)
        self.range_hotkey_switch.checkedChanged.connect(self.changeRangeHotkeySwitch)
        self.range_hotkey_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 范围快捷键设定按钮
        self.range_hotkey_button = QPushButton(shortcut_key_tab)
        self.customSetGeometry(self.range_hotkey_button, 100, 80, 60, 20)
        self.range_hotkey_button.setText(self.object.config["rangeHotkeyValue1"]+"+"+self.object.config["rangeHotkeyValue2"])
        self.range_hotkey_button.clicked.connect(lambda: self.setHotKey("range"))
        self.range_hotkey_button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 范围快捷键标签
        label = QLabel(shortcut_key_tab)
        self.customSetGeometry(label, 180, 80, 500, 20)
        label.setText("重新框选范围框的快捷键")

        # 隐藏快捷键开关
        self.hide_range_hotkey_switch = ui.switch.SwitchOCR(shortcut_key_tab, sign=self.hide_range_hotkey_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.hide_range_hotkey_switch, 20, 130, 65, 20)
        self.hide_range_hotkey_switch.checkedChanged.connect(self.changeHideRangeHotkeySwitch)
        self.hide_range_hotkey_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 隐藏快捷键设定按钮
        self.hide_range_hotkey_button = QPushButton(shortcut_key_tab)
        self.customSetGeometry(self.hide_range_hotkey_button, 100, 130, 60, 20)
        self.hide_range_hotkey_button.setText(self.object.config["hideRangeHotkeyValue1"]+"+"+self.object.config["hideRangeHotkeyValue2"])
        self.hide_range_hotkey_button.clicked.connect(lambda: self.setHotKey("hideRange"))
        self.hide_range_hotkey_button.setCursor(ui.static.icon.SELECT_CURSOR)
        # 隐藏范围快捷键标签
        label = QLabel(shortcut_key_tab)
        self.customSetGeometry(label, 180, 130, 500, 20)
        label.setText("显示/隐藏范围框的快捷键")

        # 贴字翻译开关
        self.draw_image_switch = ui.switch.DrawSwitchOCR(other_tab, sign=self.draw_image_use, startX=(65-20)*self.rate, object=self.object)
        self.customSetGeometry(self.draw_image_switch, 20, 30, 65, 20)
        self.draw_image_switch.checkedChanged.connect(self.changeDrawImageSwitch)
        self.draw_image_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 贴字翻译标签
        label = QLabel(other_tab)
        self.customSetGeometry(label, 105, 30, 400, 20)
        label.setText("将翻译的结果以贴图的形式覆盖至范围框内")

        # 原文自动复制到剪贴板开关
        self.auto_copy_original_switch = ui.switch.SwitchOCR(other_tab, sign=self.auto_clipboard_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.auto_copy_original_switch, 20, 80, 65, 20)
        self.auto_copy_original_switch.checkedChanged.connect(self.changeAutoCopyOriginalSwitch)
        self.auto_copy_original_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 原文自动复制到剪贴板标签
        label = QLabel(other_tab)
        self.customSetGeometry(label, 105, 80, 400, 20)
        label.setText("每次识别到的原文自动复制到剪贴板")

        # 自动朗读开关
        self.auto_playsound_switch = ui.switch.SwitchOCR(other_tab, sign=self.auto_playsound_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.auto_playsound_switch, 20, 130, 65, 20)
        self.auto_playsound_switch.checkedChanged.connect(self.changeAutoPlaysoundSwitch)
        self.auto_playsound_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 自动朗读标签
        label = QLabel(other_tab)
        self.customSetGeometry(label, 105, 130, 400, 20)
        label.setText("每次识别后都自动朗读识别到的原文")

        # 是否全屏下置顶开关
        self.set_top_switch = ui.switch.SwitchOCR(other_tab, self.set_top_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.set_top_switch, 20, 180, 65, 20)
        self.set_top_switch.checkedChanged.connect(self.changeSetTopSwitch)
        self.set_top_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 是否全屏下置顶
        label = QLabel(other_tab)
        self.customSetGeometry(label, 105, 180, 400, 20)
        label.setText("在全屏模式的应用下置顶翻译器")

        # 自动登录开关
        self.auto_login_switch = ui.switch.SwitchOCR(other_tab, sign=self.auto_login_use, startX=(65-20)*self.rate)
        self.customSetGeometry(self.auto_login_switch, 20, 230, 65, 20)
        self.auto_login_switch.checkedChanged.connect(self.changeAutoLoginSwitch)
        self.auto_login_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 自动登录标签
        label = QLabel(other_tab)
        self.customSetGeometry(label, 105, 230, 400, 20)
        label.setText("开启软件后自动登录账号")

        # 同意收集翻译历史开关
        self.agree_collect_switch = ui.switch.SwitchOCR(other_tab, sign=self.agree_collect_use, startX=(65-20) * self.rate)
        self.customSetGeometry(self.agree_collect_switch, 20, 280, 65, 20)
        self.agree_collect_switch.checkedChanged.connect(self.changeAgreeCollectSwitch)
        self.agree_collect_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 同意收集翻译历史标签
        label = QLabel(other_tab)
        self.customSetGeometry(label, 105, 280, 300, 20)
        label.setText("加入用户体验改善计划")
        # 同意收集翻译历史?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", other_tab)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 250, 280, 20, 20)
        button.setStyleSheet("background: transparent;")
        button.clicked.connect(lambda: self.showDesc("agreeCollect"))
        button.setCursor(ui.static.icon.QUESTION_CURSOR)


    # 关于标签页
    def setTabFive(self) :

        # 选项卡界面
        self.tab_5 = QWidget()
        self.tab_widget.addTab(self.tab_5, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_5), "关于   ")

        # 分割线
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 0, 0, 1, 420)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.2);")

        # 选项卡图标
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_5), ui.static.icon.ABOUT_ICON)

        # 此Label用于雾化工具栏1的背景图
        label = QLabel(self.tab_5)
        label.setGeometry(QRect(0, -1, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

        # 官方网站标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 30, 300, 20)
        label.setText("团子翻译器的官网哦 (欢迎来玩)")

        # 官方网站按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 30, 90, 20)
        button.setText("官方网站")
        button.clicked.connect(self.openHomePage)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 项目地址图标
        button.setIcon(ui.static.icon.HOME_ICON)

        # 项目地址标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 75, 300, 20)
        label.setText("本软件已在github开源 (欢迎来点小星星)")

        # 项目地址按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 75, 90, 20)
        button.setText("项目地址")
        button.clicked.connect(self.openGithubProject)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 项目地址图标
        button.setIcon(ui.static.icon.GITHUB_ICON)

        # 在线教程标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 120, 300, 20)
        label.setText("软件完整使用教程 (要好好阅读哦)")

        # 在线教程按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 120, 90, 20)
        button.setText("在线文档")
        button.clicked.connect(self.openTutorial)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 在线教程图标
        button.setIcon(ui.static.icon.TUTORIAL_ICON)

        # 教程视频标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 160, 300, 20)
        label.setText("软件b站教程视频 (不想看文档就看这个吧)")

        # 教程视频按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 160, 90, 20)
        button.setText("教程视频")
        button.clicked.connect(self.openBilibiliVideo)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # b站教程视频图标
        button.setIcon(ui.static.icon.BILIBILI_VIDEO_ICON)

        # 关注作者标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 205, 300, 20)
        label.setText("发布公告的地方 (不关注团子吗)")

        # 关注作者按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 205, 90, 20)
        button.setText("关注团子")
        button.clicked.connect(self.openBilibili)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # bilibili图标
        button.setIcon(ui.static.icon.BILIBILI_ICON)

        # 添加交流群标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 130, 250, 300, 20)
        label.setText("加入交流群 (QQ群申请)")

        # 添加交流群按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 250, 90, 20)
        button.setText("群聊交流")
        button.clicked.connect(lambda: self.showDesc("qqGroup"))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # QQ群图标
        button.setIcon(ui.static.icon.GROUP_ICON)

        # 特别鸣谢标签
        label = QLabel(self.tab_5)
        self.customSetGeometry(label, 20, 300, 300, 20)
        label.setText("特别鸣谢 (本软件受到以下人员和项目的帮助)")

        # PaddleOCR主页按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 20, 340, 90, 20)
        button.setText("PaddleOCR‭")
        button.clicked.connect(self.openPaddleOCR)
        button.setIcon(ui.static.icon.GITHUB_ICON)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # GT-Zhang主页按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 130, 340, 90, 20)
        button.setText("GT-Zhang")
        button.clicked.connect(self.openGT)
        button.setIcon(ui.static.icon.GITHUB_ICON)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # C4a15Wh主页按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 240, 340, 90, 20)
        button.setText("C4a15Wh")
        button.clicked.connect(self.openC44)
        button.setIcon(ui.static.icon.BLOG_ICON)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # cypas‭主页按钮
        button = QPushButton(self.tab_5)
        self.customSetGeometry(button, 350, 340, 90, 20)
        button.setText("Cypas‭")
        button.clicked.connect(self.openCy)
        button.setIcon(ui.static.icon.BLOG_ICON)
        button.setCursor(ui.static.icon.SELECT_CURSOR)


    # 支持作者标签页
    def setTabSix(self) :

        # 选项卡界面
        self.tab_6 = QWidget()
        self.tab_widget.addTab(self.tab_6, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_6), " 支持作者")

        # 分割线
        label = QLabel(self.tab_6)
        self.customSetGeometry(label, 0, 0, 1, 420)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; border-style: solid; border-color: rgba(62, 62, 62, 0.2);")

        # 选项卡图标
        self.tab_widget.setTabIcon(self.tab_widget.indexOf(self.tab_6), ui.static.icon.GOOD_ICON_ICON)

        # 此Label用于雾化工具栏1的背景图
        label = QLabel(self.tab_6)
        label.setGeometry(QRect(0, -1, self.window_width+5, self.window_height+5))
        label.setStyleSheet("background: rgba(255, 255, 255, 0.5);")

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
        self.window_height = int(420*self.rate)
        # 所使用的颜色
        self.color_1 = "#595959"  # 灰色
        self.color_2 = "#5B8FF9"  # 蓝色
        # 界面字体大小
        self.font_size = 10
        # 存被开启的翻译源
        self.translate_list = []
        # 翻译源中文映射
        self.translate_map = {
            "youdao": "【公共有道】",
            "baidu": "【公共百度】",
            "tencent": "【公共腾讯】",
            "deepl": "【公共DeepL】",
            "bing": "【公共Bing】",
            "caiyun": "【公共彩云】",
            "tencent_private": "【私人腾讯】",
            "baidu_private": "【私人百度】",
            "caiyun_private": "【私人彩云】",
            "chatgpt_private": "【私人ChatGPT】"
        }

        # OCR各开关
        self.offline_ocr_use = self.object.config["offlineOCR"]
        self.online_ocr_use = self.object.config["onlineOCR"]
        self.online_ocr_probation_use = self.object.config["onlineOCRProbation"]
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
        # 公共Bing翻译开关
        self.bing_use = eval(self.object.config["bingUse"])
        if self.bing_use :
            self.translate_list.append("bing")
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
        # 私人ChatGPT翻译开关
        self.chatgpt_use = eval(self.object.config["chatgptPrivateUse"])
        if self.chatgpt_use :
            self.translate_list.append("chatgpt_private")

        # 字体颜色 公共有道
        self.youdao_color = self.object.config["fontColor"]["youdao"]
        # 字体颜色 公共百度
        self.baidu_web_color = self.object.config["fontColor"]["baiduweb"]
        # 字体颜色 公共腾讯
        self.tencent_web_color = self.object.config["fontColor"]["tencentweb"]
        # 字体颜色 公共DeepL
        self.deepl_color = self.object.config["fontColor"]["deepl"]
        # 字体颜色 公共Bing
        self.bing_color = self.object.config["fontColor"]["bing"]
        # 字体颜色 公共彩云
        self.caiyun_web_color = self.object.config["fontColor"]["caiyun"]
        # 字体颜色 私人腾讯
        self.tencent_color = self.object.config["fontColor"]["tencent"]
        # 字体颜色 私人百度
        self.baidu_color = self.object.config["fontColor"]["baidu"]
        # 字体颜色 私人彩云
        self.caiyun_color = self.object.config["fontColor"]["caiyunPrivate"]
        # 字体颜色 私人ChatGPT
        self.chatgpt_color = self.object.config["fontColor"]["chatgptPrivate"]
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
        # 同步翻译历史开关
        self.agree_collect_use = self.object.config["agreeCollectUse"]

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
        # 自动朗读开关
        self.auto_playsound_use = self.object.config["autoPlaysoundUse"]


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
            entry = QStandardItem("自动模式  {:.2f}s".format(time_diff/1000))
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
                text = "{}  {:.2f}s".format(node_name, time_diff/1000)
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

        object.setIconSize(QSize(int(w*self.rate),
                                 int(h*self.rate)))


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
            if self.online_ocr_probation_use == True :
                self.resetSwitch("ProbationOCR")
            self.offline_ocr_use = True
            self.ocr_label.setText("当前正在使用【本地OCR】")
        else:
            self.offline_ocr_use = False
            self.ocr_label.setText("请选择开启一种OCR开关, 否则翻译将无法使用")


    # 改变在线OCR开关状态
    def changeOnlineSwitch(self, checked) :

        if checked :
            if self.offline_ocr_use == True :
                self.resetSwitch("offlineOCR")
            if self.baidu_ocr_use == True :
                self.resetSwitch("baiduOCR")
            if self.online_ocr_probation_use == True :
                self.resetSwitch("ProbationOCR")
            self.online_ocr_use = True
            self.ocr_label.setText("当前正在使用【在线OCR】")
        else:
            self.online_ocr_use = False
            self.ocr_label.setText("请选择开启一种OCR开关, 否则翻译将无法使用")


    # 改变在线OCR试用开关状态
    def changeProbationSwitch(self, checked):

        if checked:
            if self.offline_ocr_use == True:
                self.resetSwitch("offlineOCR")
            if self.baidu_ocr_use == True:
                self.resetSwitch("baiduOCR")
            if self.online_ocr_use == True:
                self.resetSwitch("onlineOCR")
            self.online_ocr_probation_use = True
            self.ocr_label.setText("当前正在使用【在线OCR试用】")
        else:
            self.online_ocr_probation_use = False
            self.ocr_label.setText("请选择开启一种OCR开关, 否则翻译将无法使用")


    # 改变百度OCR开关状态
    def changeBaiduSwitch(self, checked) :

        if checked :
            if self.offline_ocr_use == True :
                self.resetSwitch("offlineOCR")
            if self.online_ocr_use == True :
                self.resetSwitch("onlineOCR")
            if self.online_ocr_probation_use == True :
                self.resetSwitch("ProbationOCR")
            self.baidu_ocr_use = True
            self.ocr_label.setText("当前正在使用【百度OCR】")
        else :
            self.baidu_ocr_use = False
            self.ocr_label.setText("请选择开启一种OCR开关, 否则翻译将无法使用")


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
        self.setTransLabelMessage()


    # 改变公共百度翻译开关状态
    def changeBaiduWebSwitch(self, checked) :

        if checked :
            self.baidu_web_use = True
            self.translate_list.append("baidu")
            self.checkTranslaterUse()
        else:
            self.baidu_web_use = False
            self.translate_list.remove("baidu")
        self.setTransLabelMessage()


    # 改变公共腾讯翻译开关状态
    def changeTencentWebSwitch(self, checked) :

        if checked :
            self.tencent_web_use = True
            self.translate_list.append("tencent")
            self.checkTranslaterUse()
        else:
            self.tencent_web_use = False
            self.translate_list.remove("tencent")
        self.setTransLabelMessage()


    # 改变公共DeepL翻译开关状态
    def changeDeepLSwitch(self, checked) :

        if checked :
            self.deepl_use = True
            self.translate_list.append("deepl")
            self.checkTranslaterUse()
        else:
            self.deepl_use = False
            self.translate_list.remove("deepl")
        self.setTransLabelMessage()


    # 改变公共Bing翻译开关状态
    def changeBingSwitch(self, checked) :

        if checked :
            self.bing_use = True
            self.translate_list.append("bing")
            self.checkTranslaterUse()
        else:
            self.bing_use = False
            self.translate_list.remove("bing")
        self.setTransLabelMessage()


    # 改变公共彩云翻译开关状态
    def changeCaiyunWebSwitch(self, checked) :

        if checked :
            self.caiyun_web_use = True
            self.translate_list.append("caiyun")
            self.checkTranslaterUse()
        else:
            self.caiyun_web_use = False
            self.translate_list.remove("caiyun")
        self.setTransLabelMessage()


    # 改变私人腾讯翻译开关状态
    def changeTencentSwitch(self, checked) :

        if checked :
            self.tencent_use = True
            self.translate_list.append("tencent_private")
            self.checkTranslaterUse()
        else:
            self.tencent_use = False
            self.translate_list.remove("tencent_private")
        self.setTransLabelMessage()


    # 改变私人百度翻译开关状态
    def changeBaiduTranslaterSwitch(self, checked) :

        if checked :
            self.baidu_use = True
            self.translate_list.append("baidu_private")
            self.checkTranslaterUse()
        else:
            self.baidu_use = False
            self.translate_list.remove("baidu_private")
        self.setTransLabelMessage()


    # 改变私人彩云翻译开关状态
    def changeCaiyunSwitch(self, checked) :

        if checked :
            self.caiyun_use = True
            self.translate_list.append("caiyun_private")
            self.checkTranslaterUse()
        else:
            self.caiyun_use = False
            self.translate_list.remove("caiyun_private")
        self.setTransLabelMessage()


    # 改变私人ChatGPT翻译开关状态
    def changeChatGPTSwitch(self, checked):

        if checked:
            self.chatgpt_use = True
            self.translate_list.append("chatgpt_private")
            self.checkTranslaterUse()
        else:
            self.chatgpt_use = False
            self.translate_list.remove("chatgpt_private")
        self.setTransLabelMessage()


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


    # 改变自动朗读开关状态
    def changeAutoPlaysoundSwitch(self, checked) :

        if checked :
            self.auto_playsound_use = True
        else:
            self.auto_playsound_use = False


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
            self.object.config["showHotKey1"] = "True"
            self.object.translation_ui.registerTranslateHotkey()
        else:
            self.translate_hotkey_use = False
            self.object.config["showHotKey1"] = "False"
            self.object.translation_ui.unRegisterTranslateHotkey()


    # 改变范围热键开关状态
    def changeRangeHotkeySwitch(self, checked) :

        if checked :
            self.range_hotkey_use = True
            self.object.config["showHotKey2"] = "True"
            self.object.translation_ui.registerRangeHotkey()
        else:
            self.range_hotkey_use = False
            self.object.config["showHotKey2"] = "False"
            self.object.translation_ui.unRegisterRangeHotkey()


    # 改变隐藏范围热键开关状态
    def changeHideRangeHotkeySwitch(self, checked):

        if checked:
            self.hide_range_hotkey_use = True
            self.object.config["showHotKey3"] = True
            self.object.translation_ui.registerHideRangeHotkey()
        else:
            self.hide_range_hotkey_use = False
            self.object.config["showHotKey3"] = False
            self.object.translation_ui.unRegisterHideRangeHotkey()


    # 改变自动登录开关状态
    def changeAutoLoginSwitch(self, checked) :

        if checked :
            self.auto_login_use = True
        else:
            self.auto_login_use = False


    # 改变同步翻译历史开关状态
    def changeAgreeCollectSwitch(self, checked):

        if checked:
            self.agree_collect_use = True
        else:
            self.agree_collect_use = False


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
        elif switch_type == "ProbationOCR" :
            self.online_ocr_probation_switch.mousePressEvent(1)
            self.online_ocr_probation_switch.updateValue()


    # 运行本地OCR
    def runOfflineOCR(self) :

        # 杀死本地可能在运行ocr进程
        utils.offline_ocr.killOfflineOCR(self.object.yaml["port"])

        # 检查端口是否被占用
        if utils.port.detectPort(self.object.yaml["port"]) :
            utils.message.MessageBox("本地OCR运行失败",
                                     "本地OCR已启动, 请不要重复运行!     ")
        else :
            try :
                # 启动本地OCR
                os.startfile(self.object.yaml["ocr_cmd_path"])
            except FileNotFoundError :
                utils.message.MessageBox("本地OCR运行失败",
                                         "本地OCR还未安装, 请先安装!     ")
            except Exception :
                self.logger.error(format_exc())
                utils.message.MessageBox("本地OCR运行失败",
                                         "原因: %s"%format_exc())


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


    # 打开私人ChatGPT翻译教程
    def openChatGPTTutorial(self):

        try:
            url = self.object.yaml["dict_info"]["chatgpt_tutorial"]
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


    # 打开github项目地址
    def openGithubProject(self):

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
    def openBilibili(self):

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


    # 打开百度OCR额度查询地址
    def openBaiduOCRQueryQuota(self):

        url = "https://console.bce.baidu.com/ai/?_=1661324005307#/ai/ocr/overview/index"
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())
            utils.message.MessageBox("百度OCR额度查询",
                                     "打开地址失败, 请尝试手动打开此网页下载\n%s     "%url)


    # 打开安装谷歌浏览器地址
    def openInstallChrome(self):

        url = "https://www.google.cn/chrome/browser/desktop/index.html?standalone=1&platform=win32"
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())
            utils.message.MessageBox("安装谷歌浏览器",
                                     "打开地址失败, 请尝试手动打开此网页下载\n%s     "%url)


    # 打开查询私人腾讯额度地址
    def openTencentQueryQuota(self):

        url = "https://console.cloud.tencent.com/tmt"
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())
            utils.message.MessageBox("私人腾讯额度查询",
                                     "打开地址失败, 请尝试手动打开此网页下载\n%s     "%url)


    # 打开查询私人彩云额度地址
    def openCaiyunQueryQuota(self):

        url = "https://dashboard.caiyunapp.com/v1/token/5e818320d4b84b00d29a9316/?type=2"
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())
            utils.message.MessageBox("私人腾讯额度查询",
                                     "打开地址失败, 请尝试手动打开此网页下载\n%s     "%url)


    # 打开查询私人ChatGPT额度地址
    def openChatGPTQueryQuota(self):

        url = "https://platform.openai.com/account/usage"
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())
            utils.message.MessageBox("私人ChatGPT额度查询",
                                     "打开地址失败, 请尝试手动打开此网页下载\n%s     " % url)


    # 打开查询私人百度额度地址
    def openBaiduQueryQuota(self):

        url = "https://fanyi-api.baidu.com/api/trans/product/desktop"
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())
            utils.message.MessageBox("私人腾讯额度查询",
                                     "打开地址失败, 请尝试手动打开此网页下载\n%s     "%url)


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
        elif translate_type == "bing" :
            self.bing_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.bing_color = color.name()
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
        elif translate_type == "chatgpt_private" :
            self.chatgpt_private_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.chatgpt_color = color.name()
        elif translate_type == "original" :
            self.original_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=color.name()))
            self.original_color = color.name()


    # 说明窗口
    def showDesc(self, message_type) :

        self.desc_ui = ui.desc.Desc(self.object)

        # QQ交流群
        if message_type == "qqGroup" :
            try :
                qq_group_image = requests.get(self.object.yaml["dict_info"]["dango_qq_group"]).content
                qq_group_image = "data:image/png;base64,%s"%(str(base64.b64encode(qq_group_image))[2:])
            except Exception :
                qq_group_image = "./config/other/交流群.png"
            self.desc_ui.setWindowTitle("加入交流群")
            self.desc_ui.desc_text.insertHtml('<img src="{}" width="{}" height="{}">'.format(
                qq_group_image, 245*self.rate, 295*self.rate))

        # 在线OCR查询额度
        elif message_type == "onlineOCRQueryQuota" :
            self.desc_ui.setWindowTitle("在线OCR额度查询")
            self.desc_ui.desc_text.append(utils.http.onlineOCRQueryQuota(self.object))

        elif message_type == "agreeCollect" :
            self.desc_ui.setWindowTitle("用户体验改善说明")
            self.desc_ui.desc_text.append("\n开启后将会上传个人翻译历史, 帮助团子用于开发公共词库功能, 以优化翻译器未来的使用体验\n\n"
                                          "数据将会进行脱敏处理\n\n不会将数据用于任何非法用途")


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
            self.key_ui.setWindowTitle("百度OCR - 密钥编辑 - 退出会自动保存")
            self.key_ui.baidu_ocr_key_textEdit.show()
            self.key_ui.baidu_ocr_secret_textEdit.show()

        # 私人腾讯翻译
        elif key_type == "tencentTranslate" :
            self.key_ui.setWindowTitle("私人腾讯翻译 - 密钥编辑 - 退出会自动保存")
            self.key_ui.tencent_private_key_textEdit.show()
            self.key_ui.tencent_private_secret_textEdit.show()

        # 私人腾讯翻译
        elif key_type == "baiduTranslate" :
            self.key_ui.setWindowTitle("私人百度翻译 - 密钥编辑 - 退出会自动保存")
            self.key_ui.baidu_private_key_textEdit.show()
            self.key_ui.baidu_private_secret_textEdit.show()

        # 私人彩云翻译
        elif key_type == "caiyunTranslate" :
            self.key_ui.setWindowTitle("私人彩云翻译 - 密钥编辑 - 退出会自动保存")
            self.key_ui.caiyun_private_key_textEdit.show()

        # 私人ChatGPT翻译
        elif key_type == "chatgptTranslate":
            self.key_ui.setWindowTitle("私人ChatGPT翻译 - 密钥编辑 - 退出会自动保存")
            self.key_ui.chatgpt_private_key_textEdit.show()

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

        if key_type == "choiceRange" :
            self.hotkey_ui.setWindowTitle("切换范围区域快捷键")
            self.hotkey_ui.comboBox_1.setCurrentText(self.object.config["choiceRangeHotkeyValue"])
            self.hotkey_ui.comboBox_2.hide()
            self.hotkey_ui.default_label.setText("不支持单键\n"
                                                 "仅支持 ctrl/shift/win/alt + f1-f4\n"
                                                 "示例 ctrl+z / alt+f1")
            self.hotkey_ui.choice_range_label.show()
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

            elif val == "bing" :
                self.bing_switch.mousePressEvent(1)
                self.bing_switch.updateValue()

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

            elif val == "chatgpt_private" :
                self.chatgpt_private_switch.mousePressEvent(1)
                self.chatgpt_private_switch.updateValue()

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
        translater_list = ["youdaoUse", "baiduwebUse", "tencentwebUse", "deeplUse", "bingUse", "caiyunUse"]
        for val in translater_list:
            if self.object.config[val] == "False":
                continue
            web_type = val.replace("Use", "").replace("web", "")
            # 刷新翻译引擎1
            if not self.object.translation_ui.webdriver1.web_type:
                self.object.translation_ui.webdriver1.web_type = web_type
                utils.thread.createThread(self.object.translation_ui.webdriver1.openWeb, web_type)

            # 刷新翻译引擎2
            elif not self.object.translation_ui.webdriver2.web_type:
                self.object.translation_ui.webdriver2.web_type = web_type
                utils.thread.createThread(self.object.translation_ui.webdriver2.openWeb, web_type)

            # 刷新翻译引擎3
            elif not self.object.translation_ui.webdriver3.web_type:
                self.object.translation_ui.webdriver3.web_type = web_type
                utils.thread.createThread(self.object.translation_ui.webdriver3.openWeb, web_type)


    # 改变节点
    def changeNodeInfo(self) :

        node_name = self.node_info_comboBox.currentText().split("  ")[0]
        if node_name == "自动模式":
            node_url = self.object.yaml["dict_info"]["ocr_server"]
        else:
            node_url = re.sub(r"//.+?/", "//%s/"%self.node_info[node_name], self.object.yaml["dict_info"]["ocr_server"])
        self.object.config["nodeURL"] = node_url


    # 消息弹窗
    def showMessageBox(self, title, text) :

        utils.message.MessageBox(title, text)


    # 关闭进度条弹窗
    def closeProcessBar(self, title, text) :

        self.progress_bar.close()
        utils.message.MessageBox(title, text)


    # 测试公共翻译
    def testPublicTrans(self) :

        self.setCursor(Qt.WaitCursor)
        content = "无法使用公共翻译, 请先安装Chrome浏览器     \n若已安装, 请尝试重新启动翻译器\n若安装并重启后仍无法使用\n可直接通过交流群联系客服娘协助     "
        if translator.all.checkChrome() :
            content = "检测到已安装Chrome浏览器, 可以使用公共翻译     \n请直接打开想使用的翻译源开关"
        elif translator.all.checkFirefox() :
            content = "检测到已安装Firefox浏览器, 可以使用公共翻译     \n请直接打开想使用的翻译源开关"
        elif translator.all.checkEdge() :
            content = "检测到已安装Edge浏览器, 可以使用公共翻译     \n请直接打开想使用的翻译源开关"
        utils.message.MessageBox("测试公共翻译可用性", content)
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)


    # 设置翻译源消息提示
    def setTransLabelMessage(self) :

        if len(self.translate_list) > 0 :
            content = ""
            for val in self.translate_list :
                content += self.translate_map[val]
            self.translate_list_label.setText("当前正在使用%s"%content)
        else :
            self.translate_list_label.setText("请选择开启至少一种翻译源开关, 否则翻译将无法使用")


    # 退出前保存设置
    def saveConfig(self) :

        # OCR开关
        self.object.config["offlineOCR"] = self.offline_ocr_use
        self.object.config["onlineOCR"] = self.online_ocr_use
        self.object.config["onlineOCRProbation"] = self.online_ocr_probation_use
        self.object.config["baiduOCR"] = self.baidu_ocr_use

        # 翻译语种
        if self.language_comboBox.currentIndex() == 1 :
            self.object.config["language"] = "ENG"
        elif self.language_comboBox.currentIndex() == 2 :
            self.object.config["language"] = "KOR"
        elif self.language_comboBox.currentIndex() == 3 :
            self.object.config["language"] = "RU"
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
        # 公共Bing翻译开关
        self.object.config["bingUse"] = str(self.bing_use)
        # 公共彩云翻译开关
        self.object.config["caiyunUse"] = str(self.caiyun_web_use)
        # 私人腾讯翻译开关
        self.object.config["tencentUse"] = str(self.tencent_use)
        # 私人百度翻译开关
        self.object.config["baiduUse"] = str(self.baidu_use)
        # 私人彩云翻译开关
        self.object.config["caiyunPrivateUse"] = str(self.caiyun_use)
        # 私人ChatGPT翻译开关
        self.object.config["chatgptPrivateUse"] = str(self.chatgpt_use)

        # 字体颜色 公共有道
        self.object.config["fontColor"]["youdao"] = self.youdao_color
        # 字体颜色 公共百度
        self.object.config["fontColor"]["baiduweb"] = self.baidu_web_color
        # 字体颜色 公共腾讯
        self.object.config["fontColor"]["tencentweb"] = self.tencent_web_color
        # 字体颜色 公共DeepL
        self.object.config["fontColor"]["deepl"] = self.deepl_color
        # 字体颜色 公共Bing
        self.object.config["fontColor"]["bing"] = self.bing_color
        # 字体颜色 公共彩云
        self.object.config["fontColor"]["caiyun"] = self.caiyun_web_color
        # 字体颜色 私人腾讯
        self.object.config["fontColor"]["tencent"] = self.tencent_color
        # 字体颜色 私人百度
        self.object.config["fontColor"]["baidu"] = self.baidu_color
        # 字体颜色 私人彩云
        self.object.config["fontColor"]["caiyunPrivate"] = self.caiyun_color
        # 字体颜色 私人ChatGPT
        self.object.config["fontColor"]["chatgptPrivate"] = self.chatgpt_color
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
        self.object.config["showHotKey3"] = self.hide_range_hotkey_use
        # 是否全屏下置顶开关
        self.object.config["setTop"] = self.set_top_use
        # 是否同步翻译历史开关
        self.object.config["agreeCollectUse"] = self.agree_collect_use
        # 自动朗读开关
        self.object.config["autoPlaysoundUse"] = self.auto_playsound_use


    # 窗口显示信号
    def showEvent(self, e):

        # 如果处于自动模式下则暂停
        if self.object.translation_ui.translate_mode :
            self.object.translation_ui.stop_sign = True
        # 刷新在线ocr试用次数
        utils.thread.createThread(utils.http.ocrProbationReadCount, self.object)


    # 窗口关闭处理
    def closeEvent(self, event) :

        # 保存设置
        self.saveConfig()
        # 保存本地配置
        utils.config.saveConfig(self.object.yaml, self.logger)
        # 重置翻译引擎
        self.resetWebdriver()
        # 刷新百度OCR的AccessToken
        if self.baidu_ocr_use :
            translator.ocr.baidu.getAccessToken(self.object)
        # 设置上传云端
        utils.thread.createThread(utils.config.postSaveSettin, self.object)
        # 保存云本地配置
        utils.config.saveCloudConfigToLocal(self.object)

        self.hide()
        self.object.translation_ui.show()
        if self.object.range_ui.show_sign == True :
            self.object.range_ui.show()