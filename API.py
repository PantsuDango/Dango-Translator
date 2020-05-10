# -*- coding: utf-8 -*-

import requests
from base64 import b64encode

from http.client import HTTPConnection
from hashlib import md5
from urllib import parse
from random import randint
import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models
import re

from threading import Thread
from tkinter import Tk
import tkinter.messagebox

from traceback import print_exc


def error_stop():

    with open('.\\config\\settin.json') as file:
        data = json.load(file)
    if data["sign"] % 2 == 0:
        data["sign"] = 1
        with open('.\\config\\settin.json','w') as file:
            json.dump(data, file)


def message_thread(func,*args):
    
    error_stop()
    thread = Thread(target=func, args=args) 
    thread.setDaemon(True) 
    thread.start()


def message(title, message):
    
    window = Tk()
    window.geometry("1x1+0+0")
    window.attributes('-alpha', 0)
    window.iconbitmap('.\\config\\图标.ico')
    window.title("错误提示")
    tkinter.messagebox.showinfo(title=title, message=message)
    window.destroy()


def get_Access_Token():

    with open('.\\config\\settin.json') as file:
        data = json.load(file)

    client_id = data['OCR']['Key']
    client_secret = data['OCR']['Secret']

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(client_id, client_secret)
    try:
        response = requests.get(host)
    except Exception:
        print_exc()
        message_thread(message, 'OCR错误', '啊咧... Σ(っ°Д°;)っ OCR连接失败惹 (つД`)\n请打开“网络和Internet设置”的代理页面\n将其中的全部代理设置开关都关掉呢 (˘•ω•˘)')
    else:
        if response:
            try:
                access_token = response.json()['access_token']
            except Exception:
                print_exc()
                error = response.json()["error"]
                error_description = response.json()["error_description"]
                
                if error_description == 'unknown client id':
                    message_thread(message, "OCR错误", "你的OCR API Key填错啦 ヽ(#`Д´)ﾉ")
                
                elif error_description == 'Client authentication failed':
                    message_thread(message, "OCR错误", "你的OCR Secret Key填错啦 ヽ(#`Д´)ﾉ")
                
                else:
                    message_thread(message, "OCR错误", "啊咧... Σ(っ°Д°;)っ！！！  OCR连接失败惹... (つД`)\nerror：%s\nerror_description：%s"%(error, error_description))
            else:
                data['AccessToken'] = access_token
                with open('.\\config\\settin.json', 'w') as file:
                    json.dump(data, file)
        else:
            message_thread(message, "OCR错误", "啊咧... Σ(っ°Д°;)っ！！！  OCR连接失败惹... (つД`)\n好好检查一下你的OCR API Key和Secret Key哪里填错了喔 (˘•ω•˘)")


def baidu_orc(data):

    access_token = data['AccessToken']
    if not access_token:
        get_Access_Token(window)
        sentence = ''
    else:
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
        f = open('.\\config\\image.jpg', 'rb')
        img = b64encode(f.read())
        params = {"image": img, "language_type": "JAP"}
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
    
        try:
            response = requests.post(request_url, data=params, headers=headers)
        except Exception:
            print_exc()
            message_thread(message, 'OCR错误', '啊咧... Σ(っ°Д°;)っ OCR连接失败惹 (つД`)\n请打开“网络和Internet设置”的代理页面\n将其中的全部代理设置开关都关掉呢 (˘•ω•˘)')
            sentence = ''
        else:
            if response:
                try:
                    words = response.json()['words_result']
                except Exception:
                    print_exc()
                    error_code = response.json()["error_code"]
                    error_msg = response.json()["error_msg"]
                
                    if error_code == 6:
                        message_thread(message, "OCR错误", "啊咧...OCR出错惹 (つД`)\n检查一下你的OCR注册网页，注册的类型是不是文字识别呢 ⊙(・◇・)？\n你可能注册到语音技术还是其它什么奇怪的东西啦 (˘•ω•˘)")
                    elif error_code == 18:
                        pass
                    elif error_code == 111:
                        get_Access_Token()
                    else:
                        message_thread(message, "OCR错误", "啊咧... Σ(っ°Д°;)っ！！！  OCR连接失败惹... (つД`)\nerror_code：%s\nerror_msg：%s"%(error_code, error_msg))
                    sentence = ''
                else:
                    sentence = ''
                    for word in words:
                        sentence += word['words']
    return sentence


def youdao(sentence):
    
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    data = {'i':sentence,
            'from':'AUTO',
            'to':'zh',
            'smartresult':'dict',
            'client':'fanyideskweb',
            'doctype':'json',
            'version':'2.1',
            'keyfrom':'fanyi.web',
            'action':'FY_BY_REALTIME',
            'typoResult':'false'}
    try:
        res = requests.get(url, params=data, headers=headers)
        html = json.loads(res.text)
        result = ''
        for tgt in html['translateResult'][0]:
            result += tgt['tgt']
    
    except Exception:
        print_exc()
        result = "有道翻译：我抽风啦"
    
    return result


def caiyun(sentence):
    
    url = "http://api.interpreter.caiyunai.com/v1/translator"
    token = "3975l6lr5pcbvidl6jl2"
    
    payload = {
               "source" : [sentence], 
               "trans_type" : "auto2zh",
               "request_id" : "demo",
               "detect": True,
              }
    
    headers = {
               'content-type': "application/json",
               'x-authorization': "token " + token,
              }
    try:
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        result = json.loads(response.text)['target'][0]
    
    except Exception:
        print_exc()
        result = "彩云翻译：我抽风啦"

    return result


def jinshan(sentence):
    
    url = 'http://fy.iciba.com/ajax.php?a=fy'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    data = {
            'f': 'auto',
            't': 'zh',
            'w': sentence
           }
    try:
        response = requests.post(url, data=data)
        info = response.text
        data_list = json.loads(info)
        result = data_list['content']['out']
        if not result:
            result = "金山翻译：我抽风啦"
    
    except Exception:
        print_exc()
        result = "金山翻译：我抽风啦"

    return result


def yeekit(sentence):

    url = 'https://www.yeekit.com/site/dotranslate' 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    data = {
            'content[]': sentence,
            'sourceLang': 'nja',
            'targetLang': 'nzh'
            }
    try:    
        res = requests.get(url, data=data, headers=headers)
        html = res.text.encode('utf-8').decode('unicode_escape')
        result = re.findall(r'"text": "(.+?)"translationId"', html, re.S)[0]
        result = result.replace('\\', '').replace('}', '').replace(']', '').replace('"', '').replace('\n', '').replace(' ', '')
        result = result[:-1]

    except Exception:
        print_exc()
        result = "yeekit翻译：我抽风啦"

    return result


def ALAPI(sentence):

    url = 'https://v1.alapi.cn/api/fanyi?q=%s&from=auto&to=zh'%sentence

    try:
        res = requests.post(url)
        html = json.loads(res.text)
        result = html["data"]["trans_result"][0]["dst"]

    except Exception:
        print_exc()
        result = "ALAPI翻译：我抽风啦"

    return result


def baidu(sentence, data):

    appid = data['baiduAPI']['Key']
    secretKey = data['baiduAPI']['Secret']
    if (not appid) or (not secretKey):
        message_thread(message, "百度翻译错误", '你你你你还没注册百度翻译呢 Σ(っ°Д°;)っ\n乖乖注册了才可以用哦( • ̀ω•́ )✧')
        string = ''
    else:
        httpClient = None
        myurl = '/api/trans/vip/translate'

        fromLang = 'auto'
        toLang = 'zh'
        salt = randint(32768, 65536)
        q = sentence
        sign = appid + q + str(salt) + secretKey
        sign = md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

        try:
            httpClient = HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)

            string = ''
            for word in result['trans_result']:
                if word == result['trans_result'][-1]:
                    string += word['dst']
                else:
                    string += word['dst'] + '\n'
        
        except Exception:
            print_exc()
            
            if result['error_code'] == '54003':
                string = "百度翻译：我抽风啦，调用速度太快"
            elif result['error_code'] == '52001':
                string = ''
                message_thread(message, "百度翻译错误", '主人~ 我收到了来自度娘的错误说明 (｡ŏ_ŏ)\n———— 请求超时，请重试')
            elif result['error_code'] == '52002':
                string = ''
                message_thread(message, "百度翻译错误", '主人~ 我收到了来自度娘的错误说明 (｡ŏ_ŏ)\n———— 系统错误，请重试')
            elif result['error_code'] == '52003':
                string = ''
                message_thread(message, "百度翻译错误", '啊咧... Σ(っ°Д°;)っ！！！  百度翻译调用失败惹... (つД`)\n好好检查一下你的百度翻译 APPID 和 密钥 哪里填错了喔 (˘•ω•˘)')
            elif result['error_code'] == '54000':
                pass
            elif result['error_code'] == '54001':
                string = ''
                message_thread(message, "百度翻译错误", '啊咧... Σ(っ°Д°;)っ！！！  百度翻译调用失败惹... (つД`)\n好好检查一下你的百度翻译 APPID 和 密钥 哪里填错了喔 (˘•ω•˘)')
            elif result['error_code'] == '54004':
                string = ''
                message_thread(message, "百度翻译错误", '主人~ 我收到了来自度娘的错误说明 (｡ŏ_ŏ)\n———— 账户余额不足')
            elif result['error_code'] == '54005':
                string = ''
                message_thread(message, "百度翻译错误", '主人~ 我收到了来自度娘的错误说明 (｡ŏ_ŏ)\n———— 请降低长query的发送频率，3s后再试')
            elif result['error_code'] == '90107':
                string = ''
                message_thread(message, "百度翻译错误", '主人~ 我收到了来自度娘的错误说明 (｡ŏ_ŏ)\n———— 认证未通过或未生效')
            else:
                string = ''
                message_thread(message, "百度翻译错误", '主人~ 我收到了来自度娘的错误说明 (｡ŏ_ŏ)\nerror_code：%s\nerror_msg：%s'%(result['error_code'], result['error_msg']))

        finally:
            if httpClient:
                httpClient.close()

    return string


def tencent(sentence, data):

    secretId = data['tencentAPI']['Key']
    secretKey = data['tencentAPI']['Secret']

    if (not secretId) or (not secretKey):
        message_thread(message, "腾讯翻译错误", '你你你你还没注册腾讯翻译呢 Σ(っ°Д°;)っ\n乖乖注册了才可以用哦( • ̀ω•́ )✧')
        string = ''
    else:
        try: 
            cred = credential.Credential(secretId, secretKey) 
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile) 

            req = models.TextTranslateRequest()
            sentence = sentence.replace('"',"'")
            params = '''{"SourceText":"%s","Source":"auto","Target":"zh","ProjectId":0}'''%(sentence)
            req.from_json_string(params)

            resp = client.TextTranslate(req)
            result = re.findall(r'"TargetText": "(.+?)"', resp.to_json_string())[0]

        except TencentCloudSDKException as err: 
            err = str(err)
            code = re.findall(r'code:(.*?) message', err)[0]
            error = re.findall(r'message:(.+?) requestId', err)[0]
            if code == 'MissingParameter':
                pass
            elif code == 'FailedOperation.NoFreeAmount':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说你的本月免费额度已经用完惹 (｡ŏ_ŏ)')
            elif code == 'FailedOperation.ServiceIsolate':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说你的账号因为欠费停止服务惹 (｡ŏ_ŏ)')
            elif code == 'FailedOperation.UserNotRegistered':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说你还没有开通机器翻译服务 (｡ŏ_ŏ)')
            elif code == 'InternalError':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说她内部错误惹 (｡ŏ_ŏ)')
            elif code == 'InternalError.BackendTimeout':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说她后台服务超时惹，叫你稍后重试 (｡ŏ_ŏ)')
            elif code == 'InternalError.ErrorUnknown':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说她遭受了未知错误 (｡ŏ_ŏ)')
            elif code == 'LimitExceeded':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说你超过配额限制 (｡ŏ_ŏ)')
            elif code == 'UnsupportedOperation':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说你的操作不支持 (｡ŏ_ŏ)')
            elif code == 'InvalidCredential':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说你的secretId或secretKey错误惹 (｡ŏ_ŏ)')
            elif code == 'AuthFailure.SignatureFailure':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说你的secretKey错误惹 (｡ŏ_ŏ)')
            elif code == 'AuthFailure.SecretIdNotFound':
                message_thread(message, "腾讯翻译错误", '主人~ 企鹅娘说你的secretId错误惹 (｡ŏ_ŏ)')
            else:
                message_thread(message, "腾讯翻译错误", '主人~ 我收到了来自企鹅娘的错误说明 (｡ŏ_ŏ)\nerror_code：%s\nerror_msg：%s'%(code, error))
            result = ''
        except Exception:
            print_exc()
            result = ''
    
    return result