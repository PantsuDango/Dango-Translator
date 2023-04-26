# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import base64
import shutil
import json

import ui.static.icon
import utils.translater
import translator.ocr.dango
import translator.api
import utils.thread
import utils.message


# 范围框
class RenderTextBlock(QWidget) :

    def __init__(self, rect, json_data):

        super(RenderTextBlock, self).__init__()
        self.font_type = "华康方圆体W7"
        self.font_size = 12
        self.rect = rect
        self.json_data = json_data
        self.ui()


    def ui(self) :

        # 窗口大小
        w, h = self.rect[0], self.rect[1]
        self.resize(w, h)
        # 窗口无标题栏、窗口置顶、窗口透明
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)

        # 字体
        self.font = QFont()
        self.font.setFamily(self.font_type)
        self.font.setPointSize(self.font_size)

        for text_block, trans_text in zip(self.json_data["text_block"], self.json_data["translated_text"]) :
            text_edit = QTextBrowser(self)
            # 禁用滚轮
            text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # 文本框样式
            text_edit.setFontPointSize(text_block["font_size"] * 0.5)
            option = QTextOption()
            option.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
            text_edit.document().setDefaultTextOption(option)

            text_edit.setStyleSheet("background: transparent;"
                                    "white-space: pre-wrap;")
            text_edit.setReadOnly(False)
            # 文本颜色
            line = len(text_block["lines"])
            text_edit.setTextColor(QColor(
                text_block["fg_r"] // line,
                text_block["fg_g"] // line,
                text_block["fg_b"] // line
            ))
            # 实现竖向排列文字
            text_edit.setText("\n".join(trans_text))

            # 计算文本坐标
            text_edit.setGeometry(
                text_block["xyxy"][0],
                text_block["xyxy"][1],
                text_block["xyxy"][2] - text_block["xyxy"][0],
                text_block["xyxy"][3] - text_block["xyxy"][1]
            )


# 漫画翻译界面
class Manga(QWidget) :

    def __init__(self, object) :

        super(Manga, self).__init__()

        self.object = object
        self.logger = object.logger
        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("漫画翻译")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size, self.font_type))

        self.status_label = QLabel(self)
        self.customSetGeometry(self.status_label, 10, 670, 1200, 20)

        # 导入原图
        button = QPushButton(self)
        self.customSetGeometry(button, 0, 0, 120, 35)
        button.setText(" 导入原图")
        button.setStyleSheet("QPushButton {background: transparent;}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.setIcon(ui.static.icon.OPEN_ICON)
        button.clicked.connect(self.openImageFiles)

        # 选择翻译源
        button = QPushButton(self)
        self.customSetGeometry(button, 120, 0, 120, 35)
        button.setText(" 选择翻译源")
        button.setStyleSheet("QPushButton {background: transparent;}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        # 翻译源菜单
        self.trans_menu = QMenu(button)
        self.trans_action_group = QActionGroup(self.trans_menu)
        self.trans_action_group.setExclusive(True)
        self.createTransAction("私人彩云")
        self.createTransAction("私人腾讯")
        self.createTransAction("私人百度")
        self.createTransAction("私人ChatGPT")

        # 将下拉菜单设置为按钮的菜单
        button.setMenu(self.trans_menu)
        self.trans_action_group.triggered.connect(self.changeSelectTrans)

        # 工具栏横向分割线
        self.createCutLine(0, 35, self.window_width, 1)

        # 原图按钮
        self.original_image_button = QPushButton(self)
        self.customSetGeometry(self.original_image_button, 0, 35, 66, 25)
        self.original_image_button.setText("原图")
        self.original_image_button.setStyleSheet("background-color: #83AAF9;")
        self.original_image_button.clicked.connect(lambda: self.clickImageButton("original"))

        # 原图按钮 和 译图按钮 竖向分割线
        self.createCutLine(67, 35, 1, 25)

        # 编辑按钮
        self.edit_image_button = QPushButton(self)
        self.customSetGeometry(self.edit_image_button, 67, 35, 66, 25)
        self.edit_image_button.setText("编辑")
        self.edit_image_button.setStyleSheet("QPushButton {background: transparent;}"
                                             "QPushButton:hover {background-color: #83AAF9;}")
        self.edit_image_button.clicked.connect(lambda: self.clickImageButton("edit"))

        # 原图按钮 和 译图按钮 竖向分割线
        self.createCutLine(134, 35, 1, 25)

        # 译图按钮
        self.trans_image_button = QPushButton(self)
        self.customSetGeometry(self.trans_image_button, 134, 35, 66, 25)
        self.trans_image_button.setText("译图")
        self.trans_image_button.setStyleSheet("QPushButton {background: transparent;}"
                                              "QPushButton:hover {background-color: #83AAF9;}")
        self.trans_image_button.clicked.connect(lambda: self.clickImageButton("trans"))

        # 译图右侧竖向分割线
        self.createCutLine(200, 35, 1, 25)

        # 原图列表框
        self.original_image_widget = QListWidget(self)
        self.customSetGeometry(self.original_image_widget, 0, 60, 200, 610)
        self.original_image_widget.setIconSize(QSize(180*self.rate, 180*self.rate))
        self.original_image_widget.itemSelectionChanged.connect(self.loadOriginalImage)
        self.original_image_widget.show()
        self.original_image_widget.show()
        self.original_image_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.original_image_widget.customContextMenuRequested.connect(self.showOriginalListWidgetMenu)

        # 编辑图列表框
        self.edit_image_widget = QListWidget(self)
        self.customSetGeometry(self.edit_image_widget, 0, 60, 200, 610)
        self.edit_image_widget.setIconSize(QSize(180*self.rate, 180*self.rate))
        self.edit_image_widget.itemSelectionChanged.connect(self.loadEditImage)
        self.edit_image_widget.hide()
        self.edit_image_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.edit_image_widget.customContextMenuRequested.connect(self.showEditListWidgetMenu)

        # 译图列表框
        self.trans_image_widget = QListWidget(self)
        self.customSetGeometry(self.trans_image_widget, 0, 60, 200, 610)
        self.trans_image_widget.setIconSize(QSize(180*self.rate, 180*self.rate))
        self.trans_image_widget.itemSelectionChanged.connect(self.loadTransImage)
        self.trans_image_widget.hide()
        self.trans_image_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.trans_image_widget.customContextMenuRequested.connect(self.showTransListWidgetMenu)

        # 图片大图展示
        self.show_image_scroll_area = QScrollArea(self)
        self.customSetGeometry(self.show_image_scroll_area, 200, 35, 1000, 635)
        self.show_image_scroll_area.setWidgetResizable(True)
        self.show_image_label = QLabel(self)
        self.show_image_scroll_area.setWidget(self.show_image_label)

        self.show_image_layout = QHBoxLayout()
        self.show_image_label.setLayout(self.show_image_layout)

        # 底部横向分割线
        self.createCutLine(200, 670, self.window_width, 1)


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
        # 图片路径列表
        self.image_path_list = []
        # 当前图片列表框的索引
        self.image_widget_index = 0
        # 当前图片列表框的滑块坐标
        self.image_widget_scroll_bar_value = 0


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 绘制一条分割线
    def createCutLine(self, x, y, w, h) :

        label = QLabel(self)
        self.customSetGeometry(label, x, y, w, h)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")


    # 打开图片文件列表
    def openImageFiles(self):

        # 文件选择器
        dir_path = self.object.yaml.get("manga_dir_path", os.getcwd())
        options = QFileDialog.Options()
        images, _ = QFileDialog.getOpenFileNames(self,
                                                 "选择要翻译的生肉漫画原图（可多选）",
                                                 dir_path,
                                                 "图片类型(*.png *.jpg *.jpeg);;所有类型 (*)",
                                                 options=options)
        # 遍历文件列表, 将每个文件路径添加到列表框中
        for image_path in images:
            if image_path in self.image_path_list:
                continue
            # 图片添加至列表框
            self.originalImageWidgetAddImage(image_path)
            self.editImageWidgetAddImage(image_path)
            if os.path.exists(self.getIptFilePath(image_path)) :
                self.editImageWidgetRefreshImage(image_path)
            self.transImageWidgetAddImage(image_path)
            if os.path.exists(self.getRdrFilePath(image_path)) :
                self.transImageWidgetRefreshImage(image_path)

        # 记忆上次操作的目录
        for image_path in images:
            self.object.yaml["manga_dir_path"] = os.path.dirname(image_path)
            break


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


    # 设置编辑图列表框右键菜单
    def showEditListWidgetMenu(self, pos):

        item = self.edit_image_widget.itemAt(pos)
        if item is not None:
            menu = QMenu(self)
            # 添加菜单项
            rdr_action = menu.addAction("重新渲染翻译结果")
            # rdr_action.triggered.connect(lambda: self.saveImageItemWidget(item))
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


    # 原图列表框添加图片
    def originalImageWidgetAddImage(self, image_path):

        item = QListWidgetItem(image_path, self.original_image_widget)
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(180*self.rate, 180*self.rate, aspectRatioMode=Qt.KeepAspectRatio)
        item.setIcon(QIcon(pixmap))
        item.setText(os.path.basename(image_path))
        self.original_image_widget.addItem(item)
        self.image_path_list.append(image_path)


    # 编辑图列表框添加图片
    def editImageWidgetAddImage(self, image_path) :

        item = QListWidgetItem("翻译后生成", self.edit_image_widget)
        item.setSizeHint(QSize(0, 100*self.rate))
        self.edit_image_widget.addItem(item)


    # 译图列表框添加图片
    def transImageWidgetAddImage(self, image_path) :

        item = QListWidgetItem("翻译后生成", self.trans_image_widget)
        item.setSizeHint(QSize(0, 100*self.rate))
        self.trans_image_widget.addItem(item)


    # 刷新编辑图列表框内item的图片
    def editImageWidgetRefreshImage(self, image_path) :

        row = self.image_path_list.index(image_path)
        item = self.edit_image_widget.item(row)
        ipt_image_path = self.getIptFilePath(image_path)
        pixmap = QPixmap(ipt_image_path)
        pixmap = pixmap.scaled(180*self.rate, 180*self.rate, aspectRatioMode=Qt.KeepAspectRatio)
        item.setIcon(QIcon(pixmap))
        item.setText(os.path.basename(image_path))


    # 刷新译图列表框内item的图片
    def transImageWidgetRefreshImage(self, image_path):

        row = self.image_path_list.index(image_path)
        item = self.trans_image_widget.item(row)
        rdr_image_path = self.getRdrFilePath(image_path)
        pixmap = QPixmap(rdr_image_path)
        pixmap = pixmap.scaled(180*self.rate, 180*self.rate, aspectRatioMode=Qt.KeepAspectRatio)
        item.setIcon(QIcon(pixmap))
        item.setText(os.path.basename(image_path))


    # 大图展示框刷新图片
    def showImageLabelRefresh(self, image_path) :

        with open(image_path, "rb") as file:
            image = QImage.fromData(file.read())
        pixmap = QPixmap.fromImage(image)
        self.show_image_label.setPixmap(pixmap)
        self.show_image_label.resize(pixmap.width(), pixmap.height())


    # 展示原图图片大图
    def loadOriginalImage(self) :

        self.clearTextBlock()
        index = self.original_image_widget.currentRow()
        if index >= 0 and index < len(self.image_path_list) :
            image_path = self.image_path_list[index]
            self.showImageLabelRefresh(image_path)
            self.image_widget_index = index
            self.image_widget_scroll_bar_value = self.original_image_widget.verticalScrollBar().value()


    # 展示编辑图图片大图
    def loadEditImage(self) :

        self.clearTextBlock()
        index = self.edit_image_widget.currentRow()
        if index >= 0 and index < len(self.image_path_list):
            image_path = self.image_path_list[index]
            ipt_image_path = self.getIptFilePath(image_path)
            if os.path.exists(ipt_image_path) :
                self.showImageLabelRefresh(ipt_image_path)
                # 译文编辑框渲染
                self.renderTextBlock(image_path)
            else :
                self.show_image_label.clear()
            self.image_widget_index = index
            self.image_widget_scroll_bar_value = self.edit_image_widget.verticalScrollBar().value()


    # 展示译图图片大图
    def loadTransImage(self):

        self.clearTextBlock()
        index = self.trans_image_widget.currentRow()
        if index >= 0 and index < len(self.image_path_list) :
            image_path = self.image_path_list[index]
            rdr_image_path = self.getRdrFilePath(image_path)
            if os.path.exists(rdr_image_path) :
                self.showImageLabelRefresh(rdr_image_path)
            else :
                self.show_image_label.clear()
            self.image_widget_index = index
            self.image_widget_scroll_bar_value = self.trans_image_widget.verticalScrollBar().value()


    # 翻译进程
    def transProcess(self, image_path) :

        # 漫画OCR
        if not os.path.exists(self.getJsonFilePath(image_path)):
            sign, ocr_result = self.mangaOCR(image_path)
            if not sign:
                return utils.message.MessageBox("OCR过程失败", ocr_result, self.rate)

        # 翻译
        trans_sign = False
        if not os.path.exists(self.getJsonFilePath(image_path)):
            trans_sign = True
        else:
            with open(self.getJsonFilePath(image_path), "r", encoding="utf-8") as file:
                json_data = json.load(file)
            if "translated_text" not in json_data:
                trans_sign = True
        if trans_sign:
            sign, trans_result = self.mangaTrans(image_path)
            if not sign:
                return utils.message.MessageBox("翻译过程失败", trans_result, self.rate)

        # 文字消除
        if not os.path.exists(self.getIptFilePath(image_path)):
            sign, ipt_result = self.mangaTextInpaint(image_path)
            if not sign:
                return utils.message.MessageBox("文字消除过程失败", ipt_result, self.rate)
            # 消除好的图片加入编辑图列表框
            self.editImageWidgetRefreshImage(image_path)

        # 漫画文字渲染
        if not os.path.exists(self.getRdrFilePath(image_path)):
            sign, rdr_result = self.mangaTextRdr(image_path)
            if not sign:
                return utils.message.MessageBox("文字渲染过程失败", rdr_result, self.rate)
            # 渲染好的图片加入译图列表框
            self.transImageWidgetRefreshImage(image_path)


    # 单图翻译
    def translaterItemWidget(self, item) :

        # 校验是否选择了翻译源
        if not self.object.config["mangaTrans"] :
            return utils.message.MessageBox("翻译失败", "请先选择要使用的翻译源     ", self.rate)
        # 获取图片路径
        row = self.original_image_widget.indexFromItem(item).row()
        image_path = self.image_path_list[row]
        # 创建执行线程
        thread = utils.thread.createMangaTransQThread(self, image_path)
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
        for val in json_data["text_block"] :
            original = ""
            for text in val["text"] :
                original += text
            # 调用翻译
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
                                                content=self.object.translation_ui.original,
                                                logger=self.logger)
            translated_text.append(result)

        json_data["translated_text"] = translated_text
        # 缓存ocr结果
        with open(self.getJsonFilePath(image_path), "w", encoding="utf-8") as file :
            json.dump(json_data, file, indent=4)

        # @TODO 缺少错误处理
        return True, result


    # 漫画文字渲染
    def mangaTextRdr(self, image_path):

        # 从缓存文件中获取json结果
        with open(self.getJsonFilePath(image_path), "r", encoding="utf-8") as file:
            json_data = json.load(file)
        # 从缓存文件里获取mask图片
        with open(self.getMaskFilePath(image_path), "rb") as file :
            mask = base64.b64encode(file.read()).decode("utf-8")
        # 从缓存文件里获取ipt图片
        with open(self.getIptFilePath(image_path), "rb") as file :
            ipt = base64.b64encode(file.read()).decode("utf-8")
        # 漫画rdr
        sign, result = translator.ocr.dango.mangaRDR(
            object=self.object,
            mask=mask,
            trans_list=json_data["translated_text"],
            inpainted_image=ipt,
            text_block=json_data["text_block"]
        )
        if sign :
            # 缓存inpaint图片
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


    # 清除图片上的文本块
    def clearTextBlock(self):

        for i in reversed(range(self.show_image_layout.count())):
            widget = self.show_image_layout.itemAt(i).widget()
            self.show_image_layout.removeWidget(widget)
            if widget is not None:
                widget.setParent(None)


    # 渲染文本块
    def renderTextBlock(self, image_path) :

        # 从缓存文件中获取json结果
        with open(self.getJsonFilePath(image_path), "r", encoding="utf-8") as file :
            json_data = json.load(file)

        rect = (self.show_image_label.width(), self.show_image_label.height())
        text_edit = RenderTextBlock(rect, json_data)
        self.show_image_layout.addWidget(text_edit)


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.hide()
        self.object.translation_ui.show()
        if self.object.range_ui.show_sign == True:
            self.object.range_ui.show()