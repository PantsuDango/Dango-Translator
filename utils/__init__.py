import yaml
import os
import sys
import re
import time
import logging
import tkinter.font
import requests
import json
import subprocess
from traceback import format_exc, print_exc

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


YAML_PATH = os.path.join(os.getcwd(), "config", "config.yaml")
FONT_PATH = os.path.join(os.getcwd(), "config", "other", "华康方圆体W7.TTC")
LOGO_PATH = os.path.join(os.getcwd(), "config", "icon", "logo.ico")
TEST_IMAGE_PATH = "C:/Users/Dango/Desktop/翻译器/4.0/config/other/image.jpg"


# 设置日志文件
def setLog() :

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    logFileName = date + ".log"
    logPath = os.path.join(os.getcwd(), "logs", logFileName)

    try :
        os.makedirs(os.path.join(os.getcwd(), "logs"))
    except FileExistsError :
        pass

    fileHandler = logging.FileHandler(logPath, mode="a+", encoding="utf-8")
    fileHandler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s][%(pathname)s-line:%(lineno)d][%(levelname)s]\n%(message)s")
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger


# 打开配置文件
def openConfig() :

    try :
        with open(YAML_PATH, "r", encoding="utf-8") as file :
            config = yaml.load(file.read(), Loader=yaml.FullLoader)
    except Exception :
        config = {}

    return config


# 更新配置文件
def saveConfig(config) :

    with open(YAML_PATH, "w", encoding="utf-8") as file :
        yaml.dump(config, file)


# 检查字体是否存在
def checkFont(logger) :

    tkinter.Tk()
    fontList = tkinter.font.families()

    if "华康方圆体W7" not in fontList :
        checkFontMessageBox("字体文件缺失",
                            "字体文字缺失，请先安装字体文件\n"
                            "它会使你的界面更好看ヾ(๑╹◡╹)ﾉ\"     \n"
                            "安装完毕后需重新打开翻译器！", logger)


# 打开字体文件
def openFontFile(logger) :

    try :
        os.startfile(FONT_PATH)
    except Exception :
        logger.error(format_exc())
        MessageBox("打开字体文件失败",
                   "由于某种神秘力量，打开字体文件失败了(◢д◣)\n"
                   "请手动打开安装，字体文件路径如下:\n"
                   "%s     "%FONT_PATH)

    sys.exit()


# 错误提示窗口-字体检查提示
def checkFontMessageBox(title, text, logger):

    messageBox = QMessageBox()
    messageBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
    messageBox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(LOGO_PATH), QtGui.QIcon.Normal, QtGui.QIcon.On)
    messageBox.setWindowIcon(icon)

    messageBox.setWindowTitle(title)
    messageBox.setText(text)

    openFontFileButton = QPushButton("好滴")
    openFontFileButton.clicked.connect(lambda: openFontFile(logger))

    messageBox.addButton(openFontFileButton, QMessageBox.YesRole)
    messageBox.addButton(QPushButton("忽略"), QMessageBox.NoRole)

    messageBox.exec_()


# 错误提示窗口-通用
def MessageBox(title, text):

    messageBox = QMessageBox()
    messageBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
    messageBox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(LOGO_PATH), QtGui.QIcon.Normal, QtGui.QIcon.On)
    messageBox.setWindowIcon(icon)

    messageBox.setWindowTitle(title)
    messageBox.setText(text)

    messageBox.addButton(QPushButton("好滴"), QMessageBox.YesRole)

    messageBox.exec_()


# 新旧配置转换
def configConvert(config, oldConfig) :

    config.update(oldConfig)

    ################### OCR设定 ###################
    # 离线OCR开关
    config["offlineOCR"] = oldConfig.get("offlineOCR", False)
    # 在线OCR开关
    config["onlineOCR"] = oldConfig.get("onlineOCR", False)
    # 百度OCR开关
    config["baiduOCR"] = oldConfig.get("baiduOCR", False)
    # 百度OCR密钥
    config["OCR"] = oldConfig.get("OCR", {})
    config["OCR"]["Secret"] = config["OCR"].get("Secret", "")
    config["OCR"]["Key"] = config["OCR"].get("Key", "")
    config["AccessToken"] = oldConfig.get("AccessToken", "")
    # 翻译语种
    config["language"] = oldConfig.get("language", "JAP")

    ################### 翻译设定 ###################
    # 字体颜色
    config["fontColor"] = oldConfig.get("fontColor", {})
    # 字体颜色 公共有道
    config["fontColor"]["youdao"] = config["fontColor"].get("youdao", "#5B8FF9")
    # 字体颜色 公共百度
    config["fontColor"]["baiduweb"] = config["fontColor"].get("baiduweb", "#5B8FF9")
    # 字体颜色 公共腾讯
    config["fontColor"]["tencentweb"] = config["fontColor"].get("tencentweb", "#5B8FF9")
    # 字体颜色 公共DeepL
    config["fontColor"]["deepl"] = config["fontColor"].get("deepl", "#5B8FF9")
    # 字体颜色 公共谷歌
    config["fontColor"]["google"] = config["fontColor"].get("google", "#5B8FF9")
    # 字体颜色 公共彩云
    config["fontColor"]["caiyun"] = config["fontColor"].get("caiyun", "#5B8FF9")
    # 字体颜色 私人腾讯
    config["fontColor"]["tencent"] = config["fontColor"].get("tencent", "#5B8FF9")
    # 字体颜色 私人百度
    config["fontColor"]["baidu"] = config["fontColor"].get("baidu", "#5B8FF9")
    # 字体颜色 私人彩云
    config["fontColor"]["caiyunPrivate"] = config["fontColor"].get("caiyunPrivate", "#5B8FF9")

    # 公共有道翻译开关
    config["youdaoUse"] = oldConfig.get("youdaoUse", "False")
    # 公共百度翻译开关
    config["baiduwebUse"] = oldConfig.get("baiduwebUse", "False")
    # 公共腾讯翻译开关
    config["tencentwebUse"] = oldConfig.get("tencentwebUse", "False")
    # 公共DeepL翻译开关
    config["deeplUse"] = oldConfig.get("deeplUse", "False")
    # 公共谷歌翻译开关
    config["googleUse"] = oldConfig.get("googleUse", "False")
    # 公共彩云翻译开关
    config["caiyunUse"] = oldConfig.get("caiyunUse", "False")
    # 私人腾讯翻译开关
    config["tencentUse"] = oldConfig.get("tencentUse", "False")
    # 私人百度翻译开关
    config["baiduUse"] = oldConfig.get("baiduUse", "False")
    # 私人彩云翻译开关
    config["caiyunPrivateUse"] = oldConfig.get("caiyunPrivateUse", "False")

    # 私人腾讯翻译密钥
    config["tencentAPI"] = oldConfig.get("tencentAPI", {})
    config["tencentAPI"]["Secret"] = config["tencentAPI"].get("Secret", "")
    config["tencentAPI"]["Key"] = config["tencentAPI"].get("Key", "")
    # 私人百度翻译密钥
    config["baiduAPI"] = oldConfig.get("baiduAPI", {})
    config["baiduAPI"]["Secret"] = config["baiduAPI"].get("Secret", "")
    config["baiduAPI"]["Key"] = config["baiduAPI"].get("Key", "")
    # 私人彩云翻译密钥
    config["caiyunAPI"] = oldConfig.get("caiyunAPI", "")

    ################### 其他设定 ###################
    # 翻译界面透明度
    config["horizontal"] = oldConfig.get("horizontal", 30)
    # 字体大小
    config["fontSize"] = oldConfig.get("fontSize", 15)
    # 字体
    config["fontType"] = oldConfig.get("fontType", "华康方圆体W7")
    # 字体样式开关
    config["showColorType"] = oldConfig.get("showColorType", "False")
    # 自动翻译时间间隔
    config["translateSpeed"] = oldConfig.get("translateSpeed", 0.5)
    # 显示原文开关
    config["showOriginal"] = oldConfig.get("showOriginal", "False")
    # 原文自动复制到剪贴板开关
    config["showClipboard"] = oldConfig.get("showClipboard", "False")
    # 文字方向
    config["showTranslateRow"] = oldConfig.get("showTranslateRow", "False")
    # 翻译快捷键
    config["showHotKeyValue1"] = oldConfig.get("showHotKeyValue1", "F1")
    # 翻译快捷键开关
    config["showHotKey1"] = oldConfig.get("showHotKey1", "False")
    # 范围快捷键
    config["showHotKeyValue2"] = oldConfig.get("showHotKeyValue2", "F2")
    # 范围快捷键开关
    config["showHotKey2"] = oldConfig.get("showHotKey2", "False")
    # 图像相似度
    config["imageSimilarity"] = oldConfig.get("imageSimilarity", 98)
    # 文字相似度
    config["textSimilarity"] = oldConfig.get("textSimilarity", 90)
    # 范围坐标
    config["range"] = oldConfig.get("range", {"X1": 0, "Y1": 0, "X2": 500, "Y2": 500})

    return config


# 从云端获取配置信息
def getSettin(config, logger) :


    getSettinURL = "http://120.24.146.175:3000/DangoTranslate/GetSettin"

    params = json.dumps({"User": config["user"]})
    proxies = {"http": None, "https": None}

    try:
        res = requests.post(getSettinURL, data=params, proxies=proxies, timeout=10)
        res.encoding = "utf-8"
        result = json.loads(res.text).get("Result", "")

        if result == "User dose not exist" :
            pass

        elif result :
            config = configConvert(config, json.loads(result))

        else :
            pass

    except Exception :
        logger.error(format_exc())

    return config


# 检查端口是否被占用
def detectPort(port) :

    cmd = ("netstat", "-a", "-n")
    try :
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        for line in p.stdout :
            if re.findall("0\.0\.0\.0:%d"%port, str(line)) :
                return True, None

        p.kill()

    except Exception :
        return False, format_exc()

    return False, None


# 测试离线OCR
def testOfflineOCR() :

    url = "http://127.0.0.1:6666/ocr/api"
    data = {
        'ImagePath': TEST_IMAGE_PATH,
        'Language': "JAP"
    }
    proxies = {"http": None, "https": None}
    timeCount = 0

    for num in range(11) :
        try :
            start = time.time()
            res = requests.post(url, data=json.dumps(data), proxies=proxies, timeout=10)
            res.encoding = "utf-8"

            end = time.time()
            if num != 0 :
                timeCount += end-start
            print("time: {}\n".format(end-start))

        except Exception :
            print_exc()
            print("\n测试失败")
            break

        if num == 10 :
            print("avg time: {}".format(timeCount/10))


# 请求配置中心
def postConfigURL() :

    try :
        proxies = {"http": None, "https": None}
        res = requests.get("https://api.ayano.top/dango/", proxies=proxies)
        res.encoding = "utf-8"
        config_json = json.loads(res.text)
    except Exception :
        return None, format_exc()

    return config_json, None


# 保存配置至云端
def postSaveSettin(config, logger) :

    # 同时本地保存
    config["offlineOCR"] = False
    saveConfig(config)

    # 云端保存
    save_settin_url = "http://120.24.146.175:3000/DangoTranslate/SaveSettin"
    formdata = json.dumps({
        "User": config["user"],
        "Data": json.dumps(config)
    })
    proxies = {"http": None, "https": None}
    try:
        requests.post(save_settin_url, data=formdata, proxies=proxies).json()
    except Exception:
        logger.error(format_exc())