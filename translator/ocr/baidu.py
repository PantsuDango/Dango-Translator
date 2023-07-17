from traceback import format_exc
import requests
import base64
import utils.message
import utils.http

IMAGE_PATH = "./config/image.jpg"
TEST_IMAGE_PATH = "./config/other/image.jpg"

# 获取访问百度OCR用的token
def getAccessToken(object) :

    client_id = object.config["OCR"]["Key"]
    client_secret = object.config["OCR"]["Secret"]

    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"%(client_id, client_secret)
    proxies = {"http": None, "https": None}

    try:
        response = requests.get(host, proxies=proxies, timeout=5)

    except TypeError :
        object.logger.error(format_exc())
        utils.message.MessageBox("百度OCR错误",
                                 "需要翻译器目录的路径设置为纯英文\n"
                                 "否则无法在非简中区的电脑系统下运行使用     ")

    except Exception :
        object.logger.error(format_exc())
        utils.message.MessageBox("百度OCR错误",
                                 "啊咧... 百度OCR连接失败惹 (つД`)\n"
                                 "你可能会无法使用百度OCR\n"
                                 "1. 可能开了代理或者加速器, 请尝试关闭它们\n"
                                 "2. 可能是校园网屏蔽或者是自身网络断开了\n"
                                 "3. 如都无法解决, 请更换使用团子本地或在线OCR     ")

    else :
        try :
            response.encoding = "utf-8"
            result_json = response.json()

            access_token = result_json.get("access_token", "")
            if access_token :
                object.config["AccessToken"] = access_token

            else :
                error = response.json()["error"]
                error_description = response.json()["error_description"]

                if error_description == "unknown client id":
                    utils.message.MessageBox("百度OCR错误",
                                             "你可能会无法使用百度OCR\n"
                                             "你的百度OCR API Key填错啦 ヽ(#`Д´)ﾉ     ")

                elif error_description == "Client authentication failed":
                    utils.message.MessageBox("百度OCR错误",
                                             "你可能会无法使用百度OCR\n"
                                             "你的百度OCR Secret Key填错啦 ヽ(#`Д´)ﾉ     ")

                else:
                    utils.message.MessageBox("百度OCR错误",
                                             "啊咧...OCR连接失败惹... (つД`)\n"
                                             "你可能会无法使用百度OCR\n"
                                             "error：%s\n"
                                             "error_description：%s     "
                                             %(error, error_description))

        except Exception :
            object.logger.error(format_exc())
            utils.message.MessageBox("百度OCR错误",
                                     "出现了出乎意料的问题..."
                                     "你可能会无法使用百度OCR\n"
                                     "%s"%(format_exc()))


# 百度ocr
def baiduOCR(object, test=False) :

    # 获取配置
    language = object.config.get("language", "JAP")
    if language == "RU" :
        language = "RUS"
    access_token = object.config.get("AccessToken", "")
    show_translate_row = object.config.get("showTranslateRow", False)
    ocr_config = object.config.get("OCR", {})
    high_precision = ocr_config.get("highPrecision", False)
    branch_line_use = object.config.get("BranchLineUse", False)

    # 鉴权token
    if not access_token :
        return False, "百度OCR错误: 还未注册百度OCR密钥, 不可使用\n请于[设置]-[识别设定]-[百度OCR]页面内, 点击[注册]按钮完成注册并填入密钥后再使用"
    # 是否使用高精度模式
    if show_translate_row == True or high_precision :
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    else :
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 是否为接口测试
    path = IMAGE_PATH
    if test :
        path = TEST_IMAGE_PATH
        language = "JAP"

    # 封装请求体
    with open(path, "rb") as file :
        image = base64.b64encode(file.read())
    params = {"image": image, "language_type": language}
    headers = {"content-type": "application/x-www-form-urlencoded", "Connection": "close"}
    proxies = {"http": None, "https": None}
    request_url = request_url + "?access_token=" + access_token

    # 请求百度ocr
    try:
        resp = requests.post(request_url, data=params, headers=headers, proxies=proxies, timeout=5).json()
    except Exception:
        object.logger.error(format_exc())
        return False, "百度OCR错误: 网络超时, 请尝试重试\n如有正在使用任何代理或加速器, 请尝试关闭后重试\n如果频繁出现, 建议切换其他OCR使用"
    if not resp :
        return False, "百度OCR错误: 网络超时, 请尝试重试\n如有正在使用任何代理或加速器, 请尝试关闭后重试\n如果频繁出现, 建议切换其他OCR使用"

    # 正常解析
    if "words_result" in resp:
        words = resp.get("words_result", [])
        content = ""
        if show_translate_row == True :
            # 竖向翻译模式
            if words:
                for word in words[::-1]:
                    content += word["words"] + ","
                content = content.replace(",", "")
        else:
            # 横向翻译模式
            for index, word in enumerate(words):
                if branch_line_use and (index + 1 != len(words)):
                    if language == "ENG":
                        content += word["words"] + " \n"
                    else:
                        content += word["words"] + "\n"
                else:
                    if language == "ENG":
                        content += word["words"] + " "
                    else:
                        content += word["words"]
        return True, content
    # 错误解析
    else :
        # 如果接口调用错误
        error_code = resp.get("error_code", 0)
        error_msg = resp.get("error_msg", "")

        content = "百度OCR错误: 错误码-%d, 错误信息-%s\n"%(error_code, error_msg)
        if error_code == 6 :
            content += "开通的服务类型非通用文字识别, 请检查百度OCR的注册网页, 注册的类型是不是通用文字识别"
        elif error_code == 17 :
            if show_translate_row == True :
                content += "竖排翻译模式每日额度已用光, 请关闭竖排翻译模式, 或切换其他OCR使用竖排翻译"
            else:
                content += "无使用额度或免费额度已用光, 可更换本地OCR或在线OCR"
        elif error_code == 18 :
            content += "使用频率过快, 如为自动翻译可调整自动翻译时间间隔(建议1s), 手动翻译请降低使用频率"

        elif error_code == 111 :
            content += "缓存密钥已过期, 请进入设置页面一次, 以重新生成缓存密钥"

        elif error_code == 216202 :
            content += "识别范围过小无法识别, 请重新框选要翻译的区域"

        else:
            content += "错误未知或未收录"
        return False, content