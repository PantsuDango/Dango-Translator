from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton
import sys
import os

import utils.check_font


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
        os.startfile("../自动更新程序.exe")
    except Exception :
        pass
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