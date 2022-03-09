import requests
import json
import re
import time
from traceback import format_exc


# 发送http请求
def post(url, body, logger, headers=None, timeout=5, session=None) :

    proxies = {
        "http": None,
        "https": None
    }
    result = {}

    try :
        # 消除https警告
        requests.packages.urllib3.disable_warnings()
    except Exception :
        pass

    try :
        if headers :
            if session :
                response = session.post(url, headers=headers, data=json.dumps(body), proxies=proxies, verify=False, timeout=timeout)
            else :
                response = requests.post(url, headers=headers, data=json.dumps(body), proxies=proxies, verify=False, timeout=timeout)
        else :
            if session :
                response = session.post(url, data=json.dumps(body), proxies=proxies, verify=False, timeout=timeout)
            else:
                response = requests.post(url, data=json.dumps(body), proxies=proxies, verify=False, timeout=timeout)
        try :
            response.encoding = "utf-8"
            result = json.loads(response.text)
        except Exception :
            response.encoding = "gb18030"
            result = json.loads(response.text)
    except Exception :
        logger.error(format_exc())

    return result


# 登录ocr服务器
def loginDangoOCR(object) :

    url = object.yaml["dict_info"]["ocr_login"]
    body = {
        "User": object.yaml["user"],
        "Password": object.yaml["password"],
    }

    for x in range(3) :
        res = post(url, body, object.logger)
        token = res.get("Token", "")
        code = res.get("Code", -1)
        if token :
            object.config["DangoToken"] = token
            break
        else :
            if code != 0 :
                object.logger.error(res.get("ErrorMsg", ""))


# 下载文件
def downloadFile(url, save_path, logger) :

    try :
        res = requests.get(url, stream=True)
        content = res.content
        with open(save_path, "wb") as file :
            file.write(content)
        return True
    except Exception :
        logger.error(format_exc())
        return False


# 发送get请求
def get(url, logger, timeout=5) :

    try :
        res = requests.get(url, stream=True, timeout=timeout)
        return res.text
    except Exception :
        logger.error(format_exc())


# 测试在线ocr节点可用性
def getOCR(url) :

    proxies = {"http": None, "https": None}
    start = time.time()
    try :
        res = requests.get(url, proxies=proxies, verify=False, timeout=3)
        time_diff = time.time() - start
        status_code = res.status_code
    except Exception :
        return None, 0
    if status_code != 200 and status_code != 404 :
        return None, 0

    return True, int(time_diff*1000)