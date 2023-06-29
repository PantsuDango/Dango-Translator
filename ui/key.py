# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ui.static.icon


# 密钥界面
class Key(QWidget) :

    def __init__(self, object) :

        super(Key, self).__init__()
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
        self.setWindowTitle("说明")
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
                           %(self.color, self.color, self.color))

        # 百度OCR API Key 输入框
        self.baidu_ocr_key_textEdit = QLineEdit(self)
        self.customSetGeometry(self.baidu_ocr_key_textEdit, 20, 10, 330, 25)
        self.baidu_ocr_key_textEdit.setPlaceholderText("百度OCR API Key")
        self.baidu_ocr_key_textEdit.setText(self.object.config["OCR"]["Key"])
        self.baidu_ocr_key_textEdit.hide()
        self.baidu_ocr_key_textEdit.setCursor(ui.static.icon.EDIT_CURSOR)

        # 百度OCR Secret Key 输入框
        self.baidu_ocr_secret_textEdit = QLineEdit(self)
        self.customSetGeometry(self.baidu_ocr_secret_textEdit, 20, 45, 330, 25)
        self.baidu_ocr_secret_textEdit.setPlaceholderText("百度OCR Secret Key")
        self.baidu_ocr_secret_textEdit.setText(self.object.config["OCR"]["Secret"])
        self.baidu_ocr_secret_textEdit.hide()
        self.baidu_ocr_secret_textEdit.setCursor(ui.static.icon.EDIT_CURSOR)

        # 私人腾讯 SecretId 输入框
        self.tencent_private_key_textEdit = QLineEdit(self)
        self.customSetGeometry(self.tencent_private_key_textEdit, 20, 10, 330, 25)
        self.tencent_private_key_textEdit.setPlaceholderText("私人腾讯 SecretId")
        self.tencent_private_key_textEdit.setText(self.object.config["tencentAPI"]["Key"])
        self.tencent_private_key_textEdit.hide()
        self.tencent_private_key_textEdit.setCursor(ui.static.icon.EDIT_CURSOR)

        # 私人腾讯 SecretKey 输入框
        self.tencent_private_secret_textEdit = QLineEdit(self)
        self.customSetGeometry(self.tencent_private_secret_textEdit, 20, 45, 330, 25)
        self.tencent_private_secret_textEdit.setPlaceholderText("私人腾讯 SecretKey")
        self.tencent_private_secret_textEdit.setText(self.object.config["tencentAPI"]["Secret"])
        self.tencent_private_secret_textEdit.hide()
        self.tencent_private_secret_textEdit.setCursor(ui.static.icon.EDIT_CURSOR)

        # 私人百度 APP ID 输入框
        self.baidu_private_key_textEdit = QLineEdit(self)
        self.customSetGeometry(self.baidu_private_key_textEdit, 20, 10, 330, 25)
        self.baidu_private_key_textEdit.setPlaceholderText("私人百度 APP ID")
        self.baidu_private_key_textEdit.setText(self.object.config["baiduAPI"]["Key"])
        self.baidu_private_key_textEdit.hide()
        self.baidu_private_key_textEdit.setCursor(ui.static.icon.EDIT_CURSOR)

        # 私人百度 密钥 输入框
        self.baidu_private_secret_textEdit = QLineEdit(self)
        self.customSetGeometry(self.baidu_private_secret_textEdit, 20, 45, 330, 25)
        self.baidu_private_secret_textEdit.setPlaceholderText("私人百度 密钥")
        self.baidu_private_secret_textEdit.setText(self.object.config["baiduAPI"]["Secret"])
        self.baidu_private_secret_textEdit.hide()
        self.baidu_private_secret_textEdit.setCursor(ui.static.icon.EDIT_CURSOR)

        # 私人彩云 APP ID 输入框
        self.caiyun_private_key_textEdit = QLineEdit(self)
        self.customSetGeometry(self.caiyun_private_key_textEdit, 20, 20, 330, 25)
        self.caiyun_private_key_textEdit.setPlaceholderText("私人彩云 令牌")
        self.caiyun_private_key_textEdit.setText(self.object.config["caiyunAPI"])
        self.caiyun_private_key_textEdit.hide()
        self.caiyun_private_key_textEdit.setCursor(ui.static.icon.EDIT_CURSOR)

        # 私人ChatGPT api_key 输入框
        self.chatgpt_private_key_textEdit = QLineEdit(self)
        self.customSetGeometry(self.chatgpt_private_key_textEdit, 20, 20, 330, 25)
        self.chatgpt_private_key_textEdit.setPlaceholderText("私人ChatGPT api_key")
        self.chatgpt_private_key_textEdit.setText(self.object.config["chatgptAPI"])
        self.chatgpt_private_key_textEdit.hide()
        self.chatgpt_private_key_textEdit.setCursor(ui.static.icon.EDIT_CURSOR)

        # 私人ChatGPT 代理 输入框
        self.chatgpt_private_proxy_textEdit = QLineEdit(self)
        self.customSetGeometry(self.chatgpt_private_proxy_textEdit, 20, 20, 330, 25)
        self.chatgpt_private_proxy_textEdit.setPlaceholderText("私人ChatGPT 代理")
        self.chatgpt_private_proxy_textEdit.setText(self.object.config["chatgptProxy"])
        self.chatgpt_private_proxy_textEdit.hide()
        self.chatgpt_private_proxy_textEdit.setCursor(ui.static.icon.EDIT_CURSOR)

        # 私人ChatGPT 代理标签
        self.chatgpt_private_proxy_label = QLabel(self)
        self.customSetGeometry(self.chatgpt_private_proxy_label, 20, 55, 330, 20)
        self.chatgpt_private_proxy_label.setText("填入格式示例: 127.0.0.1:7890")
        self.chatgpt_private_proxy_label.hide()


    # 初始化配置
    def getInitConfig(self) :

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面尺寸
        self.window_width = int(370 * self.rate)
        self.window_height = int(95 * self.rate)
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


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.object.config["OCR"]["Key"] = self.filterNullWord(self.baidu_ocr_key_textEdit)
        self.object.config["OCR"]["Secret"] = self.filterNullWord(self.baidu_ocr_secret_textEdit)
        self.object.config["tencentAPI"]["Key"] = self.filterNullWord(self.tencent_private_key_textEdit).replace("SecretId: ", "")
        self.object.config["tencentAPI"]["Secret"] = self.filterNullWord(self.tencent_private_secret_textEdit).replace("SecretKey: ", "")
        self.object.config["baiduAPI"]["Key"] = self.filterNullWord(self.baidu_private_key_textEdit)
        self.object.config["baiduAPI"]["Secret"] = self.filterNullWord(self.baidu_private_secret_textEdit)
        self.object.config["caiyunAPI"] = self.filterNullWord(self.caiyun_private_key_textEdit)
        self.object.config["chatgptAPI"] = self.filterNullWord(self.chatgpt_private_key_textEdit)
        self.object.config["chatgptProxy"] = self.filterNullWord(self.chatgpt_private_proxy_textEdit)

        self.baidu_ocr_key_textEdit.hide()
        self.baidu_ocr_secret_textEdit.hide()
        self.tencent_private_key_textEdit.hide()
        self.tencent_private_secret_textEdit.hide()
        self.baidu_private_key_textEdit.hide()
        self.baidu_private_secret_textEdit.hide()
        self.caiyun_private_key_textEdit.hide()
        self.chatgpt_private_key_textEdit.hide()
        self.chatgpt_private_proxy_textEdit.hide()
        self.chatgpt_private_proxy_label.hide()


# ChatGPT编辑界面
class ChatGPTKey(QWidget) :

    def __init__(self, object) :

        super(ChatGPTKey, self).__init__()
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
        self.setWindowTitle("私人ChatGPT设置 - 退出会自动保存")
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
                          "QComboBox QAbstractItemView::item { min-height:40px; }"
                           %(self.color, self.color, self.color, self.color))

        # 代理地址
        label = QLabel(self)
        self.customSetGeometry(label, 20, 20, 330, 20)
        label.setText("代理地址: ")
        self.proxy_text = QLineEdit(self)
        self.customSetGeometry(self.proxy_text, 20, 40, 330, 25)
        self.proxy_text.setPlaceholderText("私人ChatGPT 代理")
        self.proxy_text.setText(self.object.config["chatgptProxy"])
        self.proxy_text.setCursor(ui.static.icon.EDIT_CURSOR)
        label = QLabel(self)
        self.customSetGeometry(label, 20, 70, 330, 20)
        label.setText("填入格式示例: 127.0.0.1:7890 (若留空则不使用代理)")
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # API接口地址
        label = QLabel(self)
        self.customSetGeometry(label, 20, 110, 330, 20)
        label.setText("API接口地址: ")
        self.api_text = QLineEdit(self)
        self.customSetGeometry(self.api_text, 20, 130, 330, 25)
        self.api_text.setPlaceholderText("私人ChatGPT API接口地址")
        self.api_text.setText(self.object.config["chatgptApiAddr"])
        self.api_text.setCursor(ui.static.icon.EDIT_CURSOR)
        label = QLabel(self)
        self.customSetGeometry(label, 20, 160, 330, 20)
        label.setText("默认为: https://api.openai.com/v1/chat/completions")
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # 使用的模型
        label = QLabel(self)
        self.customSetGeometry(label, 20, 200, 330, 20)
        label.setText("使用的模型: ")
        self.model_box = QComboBox(self)
        self.customSetGeometry(self.model_box, 20, 225, 330, 20)
        # 支持编辑和搜索
        self.model_box.setEditable(True)
        line_edit = QLineEdit()
        completer = self.model_box.completer()
        line_edit.setCompleter(completer)
        # 设置Item支持编辑样式
        self.model_box.setItemDelegate(QStyledItemDelegate())
        # 添加下拉框选项
        for i, model in enumerate(self.model_list) :
            self.model_box.addItem("")
            self.model_box.setItemText(i, model)
        self.model_box.setCurrentText(self.object.config["chatgptModel"])
        label = QLabel(self)
        self.customSetGeometry(label, 20, 250, 330, 20)
        label.setText("默认为: gpt-3.5-turbo-0613")
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)


    # 初始化配置
    def getInitConfig(self) :

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面尺寸
        self.window_width = int(370 * self.rate)
        self.window_height = int(300 * self.rate)
        # 颜色
        self.color = "#5B8FF9"
        # 模型列表
        self.model_list = [
            "whisper-1",
            "babbage",
            "davinci",
            "text-davinci-edit-001",
            "babbage-code-search-code",
            "text-similarity-babbage-001",
            "code-davinci-edit-001",
            "text-davinci-001",
            "ada",
            "babbage-code-search-text",
            "babbage-similarity",
            "code-search-babbage-text-001",
            "text-curie-001",
            "code-search-babbage-code-001",
            "gpt-3.5-turbo-0613",
            "text-ada-001",
            "text-similarity-ada-001",
            "curie-instruct-beta",
            "gpt-3.5-turbo",
            "ada-code-search-code",
            "ada-similarity",
            "code-search-ada-text-001",
            "text-search-ada-query-001",
            "davinci-search-document",
            "ada-code-search-text",
            "text-search-ada-doc-001",
            "gpt-3.5-turbo-0301",
            "davinci-instruct-beta",
            "text-similarity-curie-001",
            "code-search-ada-code-001",
            "ada-search-query",
            "text-search-davinci-query-001",
            "curie-search-query",
            "davinci-search-query",
            "babbage-search-document",
            "ada-search-document",
            "text-search-curie-query-001",
            "text-search-babbage-doc-001",
            "curie-search-document",
            "text-search-curie-doc-001",
            "babbage-search-query",
            "text-babbage-001",
            "text-search-davinci-doc-001",
            "text-search-babbage-query-001",
            "curie-similarity",
            "gpt-3.5-turbo-16k-0613",
            "curie",
            "text-embedding-ada-002",
            "gpt-3.5-turbo-16k",
            "text-similarity-davinci-001",
            "text-davinci-002",
            "text-davinci-003",
            "davinci-similarity",
        ]


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


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.object.config["chatgptProxy"] = self.filterNullWord(self.proxy_text)
        self.object.config["chatgptApiAddr"] = self.filterNullWord(self.api_text)
        self.object.config["chatgptModel"] = self.model_box.currentText()