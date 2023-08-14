# -*- coding: utf-8 -*-
import time
import traceback

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
import translator.huoshan

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
import random
import datetime

# 私人有道翻译错误码对照
YOUDAO_ERROR_CODE_MAP = {
    '101': '缺少必填的参数',
    '102': '不支持的语言类型',
    '103': '翻译文本过长',
    '104': '不支持的API类型',
    '105': '不支持的签名类型',
    '106': '不支持的响应类型',
    '107': '不支持的传输加密类型',
    '108': 'appKey无效',
    '109': 'batchLog格式不正确',
    '110': '无相关服务的有效实例',
    '111': '开发者账号无效',
    '201': '解密失败，可能为DES,BASE64,URLDecode的错误',
    '202': '签名检验失败',
    '203': '访问IP地址不在可访问IP列表',
    '205': '请求的接口与应用的平台类型不一致',
    '206': '因为时间戳无效导致签名错误',
    '207': '重放请求',
    '301': '辞典查询失败',
    '302': '翻译查询失败',
    '303': '服务端的其他异常',
    '401': '账户已经欠费停',
    '411': '访问频率受限,请稍后访问',
    '412': '长请求过于频繁，请稍后访问',
    '413': '账户已经欠费停',
    '414': '账户已经欠费停',
    '415': '账户已经欠费停',
    '416': '账户已经欠费停',
    '420': '账户已经欠费停',
    '430': '账户已经欠费停',
    '436': '账户已经欠费停',
    '501': '词典查询失败',
    '502': '词典查询失败',
    '503': '词典查询失败',
    '504': '词典查询失败',
}
# 私人ChatGPT默认话术
CHATGPT_PROMPT = "你是一个翻译引擎。\n" \
                 "根据原文逐行翻译，将每行原文翻译为简体中文。\n" \
                 "保留每行文本的原始格式，并根据所需格式输出翻译后的文本。\n" \
                 "在翻译文本时，请严格注意以下几个方面：\n" \
                 "首先，一些完整的文本可能会被分成不同的行。请严格按照每行的原始文本进行翻译，不要偏离原文。\n" \
                 "其次，无论句子的长度如何，每行都是一个独立的句子，确保不要将多行合并成一个翻译。\n" \
                 r'''第三，在每行文本中，转义字符（例如\, \r, 和\n）或非日语内容（例如数字、英文字母、特殊符号等）不需要翻译或更改，应保持原样。'''
# 私人小牛错误码
XIAONIU_ERROR_CODE_MAP = {
    "10000": "输入为空",
    "10001": "请求频繁，超出QPS限制",
    "10003": "请求字符串长度超过限制",
    "10005": "源语编码有问题，非UTF-8",
    "13001": "字符流量不足或者没有访问权限",
    "13002": "apikey参数不可以是空",
    "13003": "内容过滤异常",
    "13007": "语言不支持",
    "13008": "请求处理超时",
    "14001": "分句异常",
    "14002": "分词异常",
    "14003": "后处理异常",
    "14004": "对齐失败，不能够返回正确的对应关系",
    "000000": "请求参数有误，请检查参数",
    "000001": "Content-Type不支持【multipart/form-data】"
}
# chatgpt的当前使用时间
CHATGPT_USE_TIME = 0
# chatgpt联系上下文句子数组
CHATGPT_CONTEXT_LIST = []

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

    text = "私人彩云: "
    try:
        resp = requests.request("POST", url, data=json.dumps(payload), headers=headers, proxies=proxies, timeout=5)
        resp = json.loads(resp.text)
        if "target" in resp :
            # 翻译成功
            text = "\n".join(resp["target"])
        else :
            # 翻译失败
            message = resp.get("message", "我抽风啦, 请尝试重新翻译!")
            if message == "Invalid token" :
                message =  "无效的令牌"
            text += message
            logger.error(text)
    except Exception :
        logger.error(format_exc())
        text = "私人彩云: 我抽风啦, 请尝试重新翻译!"

    return text


# ChatGPT翻译
def chatgpt(object, content, delay_time=0) :

    # 获取配置
    api_key = object.config["chatgptAPI"]
    proxy = object.config["chatgptProxy"]
    url = object.config["chatgptApiAddr"]
    model = object.config["chatgptModel"]
    prompt = object.config["chatgptPrompt"]
    context_use = object.config["chatgptContextUse"]
    context_count = object.config["chatgptContextCount"]
    logger = object.logger

    global CHATGPT_USE_TIME, CHATGPT_CONTEXT_LIST
    if not api_key :
        return "私人ChatGPT: 还未填入私人ChatGPT密钥, 不可使用"

    messages = [{"role": "system", "content": prompt}]
    try :
        # 计算上下文最大长度
        if len(CHATGPT_CONTEXT_LIST) > context_count * 2:
            CHATGPT_CONTEXT_LIST = CHATGPT_CONTEXT_LIST[-context_count * 2:]
        # 添加上下文
        if context_use :
            messages += CHATGPT_CONTEXT_LIST
    except Exception :
        logger.error(format_exc())
    messages.append({"role": "user", "content": content})

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
    if proxy :
        proxies = {
            "http": "http://{}".format(proxy),
            "https": "https://{}".format(proxy)
        }

    text = "私人ChatGPT: "

    try :
        # 如果需要延时
        sub_time = time.time() - CHATGPT_USE_TIME
        if delay_time > 0 and sub_time < delay_time :
            time.sleep(delay_time - sub_time)

        response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies, timeout=30)
        response.encoding = "utf-8"
        result = json.loads(response.text)
        response.close()

        if result.get("error", {}).get("message", "") :
            # 翻译出错
            error = result.get("error", {}).get("message", "")
            if "Rate limit reached" in error :
                text += "请求次数超限制, 请稍后重试, 或使用不带次数限制的密钥"
            elif "You can find your API key" in error :
                text += "无效的密钥, 请检查密钥是否正确"
            elif "You exceeded your current quota" in error :
                text += "账户额度已耗尽, 请检查账户确保有额度后重试"
            elif "Invalid URL" in error :
                text += "请求失败, 无效的API接口地址, 请检查API接口地址是否正确"
            elif re.match("The model .+? does not exist", error) :
                text += "错误的模型, {} 不存在".format(model)
            elif "deactivated account" in error :
                text += "账户已被停用, 请检查账户是否被封禁"
            else :
                text += "翻译出错: {}, 请排查完错误后重试".format(error)
        else :
            # 翻译成功
            text = result["choices"][0]["message"]["content"]
            # 记录翻译时间
            CHATGPT_USE_TIME = time.time()
            # 记录上下文
            CHATGPT_CONTEXT_LIST.append({"role": "user", "content": content})
            CHATGPT_CONTEXT_LIST.append({"role": "assistant", "content": text})

            # 判断句子数量
            content_length = len(content.split("\n"))
            text_length = len(text.split("\n"))
            # 结果过滤
            if content_length == 1 :
                text = simpleChatgptFilter(text, content)
            else :
                text = multipleChatgptFilter(text, content)

            # 句子数量对不上的情况
            if content_length > 1 and text_length != content_length :
                text_list = []
                sign = False
                # 多句子分批请求chatgpt
                for value in content.split("\n") :
                    tmp_text = chatgpt(object, value, delay_time)
                    if re.match(r"^私人ChatGPT:", tmp_text) :
                        sign = True
                        break
                    text_list.append(tmp_text)
                if not sign :
                    text = "\n".join(text_list)
                    # 结果过滤
                    text = multipleChatgptFilter(text, content)

    except requests.exceptions.ReadTimeout :
        text += "翻译超时, 如有挂载代理, 请检查代理稳定性后重试"
    except requests.exceptions.ProxyError :
        text += "代理访问错误, 请检查是否有开启代理, 且代理地址正确"
    except requests.exceptions.ConnectionError :
        text += "网络连接错误, 无法访问到ChatGPT API"
        if not proxy :
            text += ", 请尝试使用代理访问"
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


# 私人有道翻译
def youdao(text, app_key, app_secret, logger) :

    if (not app_key) or (not app_secret):
        return False, "私人有道: 还未填入私人密钥, 不可使用. 请在设置-翻译设定-私人翻译中注册私人有道并填入密钥后重试"

    url = "https://openapi.youdao.com/api"
    salt = random.randint(1, 65536)
    sign = app_key + text + str(salt) + app_secret
    sign = hashlib.md5(sign.encode()).hexdigest()
    params = {
        "q": text,
        "from": "auto",
        "to": "zh-CHS",
        "appKey": app_key,
        "salt": salt,
        "sign": sign
    }

    sign = False
    result = "私人有道: 翻译出错, "
    try :
        resp = requests.get(url, params=params)
        resp = json.loads(resp.text)
        error_code = resp.get("errorCode", "-1")

        if error_code == "0" :
            sign = True
            result = "\n".join(resp["translation"])
        elif error_code in YOUDAO_ERROR_CODE_MAP :
            result += "errorCode-{}, {}".format(error_code, YOUDAO_ERROR_CODE_MAP[error_code])
        else :
            result += "errorCode-{}".format(error_code)

    except Exception as err :
        logger.error(format_exc())
        result += str(err)

    if not sign :
        logger.error(result)

    return sign, result


# 多句子ChatGPT结果过滤
def multipleChatgptFilter(text, original) :

    new_text = text
    # 过滤原文
    for v in original.split("\n") :
        new_text = re.sub(re.escape(v), "", new_text)
    # 避免过滤后破坏原有的行数结构
    if new_text.split("\n") == text.split("\n") :
        text = new_text
    # 过滤多个换行符
    text = re.sub(r"\n{2,}", "\n", text)

    return text


# 单句子ChatGPT结果过滤
def simpleChatgptFilter(text, original) :

    # 不应该出现换行符
    text = re.sub(r"\n", "", text)
    # 无法翻译的句子
    if "请提供更多详细" in text :
        text = original

    return text


# 私人小牛翻译
def xiaoniu(apikey, sentence, language, logger) :

    if not apikey :
        return False, "私人小牛: 还未填入私人密钥, 不可使用. 请在设置-翻译设定-私人翻译中注册私人小牛并填入密钥后重试"

    url = "http://api.niutrans.com/NiuTransServer/translation?"
    language_map = {
        "JAP": "ja",
        "ENG": "en",
        "KOR": "ko",
        "RU": "ru",
    }
    if language in language_map :
        language = language_map[language]
    data = {
        "from": language,
        "to": "zh",
        "apikey": apikey,
        "src_text": sentence
    }
    sign = False
    result = "私人小牛: 翻译出错, "
    try :
        data_en = urllib.parse.urlencode(data)
        req = url + "&" + data_en
        res = urllib.request.urlopen(req)
        res = res.read()
        res_dict = json.loads(res)
        if "tgt_text" in res_dict :
            result = res_dict["tgt_text"]
            sign = True
        else :
            error_code = res_dict["error_code"]
            error_msg = XIAONIU_ERROR_CODE_MAP.get(error_code, res_dict["error_msg"])
            result += "error_code-{}, {}".format(error_code, error_msg)

    except Exception as err :
        logger.error(format_exc())
        result += str(err)

    if not sign :
        logger.error(result)

    return sign, result


# 私人火山
def huoshan(ak, sk, text, logger) :

    if not ak or not sk :
        return False, "私人火山: 还未填入私人密钥, 不可使用. 请在设置-翻译设定-私人翻译中注册私人火山并填入密钥后重试"

    params = {
        "Action": "TranslateText",
        "Version": "2020-06-01"
    }
    body = {
        "TargetLanguage":"zh",
        "TextList": text.split("\n")
    }
    url = "https://translate.volcengineapi.com/"

    sign = False
    result = "私人火山: 翻译出错, "
    try :
        resp = requests.post(
            url=url,
            headers=translator.huoshan.header(ak, sk, text),
            params=params,
            data=json.dumps(body)
        ).json()

        # 请求成功
        if "TranslationList" in resp :
            text_list = []
            for val in resp["TranslationList"] :
                if not val.get("Translation", "") :
                    continue
                text_list.append(val["Translation"])
            result = "\n".join(text_list)
            sign = True
        else :
            # 请求失败
            error_map = resp.get("ResponseMetadata", {}).get("Error", {})
            code_n = error_map.get("CodeN", 0)
            code = error_map.get("Code", "")
            message = error_map.get("Message", "")
            if code_n and code and message :
                result += "CodeN-{}, Code-{}, {}".format(code_n, code, message)
            else :
                result += str(resp)

    except Exception as err :
        logger.error(format_exc())
        result += str(err)

    if not sign :
        logger.error(result)

    return sign, result