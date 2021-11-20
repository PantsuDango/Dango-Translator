from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

import utils.logger
import utils.config
import utils.screen_rate
import utils.check_font
import utils.thread

import ui.login
import ui.register
import ui.translation


import ui.filter
import ui.range
import ui.settin

import utils
import utils.check_font
from utils import http
import utils.screen_rate


class DangoTranslator() :

    # 配置初始化
    def __init__(self) :

        # 错误日志
        self.logger = utils.logger.setLog()
        # 本地配置
        self.yaml = utils.config.openConfig(self.logger)
        # 版本号
        self.yaml["version"] = "4.0"
        # 配置中心
        self.yaml["dict_info"] = utils.config.getDictInfo(self.yaml["dict_info_url"], self.logger)
        # 屏幕分辨率
        self.yaml["screen_scale_rate"] = utils.screen_rate.getScreenRate(self.logger)


    # 登录
    def login(self) :

        if not self.login_ui.login() :
            return

        # 检查邮箱
        #self.register_ui.createBindEmailThread()

        # 从云端获取配置信息
        self.config = utils.config.getDangoSettin(self)
        utils.config.configConvert(self)
        # 登录OCR服务获取token
        utils.thread.createThread(utils.http.loginDangoOCR, self)

        # 翻译界面
        self.translation_ui = ui.translation.Translation(self)
        # # 设置界面
        # self.settin_ui = ui.settin.Settin(self.config, self.logger, self.translation_ui)
        # # 屏蔽词界面
        # self.filter_ui = ui.filter.Filter(self.translation_ui)
        # 范围框界面
        # self.range_ui = ui.range.Range(self.yaml["range"]['X1'],
        #                                self.yaml["range"]['Y1'],
        #                                self.yaml["range"]['X2'],
        #                                self.yaml["range"]['Y2'],
        #                                self.yaml["screenScaleRate"],
        #                                self.translation_ui)

        self.login_ui.close()
        self.translation_ui.show()
        print(111111111111)

        # # 翻译界面设置页面按键信号
        # self.translation_ui.settin_button.clicked.connect(self.clickSettin)
        #
        # # 翻译界面按下退出键
        # self.translation_ui.quit_button.clicked.connect(self.range_ui.close)
        # self.translation_ui.quit_button.clicked.connect(self.translation_ui.quit)
        #
        # # 翻译界面屏蔽词按键信号
        # self.translation_ui.filter_word_button.clicked.connect(self.clickFilter)
        #
        # # 翻译界面选择范围键信号
        # self.translation_ui.range_button.clicked.connect(self.chooseRange)
        #
        # # 翻译界面充电按钮信号
        # self.translation_ui.battery_button.clicked.connect(self.clickBattery)
        #
        # # 范围快捷键
        # self.translation_ui.range_hotkey_sign.connect(self.chooseRange)


    # 按下充电键后做的事情
    def clickBattery(self) :

        # 如果处于自动模式下则暂停
        if self.translation_ui.translate_mode:
            self.translation_ui.stop_sign = True

        self.settin_ui.config = self.translation_ui.config
        self.translation_ui.unregisterHotKey()
        self.translation_ui.close()
        self.range_ui.close()
        self.settin_ui.tabWidget.setCurrentIndex(4)
        self.settin_ui.show()


    # 按下屏蔽词键后做的事情
    def clickFilter(self) :

        # 如果处于自动模式下则暂停
        if self.translation_ui.translate_mode :
            self.translation_ui.stop_sign = True

        self.filter_ui.refreshTable()
        self.filter_ui.show()


    # 按下设置键后做的事情
    def clickSettin(self) :

        # 如果处于自动模式下则暂停
        if self.translation_ui.translate_mode :
            self.translation_ui.stop_sign = True

        self.settin_ui.config = self.translation_ui.config
        self.translation_ui.unregisterHotKey()
        self.translation_ui.close()
        self.range_ui.close()
        self.settin_ui.show()


    # 进入范围框选
    def chooseRange(self) :

        # 如果处于自动模式下则暂停
        if self.translation_ui.translate_mode :
            self.translation_ui.stop_sign = True

        self.WScreenShot = ui.range.WScreenShot(self.translation_ui, self.range_ui)
        self.WScreenShot.show()
        self.translation_ui.show()


    # 主函数
    def main(self) :

        # 自适应高分辨率
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        app = QApplication(sys.argv)

        # 检查字体
        utils.check_font.checkFont(self.logger)

        # 登录界面
        self.login_ui = ui.login.Login(self)
        self.login_ui.show()
        self.login_ui.login_button.clicked.connect(self.login)

        # 注册页面
        self.register_ui = ui.register.Register(self)
        # 登录界面注册按键
        self.login_ui.register_button.clicked.connect(self.register_ui.clickRegister)
        # 登录界面忘记密码按键
        self.login_ui.forget_password_button.clicked.connect(self.register_ui.clickForgetPassword)

        app.exit(app.exec_())


if __name__ == "__main__" :

    app = DangoTranslator()
    app.main()