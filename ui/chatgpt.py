# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import translator.api
import ui.static.icon
import utils.thread
import utils.test
import webbrowser
import re
import urllib.parse
import utils.message
import ui.switch
import qtawesome

# 私人ChatGPT设置界面
class ChatGPTSetting(QWidget) :

    def __init__(self, object) :

        super(ChatGPTSetting, self).__init__()
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
        self.setWindowTitle("私人ChatGPT翻译设置 - 退出会自动保存")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 界面样式
        self.setStyleSheet("QWidget { font: 9pt '%s'; color: %s; background: rgba(255, 255, 255, 1);}"
                           "QLineEdit { background: transparent; border-width:0; border-style:outset; border-bottom: 2px solid %s;}"
                           "QLineEdit:focus { border-bottom: 2px dashed %s; }"
                           "QLabel {color: %s;}"
                           "QComboBox QAbstractItemView::item { min-height:40px;}"
                           "QPushButton { background: %s; border-radius: %spx; color: rgb(255, 255, 255);}"
                           "QPushButton:hover { background-color: #83AAF9;}"
                           "QPushButton:pressed { background-color: #4480F9; padding-left: 3px; padding-top: 3px;}"
                           "QTextEdit {border: 1px solid black;}"
                           %(self.font, self.color, self.color, self.color, self.color, self.color, 6.66*self.rate))

        # api_key 输入框
        label = QLabel(self)
        self.customSetGeometry(label, 20, 20, 330, 20)
        label.setText("api_key: ")
        self.secret_key_text = QLineEdit(self)
        self.customSetGeometry(self.secret_key_text, 20, 40, 330, 25)
        self.secret_key_text.setText(self.object.config["chatgptAPI"])
        self.secret_key_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 代理地址
        label = QLabel(self)
        self.customSetGeometry(label, 20, 80, 330, 20)
        label.setText("代理地址: ")
        self.proxy_text = QLineEdit(self)
        self.customSetGeometry(self.proxy_text, 20, 100, 330, 25)
        self.proxy_text.setText(self.object.config["chatgptProxy"])
        self.proxy_text.setCursor(ui.static.icon.EDIT_CURSOR)
        label = QLabel(self)
        self.customSetGeometry(label, 20, 130, 330, 20)
        label.setText("填入格式示例: 127.0.0.1:7890 (若留空则不使用代理)")
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # API接口地址
        label = QLabel(self)
        self.customSetGeometry(label, 20, 170, 330, 20)
        label.setText("API接口地址: ")
        self.api_text = QLineEdit(self)
        self.customSetGeometry(self.api_text, 20, 190, 330, 25)
        self.api_text.setText(self.object.config["chatgptApiAddr"])
        self.api_text.setCursor(ui.static.icon.EDIT_CURSOR)
        label = QLabel(self)
        self.customSetGeometry(label, 20, 220, 330, 20)
        label.setText("默认为: https://api.openai.com/v1/chat/completions")
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # 使用的模型
        label = QLabel(self)
        self.customSetGeometry(label, 20, 260, 330, 20)
        label.setText("使用的模型: ")
        self.model_box = CustomComboBox(self)
        self.customSetGeometry(self.model_box, 20, 285, 330, 20)
        # 支持编辑和搜索
        self.model_box.setEditable(True)
        line_edit = QLineEdit()
        completer = self.model_box.completer()
        line_edit.setCompleter(completer)
        # 设置Item支持编辑样式
        self.model_box.setItemDelegate(QStyledItemDelegate())
        utils.thread.createThread(self.getChatgptModels)
        label = QLabel(self)
        self.customSetGeometry(label, 20, 310, 330, 20)
        label.setText("默认为: gpt-3.5-turbo-0613")
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # 联系上下文
        label = QLabel(self)
        self.customSetGeometry(label, 20, 350, 330, 20)
        label.setText("联系上下文: ")
        # 联系上下文开关
        self.context_switch = ui.switch.SwitchOCR(self, sign=self.object.config["chatgptContextUse"], startX=(65-20)*self.rate)
        self.customSetGeometry(self.context_switch, 20, 375, 65, 20)
        self.context_switch.checkedChanged.connect(self.changeContextUseSwitch)
        self.context_switch.setCursor(ui.static.icon.SELECT_CURSOR)
        # 联系上下文句子数
        self.context_spinbox = QSpinBox(self)
        self.customSetGeometry(self.context_spinbox, 100, 375, 60, 20)
        self.context_spinbox.setMinimum(1)
        self.context_spinbox.setMaximum(10)
        self.context_spinbox.setValue(self.object.config["chatgptContextCount"])
        self.context_spinbox.setCursor(ui.static.icon.SELECT_CURSOR)
        self.context_spinbox.valueChanged.connect(self.changeContextCount)
        # 联系上下文标签
        label = QLabel(self)
        self.customSetGeometry(label, 175, 375, 200, 20)
        label.setText("最大句子数")
        # 联系上下文?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color), "", self)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 240, 375, 20, 20)
        button.clicked.connect(self.ContextDesc)
        button.setCursor(ui.static.icon.QUESTION_CURSOR)
        button.setStyleSheet("QPushButton { background: transparent;}"
                             "QPushButton:hover { background-color: #83AAF9; }"
                             "QPushButton:pressed { background-color: #4480F9; padding-left: 3px;padding-top: 3px; }")

        # 催眠话术
        label = QLabel(self)
        self.customSetGeometry(label, 20, 420, 330, 20)
        label.setText("prompt(催眠话术): ")
        self.message_text = QTextEdit(self)
        self.customSetGeometry(self.message_text, 20, 440, 330, 120)
        self.message_text.setCursor(ui.static.icon.SELECT_CURSOR)
        self.message_text.setText(self.object.config["chatgptPrompt"])

        # 测试按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 35, 590, 60, 20)
        button.setText("测试")
        button.clicked.connect(lambda: utils.test.testChatGPT(
            self.object,
            self.filterNullWord(self.secret_key_text),
            self.filterNullWord(self.proxy_text),
            self.filterNullWord(self.api_text),
            self.model_box.currentText(),
            self.checkPrompt(),
        ))
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 注册按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 115, 590, 60, 20)
        button.setText("注册")
        button.clicked.connect(self.openTutorial)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 查额度按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 195, 590, 60, 20)
        button.setText("查额度")
        button.clicked.connect(self.openQueryQuota)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 查额度按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 275, 590, 60, 20)
        button.setText("重置")
        button.clicked.connect(self.clickResetButton)
        button.setCursor(ui.static.icon.SELECT_CURSOR)


    # 获取ChatGPT模型列表
    def getChatgptModels(self) :

        models = translator.api.getChatgptModels(
            api_key=self.object.config["chatgptAPI"],
            proxy=self.object.config["chatgptProxy"],
            logger=self.object.logger
        )
        if models :
            for model in models :
                if model not in self.model_list :
                    self.model_list.append(model)
        # 添加下拉框选项
        for i, model in enumerate(self.model_list):
            self.model_box.addItem("")
            self.model_box.setItemText(i, model)
        if self.object.config["chatgptModel"] in self.model_list :
            self.model_box.setCurrentText(self.object.config["chatgptModel"])


    # 初始化配置
    def getInitConfig(self) :

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面尺寸
        self.window_width = int(370 * self.rate)
        self.window_height = int(650 * self.rate)
        # 颜色
        self.color = "#5B8FF9"
        self.font = "华康方圆体W7"
        # 模型列表
        self.model_list = [
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0301",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4",
            "gpt-4-0314",
            "gpt-4-32k",
            "gpt-4-32k-0314",
            "gpt-4-0413",
            "gpt-4-0613",
        ]


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 根据分辨率定义图标位置尺寸
    def customSetIconSize(self, object, w, h) :

        object.setIconSize(QSize(int(w * self.rate),
                                 int(h * self.rate)))


    # 打开注册教程
    def openTutorial(self) :

        try :
            url = self.object.yaml["dict_info"]["chatgpt_tutorial"]
            webbrowser.open(url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())
            utils.message.MessageBox("私人ChatGPT注册",
                                     "请尝试手动打开此地址:\n%s     " % url)


    # 打开查询额度地址
    def openQueryQuota(self) :

        url = "https://platform.openai.com/account/usage"
        try :
            webbrowser.open(url, new=0, autoraise=True)
        except Exception :
            self.logger.error(format_exc())
            utils.message.MessageBox("私人ChatGPT额度查询",
                                     "打开地址失败, 请尝试手动打开此网页下载\n%s     " % url)


    # 过滤空字符
    def filterNullWord(self, obj) :

        text = obj.text().strip()
        obj.setText(text)
        return text


    # 校验代理地址
    def checkProxy(self) :

        return re.fullmatch("\d+\.\d+\.\d+\.\d+:\d+", self.proxy_text.text().strip())


    # 校验催眠话术
    def checkPrompt(self) :

        chatgpt_prompt = self.message_text.toPlainText().strip()
        self.message_text.setText(chatgpt_prompt)
        return chatgpt_prompt


    # 点击重置按钮
    def clickResetButton(self) :

        message_box = utils.message.createMessageBox("重置chatgpt配置", "确定要将chatgpt的所有配置项重置吗？     ", self.rate)
        button = QPushButton("确定")
        button.clicked.connect(self.resetConfig)
        message_box.addButton(button, QMessageBox.YesRole)
        message_box.addButton(QPushButton("取消"), QMessageBox.NoRole)
        message_box.exec_()


    # 重置chatgpt配置
    def resetConfig(self) :

        # 重置API密钥
        self.secret_key_text.setText("")
        self.object.config["chatgptAPI"] = ""
        # 重置代理地址
        self.proxy_text.setText("")
        self.object.config["chatgptProxy"] = ""
        # 重置API地址
        self.api_text.setText("https://api.openai.com/v1/chat/completions")
        self.object.config["chatgptAPI"] = "https://api.openai.com/v1/chat/completions"
        # 重置模型
        self.model_box.setCurrentText("gpt-3.5-turbo-0613")
        self.object.config["chatgptModel"] = "gpt-3.5-turbo-0613"
        # 重置催眠话术
        self.message_text.setText(translator.api.CHATGPT_PROMPT)
        self.object.config["chatgptPrompt"] = translator.api.CHATGPT_PROMPT
        # 重置联系上下文开关
        if not self.object.config["chatgptContextUse"] :
            self.context_switch.mousePressEvent(1)
            self.context_switch.updateValue()
            self.object.config["chatgptContextUse"] = False
        # 重置联系上下文句子数
        self.context_spinbox.setValue(3)
        self.object.config["chatgptContextCount"] = 3


    # 改变联系上下文开关状态
    def changeContextUseSwitch(self, checked) :

        self.object.config["chatgptContextUse"] = checked


    # 改变联系上下文句子数
    def changeContextCount(self, value) :

        self.object.config["chatgptContextCount"] = value


    # 联系上下文说明
    def ContextDesc(self) :

        desc_ui = self.object.settin_ui.desc_ui
        signal = self.object.settin_ui.desc_signal
        desc_ui.desc_text.clear()
        desc_ui.show()

        desc_ui.setWindowTitle("chatgpt联系上下文说明")
        signal.emit("\n开关开启后, chatgpt会联系之前翻译过的句子场景进行翻译, 可能会提高翻译准确率, 但是会消耗更多的翻译额度\n\n最大可联系句子为10, 默认值为3")
        QApplication.processEvents()


    # 窗口关闭处理
    def closeEvent(self, event) :

        if self.proxy_text.text().strip() != "" :
            if not self.checkProxy() :
                utils.message.MessageBox("私人ChatGPT配置", "代理地址格式错误, 请检查    ")
                return event.ignore()
        if not self.checkPrompt() :
            utils.message.MessageBox("私人ChatGPT配置", "催眠话术不能为空    ")
            return event.ignore()

        self.object.config["chatgptAPI"] = self.filterNullWord(self.secret_key_text)
        self.object.config["chatgptProxy"] = self.filterNullWord(self.proxy_text)
        self.object.config["chatgptApiAddr"] = self.filterNullWord(self.api_text)
        self.object.config["chatgptModel"] = self.model_box.currentText()
        self.object.config["chatgptPrompt"] = self.checkPrompt()


# 自定义禁用鼠标滚轮事件的ComboBox
class CustomComboBox(QComboBox) :

    def __init__(self, parent=None) :
        super().__init__(parent)

    def wheelEvent(self, event) :
        event.ignore()