# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from Init import MainInterface
from Settin import SettinInterface
from Range import WScreenShot
from API import message_thread, message
import json
from system_hotkey import SystemHotkey


def change_horizontal(Init):

    with open('.\\config\\settin.json') as file:
        data = json.load(file)

    horizontal = (data["horizontal"]) / 100
    Init.translateText.setStyleSheet("border-width:0;border-style:outset;border-top:0px solid #e8f3f9;background-color:rgba(62, 62, 62, {}); color:#FF69B4".format(horizontal))
    
    translateMode = data["translateMode"]
    if translateMode == "auto":
        if data["sign"] % 2 == 0:
            Init.StartButton.setText("停止")
        else:
            Init.StartButton.setText("开始")
    else:
        Init.StartButton.setText("翻译")

    showHotKey = data["showHotKey"]
    showHotKeyValue = data["showHotKeyValue"]
    if showHotKey == "True":
            Init.hk_start = SystemHotkey()
            Init.hk_start.register(('alt', showHotKeyValue), callback=lambda x:Init.send_key_event("start"))

    Init.show()


def stopWarning_settin(Init, Settin):

    with open('.\\config\\settin.json') as file:
        data = json.load(file)

    if data["sign"] % 2 == 0:
        message_thread(message, "这是来自团子的警告", "不先停止自动模式，不许你点设置 (╬◣д◢)")
    else:
        Init.close()
        Settin.show()


def stopWarning_range(Init, Range):

    with open('.\\config\\settin.json') as file:
        data = json.load(file)

    if data["sign"] % 2 == 0:
        message_thread(message, "这是来自团子的警告", "不先停止自动模式，不许你点范围 (╬◣д◢)")
    else:
        Range.show()
        Init.show()


def main():
  
    with open('.\\config\\settin.json') as file:
        data = json.load(file)
    data["sign"] = 1
    with open('.\\config\\settin.json','w') as file:
        json.dump(data, file)

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    App = QApplication(sys.argv)

    Init = MainInterface()
    Settin = SettinInterface()
    Range = WScreenShot()
    Init.show()

    Init.SettinButton.clicked.connect(lambda:stopWarning_settin(Init, Settin))
    Init.RangeButton.clicked.connect(lambda:stopWarning_range(Init, Range))
    
    Settin.CancelButton.clicked.connect(Settin.close)
    Settin.CancelButton.clicked.connect(lambda:change_horizontal(Init))

    App.exit(App.exec_())

if __name__ == '__main__':
    
    main()