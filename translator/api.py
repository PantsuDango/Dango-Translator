# -*- coding: utf-8 -*-

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

import requests
from http.client import HTTPConnection
from hashlib import md5
from urllib import parse
from random import randint
from traceback import format_exc
import json
import re


# 私人百度翻译
def baidu(sentence, app_id, secret_key, logger):

    string = ""

    # 如果未注册
    if (not app_id) or (not secret_key) :
        return "私人百度: 还未注册私人百度API，不可使用"

    url = "/api/trans/vip/translate"
    fromLang = 'auto'
    toLang = 'zh'
    salt = randint(32768, 65536)
    q = sentence
    sign = app_id + q + str(salt) + secret_key
    sign = md5(sign.encode()).hexdigest()
    url = url + '?appid=' + app_id + '&q=' + parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try :
        httpClient = HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', url)
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        if httpClient:
            httpClient.close()

        try :
            for word in result['trans_result']:
                if word == result['trans_result'][-1]:
                    string += word['dst']
                else:
                    string += word['dst'] + '\n'

        except Exception :
            logger.error(format_exc())

            error_code = result["error_code"]
            if error_code == "54003":
                string = "私人百度: 我抽风啦, 请尝试重新翻译!"
            elif error_code == "52001":
                string = "私人百度: 请求超时, 请重试"
            elif error_code == "52002":
                string = "私人百度: 系统错误, 请重试"
            elif error_code == "52003":
                string = "私人百度: APPID 或 密钥 不正确"
            elif error_code == "54001":
                string = "私人百度: APPID 或 密钥 不正确"
            elif error_code == "54004":
                string = "私人百度: 账户余额不足"
            elif error_code == "54005":
                string = "私人百度: 请降低长query的发送频率，3s后再试"
            elif error_code == "58000":
                string = "私人百度: 客户端IP非法, 注册时错误填入服务器地址, 请前往开发者信息-基本信息修改, 服务器地址必须为空"
            elif error_code == "90107":
                string = "私人百度: 认证未通过或未生效"
            else:
                string = "私人百度: %s, %s"%(error_code, result["error_msg"])

    except Exception :
        logger.error(format_exc())
        string = "私人百度：我抽风啦, 请尝试重新翻译!"

    return string


# 私人腾讯翻译
def tencent(sentence, secret_id, secret_key, logger):

    result = ""

    # 如果未注册
    if (not secret_id) or (not secret_key) :
        return "私人腾讯: 还未注册私人腾讯API, 不可使用"

    try:
        cred = credential.Credential(secret_id, secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile)

        req = models.TextTranslateRequest()
        sentence = sentence.replace('"', "'")
        params = '''{"SourceText":"%s","Source":"auto","Target":"zh","ProjectId":0}'''%(sentence)
        params = params.replace('\r', '\\r').replace('\n', '\\n')
        req.from_json_string(params)

        resp = client.TextTranslate(req)
        result = re.findall(r'"TargetText": "(.+?)"', resp.to_json_string())[0]
        result = result.replace('\\r', '\r').replace('\\n', '\n')

    except TencentCloudSDKException as err :

        try:
            err = str(err)
            code = re.findall(r'code:(.*?) message', err)[0]
            error = re.findall(r'message:(.+?) requestId', err)[0]

        except Exception :
            logger.error(format_exc())
            result = "私人腾讯：我抽风啦, 请尝试重新翻译!"

        else:
            if code == "MissingParameter" :
                pass

            elif code == "FailedOperation.NoFreeAmount" :
                result = "私人腾讯：本月免费额度已经用完"

            elif code == "FailedOperation.ServiceIsolate" :
                result = "私人腾讯：账号欠费停止服务"

            elif code == "FailedOperation.UserNotRegistered" :
                result = "私人腾讯：还没有开通机器翻译服务"

            elif code == "InternalError" :
                result = "私人腾讯：内部错误"

            elif code == "InternalError.BackendTimeout" :
                result = "私人腾讯：后台服务超时，请稍后重试"

            elif code == "InternalError.ErrorUnknown" :
                result = "私人腾讯：未知错误"

            elif code == "LimitExceeded" :
                result = "私人腾讯：超过配额限制"

            elif code == "UnsupportedOperation" :
                result = "私人腾讯：操作不支持"

            elif code == "InvalidCredential" :
                result = "私人腾讯：secretId或secretKey错误"

            elif code == "AuthFailure.SignatureFailure" :
                result = "私人腾讯：secretKey错误"

            elif code == "AuthFailure.SecretIdNotFound" :
                result = "私人腾讯：secretId错误"

            elif code == "AuthFailure.SignatureExpire" :
                result = "私人腾讯：签名过期，请将电脑系统时间调整至准确的时间后重试"

            else:
                result = "私人腾讯: %s, %s"%(code, error)

    except Exception:
        logger.error(format_exc())
        result = "私人腾讯：我抽风啦, 请尝试重新翻译!"

    return result


# 私人彩云翻译
def caiyun(sentence, token, logger) :

    if not token :
        return "私人彩云: 还未注册私人彩云API, 不可使用"

    url = "http://api.interpreter.caiyunai.com/v1/translator"
    payload = {
        "source": sentence.split("\n"),
        "trans_type": "auto2zh",
        "request_id": "demo",
        "detect": True,
    }
    headers = {
        "content-type": "application/json",
        "x-authorization": "token " + token,
    }
    proxies = {"http": None, "https": None}

    text = ""
    try:
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, proxies=proxies, timeout=5)
        result = json.loads(response.text)['target']
        for word in result:
            text += word
            if word != result[-1]:
                text += "\n"
    except Exception:
        try:
            text = str(json.loads(response.text))
        except Exception:
            logger.error(format_exc())
            text = "私人彩云: 我抽风啦, 请尝试重新翻译!"

    return text


# ChatGPT翻译
def chatgpt(api_key, language, proxy, content, logger) :

    if not api_key :
        return "私人彩云: 还未填入私人ChatGPT密钥, 不可使用"

    language_map = {
        "JAP": "japanese",
        "ENG": "english",
        "KOR": "korean",
        "RU": "russian",
    }
    messages = [
        {"role": "system","content": "You are a translation engine that can only translate text and cannot interpret it."},
        {"role": "user", "content": "translate from {} to chinese".format(language_map[language])},
        {"role": "user", "content": content}
    ]
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0,
        "max_tokens": 1000,
        "top_p": 1,
        "n": 1,
        "frequency_penalty": 1,
        "presence_penalty": 1,
        "stream": False,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(api_key)
    }
    proxies = {
        "http": None,
        "https": None
    }
    if proxy :
        proxies = {
            "http": "http://{}".format(proxy),
            "https": "https://{}".format(proxy)
        }
    url = "https://api.openai.com/v1/chat/completions"
    try :
        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies, timeout=20)
        response.encoding = "utf-8"
        result = json.loads(response.text)
        response.close()
        try :
            text = result["choices"][0]["message"]["content"]
        except Exception:
            return str(result)
    except TimeoutError:
        text = "私人ChatGPT：我超时啦, 请尝试重新翻译!"
    except Exception :
        logger.error(format_exc())
        text = "私人ChatGPT：我抽风啦, 请尝试重新翻译!"

    return text