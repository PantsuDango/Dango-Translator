# -*- coding: utf-8 -*-
import copy
import time

from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import io
import base64
import shutil
import json
from math import sqrt
import webbrowser
import qtawesome
from PIL import Image

import ui.static.icon
import utils.translater
import translator.ocr.dango
import translator.api
import utils.thread
import utils.message
import ui.progress_bar


FONT_PATH_1 = "./config/other/NotoSansSC-Regular.otf"
FONT_PATH_2 = "./config/other/华康方圆体W7.TTC"


# 译文编辑界面
class TransEdit(QWidget) :

    def __init__(self, object) :

        super(TransEdit, self).__init__()
        self.object = object
        self.rate = object.yaml["screen_scale_rate"]
        self.logger = object.logger
        self.font_color = ""
        self.bg_color = ""
        self.rect = []
        self.rdr_image_path = ""
        self.text_block = {}
        self.index = 0
        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.window_width = int(500*self.rate)
        self.window_height = int(300*self.rate)
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("漫画翻译-译文编辑")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        font_type = "华康方圆体W7"
        try :
            id = QFontDatabase.addApplicationFont(FONT_PATH_1)
            font_list = QFontDatabase.applicationFontFamilies(id)
            font_type = font_list[0]
        except Exception :
            pass

        # 修改字体颜色
        self.font_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.font_color), "", self)
        self.customSetGeometry(self.font_color_button, 0, 0, 70, 30)
        self.font_color_button.setCursor(ui.static.icon.EDIT_CURSOR)
        self.font_color_button.setText(" 字体色")
        self.font_color_button.clicked.connect(self.changeTranslateColor)
        self.font_color_button.setStyleSheet("QPushButton {background: transparent; font: 8pt '华康方圆体W7';}"
                                             "QPushButton:hover {background-color: #83AAF9;}"
                                             "QPushButton:pressed {background-color: #4480F9;}")
        self.font_color_button.setToolTip("<b>修改显示的字体颜色</b>")

        # 修改轮廓颜色
        self.bg_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.bg_color), "", self)
        self.customSetGeometry(self.bg_color_button, 70, 0, 70, 30)
        self.bg_color_button.setCursor(ui.static.icon.EDIT_CURSOR)
        self.bg_color_button.setText(" 轮廓色")
        self.bg_color_button.clicked.connect(self.changeBackgroundColor)
        self.bg_color_button.setStyleSheet("QPushButton {background: transparent; font: 8pt '华康方圆体W7';}"
                                           "QPushButton:hover {background-color: #83AAF9;}"
                                           "QPushButton:pressed {background-color: #4480F9;}")
        self.bg_color_button.setToolTip("<b>修改显示的轮廓颜色</b>")

        # 私人彩云
        button = QPushButton(self)
        self.customSetGeometry(button, 140, 0, 70, 30)
        button.setCursor(ui.static.icon.EDIT_CURSOR)
        button.setText(" 彩云")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        button.setStyleSheet("QPushButton {background: transparent; font: 8pt '华康方圆体W7';}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.clicked.connect(lambda: self.refreshTrans("彩云"))
        button.setToolTip("<b>使用私人彩云重新翻译</b>")

        # 私人腾讯
        button = QPushButton(self)
        self.customSetGeometry(button, 210, 0, 70, 30)
        button.setCursor(ui.static.icon.EDIT_CURSOR)
        button.setText(" 腾讯")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        button.setStyleSheet("QPushButton {background: transparent; font: 8pt '华康方圆体W7';}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.clicked.connect(lambda: self.refreshTrans("腾讯"))
        button.setToolTip("<b>使用私人腾讯重新翻译</b>")

        # 私人百度
        button = QPushButton(self)
        self.customSetGeometry(button, 280, 0, 70, 30)
        button.setCursor(ui.static.icon.EDIT_CURSOR)
        button.setText(" 百度")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        button.setStyleSheet("QPushButton {background: transparent; font: 8pt '华康方圆体W7';}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.clicked.connect(lambda: self.refreshTrans("百度"))
        button.setToolTip("<b>使用私人百度重新翻译</b>")

        # 私人ChatGPT
        button = QPushButton(self)
        self.customSetGeometry(button, 350, 0, 70, 30)
        button.setCursor(ui.static.icon.EDIT_CURSOR)
        button.setText(" ChatGPT")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        button.setStyleSheet("QPushButton {background: transparent; font: 8pt '华康方圆体W7'; border-radius: 6px}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.clicked.connect(lambda: self.refreshTrans("ChatGPT"))
        button.setToolTip("<b>使用私人ChatGPT重新翻译</b>")

        # 原文编辑框
        self.original_text = QTextBrowser(self)
        self.customSetGeometry(self.original_text, 0, 30, 500, 100)
        self.original_text.setCursor(ui.static.icon.PIXMAP_CURSOR)
        self.original_text.setReadOnly(False)
        self.original_text.setStyleSheet("background-color: rgb(224, 224, 224); font: 10pt '%s';"%font_type)
        self.original_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 译文编辑框
        self.trans_text = QTextBrowser(self)
        self.customSetGeometry(self.trans_text, 0, 130, 500, 100)
        self.trans_text.setCursor(ui.static.icon.PIXMAP_CURSOR)
        self.trans_text.setReadOnly(False)
        self.trans_text.setStyleSheet("font: 10pt '%s';"%font_type)
        self.trans_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 确定按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 125, 240, 100, 50)
        button.setText("重新贴字")
        button.setStyleSheet("font: 12pt '华康方圆体W7';")
        button.clicked.connect(self.renderTextBlock)
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        button.setCursor(ui.static.icon.EDIT_CURSOR)

        # 取消按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 275, 240, 100, 50)
        button.setText("取消")
        button.setStyleSheet("font: 12pt '华康方圆体W7';")
        button.clicked.connect(self.close)
        button.setCursor(ui.static.icon.SELECT_CURSOR)
        button.setCursor(ui.static.icon.EDIT_CURSOR)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 重新渲染文字
    def renderTextBlock(self) :

        # 获取ipt图片路径
        file_name = os.path.splitext(os.path.basename(self.rdr_image_path))[0]
        ipt_image_path = os.path.join(os.path.dirname(self.rdr_image_path), "tmp", "{}_ipt.png".format(file_name))

        # 打开ipt图片, 按照文本块坐标截图
        image = Image.open(ipt_image_path)
        x, y, w, h = self.rect[0], self.rect[1], self.rect[2], self.rect[3]
        cropped_image = image.crop((x, y, x + w, y + h))

        # 截图转换为base64
        buffered = io.BytesIO()
        cropped_image.save(buffered, format="PNG")
        inpainted_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        text_block = copy.deepcopy(self.text_block)
        # 修改字体颜色
        color = QColor(self.font_color)
        f_r, f_g, f_b, f_a = color.getRgb()
        text_block["foreground_color"] = [f_r, f_g, f_b]
        # 修改轮廓颜色
        color = QColor(self.bg_color)
        b_r, b_g, b_b, b_a = color.getRgb()
        text_block["background_color"] = [b_r, b_g, b_b]

        # 重新计算截图后的坐标
        text_block["block_coordinate"]["upper_left"] = [0, 0]
        text_block["block_coordinate"]["upper_right"] = [w, 0]
        text_block["block_coordinate"]["lower_right"] = [w, h]
        text_block["block_coordinate"]["lower_left"] = [0, h]
        for index, val in enumerate(text_block["coordinate"]) :
            coordinate = {}
            for k in val.keys() :
                coordinate[k] = [val[k][0]-x, val[k][1]-y]
            text_block["coordinate"][index] = coordinate

        # 漫画rdr
        sign, result = translator.ocr.dango.mangaRDR(
            object=self.object,
            trans_list=[self.trans_text.toPlainText()],
            inpainted_image=inpainted_image,
            text_block=[text_block]
        )
        if not sign :
            print(result)
            #@TODO 错误处理
            return

        # 渲染后的新图贴在大图上
        ipt_image = Image.open(io.BytesIO(base64.b64decode(result["rendered_image"])))
        rdr_image = Image.open(self.rdr_image_path)
        rdr_image.paste(ipt_image, (x, y))
        rdr_image.save(self.rdr_image_path)

        # 刷新缓存文件中获取json结果
        json_file_path = os.path.join(os.path.dirname(ipt_image_path), "%s.json" % file_name)
        with open(json_file_path, "r", encoding="utf-8") as file :
            json_data = json.load(file)
        json_data["translated_text"][self.index] = self.trans_text.toPlainText()
        json_data["text_block"][self.index]["foreground_color"] = [f_r, f_g, f_b]
        json_data["text_block"][self.index]["background_color"] = [b_r, b_g, b_b]

        # 缓存ocr结果
        with open(json_file_path, "w", encoding="utf-8") as file :
            json.dump(json_data, file, indent=4)

        # 刷新大图
        w_rate = self.object.manga_ui.width() / self.object.manga_ui.window_width
        h_rate = self.object.manga_ui.height() / self.object.manga_ui.window_height
        self.object.manga_ui.show_image_scroll_area.setWidget(None)
        self.object.manga_ui.show_image_widget = RenderTextBlock(
            rate=(w_rate, h_rate),
            image_path=self.rdr_image_path,
            json_data=json_data,
            edit_window=self
        )
        self.object.manga_ui.show_image_scroll_area.setWidget(self.object.manga_ui.show_image_widget)
        self.object.manga_ui.show_image_scroll_area.show()

        self.close()


    # 刷新翻译结果
    def refreshTrans(self, trans_type) :

        original = self.original_text.toPlainText()
        if trans_type == "彩云":
            result = translator.api.caiyun(sentence=original,
                                           token=self.object.config["caiyunAPI"],
                                           logger=self.logger)
        elif trans_type == "腾讯":
            result = translator.api.tencent(sentence=original,
                                            secret_id=self.object.config["tencentAPI"]["Key"],
                                            secret_key=self.object.config["tencentAPI"]["Secret"],
                                            logger=self.logger)
        elif trans_type == "百度":
            result = translator.api.baidu(sentence=original,
                                          app_id=self.object.config["baiduAPI"]["Key"],
                                          secret_key=self.object.config["baiduAPI"]["Secret"],
                                          logger=self.logger)
        elif trans_type == "ChatGPT":
            result = translator.api.chatgpt(api_key=self.object.config["chatgptAPI"],
                                            language=self.object.config["language"],
                                            proxy=self.object.config["chatgptProxy"],
                                            content=original,
                                            logger=self.logger)
        else :
            return

        if result :
            self.trans_text.clear()
            self.trans_text.insertPlainText(result)


    # 修改字体颜色
    def changeTranslateColor(self):

        color = QColorDialog.getColor(QColor(self.font_color), None, "修改字体颜色")
        if color.isValid() :
            self.font_color = color.name()
            self.font_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=self.font_color))
            # 原文
            text = self.original_text.toPlainText()
            self.original_text.clear()
            self.original_text.setTextColor(color)
            self.original_text.insertPlainText(text)
            # 译文
            text = self.trans_text.toPlainText()
            self.trans_text.clear()
            self.trans_text.setTextColor(color)
            self.trans_text.insertPlainText(text)


    # 修改轮廓颜色
    def changeBackgroundColor(self):

        color = QColorDialog.getColor(QColor(self.bg_color), None, "修改字体颜色")
        if color.isValid():
            self.bg_color = color.name()
            self.bg_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=self.bg_color))


# 根据文本块大小计算font_size
def getFontSize(coordinate, trans_text) :

    lines = []
    for val in coordinate :
        line = []
        line.append(val["upper_left"])
        line.append(val["upper_right"])
        line.append(val["lower_right"])
        line.append(val["lower_left"])
        lines.append(line)

    line_x = [j[0] for i in lines for j in i]
    line_y = [j[1] for i in lines for j in i]
    w = max(line_x) - min(line_x)
    h = max(line_y) - min(line_y)


    def get_structure(pts) :

        p1 = [int((pts[0][0] + pts[1][0]) / 2), int((pts[0][1] + pts[1][1]) / 2)]
        p2 = [int((pts[2][0] + pts[3][0]) / 2), int((pts[2][1] + pts[3][1]) / 2)]
        p3 = [int((pts[1][0] + pts[2][0]) / 2), int((pts[1][1] + pts[2][1]) / 2)]
        p4 = [int((pts[3][0] + pts[0][0]) / 2), int((pts[3][1] + pts[0][1]) / 2)]
        return [p1, p2, p3, p4]


    def get_font_size(pts) -> float :

        [l1a, l1b, l2a, l2b] = [a for a in get_structure(pts)]
        v1 = [l1b[0] - l1a[0], l1b[1] - l1a[1]]
        v2 = [l2b[0] - l2a[0], l2b[1] - l2a[1]]
        return min(sqrt(v2[0] ** 2 + v2[1] ** 2), sqrt(v1[0] ** 2 + v1[1] ** 2))


    def findNextPowerOf2(n) :

        i = 0
        while n != 0:
            i += 1
            n = n >> 1
        return 1 << i

    font_size = int(min([get_font_size(pts) for pts in lines]))
    text_mag_ratio = 1

    font_size_enlarged = findNextPowerOf2(font_size) * text_mag_ratio
    enlarge_ratio = font_size_enlarged / font_size
    font_size = font_size_enlarged

    while True:
        enlarged_w = round(enlarge_ratio * w)
        enlarged_h = round(enlarge_ratio * h)
        rows = enlarged_h // (font_size * 1.3)
        cols = enlarged_w // (font_size * 1.3)
        if rows * cols < len(trans_text) :
            enlarge_ratio *= 1.1
            continue
        break

    return int(font_size / enlarge_ratio)


# 渲染文本块
class RenderTextBlock(QWidget) :

    def __init__(self, rate, image_path, json_data, edit_window) :

        super(RenderTextBlock, self).__init__()
        self.rate = rate
        self.image_path = image_path
        self.json_data = json_data
        self.trans_edit_ui = edit_window
        self.image_rate = []
        self.button_list = []
        self.ui()


    def ui(self) :

        # 窗口大小
        self.resize(1000*self.rate[0], 635*self.rate[1])
        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)

        # 图片大图展示
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(0, 0, self.width(), self.height())
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.image_label = QLabel(self)
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        widget.setLayout(layout)
        self.scroll_area.setWidget(widget)

        # 显示图片缩放比例
        self.rate_label = QLabel(self)
        self.rate_label.setGeometry(950*self.rate[0], 590*self.rate[1], 30*self.rate[0], 30*self.rate[1])
        # 载入大图
        self.loadImage()

        if not self.json_data or \
                not self.json_data.get("text_block", []) or \
                not self.json_data.get("translated_text", []) :
            return
        # 渲染文本框
        index = 0
        for text_block, trans_text in zip(self.json_data["text_block"], self.json_data["translated_text"]) :
            # 计算文本坐标
            x_0 = text_block["block_coordinate"]["upper_left"][0]
            y_0 = text_block["block_coordinate"]["upper_left"][1]
            w_0 = text_block["block_coordinate"]["lower_right"][0] - x_0
            h_0 = text_block["block_coordinate"]["lower_right"][1] - y_0
            # 计算缩放比例
            x = x_0*self.image_rate[0]
            y = y_0*self.image_rate[1]
            w = w_0*self.image_rate[0]
            h = h_0*self.image_rate[1]
            # 文本颜色
            font_color = tuple(text_block["foreground_color"])
            bg_color = tuple(text_block["background_color"])
            # 绘制矩形框
            button = QPushButton(self.image_label)
            button.setGeometry(x, y, w, h)
            button.setStyleSheet("QPushButton {background: transparent; border: 2px dashed red;}"
                                 "QPushButton:hover {background-color:rgba(62, 62, 62, 0.1)}")
            original = ""
            for text in text_block["texts"] :
                original += text
            button.clicked.connect(lambda _,
                                          x=original,
                                          y=trans_text,
                                          z=font_color,
                                          f=bg_color,
                                          j=(x_0, y_0, w_0, h_0),
                                          k=text_block,
                                          i=index :
                                   self.clickTextBlock(x, y, z, f, j, k, i))
            index += 1
            self.button_list.append(button)


    # 加载大图
    def loadImage(self) :

        if not os.path.exists(self.image_path) :
            return
        with open(self.image_path, "rb") as file :
            image = QImage.fromData(file.read())
        self.image_pixmap = QPixmap.fromImage(image)
        self.matchImageSize()


    # 点击文本框
    def clickTextBlock(self, original, trans, font_color, bg_color, rect, text_block, index) :

        self.trans_edit_ui.index = index
        self.trans_edit_ui.text_block = text_block
        self.trans_edit_ui.rdr_image_path = self.image_path
        self.trans_edit_ui.rect = rect
        # 文本颜色
        font_color = QColor(font_color[0], font_color[1], font_color[2])
        self.trans_edit_ui.font_color = font_color.name()
        self.trans_edit_ui.font_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=font_color.name()))
        # 轮廓颜色
        bg_color = QColor(bg_color[0], bg_color[1], bg_color[2])
        self.trans_edit_ui.bg_color = bg_color.name()
        self.trans_edit_ui.bg_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=bg_color.name()))
        # 原文
        self.trans_edit_ui.original_text.clear()
        self.trans_edit_ui.original_text.setTextColor(font_color)
        self.trans_edit_ui.original_text.insertPlainText(original)
        # 译文
        self.trans_edit_ui.trans_text.clear()
        self.trans_edit_ui.trans_text.setTextColor(font_color)
        self.trans_edit_ui.trans_text.insertPlainText(trans)

        self.trans_edit_ui.show()


    # 图片自适配比例
    def matchImageSize(self):

        pixmap = self.image_pixmap
        if pixmap.height() > self.height():
            rate = self.height() / pixmap.height()
            pixmap = pixmap.scaled(pixmap.width()*rate, pixmap.height()*rate)
        if pixmap.width() > self.width():
            rate = self.width() / pixmap.width()
            pixmap = pixmap.scaled(pixmap.width()*rate, pixmap.height()*rate)
        self.image_label.setPixmap(pixmap)

        self.image_rate = [
            pixmap.width() / self.image_pixmap.width(),
            pixmap.height() / self.image_pixmap.height()
        ]
        self.rate_label.setText("{}%".format(round(self.image_rate[0]*100)))


    # 文本框按钮自适配比例
    def matchButtonSize(self) :

        if not self.json_data or (len(self.button_list) != len(self.json_data["text_block"])) :
            return
        for button, text_block in zip(self.button_list, self.json_data["text_block"]) :
            # 计算文本坐标
            x = text_block["block_coordinate"]["upper_left"][0]
            y = text_block["block_coordinate"]["upper_left"][1]
            w = text_block["block_coordinate"]["lower_right"][0] - x
            h = text_block["block_coordinate"]["lower_right"][1] - y
            # 计算缩放比例
            x = x * self.image_rate[0]
            y = y * self.image_rate[1]
            w = w * self.image_rate[0]
            h = h * self.image_rate[1]
            button.setGeometry(x, y, w, h)


    # 鼠标滚轮信号
    def wheelEvent(self, event) :

        if event.angleDelta().y() > 0 :
            self.image_rate[0] += 0.1
            self.image_rate[1] += 0.1
        else :
            self.image_rate[0] -= 0.1
            self.image_rate[1] -= 0.1
        pixmap = self.image_pixmap.scaled(
            self.image_pixmap.width() * self.image_rate[0],
            self.image_pixmap.height() * self.image_rate[1]
        )
        self.image_label.setPixmap(pixmap)
        self.rate_label.setText("{}%".format(round(self.image_rate[0] * 100)))
        self.matchButtonSize()


    # 窗口尺寸变化信号
    def resizeEvent(self, event) :

        w = event.size().width()
        h = event.size().height()
        w_rate = w / 1000
        h_rete = h / 635
        self.scroll_area.setGeometry(0, 0, w, h)
        self.matchImageSize()
        self.matchButtonSize()
        self.rate_label.setGeometry(950*w_rate, 590*h_rete, 30*w_rate, 30*h_rete)


# 自定义按键实现鼠标进入显示, 移出隐藏
class CustomButton(QPushButton) :

    def __init__(self, text) :
        super().__init__(text)
        self.setStyleSheet("background: transparent;")

    def enterEvent(self, a0) :
        self.setStyleSheet("background-color:rgba(62, 62, 62, 0.3)")
        self.show()
        return super().enterEvent(a0)

    def leaveEvent(self, a0) :
        self.setStyleSheet("background: transparent;")
        return super().leaveEvent(a0)


# 漫画翻译界面
class Manga(QWidget) :

    def __init__(self, object) :

        super(Manga, self).__init__()
        self.object = object
        self.logger = object.logger
        self.getInitConfig()
        self.ui()
        self.trans_edit_ui = TransEdit(object)
        self.show_image_widget = None


    def ui(self) :

        # 窗口尺寸
        self.resize(self.window_width*self.rate, self.window_height*self.rate)
        # 窗口标题
        self.setWindowTitle("漫画翻译")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size, self.font_type))
        # 底部状态栏
        self.status_label = QLabel(self)

        # 导入原图按钮
        self.input_image_button = QPushButton(self)
        self.input_image_button.setText(" 导入原图")
        self.input_image_button.setStyleSheet("QPushButton {background: transparent;}"
                                              "QPushButton:hover {background-color: #83AAF9;}"
                                              "QPushButton:pressed {background-color: #4480F9;}")
        self.input_image_button.setIcon(ui.static.icon.OPEN_ICON)
        # 导入原图菜单
        self.input_menu = QMenu(self.input_image_button)
        self.input_action_group = QActionGroup(self.input_menu)
        self.input_action_group.setExclusive(True)
        self.createInputAction("从文件导入")
        self.createInputAction("从文件夹导入")
        # 将下拉菜单设置为按钮的菜单
        self.input_image_button.setMenu(self.input_menu)
        self.input_action_group.triggered.connect(self.openImageFiles)

        # 一键翻译按钮
        self.trans_all_button = QPushButton(self)
        self.trans_all_button.setText(" 一键翻译")
        self.trans_all_button.setStyleSheet("QPushButton {background: transparent;}"
                                            "QPushButton:hover {background-color: #83AAF9;}"
                                            "QPushButton:pressed {background-color: #4480F9;}")
        self.trans_all_button.setIcon(ui.static.icon.RUN_ICON)
        self.trans_all_button.clicked.connect(self.clickTransAllButton)

        # 选择翻译源按钮
        self.select_trans_button = QPushButton(self)
        self.select_trans_button.setText(" 选择翻译源")
        self.select_trans_button.setStyleSheet("QPushButton {background: transparent;}"
                                               "QPushButton:hover {background-color: #83AAF9;}"
                                               "QPushButton:pressed {background-color: #4480F9;}")
        self.select_trans_button.setIcon(ui.static.icon.TRANSLATE_ICON)
        # 翻译源菜单
        self.trans_menu = QMenu(self.select_trans_button)
        self.trans_action_group = QActionGroup(self.trans_menu)
        self.trans_action_group.setExclusive(True)
        self.createTransAction("私人彩云")
        self.createTransAction("私人腾讯")
        self.createTransAction("私人百度")
        self.createTransAction("私人ChatGPT")
        # 将下拉菜单设置为按钮的菜单
        self.select_trans_button.setMenu(self.trans_menu)
        self.trans_action_group.triggered.connect(self.changeSelectTrans)

        # 教程按钮
        self.tutorial_button = QPushButton(self)
        self.tutorial_button.setText(" 使用教程")
        self.tutorial_button.setStyleSheet("QPushButton {background: transparent;}"
                                           "QPushButton:hover {background-color: #83AAF9;}"
                                           "QPushButton:pressed {background-color: #4480F9;}")
        self.tutorial_button.setIcon(ui.static.icon.RUN_ICON)
        self.tutorial_button.clicked.connect(self.openUseTutorial)

        # 工具栏横向分割线
        self.cut_line_label1 = QLabel(self)
        self.createCutLine(self.cut_line_label1)

        # 原图按钮
        self.original_image_button = QPushButton(self)
        self.original_image_button.setText("原图")
        self.original_image_button.setStyleSheet("background-color: #83AAF9; border-right: 1px solid black;")
        self.original_image_button.clicked.connect(lambda: self.clickImageButton("original"))

        # 原图按钮 和 译图按钮 竖向分割线
        self.cut_line_label2 = QLabel(self)
        self.createCutLine(self.cut_line_label2)

        # 编辑按钮
        self.edit_image_button = QPushButton(self)
        self.edit_image_button.setText("编辑")
        self.edit_image_button.setStyleSheet("QPushButton {background: transparent;}"
                                             "QPushButton:hover {background-color: #83AAF9;}")
        self.edit_image_button.clicked.connect(lambda: self.clickImageButton("edit"))

        # 原图按钮 和 译图按钮 竖向分割线
        self.cut_line_label3 = QLabel(self)
        self.createCutLine(self.cut_line_label3)

        # 译图按钮
        self.trans_image_button = QPushButton(self)
        self.trans_image_button.setText("译图")
        self.trans_image_button.setStyleSheet("QPushButton {background: transparent;}"
                                              "QPushButton:hover {background-color: #83AAF9;}")
        self.trans_image_button.clicked.connect(lambda: self.clickImageButton("trans"))

        # 译图右侧竖向分割线
        self.cut_line_label4 = QLabel(self)
        self.createCutLine(self.cut_line_label4)

        # 原图列表框
        self.original_image_widget = QListWidget(self)
        self.original_image_widget.setIconSize(QSize(180*self.rate, 180*self.rate))
        self.original_image_widget.itemSelectionChanged.connect(self.loadOriginalImage)
        self.original_image_widget.show()
        self.original_image_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.original_image_widget.customContextMenuRequested.connect(self.showOriginalListWidgetMenu)
        self.original_image_widget.setSpacing(5)

        # 编辑图列表框
        self.edit_image_widget = QListWidget(self)
        self.edit_image_widget.setIconSize(QSize(180*self.rate, 180*self.rate))
        self.edit_image_widget.itemSelectionChanged.connect(self.loadEditImage)
        self.edit_image_widget.hide()
        self.edit_image_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.edit_image_widget.setSpacing(5)

        # 译图列表框
        self.trans_image_widget = QListWidget(self)
        self.trans_image_widget.setIconSize(QSize(180*self.rate, 180*self.rate))
        self.trans_image_widget.itemSelectionChanged.connect(self.loadTransImage)
        self.trans_image_widget.hide()
        self.trans_image_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.trans_image_widget.customContextMenuRequested.connect(self.showTransListWidgetMenu)
        self.trans_image_widget.setSpacing(5)

        # 图片大图展示
        self.show_image_scroll_area = QScrollArea(self)
        self.show_image_scroll_area.setWidgetResizable(True)
        self.show_image_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show_image_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 上一页按钮
        self.last_page_button = CustomButton(self)
        self.last_page_button.setIcon(ui.static.icon.LAST_PAGE_ICON)
        self.last_page_button.clicked.connect(lambda: self.changeImageListPosition("last"))

        # 下一页按钮
        self.next_page_button = CustomButton(self)
        self.next_page_button.setIcon(ui.static.icon.NEXT_PAGE_ICON)
        self.next_page_button.clicked.connect(lambda: self.changeImageListPosition("next"))

        # 导入图片进度条
        self.input_images_progress_bar = ui.progress_bar.ProgressBar(self.object.yaml["screen_scale_rate"], "input_images")
        # 漫画翻译进度条
        self.trans_process_bar = ui.progress_bar.MangaProgressBar(self.object.yaml["screen_scale_rate"])


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面字体
        self.font_type = "华康方圆体W7"
        # 字体颜色
        self.color = "#595959"
        # 界面字体大小
        self.font_size = 6
        # 界面尺寸
        self.window_width = 1200
        self.window_height = 700
        # 图片路径列表
        self.image_path_list = []
        # 当前图片列表框的索引
        self.image_widget_index = 0
        # 当前图片列表框的滑块坐标
        self.image_widget_scroll_bar_value = 0
        # 渲染文本块的组件列表
        self.render_text_block_label = []


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h, w_rate=1, h_rate=1):

        object.setGeometry(QRect(
            int(x * w_rate),
            int(y * w_rate),
            int(w * h_rate),
            int(h * h_rate))
        )


    # 绘制一条分割线
    def createCutLine(self, label) :

        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")


    # 上一页下一页按钮信号槽
    def changeImageListPosition(self, sign) :

        if len(self.image_path_list) == 0 :
            return

        image_widget = self.original_image_widget
        if self.edit_image_widget.isVisible() :
            image_widget = self.edit_image_widget
        elif self.trans_image_widget.isVisible() :
            image_widget = self.trans_image_widget

        row = image_widget.currentRow()
        if sign == "next" :
            if row < len(self.image_path_list) - 1 :
                image_widget.setCurrentRow(row + 1)
        else :
            if row > 0 :
                image_widget.setCurrentRow(row -1)


    # 打开图片文件列表
    def openImageFiles(self, action):

        dir_path = self.object.yaml.get("manga_dir_path", os.getcwd())
        options = QFileDialog.Options()
        images = []
        if action.data() == "从文件导入":
            images, _ = QFileDialog.getOpenFileNames(self,
                                                     "选择要翻译的生肉漫画原图（可多选）",
                                                     dir_path,
                                                     "图片类型(*.png *.jpg *.jpeg);;所有类型 (*)",
                                                     options=options)
            if not images :
                return

        elif action.data() == "从文件夹导入" :
            folder_path = QFileDialog.getExistingDirectory(self,
                                                           "选择要翻译的生肉漫画目录",
                                                           dir_path,
                                                           options=options)
            if not os.path.exists(folder_path) :
                return
            for file in os.listdir(folder_path) :
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext != ".png" and file_ext != ".jpg" and file_ext != ".jpeg" :
                    continue
                images.append(os.path.join(folder_path, file))
        else :
            return

        if images :
            # 清除所有图片
            self.clearAllImages()
            # 根据文件名排序
            images = self.dirFilesPathSort(images)
            # 进度条窗口
            self.input_images_progress_bar.modifyTitle("导入图片 -- 加载中请勿关闭此窗口")
            self.input_images_progress_bar.show()
            # 导入图片线程
            thread = utils.thread.createInputImagesQThread(self, images)
            thread.bar_signal.connect(self.input_images_progress_bar.paintProgressBar)
            thread.image_widget_signal.connect(self.inputImage)
            utils.thread.runQThread(thread)

        # 记忆上次操作的目录
        for image_path in images:
            self.object.yaml["manga_dir_path"] = os.path.dirname(image_path)
            break


    # 导入图片
    def inputImage(self, image_path, finish_sign) :

        if not finish_sign :
            # 图片添加至原图列表框
            self.originalImageWidgetAddImage(image_path)
            # 图片添加至编辑图列表框
            self.editImageWidgetAddImage()
            if os.path.exists(self.getRdrFilePath(image_path)) :
                self.editImageWidgetRefreshImage(image_path)
            # 图片添加至译图列表框
            self.transImageWidgetAddImage()
            if os.path.exists(self.getRdrFilePath(image_path)) :
                self.transImageWidgetRefreshImage(image_path)

        else :
            # 跳转到原图栏
            self.original_image_button.click()
            self.original_image_widget.setCurrentRow(0)
            self.loadOriginalImage()
            self.input_images_progress_bar.close()


    # 文件列表排序
    def dirFilesPathSort(self, files) :

        tmp_dict = {}
        for file_path in files :
            if len(file_path) not in tmp_dict :
                tmp_dict[len(file_path)] = []
            tmp_dict[len(file_path)].append(file_path)

        new_files = []
        for k in sorted(tmp_dict.keys()) :
            for val in sorted(tmp_dict[k]) :
                new_files.append(val)

        return new_files


    # 清除所有图片
    def clearAllImages(self) :

        self.original_image_widget.clear()
        self.edit_image_widget.clear()
        self.trans_image_widget.clear()
        self.image_path_list.clear()


    # 点击 原图/编辑/译图 按钮
    def clickImageButton(self, button_type):

        self.original_image_widget.hide()
        self.edit_image_widget.hide()
        self.trans_image_widget.hide()
        self.original_image_button.setStyleSheet("QPushButton {background: transparent;}"
                                                 "QPushButton:hover {background-color: #83AAF9;}")
        self.edit_image_button.setStyleSheet("QPushButton {background: transparent;}"
                                             "QPushButton:hover {background-color: #83AAF9;}")
        self.trans_image_button.setStyleSheet("QPushButton {background: transparent;}"
                                              "QPushButton:hover {background-color: #83AAF9;}")
        if button_type == "original":
            self.original_image_widget.show()
            self.original_image_button.setStyleSheet("background-color: #83AAF9;")
            self.original_image_widget.verticalScrollBar().setValue(self.image_widget_scroll_bar_value)
            self.original_image_widget.setCurrentRow(self.image_widget_index)
            self.loadOriginalImage()

        elif button_type == "edit":
            self.edit_image_widget.show()
            self.edit_image_button.setStyleSheet("background-color: #83AAF9;")
            self.edit_image_widget.verticalScrollBar().setValue(self.image_widget_scroll_bar_value)
            self.edit_image_widget.setCurrentRow(self.image_widget_index)
            self.loadEditImage()

        elif button_type == "trans":
            self.trans_image_widget.show()
            self.trans_image_button.setStyleSheet("background-color: #83AAF9;")
            self.trans_image_widget.verticalScrollBar().setValue(self.image_widget_scroll_bar_value)
            self.trans_image_widget.setCurrentRow(self.image_widget_index)
            self.loadTransImage()


    # 创建导入原图按钮的下拉菜单
    def createInputAction(self, label):

        action = QAction(label, self.input_menu)
        action.setCheckable(True)
        action.setData(label)
        self.input_action_group.addAction(action)
        self.input_menu.addAction(action)


    # 创建翻译源按钮的下拉菜单
    def createTransAction(self, label) :

        action = QAction(label, self.trans_menu)
        action.setCheckable(True)
        action.setData(label)
        self.trans_action_group.addAction(action)
        self.trans_menu.addAction(action)
        if self.object.config["mangaTrans"] == label :
            action.setChecked(True)
            self.status_label.setText("正在使用: {}".format(label))


    # 改变所使用的翻译源
    def changeSelectTrans(self, action) :

        self.object.config["mangaTrans"] = action.data()
        self.status_label.setText("正在使用: {}".format(action.data()))


    # 设置原图列表框右键菜单
    def showOriginalListWidgetMenu(self, pos) :

        item = self.original_image_widget.itemAt(pos)
        if item is not None:
            menu = QMenu(self)
            # 添加菜单项
            translater_action = menu.addAction("翻译")
            translater_action.triggered.connect(lambda: self.translaterItemWidget(item))
            delete_action = menu.addAction("移除")
            delete_action.triggered.connect(lambda: self.removeItemWidget(item))
            # 显示菜单
            cursorPos = QCursor.pos()
            menu.exec_(cursorPos)


    # 设置译图列表框右键菜单
    def showTransListWidgetMenu(self, pos):

        item = self.trans_image_widget.itemAt(pos)
        if item is not None:
            menu = QMenu(self)
            # 添加菜单项
            output_action = menu.addAction("另存为")
            output_action.triggered.connect(lambda: self.saveImageItemWidget(item))
            # 显示菜单
            cursorPos = QCursor.pos()
            menu.exec_(cursorPos)


    # 译图框保存图片
    def saveImageItemWidget(self, item) :

        row = self.trans_image_widget.indexFromItem(item).row()
        image_path = self.image_path_list[row]

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self,
                                                   "译图另存为",
                                                   image_path,
                                                   "图片类型(*.png *.jpg *.jpeg);;所有类型 (*)",
                                                   options=options)
        if file_path :
            shutil.copy(self.getRdrFilePath(image_path), file_path)


    # 列表框右键菜单删除子项
    def removeItemWidget(self, item) :

        row = self.original_image_widget.indexFromItem(item).row()
        if row > (len(self.image_path_list) - 1) :
            return
        # 列表框删除图片
        self.original_image_widget.takeItem(row)
        self.edit_image_widget.takeItem(row)
        self.trans_image_widget.takeItem(row)
        self.image_path_list.pop(row)


    # 原图列表框添加图片
    def originalImageWidgetAddImage(self, image_path):

        item = QListWidgetItem(self.original_image_widget)
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(180*self.rate, 180*self.rate, aspectRatioMode=Qt.KeepAspectRatio)
        item.setIcon(QIcon(pixmap))
        self.original_image_widget.addItem(item)
        self.image_path_list.append(image_path)


    # 编辑图列表框添加图片
    def editImageWidgetAddImage(self) :

        item = QListWidgetItem(self.edit_image_widget)
        item.setSizeHint(QSize(0, 180*self.rate))
        self.edit_image_widget.addItem(item)


    # 译图列表框添加图片
    def transImageWidgetAddImage(self) :

        item = QListWidgetItem(self.trans_image_widget)
        item.setSizeHint(QSize(0, 180*self.rate))
        self.trans_image_widget.addItem(item)


    # 刷新编辑图列表框内item的图片
    def editImageWidgetRefreshImage(self, image_path) :

        if image_path not in self.image_path_list :
            return
        row = self.image_path_list.index(image_path)
        item = self.edit_image_widget.item(row)
        rdr_image_path = self.getRdrFilePath(image_path)
        pixmap = QPixmap(rdr_image_path)
        pixmap = pixmap.scaled(180*self.rate, 180*self.rate, aspectRatioMode=Qt.KeepAspectRatio)
        item.setIcon(QIcon(pixmap))


    # 刷新译图列表框内item的图片
    def transImageWidgetRefreshImage(self, image_path):

        if image_path not in self.image_path_list :
            return
        row = self.image_path_list.index(image_path)
        item = self.trans_image_widget.item(row)
        rdr_image_path = self.getRdrFilePath(image_path)
        pixmap = QPixmap(rdr_image_path)
        pixmap = pixmap.scaled(180*self.rate, 180*self.rate, aspectRatioMode=Qt.KeepAspectRatio)
        item.setIcon(QIcon(pixmap))


    # 展示原图图片大图
    def loadOriginalImage(self) :

        index = self.original_image_widget.currentRow()
        if index >= 0 and index < len(self.image_path_list) :
            image_path = self.image_path_list[index]
            self.renderImageAndTextBlock(image_path, "original")
            self.image_widget_index = index
            self.image_widget_scroll_bar_value = self.original_image_widget.verticalScrollBar().value()


    # 展示编辑图图片大图
    def loadEditImage(self) :

        index = self.edit_image_widget.currentRow()
        if index >= 0 and index < len(self.image_path_list):
            image_path = self.image_path_list[index]
            rdr_image_path = self.getRdrFilePath(image_path)
            if os.path.exists(rdr_image_path) :
                self.renderImageAndTextBlock(image_path, "edit")
            else :
                self.show_image_scroll_area.hide()
            self.image_widget_index = index
            self.image_widget_scroll_bar_value = self.edit_image_widget.verticalScrollBar().value()


    # 展示译图图片大图
    def loadTransImage(self):

        index = self.trans_image_widget.currentRow()
        if index >= 0 and index < len(self.image_path_list) :
            image_path = self.image_path_list[index]
            rdr_image_path = self.getRdrFilePath(image_path)
            if os.path.exists(rdr_image_path) :
                self.renderImageAndTextBlock(image_path, "trans")
            else :
                self.show_image_scroll_area.hide()
            self.image_widget_index = index
            self.image_widget_scroll_bar_value = self.trans_image_widget.verticalScrollBar().value()


    # 翻译进程
    def transProcess(self, image_path, reload_sign=False) :

        # 漫画OCR
        start = time.time()
        if not os.path.exists(self.getJsonFilePath(image_path)) or reload_sign :
            sign, ocr_result = self.mangaOCR(image_path)
            if not sign :
                return "OCR过程失败: %s"%ocr_result
            else :
                # 没有文字的图
                if len(ocr_result.get("text_block", [])) == 0 :
                    shutil.copy(image_path, self.getIptFilePath(image_path))
                    shutil.copy(image_path, self.getRdrFilePath(image_path))
                    # 直接将原图加入编辑图列表框
                    self.editImageWidgetRefreshImage(image_path)
                    # 直接将原图加入译图列表框
                    self.transImageWidgetRefreshImage(image_path)
                    return
        self.trans_process_bar.paintStatus("ocr", round(time.time()-start, 1))

        # 翻译
        start = time.time()
        trans_sign = False
        if not os.path.exists(self.getJsonFilePath(image_path)) or reload_sign :
            trans_sign = True
        else:
            with open(self.getJsonFilePath(image_path), "r", encoding="utf-8") as file:
                json_data = json.load(file)
            if "translated_text" not in json_data:
                trans_sign = True
        if trans_sign :
            sign, trans_result = self.mangaTrans(image_path)
            if not sign:
                return "翻译过程失败: %s"%trans_result
        self.trans_process_bar.paintStatus("trans", round(time.time()-start, 1))

        # 文字消除
        start = time.time()
        if not os.path.exists(self.getIptFilePath(image_path)) or reload_sign :
            sign, ipt_result = self.mangaTextInpaint(image_path)
            if not sign :
                return "文字消除过程失败: %s"%ipt_result
        self.trans_process_bar.paintStatus("ipt", round(time.time()-start, 1))

        # 漫画文字渲染
        start = time.time()
        if not os.path.exists(self.getRdrFilePath(image_path)) or reload_sign :
            sign, rdr_result = self.mangaTextRdr(image_path)
            if not sign:
                return "文字渲染过程失败: %s"%rdr_result
            # 渲染好的图片加入编辑图列表框
            self.editImageWidgetRefreshImage(image_path)
            # 渲染好的图片加入译图列表框
            self.transImageWidgetRefreshImage(image_path)
        self.trans_process_bar.paintStatus("rdr", round(time.time()-start, 1))


    # 单图翻译
    def translaterItemWidget(self, item) :

        # 校验是否选择了翻译源
        if not self.object.config["mangaTrans"] :
            return utils.message.MessageBox("翻译失败", "请先选择要使用的翻译源     ", self.rate)
        # 获取图片路径
        row = self.original_image_widget.indexFromItem(item).row()
        image_path = self.image_path_list[row]
        image_paths = []
        image_paths.append(image_path)
        # 进度条窗口
        self.trans_process_bar.modifyTitle("漫画翻译 -- 执行中请勿关闭此窗口")
        self.trans_process_bar.show()
        # 创建执行线程
        self.trans_all_button.setEnabled(False)
        reload_sign = True
        thread = utils.thread.createMangaTransQThread(self, image_paths, reload_sign)
        thread.signal.connect(self.finishTransProcessRefresh)
        thread.bar_signal.connect(self.trans_process_bar.paintProgressBar)
        utils.thread.runQThread(thread)


    # 漫画OCR
    def mangaOCR(self, image_path) :

        sign, result = translator.ocr.dango.mangaOCR(self.object, image_path)
        if sign :
            # 缓存mask图片
            with open(self.getMaskFilePath(image_path), "wb") as file :
                file.write(base64.b64decode(result["mask"]))
            del result["mask"]
            # 缓存ocr结果
            with open(self.getJsonFilePath(image_path), "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4)

        return sign, result


    # 漫画文字消除
    def mangaTextInpaint(self, image_path) :

        # 从缓存文件里获取mask图片
        with open(self.getMaskFilePath(image_path), "rb") as file:
            mask = base64.b64encode(file.read()).decode("utf-8")
        # 请求漫画ipt
        sign, result = translator.ocr.dango.mangaIPT(self.object, image_path, mask)
        if sign :
            # 缓存inpaint图片
            with open(self.getIptFilePath(image_path), "wb") as file :
                file.write(base64.b64decode(result["inpainted_image"]))

        return sign, result


    # 漫画翻译
    def mangaTrans(self, image_path) :

        # 从缓存文件中获取json结果
        with open(self.getJsonFilePath(image_path), "r", encoding="utf-8") as file:
            json_data = json.load(file)
        # 翻译源
        manga_trans = self.object.config["mangaTrans"]
        # 存译文列表
        translated_text = []
        # 解析ocr结果获取原文
        original = []
        for val in json_data["text_block"] :
            tmp = ""
            for text in val["texts"]:
                tmp += text
            original.append(tmp)
        original = "\n".join(original)

        # 调用翻译
        result = ""
        if manga_trans == "私人彩云" :
            result = translator.api.caiyun(sentence=original,
                                           token=self.object.config["caiyunAPI"],
                                           logger=self.logger)
        elif manga_trans == "私人腾讯" :
            result = translator.api.tencent(sentence=original,
                                            secret_id=self.object.config["tencentAPI"]["Key"],
                                            secret_key=self.object.config["tencentAPI"]["Secret"],
                                            logger=self.logger)
        elif manga_trans == "私人百度" :
            result = translator.api.baidu(sentence=original,
                                          app_id=self.object.config["baiduAPI"]["Key"],
                                          secret_key=self.object.config["baiduAPI"]["Secret"],
                                          logger=self.logger)
        elif manga_trans == "私人ChatGPT" :
            result = translator.api.chatgpt(api_key=self.object.config["chatgptAPI"],
                                            language=self.object.config["language"],
                                            proxy=self.object.config["chatgptProxy"],
                                            content=original,
                                            logger=self.logger)

        for index, word in enumerate(result.split("\n")[:len(json_data["text_block"])]) :
            translated_text.append(word)

        json_data["translated_text"] = translated_text
        # 缓存ocr结果
        with open(self.getJsonFilePath(image_path), "w", encoding="utf-8") as file :
            json.dump(json_data, file, indent=4)

        # @TODO 缺少错误处理
        return True, result


    # 漫画文字渲染
    def mangaTextRdr(self, image_path):

        # 从缓存文件中获取json结果
        with open(self.getJsonFilePath(image_path), "r", encoding="utf-8") as file :
            json_data = json.load(file)
        # 从缓存文件里获取ipt图片
        with open(self.getIptFilePath(image_path), "rb") as file :
            ipt = base64.b64encode(file.read()).decode("utf-8")
        # 漫画rdr
        sign, result = translator.ocr.dango.mangaRDR(
            object=self.object,
            trans_list=json_data["translated_text"],
            inpainted_image=ipt,
            text_block=json_data["text_block"]
        )
        if sign :
            # 缓存ipt图片
            with open(self.getRdrFilePath(image_path), "wb") as file :
                file.write(base64.b64decode(result["rendered_image"]))

        return sign, result


    # 获取工作目录
    def getDangoMangaPath(self, image_path) :

        # 获取漫画翻译缓存目录
        base_path = os.path.dirname(image_path)
        dango_manga_path = os.path.join(base_path, "dango_manga")
        # 如果目录不存在就创建工作缓存目录
        if not os.path.exists(dango_manga_path) :
            os.mkdir(dango_manga_path)
        # 如果目录不存在就创建工作缓存目录
        tmp_path = os.path.join(dango_manga_path, "tmp")
        if not os.path.exists(tmp_path) :
            os.mkdir(tmp_path)
        # 获取不带拓展名的文件名
        file_name = os.path.splitext(os.path.basename(image_path))[0]

        return dango_manga_path, file_name


    # 获取某张图对应的Json结果文件缓存路径
    def getJsonFilePath(self, image_path) :

        dango_manga_path, file_name = self.getDangoMangaPath(image_path)
        tmp_path = os.path.join(dango_manga_path, "tmp")
        file_path = os.path.join(tmp_path, "{}.json".format(file_name))

        return file_path


    # 获取某张图对应的mask结果文件缓存路径
    def getMaskFilePath(self, image_path) :

        dango_manga_path, file_name = self.getDangoMangaPath(image_path)
        tmp_path = os.path.join(dango_manga_path, "tmp")
        file_path = os.path.join(tmp_path, "{}_mask.png".format(file_name))

        return file_path


    # 获取某张图对应的文字消除结果文件缓存路径
    def getIptFilePath(self, image_path) :

        dango_manga_path, file_name = self.getDangoMangaPath(image_path)
        tmp_path = os.path.join(dango_manga_path, "tmp")
        file_path = os.path.join(tmp_path, "{}_ipt.png".format(file_name))

        return file_path


    # 获取某张图对应的文字渲染结果文件缓存路径
    def getRdrFilePath(self, image_path) :

        dango_manga_path, file_name = self.getDangoMangaPath(image_path)
        file_path = os.path.join(dango_manga_path, "{}.png".format(file_name))

        return file_path


    # 渲染图片和文本块
    def renderImageAndTextBlock(self, image_path, show_type) :

        if show_type == "original" :
            json_data = None
        elif show_type == "edit" :
            with open(self.getJsonFilePath(image_path), "r", encoding="utf-8") as file:
                json_data = json.load(file)
            image_path = self.getRdrFilePath(image_path)
        elif show_type == "trans" :
            image_path = self.getRdrFilePath(image_path)
            json_data = None
        else :
            return

        w_rate = self.width() / self.window_width
        h_rate = self.height() / self.window_height
        self.show_image_scroll_area.setWidget(None)
        self.show_image_widget = RenderTextBlock(
            rate=(w_rate, h_rate),
            image_path=image_path,
            json_data=json_data,
            edit_window=self.trans_edit_ui
        )
        self.show_image_scroll_area.setWidget(self.show_image_widget)
        self.show_image_scroll_area.show()


    # 翻译完成后刷新译图栏
    def finishTransProcessRefresh(self, value, signal) :

        if signal :
            self.trans_image_button.click()
            row = self.image_path_list.index(value)
            self.trans_image_widget.setCurrentRow(row)
            self.loadTransImage()
        else :
            if value :
                # @TODO 缺少错误处理
                pass
            self.trans_process_bar.close()
            self.trans_all_button.setEnabled(True)


    # 一键翻译
    def clickTransAllButton(self) :

        self.trans_all_button.setEnabled(False)
        # 进度条窗口
        self.trans_process_bar.modifyTitle("漫画翻译 -- 执行中请勿关闭此窗口")
        self.trans_process_bar.show()
        # 创建执行线程
        thread = utils.thread.createMangaTransQThread(self, self.image_path_list)
        thread.signal.connect(self.finishTransProcessRefresh)
        thread.bar_signal.connect(self.trans_process_bar.paintProgressBar)
        utils.thread.runQThread(thread)


    # 打开使用教程
    def openUseTutorial(self) :

        url = self.object.yaml["dict_info"]["manga_tutorial"]
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())
            utils.message.MessageBox("漫画翻译教程",
                                     "打开失败, 请尝试手动打开此地址\n%s     "%url)


    # 窗口尺寸变化信号
    def resizeEvent(self, event) :

        w = event.size().width()
        h = event.size().height()
        w_rate = w / self.window_width
        h_rate = h / self.window_height

        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size * w_rate, self.font_type))
        # 导入原图按钮
        self.customSetGeometry(self.input_image_button, 0, 0, 120, 35, w_rate, h_rate)
        # 底部状态栏
        self.status_label.setGeometry(
            10 * w_rate, h- 30 * h_rate,
            w, 30 * h_rate
        )
        # 一键翻译按钮
        self.trans_all_button.setGeometry(
            self.input_image_button.width(), 0,
            self.input_image_button.width(), self.input_image_button.height()
        )
        # 选择翻译源按钮
        self.select_trans_button.setGeometry(
            self.trans_all_button.x() + self.input_image_button.width(), 0,
            self.input_image_button.width(), self.input_image_button.height()
        )
        # 教程按钮
        self.tutorial_button.setGeometry(
            w-self.input_image_button.width(), 0,
            self.input_image_button.width(), self.input_image_button.height()
        )
        # 工具栏横向分割线
        self.cut_line_label1.setGeometry(
            0, self.input_image_button.height(),
            w, 1
        )
        # 图片列表框原图按钮
        self.original_image_button.setGeometry(
            0, self.input_image_button.height(),
            66 * w_rate, 25 * h_rate
        )
        # 原图按钮 和 编辑按钮 竖向分割线
        self.cut_line_label2.setGeometry(
            self.original_image_button.width() + 1, self.input_image_button.height(),
            1, self.original_image_button.height()
        )
        # 图片列表框编辑按钮
        self.edit_image_button.setGeometry(
            self.cut_line_label2.x(), self.input_image_button.height(),
            self.original_image_button.width(), self.original_image_button.height()
        )
        # 编辑按钮 和 译图按钮 竖向分割线
        self.cut_line_label3.setGeometry(
            self.edit_image_button.x() + self.edit_image_button.width() + 1, self.input_image_button.height(),
            1, self.original_image_button.height()
        )
        # 图片列表框译图按钮
        self.trans_image_button.setGeometry(
            self.cut_line_label3.x(), self.input_image_button.height(),
            self.original_image_button.width(), self.original_image_button.height()
        )
        # 译图右侧竖向分割线
        self.cut_line_label4.setGeometry(
            self.trans_image_button.x() + self.trans_image_button.width(), self.input_image_button.height(),
            1, self.original_image_button.height()
        )
        # 原图列表框
        self.original_image_widget.setGeometry(
            0, self.input_image_button.height() + self.original_image_button.height(),
            self.cut_line_label4.x(), self.status_label.y() - (self.input_image_button.height() + self.original_image_button.height())
        )
        # 编辑列表框
        self.edit_image_widget.setGeometry(
            0, self.input_image_button.height() + self.original_image_button.height(),
            self.cut_line_label4.x(), self.original_image_widget.height()
        )
        # 译图列表框
        self.trans_image_widget.setGeometry(
            0, self.input_image_button.height() + self.original_image_button.height(),
            self.cut_line_label4.x(), self.original_image_widget.height()
        )
        # 图片大图展示
        self.show_image_scroll_area.setGeometry(
            self.cut_line_label4.x(), self.input_image_button.height(),
            w-self.cut_line_label4.x(), self.status_label.y() - self.input_image_button.height()
        )
        # 上一页按钮
        self.last_page_button.setGeometry(
            self.cut_line_label4.x()+20*w_rate, (self.show_image_scroll_area.height() - 300 * h_rate) // 2,
            50 * w_rate, 300 * h_rate
        )
        # 下一页按钮
        self.next_page_button.setGeometry(
            w-self.last_page_button.width()-20*w_rate, self.last_page_button.y(),
            self.last_page_button.width(), self.last_page_button.height()
        )
        # 图片大图展示
        if self.show_image_widget :
            self.show_image_widget.resize(self.show_image_scroll_area.width(), self.show_image_scroll_area.height())


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.hide()
        self.object.translation_ui.show()
        if self.object.range_ui.show_sign == True:
            self.object.range_ui.show()