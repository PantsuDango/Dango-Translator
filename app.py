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
        self.Filter = ui.filter.Filter(self.config)
        # 范围框界面
        self.Range = ui.range.Range(self.config["range"]['X1'],
                                    self.config["range"]['Y1'],
                                    self.config["range"]['X2'],
                                    self.config["range"]['Y2'],
                                    self.config["screenScaleRate"])

        self.Login.close()
        self.Translation.show()

        # 翻译界面屏蔽词按键信号
        self.Translation.settinButton.clicked.connect(self.Translation.close)
        self.Translation.settinButton.clicked.connect(self.Settin.show)

        # 翻译界面屏蔽词按键信号
        self.Translation.filterWordButton.clicked.connect(self.Filter.show)
        self.Translation.filterWordButton.clicked.connect(self.Filter.refreshTable)
        # 翻译界面选择范围键信号
        self.Translation.rangeButton.clicked.connect(self.chooseRange)


    # 进入范围框选
    def chooseRange(self) :

        # 关闭自动开关
        if self.Translation.translateMode :
            self.Translation.switchBtn.mousePressEvent(1)
            self.Translation.switchBtn.updateValue()

        self.WScreenShot = ui.range. WScreenShot(self.Translation, self.Range)
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