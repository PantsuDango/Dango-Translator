from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from traceback import format_exc
import sys
import os
import time

import utils.logger
import utils.config
import utils.screen_rate
import utils.check_font
import utils.thread
import utils.http
import utils.email
import utils.message
import utils.port
import utils.update

import ui.login
import ui.register
import ui.translation
import ui.filter
import ui.range
import ui.settin


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
        # 保存配置
        utils.config.saveConfig(self.yaml, self.logger)


    # 服务连接失败提示
    def serverClientFailMessage(self) :

        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        log_file_name = date + ".log"
        utils.message.MessageBox("连接服务器失败",
                                 "发生了意料之外的错误, 导致无法连接服务器\n"
                                 "请查阅日志文件并联系团子处理\n"
                                 "日志文件地址:\n"
                                 "%s"%os.path.join(os.path.abspath("../") , "logs", log_file_name), self.yaml["screen_scale_rate"])
        sys.exit()


    # 登录
    def login(self) :

        if not self.login_ui.login() :
            return

        # 从云端获取配置信息
        self.config = utils.config.getDangoSettin(self)
        utils.config.configConvert(self)
        # 登录OCR服务获取token
        utils.thread.createThread(utils.http.loginDangoOCR, self)

        # 翻译界面
        self.translation_ui = ui.translation.Translation(self)
        self.login_ui.close()
        self.translation_ui.show()

        # 设置界面
        self.settin_ui = ui.settin.Settin(self)
        # 翻译界面设置页面按键信号
        self.translation_ui.settin_button.clicked.connect(self.clickSettin)
        # 翻译界面充电按钮信号
        self.translation_ui.battery_button.clicked.connect(self.clickBattery)

        # 屏蔽词界面
        self.filter_ui = ui.filter.Filter(self)
        # 范围框界面
        self.range_ui = ui.range.Range(self)

        # 检查邮箱
        thread = utils.thread.createCheckBindEmailQThread(self)
        thread.signal.connect(self.register_ui.showBindEmailMessage)
        utils.thread.runQThread(thread)

        # 自动启动本地OCR
        utils.thread.createThread(self.autoOpenOfflineOCR)


    # 按下充电键后做的事情
    def clickBattery(self) :

        self.translation_ui.unregisterHotKey()
        self.translation_ui.close()
        self.range_ui.close()
        self.settin_ui.tab_widget.setCurrentIndex(4)
        self.settin_ui.show()


    # 按下设置键后做的事情
    def clickSettin(self) :

        self.translation_ui.unregisterHotKey()
        self.translation_ui.close()
        self.range_ui.close()
        self.settin_ui.show()


    # 自动打开本地OCR
    def autoOpenOfflineOCR(self) :

        if not self.config["offlineOCR"] :
            return
        if not utils.port.detectPort(self.yaml["port"]) :
            try :
                # 启动本地OCR
                os.startfile(self.yaml["ocr_cmd_path"])
            except Exception :
                self.logger.error(format_exc())


    # 初始化资源
    def InitLoadImage(self) :

        # 更新ocr源码文件
        ocr_src_file = self.yaml["dict_info"]["ocr_src_file"]
        utils.update.updateOCRSrcFile(ocr_src_file, self.logger)

        # 加载QQ群图片
        qq_group_url = self.yaml["dict_info"]["dango_qq_group"]
        utils.http.downloadFile(qq_group_url, "./config/other/交流群.png", self.logger)

        # 加载注册界面图片
        qq_group_url = self.yaml["dict_info"]["register_image_url"]
        utils.http.downloadFile(qq_group_url, "./config/other/register.gif", self.logger)

        # 加载登录界面图片
        login_image_url = self.yaml["dict_info"]["login_image_url"]
        utils.http.downloadFile(login_image_url, "./config/background/login.png", self.logger)

        # 加载设置界面图片
        settin_image_url = self.yaml["dict_info"]["settin_image_url"]
        utils.http.downloadFile(settin_image_url, "./config/background/settin.jpg", self.logger)

        # 加载屏蔽词界面图片
        settin_image_url = self.yaml["dict_info"]["settin_desc_image_url"]
        utils.http.downloadFile(settin_image_url, "./config/background/settin-desc.jpg", self.logger)


    # 检查是否是最新版本
    def showCheckVersionMessage(self) :

        message = self.yaml["dict_info"]["update_version_message"]
        text = ""
        text_list = message.split(r"\n")
        for index, val in enumerate(text_list) :
            if index+1 == len(text_list) :
                text += val
            else :
                text += val + "\n"
        utils.message.checkVersionMessageBox("检查版本更新",
                                             "%s     "%text)


    # 检查是否为测试版本
    def checkIsTestVersion(self) :

        if "Beta" in self.yaml["version"] and self.yaml["dict_info"]["test_version_switch"] != "1" :
            utils.message.MessageBox("此版本已停止服务",
                                     "目前您使用的是测试版本, 此版本已经停止更新      \n"
                                     "请下载正式版本使用, 下载地址:\n%s      "
                                     %self.yaml["dict_info"]["update_version"], self.yaml["screen_scale_rate"])
            sys.exit()

    # 主函数
    def main(self) :

        # 自适应高分辨率
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        app = QApplication(sys.argv)

        if not self.yaml["dict_info"] :
            self.serverClientFailMessage()

        # 检查是否为测试版本
        self.checkIsTestVersion()

        # 检查字体
        utils.check_font.checkFont(self.logger)

        # 检查版本更新线程
        thread = utils.thread.createCheckVersionQThread(self)
        thread.signal.connect(self.showCheckVersionMessage)
        utils.thread.runQThread(thread)

        # 初始化图片资源
        utils.thread.createThread(self.InitLoadImage)

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