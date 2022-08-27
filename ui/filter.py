from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import utils.thread


LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_PATH = "./config/icon/pixmap.png"
BG_IMAGE_PATH = "./config/background/login.png"
PIXMAP2_PATH = "./config/icon/pixmap2.png"


class Filter(QWidget) :

    def __init__(self, object) :

        super(Filter, self).__init__()
        self.object = object
        self.getInitConfig()
        self.ui()
        utils.thread.createThread(self.refreshTable)


    def ui(self) :

        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("屏蔽词设置")

        # 窗口图标
        icon = QIcon()
        icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        # 鼠标样式
        pixmap = QPixmap(PIXMAP_PATH)
        pixmap = pixmap.scaled(int(20 * self.rate),
                               int(20 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        # 鼠标选中状态图标
        select_pixmap = QPixmap(PIXMAP2_PATH)
        select_pixmap = select_pixmap.scaled(int(20 * self.rate),
                                             int(20 * self.rate),
                                             Qt.KeepAspectRatio,
                                             Qt.SmoothTransformation)
        select_pixmap = QCursor(select_pixmap, 0, 0)

        # 设置字体
        font = QFont()
        font.setFamily(self.font_type)
        font.setPointSize(self.font_size)
        self.setFont(font)

        # 背景
        image_label = QLabel(self)
        self.customSetGeometry(image_label, 0, 0, 230, 300)
        image_label.setStyleSheet("border-image: url(%s);"%BG_IMAGE_PATH)  # 长宽比1.424

        # 表格
        self.table_widget = QTableWidget(self)
        self.customSetGeometry(self.table_widget, 0, 0, 230, 270)
        self.table_widget.setColumnCount(2)
        # 表格无边框
        self.table_widget.setFrameShape(QFrame.Box)
        # 表头信息
        self.table_widget.setHorizontalHeaderLabels(["屏蔽词", "替换词"])
        # 不显示行号
        self.table_widget.verticalHeader().setVisible(False)
        # 表头不塌陷
        self.table_widget.horizontalHeader().setHighlightSections(False)
        # 表头属性
        self.table_widget.horizontalHeader().setStyleSheet("QHeaderView::section {background: transparent;"
                                                           "font: %spt %s; }"%(self.font_size, self.font_type))
        # 表格铺满窗口
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 禁用水平滚动条
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 表格行和列的大小设为与内容相匹配
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        self.table_widget.setStyleSheet("background-color:rgba(255, 255, 255, 0.3);")
        # 信号
        self.table_widget.itemChanged.connect(self.ifItemChanged)

        # 添加屏蔽词
        self.add_button = QPushButton(self)
        self.customSetGeometry(self.add_button, 0, 270, 115, 30)
        self.add_button.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        self.add_button.setText("添加")
        self.add_button.clicked.connect(self.addFilter)
        self.add_button.setCursor(select_pixmap)

        # 添加屏蔽词
        self.delete_button = QPushButton(self)
        self.customSetGeometry(self.delete_button, 115, 270, 115, 30)
        self.delete_button.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        self.delete_button.setText("删除")
        self.delete_button.clicked.connect(self.deleteFilter)
        self.delete_button.setCursor(select_pixmap)


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.object.yaml["screen_scale_rate"]
        # 界面尺寸
        self.window_width = int(230 * self.rate)
        self.window_height = int(300 * self.rate)
        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 10


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate), int(w * self.rate),
                                 int(h * self.rate)))


    # 添加一行
    def addFilter(self) :

        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)

        for x in range(2) :
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget.setItem(row, x, item)

        self.updateTable()


    # 删除一行
    def deleteFilter(self) :

        row = self.table_widget.currentRow()
        self.table_widget.removeRow(row)

        self.updateTable()


    # 将屏蔽词更新保存设置
    def updateTable(self) :

        row = self.table_widget.rowCount()
        col = self.table_widget.columnCount()

        table = []
        for i in range(row):
            val = []
            for j in range(col):
                try :
                    val.append(self.table_widget.item(i, j).text())
                except Exception:
                    pass
            table.append(val)

        self.object.config["Filter"] = table


    # 当表格的数据发生改变时
    def ifItemChanged(self) :

        self.table_widget.viewport().update()
        # 如果数据没变就跳过
        select_item = self.table_widget.selectedItems()
        if len(select_item) == 0 :
            return

        self.updateTable()


    # 更新表格信息
    def refreshTable(self) :

        data = self.object.config.get("Filter", [])
        self.table_widget.setRowCount(len(data))

        for i in range(len(data)) :
            for j in range(2):
                item = QTableWidgetItem("%s" % data[i][j])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.table_widget.setItem(i, j, item)


    # 窗口关闭处理
    def closeEvent(self, event) :

        self.object.translation_ui.show()