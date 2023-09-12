# -*- coding: utf-8 -*-
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import fileinput
import re
import os
import traceback
import pyperclip

import ui.static.icon
import utils.message
import utils.sqlite
import utils.thread


TRANS_FILE = "../翻译历史.txt"


# 翻译历史界面
class TransHistory(QWidget) :

    def __init__(self, object) :

        super(TransHistory, self).__init__()
        self.object = object
        self.logger = object.logger
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
        # 颜色
        self.blue_color = "#5B8FF9"
        self.gray_color = "#DCDCDC"
        # 界面尺寸
        self.window_width = 1000
        self.window_height = 790
        # 最多显示的记录行数
        self.max_rows = 300
        # 总表数据
        self.trans_data_total = 0
        # 当前页码
        self.page_now = 1
        # 总页码
        self.all_page = 1


    def ui(self) :

        # 窗口尺寸
        self.resize(self.window_width*self.rate, self.window_height*self.rate)
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 鼠标样式
        self.setCursor(ui.static.icon.PIXMAP_CURSOR)
        # 设置字体
        self.setStyleSheet("QWidget {font: %spt '%s';}"
                           "QPushButton {font: %spt '华康方圆体W7'; background: %s; border-radius: %spx; color: rgb(255, 255, 255);}"
                           "QPushButton:hover {background-color: #83AAF9;}"
                           "QPushButton:pressed {background-color: #4480F9; padding-left: 3px; padding-top: 3px;}"
                           "QLabel {font: %spt '华康方圆体W7';}"
                           %(self.font_size, self.font_type, self.font_size, self.blue_color, 6.66*self.rate, self.font_type))

        # 原文搜索框标签
        self.src_search_label = QLabel(self)
        self.src_search_label.setText("按原文模糊查询:")
        # 原文搜索框
        self.src_search_text = QLineEdit(self)
        self.src_search_text.setPlaceholderText("请输入要查询的原文")
        self.src_search_text.textChanged.connect(self.searchTransData)

        # 译文搜索框标签
        self.tgt_search_label = QLabel(self)
        self.tgt_search_label.setText("按译文模糊查询:")
        # 译文搜索框
        self.tgt_search_text = QLineEdit(self)
        self.tgt_search_text.setPlaceholderText("请输入要查询的译文")
        self.tgt_search_text.textChanged.connect(self.searchTransData)

        # 表格
        self.table_widget = QTableWidget(self)
        self.table_widget.setCursor(ui.static.icon.EDIT_CURSOR)
        # 表格列数
        self.table_widget.setColumnCount(4)
        # 表格无边框
        self.table_widget.setFrameShape(QFrame.Box)
        # 表头信息
        self.table_widget.setHorizontalHeaderLabels(["序号", "翻译源", "原文", "译文"])
        # 不显示行号
        self.table_widget.verticalHeader().setVisible(False)
        # 表头不塌陷
        self.table_widget.horizontalHeader().setHighlightSections(False)
        # 表头属性
        self.table_widget.horizontalHeader().setDefaultSectionSize(100*self.rate)
        self.table_widget.horizontalHeader().setStyleSheet("QHeaderView::section {font: 15pt '华康方圆体W7'; background: %s; color: rgb(255, 255, 255);}"%self.blue_color)
        # 表格铺满窗口
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # 单元格可复制
        self.table_widget.setSelectionMode(QTableWidget.ContiguousSelection)
        # 文本修改信号
        self.table_widget.cellChanged.connect(self.modifyTransData)
        # 右键菜单
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.showMenu)

        # 上一页按钮
        self.last_page_button = QPushButton(self)
        self.last_page_button.setText("<上一页")
        self.last_page_button.clicked.connect(lambda: self.paging("last"))

        # 页码输入框
        self.page_spinbox = QSpinBox(self)
        self.page_spinbox.setMinimum(1)
        self.page_spinbox.valueChanged.connect(lambda: self.paging(None))

        # 页码标签
        self.page_label = QLabel(self)

        # 下一页按钮
        self.next_page_button = QPushButton(self)
        self.next_page_button.setText("下一页>")
        self.next_page_button.clicked.connect(lambda: self.paging("next"))

        # 导出按钮
        self.output_button = QPushButton(self)
        self.output_button.setText("导出全部")
        self.output_button.clicked.connect(self.outputAllTansData)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h, w_rate=1, h_rate=1) :

        object.setGeometry(QRect(
            int(x * w_rate),
            int(y * w_rate),
            int(w * h_rate),
            int(h * h_rate))
        )


    # 刷新表格数据
    def refreshTableData(self) :

        # 清空表格
        self.table_widget.setRowCount(0)
        # 查询数据库
        offset = (self.page_now - 1) * self.max_rows
        src = self.src_search_text.text()
        tgt = self.tgt_search_text.text()
        rows = utils.sqlite.selectTranslationDBList(src, tgt, self.max_rows, offset, self.logger)
        # 表格行数
        self.table_widget.setRowCount(len(rows))
        # 数据写入表格
        for i, row in enumerate(rows) :
            for j, v in enumerate(row) :
                if j == 0 :
                    v = str(v)
                elif j == 1 and v in utils.sqlite.TRANS_MAP_INVERSION :
                    # 翻译源转换中文
                    v = utils.sqlite.TRANS_MAP_INVERSION[v]
                item = QTableWidgetItem(v)
                item.setTextAlignment(Qt.AlignVCenter)
                self.table_widget.setItem(i, j, item)
                # 翻译源和原文不可编辑
                if j < 2 :
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    item.setFlags(item.flags() | Qt.ItemIsEnabled)

        # 设置行高自适应内容
        for row in range(self.table_widget.rowCount()) :
            self.table_widget.resizeRowToContents(row)


    # 导出所有翻译数据
    def outputAllTansData(self) :

        # 选择指定位置
        options = QFileDialog.Options()
        dialog = QFileDialog()
        try :
            # 默认桌面
            dialog.setDirectory(QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[0])
        except Exception :
            # 默认用户根目录
            dialog.setDirectory(QDir.homePath())
        folder_path = dialog.getExistingDirectory(self, "选择要导出的位置", "", options=options)
        if not os.path.exists(folder_path):
            return utils.message.MessageBox("导出失败", "无效的目录      ")

        # 查询数据库导出
        file_path = os.path.join(folder_path, "团子翻译历史.csv")
        err = utils.sqlite.outputTranslationDB(file_path, self.logger)
        if err :
            if os.path.exists(file_path) :
                os.remove(file_path)
            return utils.message.MessageBox("导出翻译历史", "导出失败:\n%s"%err, self.rate)

        os.startfile(folder_path)


    # 窗口显示信号
    def showEvent(self, e) :

        # 刷新界面数据
        self.refreshTable()


    # 刷新页码
    def refreshPageLabel(self) :

        self.all_page = self.trans_data_total // self.max_rows + 1
        self.page_label.setText("/{}页".format(self.all_page))
        if self.page_now != self.page_spinbox.value() :
            self.page_spinbox.setValue(self.page_now)
        self.page_spinbox.setMaximum(self.all_page)


    # 翻页
    def paging(self, sign) :

        if sign == "next" :
            self.page_now += 1
        elif sign == "last" :
            self.page_now -= 1
        else :
            self.page_now = self.page_spinbox.value()

        if self.page_now > self.all_page :
            self.page_now = self.all_page
        elif self.page_now < 1 :
            self.page_now = 1

        # 刷新界面数据
        self.refreshTable()


    # 根据原文搜索翻译数据
    def searchTransData(self) :

        # 刷新页码
        self.page_now = 1
        # 刷新界面数据
        self.refreshTable()


    # 刷新界面数据
    def refreshTable(self) :

        # 刷新数据总量
        src = self.src_search_text.text()
        tgt = self.tgt_search_text.text()
        self.trans_data_total = utils.sqlite.selectTranslationDBTotal(src, tgt, self.logger)
        self.setWindowTitle("翻译历史(每页最多显示{}行, 数据总量{}行, 排序方式-按时间倒序, 双击原文和译文可编辑修改, 右键可复制和删除)".format(self.max_rows, self.trans_data_total))

        # 刷新页码
        self.refreshPageLabel()
        # 刷新数据总数
        self.refreshTableData()


    # 文本编辑信号
    def modifyTransData(self, row, col) :

        try :
            item = self.table_widget.item(row, col)
            if (col == 2 or col == 3) and item in self.table_widget.selectedItems() :
                id = int(self.table_widget.item(row, 0).text())
                if col == 2 :
                    # 修改原文
                    err = utils.sqlite.modifyTranslationDBSrc(id, item.text(), self.logger)
                elif col == 3 :
                    # 修改译文
                    err = utils.sqlite.modifyTranslationDBTgt(id, item.text(), self.logger)
                else :
                    return
                if err :
                    utils.message.MessageBox("修改翻译历史", "修改失败:\n{}".format(err))
                else :
                    utils.message.MessageBox("修改翻译历史", "修改成功")
        except Exception :
            err = traceback.format_exc()
            self.logger.error(err)
            utils.message.MessageBox("修改翻译历史", "修改失败:\n{}".format(err))


    # 表格右键菜单
    def showMenu(self, pos) :

        item = self.table_widget.itemAt(pos)
        if item is not None :
            menu = QMenu(self)
            menu.setStyleSheet("QMenu {color: #5B8FF9; background-color: #FFFFFF; font: 12pt '华康方圆体W7';}"
                               "QMenu::item:selected:enabled {background: #E5F5FF;}"
                               "QMenu::item:checked {background: #E5F5FF;}")
            # 添加菜单项
            copy_action = menu.addAction("复制")
            copy_action.triggered.connect(lambda: pyperclip.copy(item.text()))
            delete_action = menu.addAction("删除")
            delete_action.triggered.connect(lambda: self.deleteTransData(item))
            # 显示菜单
            cursorPos = QCursor.pos()
            menu.exec_(cursorPos)


    # 删除翻译数据
    def deleteTransData(self, item) :

        try :
            row = self.table_widget.row(item)
            id = int(self.table_widget.item(row, 0).text())
            err = utils.sqlite.deleteTranslationDBByID(id, self.logger)
            if err :
                utils.message.MessageBox("删除翻译历史", "删除失败:\n{}".format(err))
            else :
                utils.message.MessageBox("删除翻译历史", "删除成功")
        except Exception :
            err = traceback.format_exc()
            self.logger.error(err)
            utils.message.MessageBox("删除翻译历史", "删除失败:\n{}".format(err))

        self.refreshTable()


    # 窗口尺寸变化信号
    def resizeEvent(self, event) :

        w = event.size().width()
        h = event.size().height()
        w_rate = w / self.window_width
        h_rate = h / self.window_height

        # 原文搜索框标签
        self.customSetGeometry(self.src_search_label, 10, 0, 140, 30, w_rate, h_rate)
        # 原文搜索框
        self.src_search_text.setGeometry(
            self.src_search_label.x() + self.src_search_label.width(), 0,
            w-20*w_rate-self.src_search_label.width(), self.src_search_label.height()
        )
        # 译文搜索框标签
        self.tgt_search_label.setGeometry(
            self.src_search_label.x(), self.src_search_label.height(),
            self.src_search_label.width(), self.src_search_label.height()
        )
        # 译文搜索框
        self.tgt_search_text.setGeometry(
            self.src_search_text.x(), self.src_search_text.height(),
            self.src_search_text.width(), self.src_search_text.height()
        )
        # 表格
        self.table_widget.setGeometry(
            0, self.tgt_search_text.y() + self.tgt_search_text.height(),
            w, h-self.src_search_label.height()*3
        )
        # 导出按钮
        self.output_button.setGeometry(
            w-100*w_rate, self.table_widget.y()+self.table_widget.height(),
            100*w_rate, self.src_search_text.height()
        )
        # 上一页按钮
        self.last_page_button.setGeometry(
            325*w_rate,  self.output_button.y(),
            self.output_button.width(),  self.output_button.height()
        )
        # 页码输入框
        self.page_spinbox.setGeometry(
            self.last_page_button.x()+self.last_page_button.width()+25*w_rate, self.last_page_button.y(),
            self.last_page_button.width()//2, self.last_page_button.height()
        )
        # 页码标签
        self.page_label.setGeometry(
            self.page_spinbox.x()+self.page_spinbox.width(), self.page_spinbox.y(),
            self.last_page_button.width(), self.last_page_button.height()
        )
        # 下一页按钮
        self.next_page_button.setGeometry(
            self.output_button.x()-self.last_page_button.x(), self.last_page_button.y(),
            self.last_page_button.width(), self.last_page_button.height()
        )


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.close()
        self.object.translation_ui.show()
        if self.object.range_ui.show_sign == True :
            self.object.range_ui.show()