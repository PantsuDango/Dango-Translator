from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import time
import webbrowser

import utils.check_font
import utils.offline_ocr
import ui.static.icon


# 创建基础消息窗
def createMessageBox(title, text, rate=1) :

    message_box = QMessageBox()
    message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    message_box.setCursor(ui.static.icon.PIXMAP_CURSOR)
    message_box.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
    message_box.setWindowTitle(title)
    message_box.setText(text)

    return message_box


# 消息提示窗口-通用
def MessageBox(title, text, rate=1):

    message_box = createMessageBox(title, text, rate)
    message_box.addButton(QPushButton("好滴"), QMessageBox.YesRole)
    message_box.exec_()


# 检查chrome浏览器提示窗口
def checkChromeMessageBox(title, text, rate=1):

    message_box = createMessageBox(title, text, rate)
    button = QPushButton("下载")
    message_box.addButton(button, QMessageBox.YesRole)
    button.clicked.connect(lambda: webbrowser.open("https://www.google.cn/chrome/index.html", new=0, autoraise=True))
    message_box.addButton(QPushButton("取消"), QMessageBox.NoRole)
    message_box.exec_()


# 错误提示窗口-字体检查提示
def checkFontMessageBox(title, text, logger, rate=1):

    message_box = createMessageBox(title, text, rate)
    button = QPushButton("好滴")
    button.clicked.connect(lambda: utils.check_font.openFontFile(logger))
    message_box.addButton(button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("忽略"), QMessageBox.NoRole)
    message_box.exec_()


# 错误提示窗口-绑定邮箱提示
def checkEmailMessageBox(title, text, object) :

    message_box = createMessageBox(title, text, object.yaml["screen_scale_rate"])
    button = QPushButton("好滴")
    button.clicked.connect(object.register_ui.clickBindEmail)
    message_box.addButton(button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("忽略"), QMessageBox.NoRole)
    message_box.exec_()


# 消息提示窗口-停止进度条
def closeProcessBarMessageBox(title, text, object) :

    message_box = createMessageBox(title, text, object.rate)
    button = QPushButton("停止")
    button.clicked.connect(object.stopProcess)
    message_box.addButton(button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("取消"), QMessageBox.NoRole)

    message_box.exec_()


# 错误提示窗口-卸载本地OCR
def uninstallOfflineOCRMessageBox(title, text, object) :

    message_box = createMessageBox(title, text, object.yaml["screen_scale_rate"])
    button = QPushButton("卸载")
    button.clicked.connect(lambda: utils.offline_ocr.uninstall_offline_ocr(object))
    message_box.addButton(button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("取消"), QMessageBox.NoRole)

    message_box.exec_()


# 打开自动更新程序
def updateVersion() :

    try :
        os.chdir(os.path.abspath(".."))
        os.startfile("自动更新程序.exe")
    except Exception as err :
        MessageBox("自动更新失败", "打开自动更新程序失败:\n%s"%err)

    sys.exit()


# 错误提示窗口-更新版本用
def checkVersionMessageBox(title, text, rate=1) :

    message_box = createMessageBox(title, text, rate)
    button = QPushButton("好滴")
    button.clicked.connect(updateVersion)
    message_box.addButton(button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("忽略"), QMessageBox.NoRole)

    message_box.exec_()


# 错误提示窗口-关闭程序用
def quitAppMessageBox(title, text, object, rate=1) :

    message_box = createMessageBox(title, text, rate)
    button = QPushButton("再见")
    button.clicked.connect(object.translation_ui.quit)
    message_box.addButton(button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("我点错了"), QMessageBox.NoRole)

    message_box.exec_()


# 服务连接失败提示
def serverClientFailMessage(object) :

    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    log_file_name = date + ".log"
    utils.message.MessageBox("连接服务器失败",
                             "无法连接服务器, 请检查你的网络环境是否正常\n"
                             "并留意是否开启了梯子、加速器等代理软件, 如有可尝试关闭后重试    \n"
                             "若仍无法解决, 可获取日志文件并通过交流群联系客服处理\n"
                             "日志文件地址:\n"
                             "%s"%os.path.join(os.path.abspath("../") , "logs", log_file_name), object.yaml["screen_scale_rate"])
    sys.exit()


# 检查是否是最新版本
def showCheckVersionMessage(object) :

    message = object.yaml["dict_info"]["update_version_message"]
    text = ""
    text_list = message.split(r"\n")
    for index, val in enumerate(text_list) :
        if index+1 == len(text_list) :
            text += val
        else :
            text += val + "\n"
    checkVersionMessageBox("检查版本更新",
                           "%s     "%text)


# 检查是否为测试版本
def checkIsTestVersion(object) :

    if "Beta" in object.yaml["version"] and object.yaml["dict_info"]["test_version_switch"] != "1" :
        MessageBox("此版本已停止服务",
                   "目前您使用的是测试版本, 此版本已经停止更新      \n"
                   "请下载正式版本使用, 下载地址:\n%s      "
                   %object.yaml["dict_info"]["dango_home_page"], object.yaml["screen_scale_rate"])
        sys.exit()