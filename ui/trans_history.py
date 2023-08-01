# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import fileinput
import re
import os

import ui.static.icon
import utils.message
import utils.sqlite


TRANS_FILE = "../翻译历史.txt"

# 翻译历史界面
class TransHistory(QWidget) :

    def __init__(self, object) :

        super(TransHistory, self).__init__()
        self.object = object
        self.getInitConfig()
        self.ui()


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面字体
        self.font_type = "微软雅黑"
        # 界面字体大小
        self.font_size = 12
        # 界面尺寸
        self.window_width = int(1000 * self.rate)
        self.window_height = int(700 * self.rate)
        # 最多显示的记录行数
        self.max_rows = 300


    def ui(self) :

        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # 窗口标题
        self.setWindowTitle("翻译历史(最多显示{}行)".format(self.max_rows))
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("font: %spt '%s';"%(self.font_size, self.font_type))

        # 表格
        self.table_widget = QTableWidget(self)
        self.customSetGeometry(self.table_widget, 0, 0, 1000, 700)
        self.table_widget.setCursor(ui.static.icon.EDIT_CURSOR)
        # 表格列数
        self.table_widget.setColumnCount(3)
        # 表格无边框
        self.table_widget.setFrameShape(QFrame.Box)
        # 表头信息
        self.table_widget.setHorizontalHeaderLabels(["翻译源", "原文", "译文"])
        # 不显示行号
        self.table_widget.verticalHeader().setVisible(False)
        # 表头不塌陷
        self.table_widget.horizontalHeader().setHighlightSections(False)
        # 表头属性
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setDefaultSectionSize(100*self.rate)
        self.table_widget.horizontalHeader().setStyleSheet("QHeaderView::section {background: transparent;}")
        # 表格铺满窗口
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # 单元格可复制
        self.table_widget.setSelectionMode(QTableWidget.ContiguousSelection)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 刷新表格数据
    def refreshTableData(self) :

        # 查询数据库
        rows = utils.sqlite.selectTranslationDBList(self.max_rows, self.object.logger)
        rows = list(reversed(rows))
        # 表格行数
        self.table_widget.setRowCount(len(rows))
        # 数据写入表格
        for i, row in enumerate(rows) :
            for j, v in enumerate(row[1:4]) :
                # 翻译源转换中文
                if j == 1 and v in utils.sqlite.TRANS_MAP_INVERSION :
                    v = utils.sqlite.TRANS_MAP_INVERSION[v]
                # 调换位置
                if j == 0 :
                    j = 1
                elif j == 1 :
                    j = 0
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignVCenter)
                self.table_widget.setItem(i, j, item)

        # 设置行高自适应内容
        for row in range(self.table_widget.rowCount()):
            self.table_widget.resizeRowToContents(row)


    # 窗口显示信号
    def showEvent(self, e) :

        self.refreshTableData()
        self.table_widget.verticalScrollBar().setValue(self.table_widget.verticalScrollBar().maximum())


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.close()
        self.object.translation_ui.show()
        if self.object.range_ui.show_sign == True :
            self.object.range_ui.show()