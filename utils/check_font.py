import os
import sys
import locale
import tkinter.font
from traceback import format_exc

import utils.message


FONT_PATH = os.path.join(os.getcwd(), "config", "other", "华康方圆体W7.TTC")


# 检查字体是否存在
def checkFont(logger) :

    try :
        if locale.getdefaultlocale()[1] != "cp936" :
            return
    except Exception :
        logger.error(format_exc())

    tkinter.Tk()
    font_list = tkinter.font.families()

    if "华康方圆体W7" not in font_list :
        utils.message.checkFontMessageBox("字体文件缺失",
                                          "字体文字缺失，请先安装字体文件\n"
                                          "它会使你的界面更好看ヾ(๑╹◡╹)ﾉ\"     \n"
                                          "安装完毕后需重新打开翻译器！", logger)


# 打开字体文件
def openFontFile(logger) :

    try :
        os.startfile(FONT_PATH)
    except Exception :
        logger.error(format_exc())
        utils.message.MessageBox("打开字体文件失败",
                                 "由于某种神秘力量，打开字体文件失败了(◢д◣)\n"
                                 "请手动打开安装，字体文件路径如下:\n"
                                 "%s     "%FONT_PATH)
    sys.exit()