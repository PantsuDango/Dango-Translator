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
import traceback
import pyperclip

import ui.static.icon
import utils.translater
import translator.ocr.dango
import translator.api
import utils.thread
import utils.message
import ui.progress_bar
import utils.zip


FONT_PATH_1 = "./config/other/NotoSansSC-Regular.otf"
FONT_PATH_2 = "./config/other/华康方圆体W7.TTC"


# 图片翻译界面
class Manga(QWidget) :

    show_error_signal = pyqtSignal(list)

    def __init__(self, object) :

        super(Manga, self).__init__()
        self.object = object
        self.logger = object.logger
        self.getInitConfig()
        self.setting_ui = Setting(object)
        self.ui()
        self.trans_edit_ui = TransEdit(object)
        self.show_image_widget = None
        self.show_error_sign = False


    def ui(self) :

        # 窗口尺寸
        self.resize(self.window_width*self.rate, self.window_height*self.rate)
        # 窗口标题
        self.setWindowTitle("图片翻译")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size, self.font_type))
        # # 最大化
        # self.setWindowState(Qt.WindowMaximized)

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
        self.createInputAction("从多个文件夹导入")
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

        # 译图导出按钮
        self.output_image_button = QPushButton(self)
        self.output_image_button.setText(" 译图导出")
        self.output_image_button.setStyleSheet("QPushButton {background: transparent;}"
                                               "QPushButton:hover {background-color: #83AAF9;}"
                                               "QPushButton:pressed {background-color: #4480F9;}")
        self.output_image_button.setIcon(ui.static.icon.OUTPUT_ICON)
        # 译图导出菜单
        self.output_menu = QMenu(self.output_image_button)
        self.output_action_group = QActionGroup(self.output_menu)
        self.output_action_group.setExclusive(True)
        self.createOutputAction("导出到指定目录")
        self.createOutputAction("导出为压缩包")
        # 将下拉菜单设置为按钮的菜单
        self.output_image_button.setMenu(self.output_menu)
        self.output_action_group.triggered.connect(self.outputImages)

        # 选择语种按钮
        self.select_language_button = QPushButton(self)
        self.select_language_button.setText(" 选择语种")
        self.select_language_button.setStyleSheet("QPushButton {background: transparent;}"
                                                  "QPushButton:hover {background-color: #83AAF9;}"
                                                  "QPushButton:pressed {background-color: #4480F9;}")
        self.select_language_button.setIcon(ui.static.icon.LANGUAGE_ICON)
        # 选择语种菜单
        self.language_menu = QMenu(self.select_language_button)
        self.language_action_group = QActionGroup(self.language_menu)
        self.language_action_group.setExclusive(True)
        self.createLanguageAction("日语(Japanese)")
        self.createLanguageAction("英语(English)")
        # 将下拉菜单设置为按钮的菜单
        self.select_language_button.setMenu(self.language_menu)
        self.language_action_group.triggered.connect(self.changeSelectLanguage)

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
        self.createTransAction("私人团子")
        self.createTransAction("私人彩云")
        self.createTransAction("私人腾讯")
        self.createTransAction("私人百度")
        self.createTransAction("私人ChatGPT")
        # 将下拉菜单设置为按钮的菜单
        self.select_trans_button.setMenu(self.trans_menu)
        self.trans_action_group.triggered.connect(self.changeSelectTrans)

        # 高级设置按钮
        self.setting_button = QPushButton(self)
        self.setting_button.setText(" 高级设置")
        self.setting_button.setStyleSheet("QPushButton {background: transparent;}"
                                          "QPushButton:hover {background-color: #83AAF9;}"
                                          "QPushButton:pressed {background-color: #4480F9;}")
        self.setting_button.setIcon(ui.static.icon.SETTING_ICON)
        self.setting_button.clicked.connect(self.setting_ui.show)

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
        self.setAcceptDrops(True)

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
        self.show_image_scroll_area = CustomScrollArea(self)
        self.show_image_scroll_area.setWidgetResizable(True)
        self.show_image_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show_image_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 错误展示提示窗
        self.show_error_label = QPushButton(self)
        self.show_error_label.setIcon(ui.static.icon.ERROR_ICON)
        self.show_error_label.hide()
        self.show_error_signal.connect(self.showError)

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
        # 图片翻译进度条
        self.trans_process_bar = ui.progress_bar.MangaProgressBar(self.object.yaml["screen_scale_rate"])

        self.refreshStatusLabel()


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
        # 语种映射表
        self.language_map = {
            "JAP": "日语(Japanese)",
            "ENG": "英语(English)",
            "RUS": "韩语(Korean)",
            "KOR": "俄语(Russian)",
        }


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
    def openImageFiles(self, action) :

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

        elif action.data() == "从多个文件夹导入" :
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.Directory)
            file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
            l = file_dialog.findChild(QListView, "listView")
            if l :
                l.setSelectionMode(QAbstractItemView.MultiSelection)
            t = file_dialog.findChild(QTreeView)
            if t :
                t.setSelectionMode(QAbstractItemView.MultiSelection)
            file_dialog.setFilter(QDir.Dirs)
            if file_dialog.exec_() == QDialog.Accepted :
                folder_paths = file_dialog.selectedFiles()
                # 遍历多个文件夹
                for folder_path in folder_paths[1:] :
                    if not os.path.exists(folder_path) :
                        continue
                    for file in os.listdir(folder_path) :
                        file_ext = os.path.splitext(file)[1].lower()
                        if file_ext != ".png" and file_ext != ".jpg" and file_ext != ".jpeg":
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
        for image_path in images :
            self.object.yaml["manga_dir_path"] = os.path.dirname(image_path)
            break


    # 导出译图文件
    def outputImages(self, action) :

        try :
            output_image_list = []
            for image_path in self.image_path_list :
                rdr_image_path = self.getRdrFilePath(image_path)
                if os.path.exists(rdr_image_path) :
                    output_image_list.append(rdr_image_path)
            if len(output_image_list) == 0 :
                return utils.message.MessageBox("导出失败", "没有可以导出的译图文件      ")

            # 选择指定位置
            options = QFileDialog.Options()
            folder_path = QFileDialog.getExistingDirectory(self, "选择要导出的位置", "", options=options)
            if not os.path.exists(folder_path):
                return utils.message.MessageBox("导出失败", "无效的目录      ")

            if action.data() == "导出到指定目录" :
                # 新建导出文件夹
                folder_path = os.path.join(folder_path, os.path.basename(self.object.yaml["manga_dir_path"]))
                if not os.path.exists(folder_path) :
                    os.mkdir(folder_path)
                # 复制完成的rdr图片
                for image_path in output_image_list :
                    new_image_path = os.path.join(folder_path, os.path.basename(image_path))
                    shutil.copy(image_path, new_image_path)
                os.startfile(folder_path)

            elif action.data() == "导出为压缩包" :
                zip_name = "{}.zip".format(os.path.basename(self.object.yaml["manga_dir_path"]))
                zip_path = os.path.join(folder_path, zip_name)
                utils.zip.zipFiles(output_image_list, zip_path)
                os.startfile(folder_path)

            else :
                return
        except Exception :
            traceback.print_exc()


    # 导入图片
    def inputImage(self, index, image_path, finish_sign) :

        if not finish_sign :
            # 图片添加至原图列表框
            self.originalImageWidgetAddImage(index, image_path)
            # 图片添加至编辑图列表框
            self.editImageWidgetAddImage(index)
            if os.path.exists(self.getRdrFilePath(image_path)) :
                self.editImageWidgetRefreshImage(image_path)
            # 图片添加至译图列表框
            self.transImageWidgetAddImage(index)
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
        if button_type == "original" :
            self.original_image_widget.show()
            self.original_image_button.setStyleSheet("background-color: #83AAF9;")
            self.original_image_widget.verticalScrollBar().setValue(self.image_widget_scroll_bar_value)
            self.original_image_widget.setCurrentRow(self.image_widget_index)
            self.loadOriginalImage()

        elif button_type == "edit" :
            self.edit_image_widget.show()
            self.edit_image_button.setStyleSheet("background-color: #83AAF9;")
            self.edit_image_widget.verticalScrollBar().setValue(self.image_widget_scroll_bar_value)
            self.edit_image_widget.setCurrentRow(self.image_widget_index)
            self.loadEditImage()

        elif button_type == "trans" :
            self.trans_image_widget.show()
            self.trans_image_button.setStyleSheet("background-color: #83AAF9;")
            self.trans_image_widget.verticalScrollBar().setValue(self.image_widget_scroll_bar_value)
            self.trans_image_widget.setCurrentRow(self.image_widget_index)
            self.loadTransImage()


    # 创建导入原图按钮的下拉菜单
    def createInputAction(self, label) :

        action = QAction(label, self.input_menu)
        action.setCheckable(True)
        action.setData(label)
        self.input_action_group.addAction(action)
        self.input_menu.addAction(action)


    # 创建译图导出按钮的下拉菜单
    def createOutputAction(self, label) :

        action = QAction(label, self.output_menu)
        action.setCheckable(True)
        action.setData(label)
        self.output_action_group.addAction(action)
        self.output_menu.addAction(action)


    # 创建语种按钮的下拉菜单
    def createLanguageAction(self, label) :

        action = QAction(label, self.language_menu)
        action.setCheckable(True)
        action.setData(label)
        self.language_action_group.addAction(action)
        self.language_menu.addAction(action)
        if self.language_map[self.object.config["mangaLanguage"]] == label :
            action.setChecked(True)


    # 创建翻译源按钮的下拉菜单
    def createTransAction(self, label) :

        action = QAction(label, self.trans_menu)
        action.setCheckable(True)
        action.setData(label)
        self.trans_action_group.addAction(action)
        self.trans_menu.addAction(action)
        if self.object.config["mangaTrans"] == label :
            action.setChecked(True)


    # 改变所使用的语种
    def changeSelectLanguage(self, action) :

        tmp_map = {}
        for k, v in self.language_map.items() :
            tmp_map[v] = k
        self.object.config["mangaLanguage"] = tmp_map[action.data()]
        self.refreshStatusLabel()


    # 改变所使用的翻译源
    def changeSelectTrans(self, action) :

        self.object.config["mangaTrans"] = action.data()
        self.refreshStatusLabel()


    # 刷新底部状态栏信息
    def refreshStatusLabel(self) :

        self.status_label.setText(
            "原文语种: {}     翻译源: {}"
            .format(self.language_map[self.object.config["mangaLanguage"]],
                    self.object.config["mangaTrans"]))


    # 设置原图列表框右键菜单
    def showOriginalListWidgetMenu(self, pos) :

        item = self.original_image_widget.itemAt(pos)
        if item is not None:
            menu = QMenu(self)
            # 添加菜单项
            translater_action = menu.addAction("翻译当前图片")
            translater_action.triggered.connect(lambda: self.translaterItemWidget(item))
            delete_action = menu.addAction("移除当前图片")
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
    def originalImageWidgetAddImage(self, index, image_path):

        item = QListWidgetItem(self.original_image_widget)
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(180*self.rate, 180*self.rate, aspectRatioMode=Qt.KeepAspectRatio)
        item.setText(index)
        item.setIcon(QIcon(pixmap))
        item.listWidget()
        self.original_image_widget.addItem(item)
        self.image_path_list.append(image_path)


    # 编辑图列表框添加图片
    def editImageWidgetAddImage(self, index) :

        item = QListWidgetItem(self.edit_image_widget)
        item.setSizeHint(QSize(0, 180*self.rate))
        item.setText(index)
        self.edit_image_widget.addItem(item)


    # 译图列表框添加图片
    def transImageWidgetAddImage(self, index) :

        item = QListWidgetItem(self.trans_image_widget)
        item.setSizeHint(QSize(0, 180*self.rate))
        item.setText(index)
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
                message = "OCR过程失败: %s"%ocr_result
                self.show_error_signal.emit([image_path, message])
                return message
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
        self.trans_result = ""
        def transThread() :
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
                if not sign :
                    self.trans_result = "翻译过程失败: %s"%trans_result
                    return
            self.trans_process_bar.paintStatus("trans", round(time.time()-start, 1))
        trans_thread = utils.thread.createThread(transThread)

        # 文字消除
        start = time.time()
        if not os.path.exists(self.getIptFilePath(image_path)) or reload_sign :
            sign, ipt_result = self.mangaTextInpaint(image_path)
            if not sign :
                message = "文字消除过程失败: %s"%ipt_result
                self.show_error_signal.emit([image_path, message])
                return message
        self.trans_process_bar.paintStatus("ipt", round(time.time()-start, 1))

        # 阻塞, 等待翻译完成
        trans_thread.join()
        if self.trans_result :
            self.show_error_signal.emit([image_path, self.trans_result])
            return self.trans_result

        # 漫画文字渲染
        start = time.time()
        if not os.path.exists(self.getRdrFilePath(image_path)) or reload_sign :
            sign, rdr_result = self.mangaTextRdr(image_path)
            if not sign :
                message = "文字渲染过程失败: %s"%rdr_result
                self.show_error_signal.emit([image_path, message])
                return message
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
        self.trans_process_bar.modifyTitle("图片翻译 -- 执行中请勿关闭此窗口")
        self.trans_process_bar.show()
        # 创建执行线程
        self.trans_all_button.setEnabled(False)
        reload_sign = True
        thread = utils.thread.createMangaTransQThread(self, image_paths, reload_sign)
        thread.signal.connect(self.finishTransProcessRefresh)
        thread.bar_signal.connect(self.trans_process_bar.paintProgressBar)
        thread.add_message_signal.connect(self.trans_process_bar.setMessageText)
        utils.thread.runQThread(thread)


    # 漫画OCR
    def mangaOCR(self, image_path) :

        sign, result = translator.ocr.dango.mangaOCR(self.object, image_path)
        if sign :
            # 缓存mask图片
            with open(self.getMaskFilePath(image_path), "wb") as file :
                file.write(base64.b64decode(result["mask"]))
            del result["mask"]
            # 过滤错误的文本块
            new_text_block = []
            for index, val in enumerate(result.get("text_block", [])) :
                texts = val.get("texts", [])
                if not texts :
                    continue
                skip_sign = False
                for text in texts :
                    if not text or text == "<skip>" :
                        skip_sign = True
                        break
                if skip_sign :
                    continue
                new_text_block.append(val)
            # 过滤屏蔽词和替换词
            for index, val in enumerate(new_text_block) :
                new_texts = []
                for text in val["texts"] :
                    for filter in self.object.config["Filter"]:
                        if not filter[0]:
                            continue
                        text = text.replace(filter[0], filter[1])
                    new_texts.append(text)
                new_text_block[index]["texts"] = new_texts

            result["text_block"] = new_text_block
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


    # 图片翻译
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
        if manga_trans == "私人团子" :
            sign, result = translator.ocr.dango.dangoTrans(object=self.object,
                                                           sentence=original,
                                                           language=self.object.config["mangaLanguage"])
            if not sign :
                return False, result

        if manga_trans == "私人彩云" :
            result = translator.api.caiyun(sentence=original,
                                           token=self.object.config["caiyunAPI"],
                                           logger=self.logger)
            if result[:6] == "私人彩云: " :
                return False, result

        elif manga_trans == "私人腾讯" :
            result = translator.api.tencent(sentence=original,
                                            secret_id=self.object.config["tencentAPI"]["Key"],
                                            secret_key=self.object.config["tencentAPI"]["Secret"],
                                            logger=self.logger)
            if result[:6] == "私人腾讯: " :
                return False, result

        elif manga_trans == "私人百度" :
            result = translator.api.baidu(sentence=original,
                                          app_id=self.object.config["baiduAPI"]["Key"],
                                          secret_key=self.object.config["baiduAPI"]["Secret"],
                                          logger=self.logger)
            if result[:6] == "私人百度: " :
                return False, result

        elif manga_trans == "私人ChatGPT" :
            result = translator.api.chatgpt(api_key=self.object.config["chatgptAPI"],
                                            language=self.object.config["language"],
                                            proxy=self.object.config["chatgptProxy"],
                                            content=original,
                                            logger=self.logger)
            if result[:11] == "私人ChatGPT: " :
                return False, result

        # 根据屏蔽词过滤
        for filter in self.object.config["Filter"]:
            if not filter[0]:
                continue
            result = result.replace(filter[0], filter[1])

        for index, word in enumerate(result.split("\n")[:len(json_data["text_block"])]) :
            translated_text.append(word)

        json_data["translated_text"] = translated_text
        # 缓存翻译结果
        with open(self.getJsonFilePath(image_path), "w", encoding="utf-8") as file :
            json.dump(json_data, file, indent=4)

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

        # 获取图片翻译缓存目录
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

        original_image_path = image_path
        ipt_image_path = self.getIptFilePath(image_path)
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

        # 切换图片的时候保持比例
        init_image_rate = []
        if self.show_image_widget :
            init_image_rate = copy.deepcopy(self.show_image_widget.image_rate)

        w_rate = self.width() / self.window_width
        h_rate = self.height() / self.window_height
        self.show_image_scroll_area.setWidget(None)
        self.show_image_widget = RenderTextBlock(
            rate=(w_rate, h_rate),
            image_path=image_path,
            original_image_path=original_image_path,
            ipt_image_path=ipt_image_path,
            json_data=json_data,
            edit_window=self.trans_edit_ui
        )
        self.show_image_scroll_area.setWidget(self.show_image_widget)
        self.show_image_scroll_area.show()

        # 切换图片的时候保持比例
        if init_image_rate :
            self.setImageInitRate(init_image_rate)


    # 设置图片初始缩放比例
    def setImageInitRate(self, init_image_rate) :

        self.show_image_widget.image_rate = init_image_rate
        pixmap = self.show_image_widget.image_pixmap.scaled(
            self.show_image_widget.image_pixmap.width() * self.show_image_widget.image_rate[0],
            self.show_image_widget.image_pixmap.height() * self.show_image_widget.image_rate[1]
        )
        self.show_image_widget.image_label.setPixmap(pixmap)
        self.show_image_widget.rate_label.setText("{}%".format(round(self.show_image_widget.image_rate[0] * 100)))
        self.show_image_widget.matchButtonSize()


    # 翻译完成后刷新译图栏
    def finishTransProcessRefresh(self, value, signal) :

        if not signal :
            if value:
                # @TODO 缺少错误处理
                pass
            self.trans_process_bar.close()
            self.trans_all_button.setEnabled(True)


    # 一键翻译
    def clickTransAllButton(self) :

        self.trans_all_button.setEnabled(False)
        # 进度条窗口
        self.trans_process_bar.modifyTitle("图片翻译 -- 执行中请勿关闭此窗口")
        self.trans_process_bar.show()
        # 创建执行线程
        thread = utils.thread.createMangaTransQThread(self, self.image_path_list)
        thread.signal.connect(self.finishTransProcessRefresh)
        thread.bar_signal.connect(self.trans_process_bar.paintProgressBar)
        thread.add_message_signal.connect(self.trans_process_bar.setMessageText)
        utils.thread.runQThread(thread)


    # 打开使用教程
    def openUseTutorial(self) :

        url = self.object.yaml["dict_info"]["manga_tutorial"]
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            self.logger.error(format_exc())
            utils.message.MessageBox("图片翻译教程",
                                     "打开失败, 请尝试手动打开此地址\n%s     "%url)


    # 窗口尺寸变化信号
    def resizeEvent(self, event) :

        w = event.size().width()
        h = event.size().height()
        w_rate = w / self.window_width
        h_rate = h / self.window_height

        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size*w_rate, self.font_type))
        # 导入原图按钮
        self.customSetGeometry(self.input_image_button, 0, 0, 120, 35, w_rate, h_rate)
        # 底部状态栏
        self.status_label.setGeometry(
            10 * w_rate, h - 30 * h_rate,
            w, 30 * h_rate
        )
        # 一键翻译按钮
        self.trans_all_button.setGeometry(
            self.input_image_button.width(), 0,
            self.input_image_button.width(), self.input_image_button.height()
        )
        # 译图导出按钮
        self.output_image_button.setGeometry(
            self.trans_all_button.x() + self.input_image_button.width(), 0,
            self.input_image_button.width(), self.input_image_button.height()
        )
        # 选择语种
        self.select_language_button.setGeometry(
            self.output_image_button.x() + self.input_image_button.width(), 0,
            self.input_image_button.width(), self.input_image_button.height()
        )
        # 选择翻译源按钮
        self.select_trans_button.setGeometry(
            self.select_language_button.x() + self.input_image_button.width(), 0,
            self.input_image_button.width(), self.input_image_button.height()
        )
        # 高级设置按钮
        self.setting_button.setGeometry(
            self.select_trans_button.x() + self.input_image_button.width(), 0,
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
        # 错误展示提示窗
        self.show_error_label.setGeometry(
            self.show_image_scroll_area.x(), self.show_image_scroll_area.y(),
            self.show_image_scroll_area.width(), self.show_image_scroll_area.height() / 8
        )
        self.show_error_label.setStyleSheet("background-color: #98ff98;"
                                            "font: %spt '%s';"%((self.font_size+5*w_rate), self.font_type))
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


    # 展示错误消息
    def showError(self, messages: list) :

        # 刷新提示消息
        text = ""
        for message in messages :
            if message == messages[-1] :
                text += "     " + message
            else :
                text += "     " + message + "\n"
        self.show_error_label.setText(text)
        self.show_error_label.show()

        # 刷新停留时间
        self.show_error_start_time = time.time()
        if self.show_error_sign :
            return

        # 展示消息等待线程, 停留时间5s
        def waitThread() :
            self.show_error_sign = True
            while True :
                if time.time() - self.show_error_start_time >= 5 :
                    self.show_error_sign = False
                    return self.show_error_label.hide()
        utils.thread.createThread(waitThread)


    # 拖拽文件信号
    def dragEnterEvent(self, event) :
        try :
            if event.mimeData().hasUrls():
                event.accept()
            else:
                event.ignore()
        except Exception :
            traceback.print_exc()


    # 拖拽导入文件
    def dropEvent(self, event) :

        try :
            image_list = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                # 过滤非图片文件
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext != ".png" and file_ext != ".jpg" and file_ext != ".jpeg" :
                    continue
                image_list.append(file_path)
            # 去重
            image_list = list(set(image_list))

            if image_list :
                event.accept()
                # 清除所有图片
                self.clearAllImages()
                # 根据文件名排序
                image_list = self.dirFilesPathSort(image_list)
                # 进度条窗口
                self.input_images_progress_bar.modifyTitle("导入图片 -- 加载中请勿关闭此窗口")
                self.input_images_progress_bar.show()
                # 导入图片线程
                thread = utils.thread.createInputImagesQThread(self, image_list)
                thread.bar_signal.connect(self.input_images_progress_bar.paintProgressBar)
                thread.image_widget_signal.connect(self.inputImage)
                utils.thread.runQThread(thread)

        except Exception :
            traceback.print_exc()


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.hide()
        self.object.translation_ui.show()
        if self.object.range_ui.show_sign == True:
            self.object.range_ui.show()


# 渲染文本块
class RenderTextBlock(QWidget) :

    def __init__(self, rate, image_path, original_image_path,
                 ipt_image_path, json_data, edit_window) :

        super(RenderTextBlock, self).__init__()
        self.rate = rate
        self.image_path = image_path
        self.original_image_path = original_image_path
        self.ipt_image_path = ipt_image_path
        self.json_data = json_data
        self.trans_edit_ui = edit_window
        self.object = edit_window.object
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
        self.scroll_area = CustomScrollArea(self)
        self.scroll_area.setGeometry(0, 0, self.width(), self.height())
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setCursor(Qt.OpenHandCursor)
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
            # 绘制矩形框
            button = CustomTextBlockButton(self.image_label)
            button.setCursor(ui.static.icon.EDIT_CURSOR)
            button.initConfig(
                text_block=text_block,
                trans=trans_text,
                rect=(x_0, y_0, w_0, h_0),
                index=index,
                original_image_path=self.original_image_path,
                ipt_image_path=self.ipt_image_path,
                rdr_image_path=self.image_path
            )
            # 打开文本框编辑信号
            button.click_signal.connect(self.clickTextBlock)
            # 移动文本框信号
            button.move_signal.connect(self.refreshTextBlockPosition)
            button.setGeometry(x, y, w, h)
            button.setStyleSheet("QPushButton {background: transparent; border: 2px solid red;}"
                                 "QPushButton:hover {background-color:rgba(62, 62, 62, 0.1)}")
            # 文本框右键菜单
            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(lambda _, b=button: self.showTextBlockButtonMenu(b))
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
    def clickTextBlock(self, button) :

        self.trans_edit_ui.button = button

        # 文本颜色
        font_color = QColor(button.font_color[0], button.font_color[1], button.font_color[2])
        self.trans_edit_ui.font_color = font_color.name()
        self.trans_edit_ui.font_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=font_color.name()))
        # 轮廓颜色
        bg_color = QColor(button.bg_color[0], button.bg_color[1], button.bg_color[2])
        self.trans_edit_ui.bg_color = bg_color.name()
        self.trans_edit_ui.bg_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=bg_color.name()))
        # 原文
        self.trans_edit_ui.original_text.clear()
        self.trans_edit_ui.original_text.insertPlainText(button.original)
        # 译文
        self.trans_edit_ui.trans_text.clear()
        self.trans_edit_ui.trans_text.insertPlainText(button.trans)

        self.trans_edit_ui.show()


    # 图片自适配比例
    def matchImageSize(self) :

        pixmap = self.image_pixmap
        if pixmap.height() > self.height() :
            rate = self.height() / pixmap.height()
            pixmap = pixmap.scaled(pixmap.width()*rate, pixmap.height()*rate)
        if pixmap.width() > self.width() :
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

        for button in self.button_list :
            # 计算缩放比例
            x = button.rect[0] * self.image_rate[0]
            y = button.rect[1] * self.image_rate[1]
            w = button.rect[2] * self.image_rate[0]
            h = button.rect[3] * self.image_rate[1]
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


    # 文字块按钮右键菜单
    def showTextBlockButtonMenu(self, button) :

        menu = QMenu(self)
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(lambda: self.deleteTextBlock(button))
        cursorPos = QCursor.pos()
        menu.exec_(cursorPos)


    # 删除文本块
    def deleteTextBlock(self, button) :

        # 打开原图, 按照文本块坐标截图
        image = Image.open(self.original_image_path)
        x, y, w, h = button.rect[0], button.rect[1], button.rect[2], button.rect[3]
        cropped_image = image.crop((x, y, x + w, y + h))
        # 打开rdr图片, 将截图贴图
        rdr_image = Image.open(self.image_path)
        rdr_image.paste(cropped_image, (x, y))
        rdr_image.save(self.image_path)

        # 刷新缓存文件中获取json结果
        file_name = os.path.splitext(os.path.basename(self.original_image_path))[0]
        json_file_path = os.path.join(os.path.dirname(self.ipt_image_path), "%s.json"%file_name)
        with open(json_file_path, "r", encoding="utf-8") as file :
            json_data = json.load(file)
        del json_data["translated_text"][button.index]
        del json_data["text_block"][button.index]
        # 缓存ocr结果
        with open(json_file_path, "w", encoding="utf-8") as file :
            json.dump(json_data, file, indent=4)
        # 删除文本框按钮
        button.close()
        del self.button_list[button.index]
        # 刷新文本框按钮索引值
        for i, button in enumerate(self.button_list) :
            button.index = i
        # 刷新大图
        init_image_rate = copy.deepcopy(self.image_rate)
        self.loadImage()
        self.matchButtonSize()
        self.object.manga_ui.setImageInitRate(init_image_rate)


    # 移动文本块位置后重新渲染
    def refreshTextBlockPosition(self, button) :

        try :
            # 原坐标
            x_0 = button.rect[0]
            y_0 = button.rect[1]
            w_0 = button.rect[2]
            h_0 = button.rect[3]
            # 当前坐标
            x_n = round(button.x() / self.image_rate[0])
            y_n = round(button.y() / self.image_rate[1])
            w_n = w_0
            h_n = h_0

            # 基于原坐标, 对ipt截图
            ipt_image = Image.open(self.ipt_image_path)
            cropped_image = ipt_image.crop((x_0, y_0, x_0 + w_0, y_0 + h_0))
            # 打开rdr图片, 将截图贴图
            rdr_image = Image.open(self.image_path)
            rdr_image.paste(cropped_image, (x_0, y_0))

            # 新位置ipt截图
            cropped_image = ipt_image.crop((x_n, y_n, x_n + w_n, y_n + h_n))
            # 截图转换为base64
            buffered = io.BytesIO()
            cropped_image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # 重新计算截图后的坐标
            text_block = copy.deepcopy(button.text_block)
            text_block["block_coordinate"]["upper_left"] = [0, 0]
            text_block["block_coordinate"]["upper_right"] = [w_n, 0]
            text_block["block_coordinate"]["lower_right"] = [w_n, h_n]
            text_block["block_coordinate"]["lower_left"] = [0, h_n]
            for i, val in enumerate(text_block["coordinate"]):
                coordinate = {}
                for k in val.keys():
                    coordinate[k] = [val[k][0] - x_0, val[k][1] - y_0]
                text_block["coordinate"][i] = coordinate

            # 调用漫画rdr
            sign, result = translator.ocr.dango.mangaRDR(
                object=self.trans_edit_ui.object,
                trans_list=[button.trans],
                inpainted_image=image_base64,
                text_block=[text_block]
            )
            if not sign or not result.get("rendered_image", ""):
                # @TODO 错误处理
                return

            # 渲染后的新图贴在rdr大图上
            image_base64 = base64.b64decode(result["rendered_image"])
            cropped_image = Image.open(io.BytesIO(image_base64))
            rdr_image.paste(cropped_image, (x_n, y_n))
            rdr_image.save(self.image_path)

            # 获取文件名
            file_name = os.path.splitext(os.path.basename(self.original_image_path))[0]
            # 获取ocr缓存文件路径
            json_file_path = os.path.join(os.path.dirname(self.ipt_image_path), "%s.json"%file_name)
            # 从缓存文件中获取ocr信息
            with open(json_file_path, "r", encoding="utf-8") as file :
                json_data = json.load(file)

            # 修改移动后的block_coordinate
            block_coordinate = json_data["text_block"][button.index]["block_coordinate"]
            block_coordinate["upper_left"] = [x_n, y_n]
            block_coordinate["upper_right"] = [x_n + w_n, y_n]
            block_coordinate["lower_right"] = [x_n + w_n, y_n + h_n]
            block_coordinate["lower_left"] = [x_n, y_n + h_n]
            json_data["text_block"][button.index]["block_coordinate"] = block_coordinate

            # 修改移动后的coordinate
            coordinate = json_data["text_block"][button.index]["coordinate"]
            for i, val in enumerate(coordinate) :
                tmp_coordinate = {}
                for k in val.keys() :
                    tmp_coordinate[k] = [
                        val[k][0] - (x_0 - x_n),
                        val[k][1] - (y_0 - y_n)
                    ]
                coordinate[i] = tmp_coordinate
            json_data["text_block"][button.index]["coordinate"] = coordinate

            # 缓存修改后的ocr结果
            with open(json_file_path, "w", encoding="utf-8") as file :
                json.dump(json_data, file, indent=4)

            # 刷新按钮信息
            button.rect = (x_n, y_n, w_n, h_n)
            button.text_block = json_data["text_block"][button.index]
            # 刷新大图
            init_image_rate = copy.deepcopy(self.image_rate)
            self.loadImage()
            self.matchButtonSize()
            self.object.manga_ui.setImageInitRate(init_image_rate)

        except Exception :
            traceback.print_exc()


# 译文编辑界面
class TransEdit(QWidget) :

    def __init__(self, object) :

        super(TransEdit, self).__init__()
        self.object = object
        self.rate = object.yaml["screen_scale_rate"]
        self.logger = object.logger
        self.font_color = "#83AAF9"
        self.bg_color = "#83AAF9"
        self.button = None
        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.window_width = int(500*self.rate)
        self.window_height = int(330*self.rate)
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("图片翻译-译文编辑")
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
        self.font_color_button.setStyleSheet("QPushButton {background: transparent; font: 9pt '华康方圆体W7';}"
                                             "QPushButton:hover {background-color: #83AAF9;}"
                                             "QPushButton:pressed {background-color: #4480F9;}")
        self.font_color_button.setToolTip("<b>修改显示的字体颜色</b>")

        # 修改轮廓颜色
        self.bg_color_button = QPushButton(qtawesome.icon("fa5s.paint-brush", color=self.bg_color), "", self)
        self.customSetGeometry(self.bg_color_button, 70, 0, 70, 30)
        self.bg_color_button.setCursor(ui.static.icon.EDIT_CURSOR)
        self.bg_color_button.setText(" 轮廓色")
        self.bg_color_button.clicked.connect(self.changeBackgroundColor)
        self.bg_color_button.setStyleSheet("QPushButton {background: transparent; font: 9pt '华康方圆体W7';}"
                                           "QPushButton:hover {background-color: #83AAF9;}"
                                           "QPushButton:pressed {background-color: #4480F9;}")
        self.bg_color_button.setToolTip("<b>修改显示的轮廓颜色</b>")

        # 字体样式
        label = QLabel(self)
        self.customSetGeometry(label, 7, 32, 20, 20)
        label.setPixmap(ui.static.icon.FONT_PIXMAP)
        self.font_box = QComboBox(self)
        self.customSetGeometry(self.font_box, 28, 30, 185, 25)
        self.font_box.setCursor(ui.static.icon.EDIT_CURSOR)
        self.font_box.setToolTip("<b>设置字体样式</b>")
        self.font_box.setStyleSheet("font: 9pt '华康方圆体W7';")
        utils.thread.createThread(self.createFontBox)

        # 私人彩云
        button = QPushButton(self)
        self.customSetGeometry(button, 140, 0, 70, 30)
        button.setCursor(ui.static.icon.EDIT_CURSOR)
        button.setText(" 团子")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        button.setStyleSheet("QPushButton {background: transparent; font: 9pt '华康方圆体W7';}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.clicked.connect(lambda: self.refreshTrans("团子"))
        button.setToolTip("<b>使用私人团子重新翻译</b>")

        # 私人彩云
        button = QPushButton(self)
        self.customSetGeometry(button, 210, 0, 70, 30)
        button.setCursor(ui.static.icon.EDIT_CURSOR)
        button.setText(" 彩云")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        button.setStyleSheet("QPushButton {background: transparent; font: 9pt '华康方圆体W7';}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.clicked.connect(lambda: self.refreshTrans("彩云"))
        button.setToolTip("<b>使用私人彩云重新翻译</b>")

        # 私人腾讯
        button = QPushButton(self)
        self.customSetGeometry(button, 280, 0, 70, 30)
        button.setCursor(ui.static.icon.EDIT_CURSOR)
        button.setText(" 腾讯")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        button.setStyleSheet("QPushButton {background: transparent; font: 9pt '华康方圆体W7';}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.clicked.connect(lambda: self.refreshTrans("腾讯"))
        button.setToolTip("<b>使用私人腾讯重新翻译</b>")

        # 私人百度
        button = QPushButton(self)
        self.customSetGeometry(button, 350, 0, 70, 30)
        button.setCursor(ui.static.icon.EDIT_CURSOR)
        button.setText(" 百度")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        button.setStyleSheet("QPushButton {background: transparent; font: 9pt '华康方圆体W7';}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.clicked.connect(lambda: self.refreshTrans("百度"))
        button.setToolTip("<b>使用私人百度重新翻译</b>")

        # 私人ChatGPT
        button = QPushButton(self)
        self.customSetGeometry(button, 420, 0, 70, 30)
        button.setCursor(ui.static.icon.EDIT_CURSOR)
        button.setText(" ChatGPT")
        button.setIcon(ui.static.icon.TRANSLATE_ICON)
        button.setStyleSheet("QPushButton {background: transparent; font: 9pt '华康方圆体W7'; border-radius: 6px}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.clicked.connect(lambda: self.refreshTrans("ChatGPT"))
        button.setToolTip("<b>使用私人ChatGPT重新翻译</b>")

        # 原文编辑框
        self.original_text = QTextBrowser(self)
        self.customSetGeometry(self.original_text, 0, 60, 500, 100)
        self.original_text.setReadOnly(False)
        self.original_text.setStyleSheet("font: 12pt '%s';"%font_type)
        self.original_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 原文复制按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 480, 140, 20, 20)
        button.setIcon(ui.static.icon.COPY_ICON)
        self.customSetIconSize(button, 20, 20)
        button.setStyleSheet("QPushButton {background: transparent; border-radius: 6px}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.setToolTip("<b>复制当前原文</b>")
        button.clicked.connect(lambda: pyperclip.copy(self.original_text.toPlainText()))

        # 译文编辑框
        self.trans_text = QTextBrowser(self)
        self.customSetGeometry(self.trans_text, 0, 160, 500, 100)
        self.trans_text.setCursor(ui.static.icon.EDIT_CURSOR)
        self.trans_text.setReadOnly(False)
        self.trans_text.setStyleSheet("font: 12pt '%s';"%font_type)
        self.trans_text.setCursor(ui.static.icon.EDIT_CURSOR)

        # 译文复制按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 480, 240, 20, 20)
        button.setIcon(ui.static.icon.COPY_ICON)
        self.customSetIconSize(button, 20, 20)
        button.setStyleSheet("QPushButton {background: transparent; border-radius: 6px}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.setToolTip("<b>复制当前译文</b>")
        button.clicked.connect(lambda: pyperclip.copy(self.trans_text.toPlainText()))

        # 重新贴字按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 125, 270, 100, 50)
        button.setText("重新贴字")
        button.setStyleSheet("font: 12pt '华康方圆体W7';")
        button.clicked.connect(self.renderTextBlock)
        button.setCursor(ui.static.icon.SELECT_CURSOR)

        # 取消按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 275, 270, 100, 50)
        button.setText("取消")
        button.setStyleSheet("font: 12pt '华康方圆体W7';")
        button.clicked.connect(self.close)
        button.setCursor(ui.static.icon.SELECT_CURSOR)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))

    # 根据分辨率定义图标位置尺寸
    def customSetIconSize(self, object, w, h) :

        object.setIconSize(QSize(int(w * self.rate), int(h * self.rate)))


    # 重新渲染文字
    def renderTextBlock(self) :

        try :
            if not self.button :
                return

            # 打开ipt图片, 按照文本块坐标截图
            image = Image.open(self.button.ipt_image_path)
            x = self.button.rect[0]
            y = self.button.rect[1]
            w = self.button.rect[2]
            h = self.button.rect[3]
            cropped_image = image.crop((x, y, x + w, y + h))

            # 截图转换为base64
            buffered = io.BytesIO()
            cropped_image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            text_block = copy.deepcopy(self.button.text_block)
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
            for i, val in enumerate(text_block["coordinate"]) :
                coordinate = {}
                for k in val.keys() :
                    coordinate[k] = [val[k][0] - x, val[k][1] - y]
                text_block["coordinate"][i] = coordinate

            # 漫画rdr
            sign, result = translator.ocr.dango.mangaRDR(
                object=self.object,
                trans_list=[self.trans_text.toPlainText()],
                inpainted_image=image_base64,
                text_block=[text_block],
                font=self.font_box.currentText()
            )
            if not sign or not result.get("rendered_image", "") :
                #@TODO 错误处理
                return

            # 渲染后的新图贴在大图上
            image_base64 = base64.b64decode(result["rendered_image"])
            cropped_image = Image.open(io.BytesIO(image_base64))
            rdr_image = Image.open(self.button.rdr_image_path)
            rdr_image.paste(cropped_image, (x, y))
            rdr_image.save(self.button.rdr_image_path)

            # 刷新缓存文件中获取json结果
            file_name = os.path.splitext(os.path.basename(self.button.original_image_path))[0]
            json_file_path = os.path.join(os.path.dirname(self.button.ipt_image_path), "%s.json"%file_name)
            with open(json_file_path, "r", encoding="utf-8") as file :
                json_data = json.load(file)
            json_data["translated_text"][self.button.index] = self.trans_text.toPlainText()
            json_data["text_block"][self.button.index]["foreground_color"] = [f_r, f_g, f_b]
            json_data["text_block"][self.button.index]["background_color"] = [b_r, b_g, b_b]

            # 缓存ocr结果
            with open(json_file_path, "w", encoding="utf-8") as file :
                json.dump(json_data, file, indent=4)

            # 刷新文本块按钮信息
            self.button.text_block = json_data["text_block"][self.button.index]
            self.button.trans = self.trans_text.toPlainText()
            self.button.font_color = [f_r, f_g, f_b]
            self.button.bg_color = [b_r, b_g, b_b]
            # 刷新大图
            init_image_rate = copy.deepcopy(self.object.manga_ui.show_image_widget.image_rate)
            self.object.manga_ui.show_image_widget.loadImage()
            self.object.manga_ui.show_image_widget.matchButtonSize()
            self.object.manga_ui.setImageInitRate(init_image_rate)

        except Exception :
            traceback.print_exc()


    # 刷新翻译结果
    def refreshTrans(self, trans_type) :

        original = self.original_text.toPlainText()
        if trans_type == "团子" :
            sign, result = translator.ocr.dango.dangoTrans(object=self.object,
                                                           sentence=original,
                                                           language=self.object.config["mangaLanguage"])
        elif trans_type == "彩云" :
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

        self.hide()
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
        self.show()


    # 修改轮廓颜色
    def changeBackgroundColor(self):

        self.hide()
        color = QColorDialog.getColor(QColor(self.bg_color), None, "修改轮廓颜色")
        if color.isValid():
            self.bg_color = color.name()
            self.bg_color_button.setIcon(qtawesome.icon("fa5s.paint-brush", color=self.bg_color))
        self.show()

    # 创建字体按钮的下拉菜单
    def createFontBox(self):

        sign, resp = translator.ocr.dango.mangaFontList(self.object)
        if not sign:
            # @TODO 错误处理
            return
        font_list = resp.get("available_fonts", [])
        for index, font in enumerate(font_list) :
            self.font_box.addItem("")
            self.font_box.setItemText(index, font)
        self.font_box.setCurrentText("Noto_Sans_SC/NotoSansSC-Regular")


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


# 自定义QScrollArea禁用鼠标滚轮控制滚动条
class CustomScrollArea(QScrollArea) :

    def __init__(self, parent=None) :
        super().__init__(parent)


    # 取消事件的传递，禁用滚轮控制滚动条
    def wheelEvent(self, event) :
        event.ignore()


    # 鼠标移动事件
    def mouseMoveEvent(self, e: QMouseEvent) :
        try :
            self._endPos = e.pos() - self._startPos
            horizontal = self.horizontalScrollBar()
            if self._endPos.x() > 3 :
                horizontal.setValue(horizontal.value() -3)
            else :
                horizontal.setValue(horizontal.value() +3)
            vertical = self.verticalScrollBar()
            if self._endPos.y() > 3 :
                vertical.setValue(vertical.value() -3)
            else :
                vertical.setValue(vertical.value() +3)
        except Exception :
            traceback.print_exc()


    # 鼠标按下事件
    def mousePressEvent(self, e: QMouseEvent) :
        try :
            if e.button() == Qt.LeftButton :
                self._isTracking = True
                self._startPos = QPoint(e.x(), e.y())
                self.setCursor(Qt.ClosedHandCursor)
        except Exception:
            traceback.print_exc()


    # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent):
        try :
            if e.button() == Qt.LeftButton :
                self._isTracking = False
                self._startPos = None
                self._endPos = None
                self.setCursor(Qt.OpenHandCursor)

        except Exception:
            traceback.print_exc()


# 自定义TextBlock的按钮
class CustomTextBlockButton(QPushButton) :

    move_signal = pyqtSignal(QPushButton)
    click_signal = pyqtSignal(QPushButton)

    def __init__(self, text) :
        super().__init__(text)
        self._move = False
        self._isTracking = False
        self._startPos = None
        self._endPos = None


    # 参数初始化
    def initConfig(self, text_block, trans, rect, index, original_image_path, ipt_image_path, rdr_image_path) :

        self.trans = trans
        self.text_block = text_block
        self.rect = rect
        self.index = index
        self.original_image_path = original_image_path
        self.ipt_image_path = ipt_image_path
        self.rdr_image_path = rdr_image_path

        # 文本块信息
        self.original = ""
        for text in text_block["texts"]:
            self.original += text
        # 文字颜色
        self.font_color = text_block["foreground_color"]
        self.bg_color = text_block["background_color"]


    # 鼠标移动事件
    def mouseMoveEvent(self, e: QMouseEvent) :
        try :
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)
            self._move = True
        except Exception :
            traceback.print_exc()


    # 鼠标按下事件
    def mousePressEvent(self, e: QMouseEvent) :
        try :
            if e.button() == Qt.LeftButton :
                self._isTracking = True
                self._startPos = QPoint(e.x(), e.y())
        except Exception :
            traceback.print_exc()


    # 鼠标松开事件
    def mouseReleaseEvent(self, e: QMouseEvent) :
        try :
            if e.button() == Qt.LeftButton :
                if self._move :
                    # 移动事件
                    self.move_signal.emit(self)
                else :
                    # 点击事件
                    self.click_signal.emit(self)
                self._isTracking = False
                self._startPos = None
                self._endPos = None
                self._move = False

        except Exception :
            traceback.print_exc()


# 高级设置界面
class Setting(QWidget) :

    def __init__(self, object) :

        super(Setting, self).__init__()
        self.object = object
        self.rate = object.yaml["screen_scale_rate"]
        self.logger = object.logger
        self.color_1 = "#595959"  # 灰色
        self.color_2 = "#5B8FF9"  # 蓝色
        self.detect_scale = self.object.config.get("mangaDetectScale", 1)
        self.ui()


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.window_width = int(500*self.rate)
        self.window_height = int(300*self.rate)
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("图片翻译-高级设置")
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("font: 10pt '华康方圆体W7';")

        # 渲染缩放比例标签
        label = QLabel(self)
        label.setText("渲染缩放比例: ")
        self.customSetGeometry(label, 20, 20, 500, 20)
        # 渲染缩放比例滑块
        self.detect_scale_slider = QSlider(self)
        self.customSetGeometry(self.detect_scale_slider, 120, 20, 280, 25)
        self.detect_scale_slider.setRange(1, 4)
        self.detect_scale_slider.setSingleStep(1)
        self.detect_scale_slider.setOrientation(Qt.Horizontal)
        self.detect_scale_slider.setValue(self.detect_scale)
        self.detect_scale_slider.valueChanged.connect(self.changeDetectScale)
        self.detect_scale_slider.installEventFilter(self)
        self.detect_scale_slider.setCursor(ui.static.icon.SELECT_CURSOR)
        # 设置字体
        self.detect_scale_slider.setStyleSheet("QSlider:groove:horizontal { height: %spx;"
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
                                              %(8.66*self.rate, 4*self.rate, 13.33*self.rate, 13.33*self.rate,
                                                33.33*self.rate, 33.33*self.rate, -13.33*self.rate, -13.33*self.rate,
                                                -13.33*self.rate, -13.33*self.rate, 8.66*self.rate, 4*self.rate,
                                                10*self.rate, self.color_2))
        # 渲染缩放比例滑块数值标签
        self.detect_scale_slider_label = QLabel(self)
        self.customSetGeometry(self.detect_scale_slider_label, 400, 20, 30, 20)
        self.detect_scale_slider_label.setText("x%s"%self.detect_scale)
        # 渲染缩放比例?号图标
        button = QPushButton(qtawesome.icon("fa.question-circle", color=self.color_2), "", self)
        self.customSetIconSize(button, 20, 20)
        self.customSetGeometry(button, 430, 20, 20, 20)
        button.clicked.connect(lambda: self.showDesc("detect_scale"))
        button.setCursor(ui.static.icon.QUESTION_CURSOR)
        button.setStyleSheet("QPushButton { background: transparent;}"
                             "QPushButton:hover { background-color: #83AAF9; }"
                             "QPushButton:pressed { background-color: #4480F9; padding-left: 3px;padding-top: 3px; }")


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))

    # 根据分辨率定义图标位置尺寸
    def customSetIconSize(self, object, w, h) :

        object.setIconSize(QSize(int(w * self.rate), int(h * self.rate)))


    # 改变渲染缩放比例
    def changeDetectScale(self) :

        self.detect_scale = self.detect_scale_slider.value()
        self.object.config["mangaDetectScale"] = self.detect_scale
        self.detect_scale_slider_label.setText("x{}".format(self.detect_scale))


    # 说明窗口
    def showDesc(self, message_type) :

        self.desc_ui = ui.desc.Desc(self.object)
        # 文字缩放比例
        if message_type == "detect_scale" :
            self.desc_ui.setWindowTitle("文字缩放比例说明")
            self.desc_ui.desc_text.append("\n会对图片进行放大后再进行识别, 对于字体较小的图片可以调大此参数, 调大可能会增加文字识别耗时"
                                          "\n\n日文默认值为1, \n英文默认值为3")
        else :
            return

        self.desc_ui.show()


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.hide()
        self.object.manga_ui.show()

