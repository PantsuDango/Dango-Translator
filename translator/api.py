# -*- coding: utf-8 -*-
import time
import traceback

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

import urllib.parse
import hashlib
import base64
import hmac


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
        string = "私人百度: 我抽风啦, 请尝试重新翻译!"

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
            result = "私人腾讯: 我抽风啦, 请尝试重新翻译!"

        else:
            if code == "MissingParameter" :
                pass

            elif code == "FailedOperation.NoFreeAmount" :
                result = "私人腾讯: 本月免费额度已经用完"

            elif code == "FailedOperation.ServiceIsolate" :
                result = "私人腾讯: 账号欠费停止服务"

            elif code == "FailedOperation.UserNotRegistered" :
                result = "私人腾讯: 还没有开通机器翻译服务"

            elif code == "InternalError" :
                result = "私人腾讯: 内部错误"

            elif code == "InternalError.BackendTimeout" :
                result = "私人腾讯: 后台服务超时，请稍后重试"

            elif code == "InternalError.ErrorUnknown" :
                result = "私人腾讯: 未知错误"

            elif code == "LimitExceeded" :
                result = "私人腾讯: 超过配额限制"

            elif code == "UnsupportedOperation" :
                result = "私人腾讯: 操作不支持"

            elif code == "InvalidCredential" :
                result = "私人腾讯: secretId或secretKey错误"

            elif code == "AuthFailure.SignatureFailure" :
                result = "私人腾讯: secretKey错误"

            elif code == "AuthFailure.SecretIdNotFound" :
                result = "私人腾讯: secretId错误"

            elif code == "AuthFailure.SignatureExpire" :
                result = "私人腾讯: 签名过期，请将电脑系统时间调整至准确的时间后重试"

            else:
                result = "私人腾讯: %s, %s"%(code, error)

    except Exception:
        logger.error(format_exc())
        result = "私人腾讯: 我抽风啦, 请尝试重新翻译!"

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
        result = json.loads(response.text)["target"]
        for word in result :
            text += word
            if word != result[-1] :
                text += "\n"
    except Exception :
        try :
            logger.error(format_exc())
            text = "私人彩云: %s"%str(json.loads(response.text))
        except Exception :
            logger.error(format_exc())
            text = "私人彩云: 我抽风啦, 请尝试重新翻译!"

    return text


# ChatGPT翻译
def chatgpt(api_key, language, proxy, url, model, content, logger) :

    try :
        if not api_key:
            return "私人ChatGPT: 还未填入私人ChatGPT密钥, 不可使用"
        language_map = {
            "JAP": "日语",
            "ENG": "英文",
            "KOR": "韩语",
            "RU": "俄语",
        }
        content_list = content.split("\n")
        # 多句子情况的处理, 转为map
        if len(content_list) > 1:
            new_content = ""
            for i, val in enumerate(content_list) :
                if (i + 1) != len(content_list) :
                    new_content += "{%s}\n"%val
                else :
                    new_content += "{%s}"%val
            messages = [
                {"role": "system", "content": "你是一个翻译引擎, 只需要翻译内容而不要解释它, 请将以下{ }内的内容翻译成中文，并且将答案以{翻译结果}分行答复"},
                {"role": "user", "content": new_content}
            ]
        else:
            # 单个句子的情况
            messages = [
                {"role": "system", "content": "你是一个翻译引擎, 只需要翻译内容而不要解释它, 我需要你完成{}翻译为中文.".format(language_map[language])},
                {"role": "user", "content": content}
            ]
        data = {
            "model": model,
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
        if proxy:
            proxies = {
                "http": "http://{}".format(proxy),
                "https": "https://{}".format(proxy)
            }

        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies, timeout=30)
        response.encoding = "utf-8"
        result = json.loads(response.text)
        response.close()
        try :
            if result.get("error", {}).get("message", "") :
                # 翻译出错
                error = result.get("error", {}).get("message", "")
                if "Rate limit reached" in error :
                    text = "私人ChatGPT: 请求次数超限制, 请稍后重试, 或使用不带QPS限制的密钥"
                else :
                    text = "私人ChatGPT: 翻译出错: {}, 请排查完错误后重试".format(error)
            else :
                # 翻译成功
                text = result["choices"][0]["message"]["content"]
                text = re.sub("\(Translated from .+? to .+?\)", "", text)
                text = re.sub("\(Note.+?\)", "", text)

                # 多句子翻译的情况
                if len(content_list) > 1 :
                    text = text.replace("{", "").replace("}", "")
                    text = text.replace("翻译结果：", "").replace("翻译结果:", "").replace("翻译结果", "")
                    # 过滤多余的换行符
                    if "\n\n" in text :
                        text = re.sub("\n{2,}", "\n", text)
                    # 过滤带有 -> 的翻译结果
                    if "->" in text :
                        tmp_list = []
                        for val in text.split("\n") :
                            if "->" in val :
                                regex = re.findall("->(.+)", val)
                                if len(regex) == 1 :
                                    val = regex[0]
                            tmp_list.append(val)
                        text = "\n".join(tmp_list)

                    # 过滤带有 - 的翻译结果
                    if "-" in text :
                        tmp_list = []
                        for i, val in enumerate(text.split("\n")) :
                            if "-" in val and "-" not in content_list[i] :
                                regex = re.findall("-(.+)", val)
                                if len(regex) == 1 :
                                    val = regex[0]
                            tmp_list.append(val)
                        text = "\n".join(tmp_list)

                    # 过滤双倍句子的情况, 双倍句子下前部分都会是原文
                    if len(text.split("\n")) == len(content_list) * 2 :
                        text = "\n".join(text.split("\n")[len(content_list):])

        except Exception :
            logger.error(format_exc())
            return "私人ChatGPT: 翻译出错: {}".format(str(result))
    except requests.exceptions.ReadTimeout :
        text = "私人ChatGPT: 翻译超时, ChatGPT需要挂载代理才可使用, 请点击[代理]按钮, 正确配置好代理后重试"
    except Exception as err :
        logger.error(format_exc())
        text = "私人ChatGPT: 翻译出错: {}, 请排查完错误后重试".format(err)

    return text


# 获取ChatGPT模型列表
def getChatgptModels(api_key, proxy, logger) :

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(api_key)
    }
    proxies = {
        "http": None,
        "https": None
    }
    if proxy:
        proxies = {
            "http": "http://{}".format(proxy),
            "https": "https://{}".format(proxy)
        }
    url = "https://api.openai.com/v1/models"
    models = []
    try :
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        response.encoding = "utf-8"
        result = json.loads(response.text)
        response.close()
        data = result.get("data", [])
        for val in data :
            model = val.get("id", "")
            if model and "gpt-" in model :
                models.append(model)
    except Exception :
        logger.error(format_exc())

    return models


# 阿里云翻译
def aliyun(access_key_id, access_key_secret, source_language, text_to_translate, logger) :

    if access_key_id == "" or access_key_secret == "" :
        return False, "私人阿里: 还未填入私人密钥, 不可使用. 请在设置-翻译设定-私人翻译中注册阿里云并填入密钥后重试"

    source_language_map = {
        "JAP": "ja",
        "ENG": "en",
        "KOR": "ko",
        "RU": "ru",
    }
    # 语种解释适配
    if source_language in source_language_map :
        source_language = source_language_map[source_language]

    # 请求参数
    api_url = "https://mt.aliyuncs.com"
    api_version = "2018-10-12"
    format_type = "text"
    # 构建请求参数
    params = {
        "AccessKeyId": access_key_id,
        "Action": "Translate",
        "FormatType": format_type,
        "Version": api_version,
        "SourceLanguage": source_language,
        "TargetLanguage": "zh",
        "SourceText": text_to_translate,
        "Scene": "general",
        "Format": "JSON",
        "Timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": str(time.time()),
    }
    try :
        # 对请求参数按照字母顺序进行排序
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        # 构建待签名的字符串
        canonicalized_query_string = ""
        for k, v in sorted_params :
            canonicalized_query_string += "&" + urllib.parse.quote(k, safe="") + "=" + urllib.parse.quote(v, safe="")
        # 构建待签名的字符串
        string_to_sign = "GET&%2F&" + urllib.parse.quote(canonicalized_query_string[1:], safe="")
        # 计算签名
        hmac_sha1 = hmac.new((access_key_secret + "&").encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha1)
        signature = base64.b64encode(hmac_sha1.digest()).decode("utf-8")
        # 添加签名到请求参数中
        params["Signature"] = signature
    except Exception as err :
        logger.error(format_exc())
        return False, "私人阿里: 生成签名出错-{}, 请排查完错误后重试".format(err)

    try :
        # 发送HTTP请求
        response = requests.get(api_url, params=params)
        # 读取响应内容
        response_content = response.json()
        if response_content.get("Code", "") == "200" :
            response_content = response_content.get("Data", {}).get("Translated", "")
        else :
            return False, "私人阿里: 翻译出错-{}, 请排查完错误后重试".format(response_content.get("Message", "我抽风啦, 请尝试重新翻译!"))
    except Exception as err :
        logger.error(format_exc())
        return False, "私人阿里: 翻译出错-{}, 请排查完错误后重试".format(err)

    return True, response_content