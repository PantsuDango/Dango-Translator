import requests
import json
from traceback import format_exc


# 发送http请求
def post(url, body, logger, timeout=5) :

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
        with requests.post(url, data=json.dumps(body), proxies=proxies, verify=False, timeout=timeout) as response :
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

    res = post(url, body, object.logger)
    object.config["DangoToken"] = res.get("Token", "")
    if res.get("Code", -1) != 0 :
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


# 发送get请求
def get(url, logger, timeout=5) :

    try :
        res = requests.get(url, stream=True, timeout=timeout)
        return res.text
    except Exception :
        logger.error(format_exc())