import re
import time
import requests
import json
import subprocess
from traceback import format_exc, print_exc

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