from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import json



class FilterWord(QWidget) :

    def __init__(self, screen_scale_rate) :

        super(FilterWord, self).__init__()
        self.rate = screen_scale_rate  # 屏幕缩放比例
        self.ui()


    def ui(self) :

        self.resize(230*self.rate, 300*self.rate)
        self.setMinimumSize(QSize(230*self.rate, 300*self.rate))
        self.setMaximumSize(QSize(230*self.rate, 300*self.rate))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("屏蔽词设置")

        # 窗口图标
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("./config/图标.ico"), QIcon.Normal, QIcon.On)
        self.setWindowIcon(self.icon)

        # 鼠标样式
        self.pixmap = QPixmap('.\config\光标.png')
        self.cursor = QCursor(self.pixmap, 0, 0)
        self.setCursor(self.cursor)

        self.setStyleSheet("font: 10pt \"华康方圆体W7\";")

        image_label = QLabel(self)
        image_label.setGeometry(QRect(0, 0, 230*self.rate, 300*self.rate))
        image_label.setStyleSheet("border-image: url(./config/Background100.jpg);")

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(0, 0, 230*self.rate, 270*self.rate)
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
        self.AddButton.setGeometry(QRect(0, 270*self.rate, 115*self.rate, 30*self.rate))
        self.AddButton.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        self.AddButton.setText("添加")
        self.AddButton.clicked.connect(self.addFilter)

        # 添加屏蔽词
        self.DeleteButton = QPushButton(self)
        self.DeleteButton.setGeometry(QRect(115*self.rate, 270*self.rate, 115*self.rate, 30*self.rate))
        self.DeleteButton.setStyleSheet("background: rgba(255, 255, 255, 0.4);")
        self.DeleteButton.setText("删除")
        self.DeleteButton.clicked.connect(self.deleteFilter)


    # 打开配置文件
    def open_settin(self) :

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)


    # 保存配置文件
    def save_settin(self):

        with open('.\\config\\settin.json', 'w') as file:
            json.dump(self.data, file)


    # 添加一行
    def addFilter(self) :

        try :
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)

            for x in range(2) :
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(row, x, item)

            self.updateTable()
        except Exception :
            import traceback
            traceback.print_exc()


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

        self.open_settin()
        self.data["filter"] = table
        self.save_settin()


    # 当表格的数据发生改变时
    def ifItemChanged(self) :

        self.tableWidget.viewport().update()
        # 如果数据没变就跳过
        select_item = self.tableWidget.selectedItems()
        if len(select_item) == 0 :
            return

        self.updateTable()


    # 更新表格信息
    def update_table(self) :

        self.open_settin()

        data = self.data.get("filter", [])
        self.tableWidget.setRowCount(len(data))

        for i in range(len(data)) :
            for j in range(2):
                item = QTableWidgetItem("%s" % data[i][j])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)