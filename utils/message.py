from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton
import sys
import os
import time

import utils.check_font
import utils.lock


LOGO_PATH = "./config/icon/logo.ico"
PIXMAP_ICON_PATH = "./config/icon/pixmap.png"
PIXMAP2_PATH = "./config/icon/pixmap2.png"


# 错误提示窗口-通用
def MessageBox(title, text, rate=1):

    message_box = QMessageBox()
    message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    # 鼠标样式
    pixmap = QPixmap(PIXMAP_ICON_PATH)
    pixmap = pixmap.scaled(int(20*rate),
                           int(20*rate),
                           Qt.KeepAspectRatio,
                           Qt.SmoothTransformation)
    cursor = QCursor(pixmap, 0, 0)
    message_box.setCursor(cursor)

    icon = QIcon()
    icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
    message_box.setWindowIcon(icon)

    message_box.setWindowTitle(title)
    message_box.setText(text)

    message_box.addButton(QPushButton("好滴"), QMessageBox.YesRole)

    message_box.exec_()


# 错误提示窗口-字体检查提示
def checkFontMessageBox(title, text, logger, rate=1):

    message_box = QMessageBox()
    message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    # 鼠标样式
    pixmap = QPixmap(PIXMAP_ICON_PATH)
    pixmap = pixmap.scaled(int(20*rate),
                           int(20*rate),
                           Qt.KeepAspectRatio,
                           Qt.SmoothTransformation)
    cursor = QCursor(pixmap, 0, 0)
    message_box.setCursor(cursor)

    icon = QIcon()
    icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
    message_box.setWindowIcon(icon)

    message_box.setWindowTitle(title)
    message_box.setText(text)

    open_font_file_button = QPushButton("好滴")
    open_font_file_button.clicked.connect(lambda: utils.check_font.openFontFile(logger))

    message_box.addButton(open_font_file_button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("忽略"), QMessageBox.NoRole)

    message_box.exec_()


# 错误提示窗口-绑定邮箱提示
def checkEmailMessageBox(title, text, object) :

    message_box = QMessageBox()
    message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    # 鼠标样式
    pixmap = QPixmap(PIXMAP_ICON_PATH)
    pixmap = pixmap.scaled(int(20*object.yaml["screen_scale_rate"]),
                           int(20*object.yaml["screen_scale_rate"]),
                           Qt.KeepAspectRatio,
                           Qt.SmoothTransformation)
    cursor = QCursor(pixmap, 0, 0)
    message_box.setCursor(cursor)

    icon = QIcon()
    icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
    message_box.setWindowIcon(icon)

    message_box.setWindowTitle(title)
    message_box.setText(text)

    bind_email_button = QPushButton("好滴")
    bind_email_button.clicked.connect(object.register_ui.clickBindEmail)

    message_box.addButton(bind_email_button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("忽略"), QMessageBox.NoRole)

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

    message_box = QMessageBox()
    message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    # 鼠标样式
    pixmap = QPixmap(PIXMAP_ICON_PATH)
    pixmap = pixmap.scaled(int(20*rate),
                           int(20*rate),
                           Qt.KeepAspectRatio,
                           Qt.SmoothTransformation)
    cursor = QCursor(pixmap, 0, 0)
    message_box.setCursor(cursor)

    icon = QIcon()
    icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
    message_box.setWindowIcon(icon)

    message_box.setWindowTitle(title)
    message_box.setText(text)

    check_version_button = QPushButton("好滴")
    check_version_button.clicked.connect(updateVersion)

    message_box.addButton(check_version_button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("忽略"), QMessageBox.NoRole)

    message_box.exec_()


# 错误提示窗口-关闭程序用
def quitAppMessageBox(title, text, object, rate=1) :

    message_box = QMessageBox()
    message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    # 鼠标样式
    pixmap = QPixmap(PIXMAP_ICON_PATH)
    pixmap = pixmap.scaled(int(20*rate),
                           int(20*rate),
                           Qt.KeepAspectRatio,
                           Qt.SmoothTransformation)
    cursor = QCursor(pixmap, 0, 0)
    message_box.setCursor(cursor)

    icon = QIcon()
    icon.addPixmap(QPixmap(LOGO_PATH), QIcon.Normal, QIcon.On)
    message_box.setWindowIcon(icon)

    message_box.setWindowTitle(title)
    message_box.setText(text)

    button1 = QPushButton("再见")
    button1.clicked.connect(object.translation_ui.quit)
    message_box.addButton(button1, QMessageBox.YesRole)

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


# 唯一进程锁提示
def checkLockMessage() :

    MessageBox("启动失败",
               "团子翻译器已在运行中\n"
               "请不要重复运行, 如你并没有重复运行\n"
               "请尝试删除以下文件后重试:\n"
               "%s"%utils.lock.LOCK_FILE_PATH)
    sys.exit()


# 检查是否为测试版本
def checkIsTestVersion(object) :

    if "Beta" in object.yaml["version"] and object.yaml["dict_info"]["test_version_switch"] != "1" :
        MessageBox("此版本已停止服务",
                   "目前您使用的是测试版本, 此版本已经停止更新      \n"
                   "请下载正式版本使用, 下载地址:\n%s      "
                   %object.yaml["dict_info"]["update_version"], object.yaml["screen_scale_rate"])
        sys.exit()