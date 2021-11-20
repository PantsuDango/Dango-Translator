import re
import time
import requests
import json
import subprocess
from traceback import format_exc, print_exc
from difflib import SequenceMatcher

from utils.check_font import openFontFile
from utils.config import saveConfig

TEST_IMAGE_PATH = "C:/Users/Dango/Desktop/翻译器/4.0/config/other/image.jpg"


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


# 判断原文相似度
def get_equal_rate(str1, str2) :

    return SequenceMatcher(None, str1, str2).quick_ratio()



# 保存翻译历史
def saveTransHisTory(text, translate_type) :

    if translate_type == "youdao" :
        content = "\n[公共有道]\n%s"%text
    elif translate_type == "caiyun" :
        content = "\n[公共彩云]\n%s"%text
    elif translate_type == "deepl" :
        content = "\n[公共DeepL]\n%s"%text
    elif translate_type == "baidu" :
        content = "\n[公共百度]\n%s"%text
    elif translate_type == "tencent" :
        content = "\n[公共腾讯]\n%s"%text
    elif translate_type == "google" :
        content = "\n[公共谷歌]\n%s"%text
    elif translate_type == "baidu_private" :
        content = "\n[私人百度]\n%s"%text
    elif translate_type == "tencent_private" :
        content = "\n[私人腾讯]\n%s"%text
    elif translate_type == "caiyun_private" :
        content = "\n[私人彩云]\n%s"%text
    else:
        return

    with open("./config/翻译历史.txt", "a+", encoding="utf-8") as file :
        file.write(content)


# 判断矩形是否碰撞
class Rectangular :

    def __init__(self, x, y, w, h):

        self.x0 = x
        self.y0 = y
        self.x1 = x + w
        self.y1 = y + h
        self.w = w
        self.h = h


    def __gt__(self, other) :

        if self.w > other.w and self.h > other.h:
            return True
        return False


    def __lt__(self, other) :
        if self.w < other.w and self.h < other.h:
            return True
        return False


    def collision(self, r2) :

        if self.x0 < r2.x1 and self.y0 < r2.y1 and self.x1 > r2.x0 and self.y1 > r2.y0:
            return True
        return False