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

        # 打开按钮
        button = QPushButton(self)
        self.customSetGeometry(button, 0, 0, 120, 35)
        button.setText(" 导入原图")
        button.setStyleSheet("QPushButton {background: transparent;}"
                             "QPushButton:hover {background-color: #83AAF9;}"
                             "QPushButton:pressed {background-color: #4480F9;}")
        button.setIcon(ui.static.icon.OPEN_ICON)
        button.clicked.connect(self.openImageFiles)

        # 工具栏横向分割线
        label = QLabel(self)
        self.customSetGeometry(label, 0, 35, self.window_width, 1)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 原图按钮
        self.old_images_button = QPushButton(self)
        self.customSetGeometry(self.old_images_button, 0, 35, 75, 25)
        self.old_images_button.setText("原图")
        self.old_images_button.setStyleSheet("QPushButton {background: transparent;}"
                             "QPushButton:hover {background-color: #83AAF9;}")
        self.old_images_button.clicked.connect(self.clickOldImages)

        # 原图按钮 和 译图按钮 竖向分割线
        label = QLabel(self)
        self.customSetGeometry(label, 74, 35, 1, 25)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 译图按钮
        self.new_images_button = QPushButton(self)
        self.customSetGeometry(self.new_images_button, 75, 35, 75, 25)
        self.new_images_button.setText("译图")
        self.new_images_button.setStyleSheet("QPushButton {background: transparent;}"
                             "QPushButton:hover {background-color: #83AAF9;}")
        self.new_images_button.clicked.connect(self.clickNewImages)

        # 译图右侧竖向分割线
        label = QLabel(self)
        self.customSetGeometry(label, 149, 35, 1, 25)
        label.setFrameShadow(QFrame.Raised)
        label.setFrameShape(QFrame.Box)
        label.setStyleSheet("border-width: 1px; "
                            "border-style: solid; "
                            "border-color: rgba(62, 62, 62, 0.2);")

        # 原图列表框
        self.old_image_widget = QListWidget(self)
        self.customSetGeometry(self.old_image_widget, 0, 60, 150, 610)
        self.old_image_widget.setIconSize(QSize(150 * self.rate, 150 * self.rate))
        self.old_image_widget.itemSelectionChanged.connect(self.loadOldImage)
        self.old_image_widget.hide()
        self.old_image_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.old_image_widget.customContextMenuRequested.connect(self.showListWidgetMenu)

        # 译图列表框
        self.new_image_widget = QListWidget(self)
        self.customSetGeometry(self.new_image_widget, 0, 60, 150, 610)
        self.new_image_widget.setIconSize(QSize(150 * self.rate, 150 * self.rate))
        #self.new_image_widget.itemSelectionChanged.connect(self.loadNewImage)
        self.new_image_widget.hide()

        # 图片大图展示
        self.show_image_scroll_area = QScrollArea(self)
        self.customSetGeometry(self.show_image_scroll_area, 150, 35, 850, 635)
        self.show_image_scroll_area.setWidgetResizable(True)
        #self.show_image_scroll_area.setFixedSize(600, 400)
        self.show_image_label = QLabel(self)
        self.show_image_scroll_area.setWidget(self.show_image_label)

        # 底部横向分割线
        label = QLabel(self)
        self.customSetGeometry(label, 150, 670, self.window_width, 1)
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
        # 原图路径字典
        self.old_image_path_list = []


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 设置列表框右键菜单
    def showListWidgetMenu(self, pos) :

        item = self.old_image_widget.itemAt(pos)
        if item is not None:
            menu = QMenu(self)
            # 添加菜单项
            delete_action = menu.addAction("移除")
            delete_action.triggered.connect(lambda: self.removeItemWidget(item))
            # 显示菜单
            cursorPos = QCursor.pos()
            menu.exec_(cursorPos)


    # 列表框右键菜单删除子项
    def removeItemWidget(self, item) :

        row = self.old_image_widget.indexFromItem(item).row()
        self.old_image_widget.takeItem(row)
        del self.old_image_path_list[row]


    # 打开图片文件列表
    def openImageFiles(self) :

        options = QFileDialog.Options()
        images, _ = QFileDialog.getOpenFileNames(self,
                                                 "选择要翻译的生肉漫画原图（可多选）",
                                                 "",
                                                 "图片类型(*.png *.jpg *.jpeg);;所有类型 (*)",
                                                 options=options)
        # 遍历文件列表，将每个文件路径添加到 QListWidget 中
        for image_path in images :
            if image_path in self.old_image_path_list :
                continue
            self.old_image_path_list.append(image_path)
            item = QListWidgetItem(image_path, self.old_image_widget)
            item.setIcon(QIcon(image_path))
            item.setText("")
            self.old_image_widget.addItem(item)


    # 点击原图按钮
    def clickOldImages(self) :

        self.old_image_widget.show()
        self.new_image_widget.hide()
        self.old_images_button.setStyleSheet("background-color: #83AAF9;")
        self.new_images_button.setStyleSheet("QPushButton {background: transparent;}"
                                             "QPushButton:hover {background-color: #83AAF9;}")


    # 点击译图按钮
    def clickNewImages(self) :

        self.old_image_widget.hide()
        self.new_image_widget.show()
        self.new_images_button.setStyleSheet("background-color: #83AAF9;")
        self.old_images_button.setStyleSheet("QPushButton {background: transparent;}"
                                             "QPushButton:hover {background-color: #83AAF9;}")


    # 展示图片大图
    def loadOldImage(self) :

        index = self.old_image_widget.currentIndex().row()
        if index < len(self.old_image_path_list) :
            with open(self.old_image_path_list[index], "rb") as file :
                image = QImage.fromData(file.read())
            pixmap = QPixmap.fromImage(image)
            self.show_image_label.setPixmap(pixmap)
            self.show_image_label.resize(pixmap.width(), pixmap.height())


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.hide()
        self.object.translation_ui.show()
        if self.object.range_ui.show_sign == True:
            self.object.range_ui.show()