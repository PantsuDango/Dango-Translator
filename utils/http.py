import requests
import json
from traceback import format_exc


# 发送http请求
def post(url, body, logger):

    proxies = {
        "http": None,
        "https": None
    }
    result = {}
    try:
        response = requests.post(url, data=json.dumps(body), proxies=proxies, timeout=10)
        response.encoding = "utf-8"
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
    if res.get("Code", -1) == 0 :
        object.config["DangoToken"] = res.get("Token", "")
    else :
        object.logger.error(res.get("ErrorMsg", ""))