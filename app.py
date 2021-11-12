from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

import ui.login
import ui.translation
import ui.filter
import ui.range
import ui.settin

import utils
import utils.screen_rate


class DangoTranslator() :

    def __init__(self) :

        # 从配置文件获取配置信息
        self.config = utils.openConfig()


    # 登录
    def login(self) :

        if not self.Login.login() :
            return

        self.config["user"] = self.Login.user
        self.config["password"] = self.Login.password

        # 从云端获取配置信息
        self.config = utils.getSettin(self.config, self.logger)
        utils.saveConfig(self.config)

        # 翻译界面
        self.Translation = ui.translation.Translation(self.config, self.logger)
        # 设置界面
        self.Settin = ui.settin.Settin(self.config, self.logger, self.Translation)
        # 屏蔽词界面
        self.Filter = ui.filter.Filter(self.Translation)
        # 范围框界面
        self.Range = ui.range.Range(self.config["range"]['X1'],
                                    self.config["range"]['Y1'],
                                    self.config["range"]['X2'],
                                    self.config["range"]['Y2'],
                                    self.config["screenScaleRate"],
                                    self.Translation)
        self.Translation.range_window = self.Range

        self.Login.close()
        self.Translation.show()

        # 翻译界面设置页面按键信号
        self.Translation.settinButton.clicked.connect(self.clickSettin)

        # 翻译界面按下退出键
        self.Translation.quitButton.clicked.connect(self.Range.close)
        self.Translation.quitButton.clicked.connect(self.Translation.quit)

        # 翻译界面屏蔽词按键信号
        self.Translation.filterWordButton.clicked.connect(self.clickFilter)

        # 翻译界面选择范围键信号
        self.Translation.rangeButton.clicked.connect(self.chooseRange)

        # 翻译界面充电按钮信号
        self.Translation.batteryButton.clicked.connect(self.clickBattery)

        # 范围快捷键
        self.Translation.range_hotkey_sign.connect(self.chooseRange)


    # 按下充电键后做的事情
    def clickBattery(self) :

        # 如果处于自动模式下则暂停
        if self.Translation.translateMode:
            self.Translation.stop_sign = True

        self.Settin.config = self.Translation.config
        self.Translation.unregisterHotKey()
        self.Translation.close()
        self.Range.close()
        self.Settin.tabWidget.setCurrentIndex(4)
        self.Settin.show()


    # 按下屏蔽词键后做的事情
    def clickFilter(self) :

        # 如果处于自动模式下则暂停
        if self.Translation.translateMode:
            self.Translation.stop_sign = True

        self.Filter.refreshTable()
        self.Filter.show()


    # 按下设置键后做的事情
    def clickSettin(self) :

        # 如果处于自动模式下则暂停
        if self.Translation.translateMode:
            self.Translation.stop_sign = True

        self.Settin.config = self.Translation.config
        self.Translation.unregisterHotKey()
        self.Translation.close()
        self.Range.close()
        self.Settin.show()


    # 进入范围框选
    def chooseRange(self) :

        # 如果处于自动模式下则暂停
        if self.Translation.translateMode :
            self.Translation.stop_sign = True

        self.WScreenShot = ui.range.WScreenShot(self.Translation, self.Range)
        self.WScreenShot.show()
        self.Translation.show()


    def main(self) :

        # 记录日志
        self.logger = utils.setLog()

        # 获取屏幕分辨率
        self.config = utils.screen_rate.getScreenRate(self.config)

        # 自适应高分辨率
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        app = QApplication(sys.argv)

        # 检查字体
        utils.checkFont(self.logger)

        # 登录界面
        self.Login = ui.login.Login(self.config, self.logger)
        self.Login.show()
        self.Login.loginButton.clicked.connect(self.login)

        app.exit(app.exec_())


if __name__ == "__main__" :

    app = DangoTranslator()
    app.main()