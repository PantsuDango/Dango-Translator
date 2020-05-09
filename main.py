# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from Init import MainInterface
from Settin import SettinInterface
from Range import WScreenShot

import json
import qtawesome
from traceback import print_exc

from hotKey import pyhk
from threading import Thread

from ScreenRate import get_screen_rate


class Translater():

    # 打开配置文件
    def open_settin(self):

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)


    # 保存配置文件
    def save_settin(self):

        with open('.\\config\\settin.json','w') as file:
            json.dump(self.data, file)


    # 设置快捷键
    def set_hotKey(self):

        try:
            self.hotKey = pyhk()
            self.id_translate = False  # 翻译快捷键预设
            self.id_range = False  # 范围快捷键预设

            # 是否启用翻译键快捷键
            if self.data["showHotKey1"] == "True":
                self.id_translate = self.hotKey.addHotkey([self.data["showHotKeyValue1"]], self.Init.start_login)
            # 是否截图键快捷键
            if self.data["showHotKey2"] == "True":
                self.id_range = self.hotKey.addHotkey([self.data["showHotKeyValue2"]], self.goto_range)

        except Exception:
            print_exc()


    # 进入范围选取
    def goto_range(self):

        try:
            # 判断当前翻译运行状态，若为开始则切换为停止
            if self.Init.mode == True:
                self.open_settin()
                self.data["sign"] = 1  # 重置运行状态标志符
                self.save_settin()
                # 改变翻译键的图标为停止图标
                self.Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
    
            self.Range.show()  # 打开范围界面
            self.Init.show()  # 翻译界面会被顶掉，再次打开
        except Exception:
            print_exc()


    # 进入设置页面
    def goto_settin(self):

        # 判断当前翻译运行状态，若为开始则切换为停止
        if self.Init.mode == True:
            self.open_settin()
            self.data["sign"] = 1  # 重置运行状态标志符
            self.save_settin()
            # 改变翻译键的图标为停止图标
            self.Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))

        #self.Init.close()  # 关闭翻译界面
        self.Settin.tabWidget.setCurrentIndex(0)  # 预设设置页面的初始为第一栏
        self.Settin.show()  # 打开设置页面


    # 刷新主界面
    def updata_Init(self):

        #self.Settin.close()  # 关闭设置页面
        self.Settin.save_settin()  # 保存设置
        self.open_settin()
    
        # 刷新翻译界面的背景透明度
        horizontal = (self.data["horizontal"]) / 100
        if horizontal == 0:
            horizontal = 0.01
        self.Init.translateText.setStyleSheet("border-width:0;\
                                               border-style:outset;\
                                               border-top:0px solid #e8f3f9;\
                                               color:white;\
                                               font-weight: bold;\
                                               background-color:rgba(62, 62, 62, %s)"
                                               %(horizontal))

        # 是否注销翻译键快捷键
        if self.id_translate:
            self.hotKey.removeHotkey(id=self.id_translate)
        # 是否注销范围键快捷键
        if self.id_range:
            self.hotKey.removeHotkey(id=self.id_range)
        # 是否启用翻译键快捷键
        if self.data["showHotKey1"] == "True":
            self.id_translate = self.hotKey.addHotkey([self.data["showHotKeyValue1"]], self.Init.start_login)
        # 是否截图键快捷键
        if self.data["showHotKey2"] == "True":
            self.id_range = self.hotKey.addHotkey([self.data["showHotKeyValue2"]], self.goto_range)
    
        #self.Init.show()  # 打开翻译界面


    # 进入充电界面
    def goto_Battery(self):

        # 判断当前翻译运行状态，若为开始则切换为停止
        if self.Init.mode == True:
            self.open_settin()
            self.data["sign"] = 1  # 重置运行状态标志符
            self.save_settin()
            # 改变翻译键的图标为停止图标
            self.Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
    
        self.Init.close()  # 关闭翻译界面
        self.Settin.tabWidget.setCurrentIndex(4)  # 预设设置页面的初始为第五栏
        self.Settin.show()  # 打开设置页面


    # 退出程序
    def close(self):

        self.hotKey.end()  # 关闭监控快捷键事件
        self.Init.close()  # 关闭翻译界面


    # 主循环
    def main(self):
    
        screen_scale_rate = get_screen_rate()

        self.open_settin()
        self.data["sign"] = 1  # 重置运行状态标志符
        self.save_settin()

        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        App = QApplication(sys.argv)

        self.Init = MainInterface(screen_scale_rate)  # 翻译界面
        self.Settin = SettinInterface(screen_scale_rate)  # 设置界面
        self.Range = WScreenShot()  # 范围界面
        self.Init.show()
        self.set_hotKey()  # 设置快捷键

        # 监听快捷键事件加入子线程
        thread_hotKey = Thread(target=self.hotKey.start)
        thread_hotKey.setDaemon(True)
        thread_hotKey.start()

        # 点击设置键后执行的函数
        self.Init.SettinButton.clicked.connect(self.goto_settin)
        # 点击范围键后执行的函数
        self.Init.RangeButton.clicked.connect(self.goto_range)
        # 点击充电键后执行的函数
        self.Init.BatteryButton.clicked.connect(self.goto_Battery)
        # 点击退出键后执行的函数
        self.Init.QuitButton.clicked.connect(self.close)
        
        # 点击设置页面的保存键后执行的函数
        self.Settin.SaveButton.clicked.connect(self.updata_Init)
        # 点击设置页面的退出键后执行的函数
        self.Settin.CancelButton.clicked.connect(self.Settin.close)

        App.exit(App.exec_())
        self.hotKey.end()


if __name__ == '__main__':
    
    Dango = Translater()
    Dango.main()