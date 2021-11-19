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