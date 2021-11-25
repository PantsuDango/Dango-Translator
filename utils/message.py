from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton
import sys

import utils.check_font


LOGO_PATH = "./config/icon/logo.ico"


# 错误提示窗口-通用
def MessageBox(title, text):

    message_box = QMessageBox()
    message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(LOGO_PATH), QtGui.QIcon.Normal, QtGui.QIcon.On)
    message_box.setWindowIcon(icon)

    message_box.setWindowTitle(title)
    message_box.setText(text)

    message_box.addButton(QPushButton("好滴"), QMessageBox.YesRole)

    message_box.exec_()


# 错误提示窗口-字体检查提示
def checkFontMessageBox(title, text, logger):

    message_box = QMessageBox()
    message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(LOGO_PATH), QtGui.QIcon.Normal, QtGui.QIcon.On)
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

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(LOGO_PATH), QtGui.QIcon.Normal, QtGui.QIcon.On)
    message_box.setWindowIcon(icon)

    message_box.setWindowTitle(title)
    message_box.setText(text)

    bind_email_button = QPushButton("好滴")
    bind_email_button.clicked.connect(object.register_ui.clickBindEmail)

    message_box.addButton(bind_email_button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("忽略"), QMessageBox.NoRole)

    message_box.exec_()


# 错误提示窗口-更新版本用
def checkVersionMessageBox(title, text) :

    message_box = QMessageBox()
    message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(LOGO_PATH), QtGui.QIcon.Normal, QtGui.QIcon.On)
    message_box.setWindowIcon(icon)

    message_box.setWindowTitle(title)
    message_box.setText(text)

    check_version_button = QPushButton("好滴")
    check_version_button.clicked.connect(lambda: sys.exit())

    message_box.addButton(check_version_button, QMessageBox.YesRole)
    message_box.addButton(QPushButton("忽略"), QMessageBox.NoRole)

    message_box.exec_()