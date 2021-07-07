# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import *
import requests
import json
import qtawesome
from traceback import print_exc

from Init import MainInterface
from Settin import SettinInterface
from Range import WScreenShot
from chooseRange import Range
from login import Login
from Dango import DangoUI
from API import MessageBox
from filterUI import FilterWord

from hotKey import pyhk
from threading import Thread

from ScreenRate import get_screen_rate
from playsound import playsound

import webbrowser


class Translater():

    # 打开配置文件
    def open_settin(self):

        with open('.\\config\\settin.json') as file:
            self.data = json.load(file)


    # 保存配置文件
    def save_settin(self):

        with open('.\\config\\settin.json','w') as file:
            json.dump(self.data, file)


    # 登录
    def sign_up(self):

        # 检查用户名和密码是否合法
        user = self.login.user_text.toPlainText()
        try :
            password = self.login.password_text.text()
        except Exception :
            print_exc()
        if user == "" :
            MessageBox('用户名不合法', '用户名不能为空！   ')
            return
        if password == "" :
            MessageBox('密码不合法', '密码不能为空！   ')
            return
        if ' ' in user or '\n' in user or '\t' in user :
            MessageBox('用户名不合法', '用户名含有不合法的字符！   ')
            return
        if ' ' in password or '\n' in password or '\t' in password:
            MessageBox('密码不合法', '密码含有不合法的字符！   ')
            return

        url = "http://120.24.146.175:3000/DangoTranslate/Login"
        formdata = json.dumps({
            "User": user,
            "Password": password
        })
        try :
            res = requests.post(url, data=formdata).json()
            result = res.get("Result", "")
            if result == "User dose not exist" :
                MessageBox('登录失败', '用户名不存在，请先注册哦！   ')
            elif result == "Password error":
                MessageBox('登录失败', '密码输错啦！   ')
            elif result == "User is black list":
                MessageBox('登录失败', '你已经被团子纳入黑名单了！   ')
            elif result == "OK":

                self.user = user
                self.password = password
                self.Login_success()

                # 保存账号密码
                self.open_settin()
                self.data["user"] = user
                self.data["password"] = password
                self.save_settin()

                self.login.close()
                self.Init.show()
                self.dango.show()
            else :
                MessageBox('登录失败', '请联系团子解决   ')
        except Exception as err:
            MessageBox('登录失败', '原因: %s   '%err)


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
            self.Range = WScreenShot(self.Init, self.chooseRange)  # 范围界面
            # 判断当前翻译运行状态，若为开始则切换为停止
            if self.Init.mode == True:
                self.open_settin()
                self.data["sign"] = 1  # 重置运行状态标志符
                self.save_settin()
                # 改变翻译键的图标为停止图标
                self.Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
    
            self.Range.show()  # 打开范围界面
            self.Init.show()  # 翻译界面会被顶掉，再次打开

            if not self.thread_hotKey.isAlive():
                self.thread_hotKey.start()
        
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

        self.Settin.tabWidget.setCurrentIndex(0)  # 预设设置页面的初始为第一栏
        self.Init.hide()
        self.Settin.show()  # 打开设置页面


    # 刷新主界面
    def updata_Init(self):

        self.Settin.save_settin(self.user, self.password)  # 保存设置
        self.open_settin()
    
        # 刷新翻译界面的背景透明度
        self.Init.horizontal = (self.data["horizontal"]) / 100
        if self.Init.horizontal == 0:
            self.Init.horizontal = 0.01
        self.Init.translateText.setStyleSheet("border-width:0;\
                                               border-style:outset;\
                                               border-top:0px solid #e8f3f9;\
                                               color:white;\
                                               font-weight: bold;\
                                               background-color:rgba(62, 62, 62, %s)"
                                               %(self.Init.horizontal))

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
        
        if not self.thread_hotKey.isAlive():
            self.thread_hotKey.start()
    

    # 进入充电界面
    def goto_Battery(self):

        # 判断当前翻译运行状态，若为开始则切换为停止
        if self.Init.mode == True:
            self.open_settin()
            self.data["sign"] = 1  # 重置运行状态标志符
            self.save_settin()
            # 改变翻译键的图标为停止图标
            self.Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))
    
        self.Settin.tabWidget.setCurrentIndex(4)  # 预设设置页面的初始为第五栏
        self.Init.hide()
        self.Settin.show()  # 打开设置页面


    # 退出程序
    def close(self):

        path = os.getcwd() + "\\config\\翻译历史.txt"
        MessageBox('团子的贴心小提示~', '翻译结果已自动保存至\n%s\n可自行定期清理'%path)
        self.hotKey.end()  # 关闭监控快捷键事件
        self.Init.close()  # 关闭翻译界面

        # 退出程序前保存设置
        self.open_settin()
        url = "http://120.24.146.175:3000/DangoTranslate/SaveSettin"
        formdata = json.dumps({
            "User": self.user,
            "Data": json.dumps(self.data)
        })
        try :
            requests.post(url, data=formdata).json()
        except Exception :
            print_exc()


    # 打开教程视频
    def open_tutorials(self):

        url = 'https://www.bilibili.com/video/BV1gp4y1Q7Ts?from=search&seid=2515920591076249883'
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except Exception:
            print_exc()


    def getSettin(self):

        url = "http://120.24.146.175:3000/DangoTranslate/GetSettin"
        formdata = json.dumps({"User": self.user,})

        try :
            res = requests.post(url, data=formdata).json()
            result = res.get("Result", "")
            if result == "User dose not exist" :
                MessageBox('同步失败', '该用户云端没有配置信息！   ')
            elif result != "":
                with open('.\\config\\settin.json', 'w') as file:
                    json.dump(json.loads(result), file)

                self.Settin.close()
                self.Settin = SettinInterface(self.screen_scale_rate)
                self.Settin.SaveButton.clicked.connect(self.updata_Init)
                self.Settin.CancelButton.clicked.connect(self.Settin.close)
                self.Settin.CancelButton.clicked.connect(self.Init.show)
                self.Settin.GetSettin_Button.clicked.connect(self.getSettin)
                self.Settin.show()

                MessageBox('同步成功', '同步成功啦！   ')
            else :
                MessageBox('同步失败', '请联系团子解决   ')
        except Exception as err:
            MessageBox('同步失败', '原因: %s   '%err)

    # 进入屏蔽词界面
    def goto_Filter(self):

        # 判断当前翻译运行状态，若为开始则切换为停止
        if self.Init.mode == True:
            self.open_settin()
            self.data["sign"] = 1  # 重置运行状态标志符
            self.save_settin()
            # 改变翻译键的图标为停止图标
            self.Init.StartButton.setIcon(qtawesome.icon('fa.play', color='white'))

        self.Filter.show()  # 打开设置页面


    # 登录成功后
    def Login_success(self):

        try :
            # 从云端获取配置信息
            url = "http://120.24.146.175:3000/DangoTranslate/GetSettin"
            formdata = json.dumps({"User": self.user, })
            try :
                res = requests.post(url, data=formdata).json()
                result = res.get("Result", "")
                if result == "User dose not exist":
                    pass
                elif result != "":
                    with open('.\\config\\settin.json', 'w') as file:
                        json.dump(json.loads(result), file)
            except Exception :
                pass

            # 界面初始化
            self.dango = DangoUI()
            self.Init = MainInterface(self.screen_scale_rate, self.user)  # 翻译界面
            self.Settin = SettinInterface(self.screen_scale_rate)  # 设置界面
            self.Filter = FilterWord(self.screen_scale_rate)  # 屏蔽词界面

            self.chooseRange = Range(self.data["range"]['X1'], self.data["range"]['Y1'], self.data["range"]['X2'],
                                     self.data["range"]['Y2'])

            self.set_hotKey()  # 设置快捷键

            # 监听快捷键事件加入子线程
            self.thread_hotKey = Thread(target=self.hotKey.start)
            self.thread_hotKey.setDaemon(True)
            self.thread_hotKey.start()

            # 点击设置键后执行的函数
            self.Init.SettinButton.clicked.connect(self.goto_settin)
            # 点击范围键后执行的函数
            self.Init.RangeButton.clicked.connect(self.goto_range)
            # 点击充电键后执行的函数
            self.Init.BatteryButton.clicked.connect(self.goto_Battery)
            # 点击退出键后执行的函数
            self.Init.QuitButton.clicked.connect(self.close)
            # 点击屏蔽键后执行的函数
            self.Init.FilterWordButton.clicked.connect(self.goto_Filter)
            self.Init.FilterWordButton.clicked.connect(self.Filter.update_table)
            # 点击设置页面的保存键后执行的函数
            self.Settin.SaveButton.clicked.connect(self.updata_Init)
            # 点击设置页面的退出键后执行的函数
            self.Settin.CancelButton.clicked.connect(self.Settin.close)
            self.Settin.CancelButton.clicked.connect(self.Init.show)
            self.Settin.GetSettin_Button.clicked.connect(self.getSettin)

        except Exception :
            print_exc()
            input()


    # 主循环
    def main(self):
    
        try :
            self.screen_scale_rate = get_screen_rate()

            self.open_settin()
            self.data["sign"] = 1  # 重置运行状态标志符
            self.save_settin()

            App = QApplication(sys.argv)

            self.login = Login(self.screen_scale_rate, self.data)
            self.login.show()
            self.login.login_Button.clicked.connect(self.sign_up)

            App.exit(App.exec_())

        except Exception :
            print_exc()
            input()


def start_music():

    def play():
        try:
            playsound('.\\config\\Dango.mp3')
        except Exception:
            print_exc()

    thread = Thread(target=play)
    thread.setDaemon(True)
    thread.start()


if __name__ == '__main__':
    
    start_music() # 程序启动音
    Dango = Translater()
    Dango.main()