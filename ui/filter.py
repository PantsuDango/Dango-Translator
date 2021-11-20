from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import utils


class Filter(QWidget) :

    def __init__(self, window) :

        super(Filter, self).__init__()

        self.window = window
        self.getInitConfig()

        self.ui()


    def ui(self) :

        self.resize(self.windowWidth, self.windowHeight)
        self.setMinimumSize(QSize(self.windowWidth, self.windowHeight))
        self.setMaximumSize(QSize(self.windowWidth, self.windowHeight))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("屏蔽词设置")

        # 窗口图标
        icon = QIcon()
        icon.addPixmap(QPixmap("./config/icon/logo.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        # 鼠标样式
        pixmap = QPixmap("./config/icon/pixmap.png")
        pixmap = pixmap.scaled(int(30 * self.rate),
                               int(34 * self.rate),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        cursor = QCursor(pixmap, 0, 0)
        self.setCursor(cursor)

        self.setStyleSheet('font: 10pt "华康方圆体W7";')

        image_label = QLabel(self)
        self.customSetGeometry(image_label, 0, 0, 230, 300)
        image_label.setStyleSheet("border-image: url(./config/background/login.png);")  # 长宽比1.424

        self.tableWidget = QTableWidget(self)
        self.customSetGeometry(self.tableWidget, 0, 0, 230, 270)
        self.tableWidget.setColumnCount(2)
        # 表格无边框
        self.tableWidget.setFrameShape(QFrame.Box)
        # 表头信息
        self.tableWidget.setHorizontalHeaderLabels(["屏蔽词", "替换词"])
        # 不显示行号
        self.tableWidget.verticalHeader().setVisible(False)
        # 表头不塌陷
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        # 表头属性
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{"
                                                          "background-color:rgba(255, 255, 255, 0);""};")
        # 表格铺满窗口
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 禁用水平滚动条
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 表格行和列的大小设为与内容相匹配
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setStyleSheet("background-color:rgba(255, 255, 255, 0.3);")
        # 信号
        self.tableWidget.itemChanged.connect(self.ifItemChanged)

        # 添加屏蔽词
        self.AddButton = QPushButton(self)
        self.customSetGeometry(self.AddButton, 0, 270, 115, 30)
        self.AddButton.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        self.AddButton.setText("添加")
        self.AddButton.clicked.connect(self.addFilter)

        # 添加屏蔽词
        self.DeleteButton = QPushButton(self)
        self.customSetGeometry(self.DeleteButton, 115, 270, 115, 30)
        self.DeleteButton.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        self.DeleteButton.setText("删除")
        self.DeleteButton.clicked.connect(self.deleteFilter)


    # 初始化配置
    def getInitConfig(self):

        # 界面缩放比例
        self.rate = self.window.config["screenScaleRate"]
        # 界面尺寸
        self.windowWidth = int(230 * self.rate)
        self.windowHeight = int(300 * self.rate)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h):

        object.setGeometry(QRect(x*self.rate, y*self.rate, w*self.rate, h*self.rate))


    # 添加一行
    def addFilter(self) :

        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        for x in range(2) :
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(row, x, item)

        self.updateTable()


    # 删除一行
    def deleteFilter(self) :

        row = self.tableWidget.currentRow()
        self.tableWidget.removeRow(row)

        self.updateTable()


    # 将屏蔽词更新保存设置
    def updateTable(self) :

        row = self.tableWidget.rowCount()
        col = self.tableWidget.columnCount()

        table = []
        for i in range(row):
            val = []
            for j in range(col):
                try :
                    val.append(self.tableWidget.item(i, j).text())
                except Exception:
                    pass
            table.append(val)

        self.window.config["Filter"] = table


    # 当表格的数据发生改变时
    def ifItemChanged(self) :

        self.tableWidget.viewport().update()
        # 如果数据没变就跳过
        select_item = self.tableWidget.selectedItems()
        if len(select_item) == 0 :
            return

        self.updateTable()


    # 更新表格信息
    def refreshTable(self) :

        data = self.window.config.get("Filter", [])
        self.tableWidget.setRowCount(len(data))

        for i in range(len(data)) :
            for j in range(2):
                item = QTableWidgetItem("%s" % data[i][j])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)


    # 窗口关闭处理
    def closeEvent(self, event) :

        # 如果是自动模式下, 则解除暂停
        if self.window.translate_mode :
            self.window.stop_sign = False