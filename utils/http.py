import requests
import json
import time
from traceback import format_exc
import utils.enctry


# 发送http请求
def post(url, body, logger, headers=None, timeout=5) :

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

    response = None
    try :
        if headers :
            response = requests.post(url, headers=headers, data=json.dumps(body), proxies=proxies, verify=False, timeout=timeout)
        else :
            response = requests.post(url, data=json.dumps(body), proxies=proxies, verify=False, timeout=timeout)
        try :
            response.encoding = "utf-8"
            result = json.loads(response.text)
            response.close()
        except Exception :
            response.encoding = "gb18030"
            result = json.loads(response.text)
    except json.decoder.JSONDecodeError :
        try :
            logger.error("post %s error, httpcode is %s, response is %s"%(url, response.status_code, response.text))
        except Exception :
            pass
    except Exception :
        logger.error(format_exc())


    return result


# 登录ocr服务器
def loginDangoOCR(object) :

    url = object.yaml["dict_info"]["ocr_login"]

    psw = str(object.yaml["password"])
    if psw.find('%6?u!') != -1:
        psw = utils.enctry.dectry(psw)
    body = {
        "User": object.yaml["user"],
        "Password": psw,
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


# 查询在线OCR额度
def onlineOCRQueryQuota(object) :

    url = "%s?Token=%s"%(object.yaml["dict_info"]["ocr_query_quota"], object.config["DangoToken"])
    try :
        res = post(url, {}, object.logger)
        if len(res["Result"]) == 0 :
            return "您尚未购买过在线OCR, 请先购买后再查询有效期"
        max_end_time = ""
        for val in res["Result"] :
            if "文字识别" not in val["PackName"] :
                continue
            if val["EndTime"] > max_end_time :
                max_end_time = val["EndTime"]
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if now_time > max_end_time :
            return "您的有效期截止至:\n\n%s\n\n在线OCR已不可使用, 若要继续使用请购买\n\n对额度如有任何疑问请联系客服娘"%max_end_time
        else :
            return "您的有效期截止至:\n\n%s\n\n在线OCR还可以继续使用~\n\n对额度如有任何疑问请联系客服娘" % max_end_time
    except Exception :
        object.logger.error(format_exc())
        return "查询出错, 可联系客服娘, 或直接浏览器登录 https://cloud.stariver.org/auth/login.html 地址查看"


# 登录检查
def loginCheck(object) :

    url = object.yaml["dict_info"]["dango_login"]
    user = str(object.yaml["user"])
    password = str(object.yaml["password"])
    if password.find('%6?u!') != -1:
        password = utils.enctry.dectry(password)
    body = {
        "User": user,
        "Password": password
    }
    resp = post(url=url, body=body, logger=object.logger)
    if not resp:
        url = "https://trans.dango.cloud/DangoTranslate/Login"
        resp = post(url=url, body=body, logger=object.logger)
        # 如果因为网络原因登录失败
        if not resp :
            return "网络错误\n具体情况可查阅错误日志\n并通过交流群联系客服娘处理     "

    result = resp.get("Result", "")
    if result == "" :
        object.logger.error("登录出错, response: %s"%resp)
        return "网络错误\n具体情况可查阅错误日志\n并通过交流群联系客服娘处理     "

    if result == "User dose not exist":
        return "用户名不存在, 请先注册!     "

    elif result == "Password error":
        return "用户名和密码不匹配     "

    elif result == "User is black list":
        return "账户已被纳入黑名单     "

    elif result == "OK":
        # 保存配置
        object.yaml["user"] = user
        object.yaml["password"] = utils.enctry.enctry(password)
        utils.config.saveConfig(object.yaml, object.logger)

    else:
        object.logger.error("登录出错, response: %s"%resp)
        return "出现了出乎意料的情况\n请联系团子解决!     "


# 查询在线ocr试用次数
def ocrProbationReadCount(object) :

    url = object.yaml["dict_info"]["ocr_probation_read_count"]
    body = {"Username": object.yaml["user"]}
    resp = post(url=url, body=body, logger=object.logger)
    if not resp :
        return
    if resp.get("Code", -1) != 0 :
        return
    count = resp.get("Result", 0)
    object.settin_ui.online_ocr_probation_label.setText("试用在线OCR, 剩余%d次"%count)