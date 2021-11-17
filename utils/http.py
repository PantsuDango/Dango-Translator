import requests
import json
from traceback import format_exc


# 发送http请求
def post(url:str, body:dict) -> (dict, str) :

    proxies = {
        "http": None,
        "https": None
    }
    try:
        res = requests.post(url, data=json.dumps(body), proxies=proxies)
        res.encoding = "utf-8"
        result = json.loads(res.text)
        return result, None

    except Exception :
        return format_exc()