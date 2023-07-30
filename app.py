from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from traceback import format_exc
import base64
import sys
import os

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
import utils.hwnd
import utils.sqlite

import ui.login
import ui.register
import ui.translation
import ui.filter
import ui.range
import ui.settin
import ui.static.icon
import ui.trans_history
import ui.manga

import translator.update_chrome_driver
import translator.update_edge_driver
import translator.upload_firefox_driver


class DangoTranslator :

    # 配置初始化
    def __init__(self) :

        # 错误日志
        self.logger = utils.logger.setLog()
        # 本地配置
        self.yaml = utils.config.openConfig(self.logger)
        # 版本号
        self.yaml["version"] = "4.5.6"
        # 配置中心
        dict_info = utils.config.getDictInfo(self.yaml["dict_info_url"], self.logger)
        if dict_info :
            self.yaml["dict_info"] = dict_info
        # 屏幕分辨率
        self.yaml["screen_scale_rate"] = utils.screen_rate.getScreenRate(self.logger)
        # 保存配置
        utils.config.saveConfig(self.yaml, self.logger)
        # selenium引擎加载完成信号: 0-进行中, 1-成功, 2-失败
        self.chrome_driver_finish = 0
        self.firefox_driver_finish = 0
        self.edge_driver_finish = 0
        # 是否屏蔽绑定邮箱消息窗
        self.checkBindEmailSign = False
        # 记录截图坐标
        self.range = (0, 0, 0, 0)
        # 在线ocr可用性
        self.online_ocr_sign = False
        # 连接db
        utils.sqlite.connectTranslationDB(self.logger)
        # 同步旧翻译历史文件
        utils.thread.createThread(utils.sqlite.initTranslationDB, self)


    # 登录
    def login(self, auto_login=False) :

        # 是否为自动登录
        if auto_login :
            thread = utils.thread.createCheckAutoLoginQThread(self)
            thread.signal.connect(self.autoLoginCheck)
            utils.thread.runQThread(thread)
        else :
            if not self.login_ui.login() :
                return

        # 从本地获取配置信息
        self.config = utils.config.readCloudConfigFormLocal(self.logger)
        if not self.config :
            # 从云端获取配置信息
            self.config = utils.config.getDangoSettin(self)
        # 配置转换组包
        utils.config.configConvert(self)
        # 登录OCR服务获取token
        utils.thread.createThread(utils.http.loginDangoOCR, self)

        # 翻译界面
        self.translation_ui = ui.translation.Translation(self)
        if not auto_login:
            self.login_ui.close()
        self.translation_ui.show()
        # 设置界面
        self.settin_ui = ui.settin.Settin(self)
        # 翻译界面设置页面按键信号
        self.translation_ui.settin_button.clicked.connect(self.clickSettin)
        # 屏蔽词界面
        self.filter_ui = ui.filter.Filter(self)
        # 范围框界面
        self.range_ui = ui.range.Range(self)
        self.range_ui.show()
        # 多范围参数页面
        self.multi_range_ui = ui.range.MultiRange(self)
        self.translation_ui.multi_range_button.clicked.connect(self.clickMultiRange)
        # 翻译历史页面
        self.trans_history_ui = ui.trans_history.TransHistory(self)
        self.translation_ui.trans_history_button.clicked.connect(self.clickTransHistory)
        # 图片翻译页面
        self.manga_ui = ui.manga.Manga(self)
        self.translation_ui.manga_button.clicked.connect(self.clickManga)

        # 检查邮箱
        thread = utils.thread.createCheckBindEmailQThread(self)
        thread.signal.connect(self.register_ui.showBindEmailMessage)
        utils.thread.runQThread(thread)
        # 自动启动本地OCR
        utils.thread.createThread(self.autoOpenOfflineOCR)
        # 界面置顶
        self.hwndObj = utils.hwnd.WindowHwnd(self)
        if self.config["setTop"] :
            self.hwndObj.run()
        # 清理历史日志缓存
        utils.thread.createThread(utils.logger.clearLog)
        # 登录后自动打开图片翻译界面
        if self.yaml["auto_open_manga_use"] :
            self.clickManga()


    # 点击图片翻译键
    def clickManga(self) :

        self.translation_ui.hide()
        self.range_ui.hide()
        self.trans_history_ui.hide()
        self.manga_ui.show()


    # 点击翻译历史键
    def clickTransHistory(self) :

        self.trans_history_ui.show()
        self.translation_ui.hide()


    # 自动登录后检查
    def autoLoginCheck(self, message) :

        self.checkBindEmailSign = True
        utils.message.MessageBox("自动登录失败", message, self.yaml["screen_scale_rate"])

        # 如果自动登录失败就返回登录界面
        self.login_ui = ui.login.Login(self)
        self.login_ui.login_button.clicked.connect(self.login)
        # 登录界面注册按键
        self.login_ui.register_button.clicked.connect(self.register_ui.clickRegister)
        # 登录界面忘记密码按键
        self.login_ui.forget_password_button.clicked.connect(self.register_ui.clickForgetPassword)
        # 关闭已经打开的界面
        if self.translation_ui:
            self.translation_ui.close()
        if self.range_ui:
            self.range_ui.close()
        self.login_ui.show()


    # 按下多范围键后做的事情
    def clickMultiRange(self) :

        self.translation_ui.hide()
        self.multi_range_ui.show()
        self.range_ui.show()


    # 按下设置键后做的事情
    def clickSettin(self) :

        # 直接跳转到正在使用的ocr页签
        if self.settin_ui.online_ocr_use :
            self.settin_ui.ocr_tab_widget.setCurrentIndex(0)
        elif self.settin_ui.offline_ocr_use :
            self.settin_ui.ocr_tab_widget.setCurrentIndex(1)
        elif self.settin_ui.baidu_ocr_use :
            self.settin_ui.ocr_tab_widget.setCurrentIndex(2)

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
    def InitLoadFile(self) :

        # 更新谷歌浏览器引擎文件
        utils.thread.createThread(translator.update_chrome_driver.updateChromeDriver, self)
        # 更新Edge浏览器引擎文件
        utils.thread.createThread(translator.update_edge_driver.updateEdgeDriver, self)
        # 更新火狐浏览器引擎文件
        utils.thread.createThread(translator.upload_firefox_driver.updateFirefoxDriver, self)

        # 加载注册界面图片
        qq_group_url = self.yaml["dict_info"]["register_image_url"]
        utils.http.downloadFile(qq_group_url, "./config/background/register.gif", self.logger)
        # 加载设置界面图片
        settin_image_url = self.yaml["dict_info"]["settin_image_url"]
        utils.http.downloadFile(settin_image_url, "./config/background/settin.jpg", self.logger)
        # 加载测试ocr图片
        if not os.path.exists("./config/other/image.jpg") :
            test_image_url = self.yaml["dict_info"]["test_image"]
            utils.http.downloadFile(test_image_url, "./config/other/image.jpg", self.logger)


    # 启动图标
    def showSplash(self) :

        self.splash = QSplashScreen(ui.static.icon.APP_LOGO_SPLASH, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.splash.resize(int(250*self.yaml["screen_scale_rate"]), int(50*self.yaml["screen_scale_rate"]))
        self.splash.setStyleSheet("font: 15pt '华康方圆体W7';")
        self.splash.showMessage("团子翻译器启动中...", Qt.AlignVCenter | Qt.AlignRight)
        self.splash.show()
        QCoreApplication.processEvents()


    # 主函数
    def main(self) :

        # 自适应高分辨率
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        app = QApplication(sys.argv)
        # 加载静态资源
        ui.static.icon.initIcon(self.yaml["screen_scale_rate"])
        # 连接配置中心
        if not self.yaml.get("dict_info", {}) :
            utils.message.serverClientFailMessage(self)
        # 更新缺失的运行库
        utils.thread.createThread(utils.update.updatePilFile(self))
        # 更新自动更新程序
        utils.thread.createThread(utils.update.updateAutoUpdateFile(self))
        # 更新图片翻译字体
        utils.thread.createThread(utils.update.updateManFontFile(self))
        # 启动图标
        self.showSplash()
        # 检查是否为测试版本
        utils.message.checkIsTestVersion(self)
        # 检查字体
        utils.check_font.checkFont(self.logger)
        # 检查版本更新线程
        if "Beta" not in self.yaml["version"] :
            thread = utils.thread.createCheckVersionQThread(self)
            thread.signal.connect(lambda: utils.message.showCheckVersionMessage(self))
            utils.thread.runQThread(thread)
        # 初始化图片资源
        utils.thread.createThread(self.InitLoadFile)
        # 注册页面
        self.register_ui = ui.register.Register(self)

        # 是否自动登录
        if not self.yaml["auto_login"] :
            # 登录界面
            self.login_ui = ui.login.Login(self)
            self.login_ui.login_button.clicked.connect(self.login)

            # 登录界面注册按键
            self.login_ui.register_button.clicked.connect(self.register_ui.clickRegister)
            # 登录界面忘记密码按键
            self.login_ui.forget_password_button.clicked.connect(self.register_ui.clickForgetPassword)

            self.login_ui.show()
        else :
            # 自动登录
            self.login(auto_login=True)

        self.splash.close()
        app.exit(app.exec_())


if __name__ == "__main__" :

    app = DangoTranslator()
    app.main()