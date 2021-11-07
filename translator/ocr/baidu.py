import requests
from base64 import b64encode
import json

from utils import MessageBox
from traceback import print_exc, format_exc


# 获取访问百度OCR用的token
def getAccessToken(client_id, client_secret, logger):

    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"%(client_id, client_secret)
    proxies = {"http": None, "https": None}

    try:
        response = requests.get(host, proxies=proxies, timeout=10)

    except TypeError :
        logger.error(format_exc())
        MessageBox("百度OCR错误",
                   "需要翻译器目录的路径设置为纯英文\n"
                   "否则无法在非简中区的电脑系统下运行使用     ")

    except Exception :
        logger.error(format_exc())
        MessageBox("百度OCR错误",
                   "啊咧... 百度OCR连接失败惹 (つД`)\n"
                   "你可能会无法使用百度OCR\n"
                   "1. 可能开了代理或者加速器, 请尝试关闭它们\n"
                   "2. 可能是校园网屏蔽或者是自身网络断开了\n"
                   "3. 如都无法解决, 请更换使用团子离线或在线OCR     ")

    else :
        try :
            response.encoding = "utf-8"
            result_json = response.json()

            access_token = result_json.get("access_token", "")
            if access_token :
                return True, access_token

            else :
                error = response.json()["error"]
                error_description = response.json()["error_description"]

                if error_description == "unknown client id":
                    MessageBox("百度OCR错误",
                               "你可能会无法使用百度OCR\n"
                               "你的百度OCR API Key填错啦 ヽ(#`Д´)ﾉ     ")

                elif error_description == "Client authentication failed":
                    MessageBox("百度OCR错误",
                               "你可能会无法使用百度OCR\n"
                               "你的百度OCR Secret Key填错啦 ヽ(#`Д´)ﾉ     ")

                else:
                    MessageBox("百度OCR错误",
                               "啊咧...OCR连接失败惹... (つД`)\n"
                               "你可能会无法使用百度OCR\n"
                               "error：%s\n"
                               "error_description：%s     "
                               %(error, error_description))

        except Exception :
            logger.error(format_exc())
            MessageBox("百度OCR错误",
                       "出现了出乎意料的问题..."
                       "你可能会无法使用百度OCR\n"
                       "%s"%(format_exc()))

    return False, None


# 百度ocr
def baiduOCR(config, logger) :

    language = config["language"]
    access_token = config["AccessToken"]
    showTranslateRow = config["showTranslateRow"]

    if not access_token :
        sentence = "百度OCR错误：还未注册OCR API，不可使用"

    else:
        if showTranslateRow == "True" :
            # 高精度
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        else :
            # 普通
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

        with open("./config/image.jpg", "rb") as file :
            image = b64encode(file.read())
        params = {"image": image, "language_type": language}
        headers = {"content-type": "application/x-www-form-urlencoded"}
        proxies = {"http": None, "https": None}
        request_url = request_url + "?access_token=" + access_token

        try:
            response = requests.post(request_url, data=params, headers=headers, proxies=proxies, timeout=10)

        except TypeError:
            logger.error(format_exc())
            MessageBox("百度OCR错误",
                       "需要翻译器目录的路径设置为纯英文\n"
                       "否则无法在非简中区的电脑系统下运行使用     ")

            sentence = "百度OCR错误: 需要翻译器目录的路径设置为纯英文, 否则无法在非简中区的电脑系统下运行使用"

        except Exception:
            logger.error(format_exc())
            sentence = "百度OCR错误: 请打开[网络和Internet设置]的[代理]页面, 将其中的全部代理设置开关都关掉, 保证关闭后请重试"

        else:
            if response:
                try:
                    words = response.json()["words_result"]

                except Exception :
                    logger.error(format_exc())
                    error_code = response.json()["error_code"]
                    error_msg = response.json()["error_msg"]

                    if error_code == 6 :
                        sentence = "百度OCR错误: 检查一下你的OCR注册网页, 注册的类型是不是文字识别, 你可能注册到语音技术还是其它什么奇怪的东西了"

                    elif error_code == 17 :
                        if showTranslateRow == "True":
                            sentence = "百度OCR错误：竖排翻译模式每日额度已用光, 请取消竖排翻译模式"
                        else:
                            sentence = "百度OCR错误: 无额度, 可使用离线ocr"

                    elif error_code == 111 :
                        sentence = "百度OCR错误: 密钥过期了, 请进入设置页面后保存一次设置, 以重新生成密钥"

                    elif error_code == 216202:
                        sentence = "百度OCR错误：范围截取过小无法识别，请重新框选一下你要翻译的区域"

                    else:
                        sentence = "百度OCR错误：%s, %s"%(error_code, error_msg)

                else:
                    sentence = ""

                    # 竖排翻译模式
                    if showTranslateRow == "True":
                        if words :
                            for word in words[::-1] :
                                sentence += word["words"] + ","
                            sentence = sentence.replace(",", "")

                    # 普通翻译模式
                    else:
                        for word in words:
                            sentence += word["words"]
                    return True, sentence

            else:
                sentence = "OCR错误: response无响应"

    return False, sentence