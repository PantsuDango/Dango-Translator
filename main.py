# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from Init import MainInterface
from Settin import SettinInterface
from Range import WScreenShot
from API import message_thread
from ScreenRate import get_screen_rate

import json
from system_hotkey import SystemHotkey

import qtawesome
from traceback import print_exc


def change_horizontal(Init):

    with open('.\\config\\settin.json') as file:
        data = json.load(file)

    horizontal = (data["horizontal"]) / 100
    if horizontal == 0:
        horizontal = 0.01
    Init.translateText.setStyleSheet("border-width:0;\
                                          border-style:outset;\
                                          border-top:0px solid #e8f3f9;\
                                          color:white;\
                                          font-weight: bold;\
                                          background-color:rgba(62, 62, 62, %s)"
                                          %(horizontal))

    showHotKey = data["showHotKey"]
    showHotKeyValue1 = data["showHotKeyValue1"]
    showHotKeyValue2 = data["showHotKeyValue2"]
    if showHotKey == "True":
        try:
            Init.hk_start = SystemHotkey()
            Init.hk_start.register((showHotKeyValue1, showHotKeyValue2), callback=lambda x:Init.send_key_event("start"))
        except Exception:
                print_exc()

    Init.show()


def stopWarning_settin(Init, Settin):

    if Init.mode == True:
        with open('.\\config\\settin.json') as file:
            data = json.load(file)
            data["sign"] = 1
        with open('.\\config\\settin.json','w') as file:
            json.dump(data, file)
        Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))

    Init.close()
    Settin.tabWidget.setCurrentIndex(0)
    Settin.show()


def stopWarning_range(Init, Range):

    if Init.mode == True:
        with open('.\\config\\settin.json') as file:
            data = json.load(file)
            data["sign"] = 1
        with open('.\\config\\settin.json','w') as file:
            json.dump(data, file)
        Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
    
    Range.show()
    Init.show()


def stopWarning_Battery(Init, Settin):

    if Init.mode == True:
        with open('.\\config\\settin.json') as file:
            data = json.load(file)
            data["sign"] = 1
        with open('.\\config\\settin.json','w') as file:
            json.dump(data, file)
        Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
    
    Init.close()
    Settin.tabWidget.setCurrentIndex(4)
    Settin.show()


def main():
  
    message_thread(get_screen_rate)
    
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

    Init.BatteryButton.clicked.connect(lambda:stopWarning_Battery(Init, Settin))


    App.exit(App.exec_())

if __name__ == '__main__':
    
    main()