import requests
from base64 import b64encode

from http.client import HTTPConnection
from hashlib import md5
from urllib import parse
from random import randint
from json import loads

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models
from re import findall

import interface
import tkinter.messagebox


def get_Access_Token():

    data = interface.get_config()
    client_id = data['OCR']['Key']
    client_secret = data['OCR']['Secret']

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(client_id, client_secret)
    try:
        response = requests.get(host)
    except Exception:
        tkinter.messagebox.showerror(title='警告：网络连接失败', message='网络连接失败，请确保网络连接正常后重试\n若网络连接正常，请尝试重启路由器')
    else:
        if response:
            try:
                access_token = response.json()['access_token']
            except KeyError:
                error = response.json()["error"]
                error_description = response.json()["error_description"]
                if error_description == 'unknown client id':
                    tkinter.messagebox.showerror(title='invalid_client', message='OCR API Key 不正确')
                elif error_description == 'Client authentication failed':
                    tkinter.messagebox.showerror(title='invalid_client', message='OCR Secret Key 不正确')
                else:
                    tkinter.messagebox.showerror(title=error, message=error_description)
            else:
                data['AccessToken'] = access_token
                interface.save_config(data)

        else:
            tkinter.messagebox.showerror(title='error', message='OCR连接失败，请检查 设置 的 OCR API Key \n以及 OCR Secret Key 是否填写正确！')


def baidu_orc():

    data = interface.get_config()
    access_token = data['AccessToken']
    
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    f = open('.\\config\\image.png', 'rb')
    img = b64encode(f.read())

    params = {"image":img,
              "language_type":"JAP"}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(request_url, data=params, headers=headers)
    except Exception:
        tkinter.messagebox.showwarning(title='警告：网络连接失败', message='网络连接失败，请确保网络连接正常后重试\n若网络连接正常，请尝试重启路由器')
        sentence = ' '
        return sentence
    else:
        if response:
            try:
                words = response.json()['words_result']
        
            except KeyError:
                error_code = response.json()["error_code"]
                error_msg = response.json()["error_msg"]
                if error_code == 6:
                    tkinter.messagebox.showerror(title='OCR错误%s'%error_code, message='请检查你的 OCR API 注册的是否为 文字识别 而非其他类型\n并检查OCR API Key 以及 Secret Key 是否填写正确')
                elif error_code == 18:
                    tkinter.messagebox.showerror(title='OCR错误%s'%error_code, message='请避免访问过快，手动模式放慢点击速度，自动模式降低速率')
                elif error_code == 111:
                    get_Access_Token()
                else:
                    tkinter.messagebox.showerror(title='OCR错误：%s'%error_code, message=error_msg)
                sentence = ' '
            else:
                sentence = ''
                for word in words:
                    sentence += word['words']
            return sentence


def youdao(sentence):

    sentence = sentence.replace('\n','')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    data = {'from': 'jp',
            'to': 'zh',
            'doctype': 'json',
            'type': 'AUTO',
            'i':sentence}

    url = "http://fanyi.youdao.com/translate"
    res = requests.get(url, params=data)
    try:
        html = loads(res.text)
        result = ''
        for tgt in html['translateResult'][0]:
            result += tgt['tgt']
    except Exception:
        result = ' '
    return result


def baidu(sentence):

    data = interface.get_config()
    appid = data['BaiduAPI']['Key']
    secretKey = data['BaiduAPI']['Secret']

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
        result = loads(result_all)

        string = ''
        for word in result['trans_result']:
            if word == result['trans_result'][-1]:
                string += word['dst']
            else:
                string += word['dst'] + '\n'
        
    except KeyError:
        if result['error_code'] == '54003':
            tkinter.messagebox.showerror(title='百度翻译错误：访问频率受限', message='请避免访问过快，手动模式放慢点击速度，自动模式降低速率\n另外请确保自己的百度翻译注册时为高级版，若不是请自行升级\n确认地址：https://api.fanyi.baidu.com/api/trans/product/desktop')
        elif result['error_code'] == '52001':
            tkinter.messagebox.showerror(title='百度翻译错误：请求超时', message='请求超时，请重试')
        elif result['error_code'] == '52002':
            tkinter.messagebox.showerror(title='百度翻译错误：系统错误', message='系统错误，请重试')
        elif result['error_code'] == '52003':
            tkinter.messagebox.showerror(title='百度翻译错误：未授权用户', message='请检查 设置-百度翻译-设定 中的 APPID 和 密钥 是否填写正确\n如未注册，注册方式详见翻译器目录下的百度翻译注册方法')
        elif result['error_code'] == '54000':
            pass
        elif result['error_code'] == '54001':
            tkinter.messagebox.showerror(title='百度翻译错误：未授权用户', message='请检查 设置-百度翻译-设定 中的 APPID 和 密钥 是否填写正确\n如未注册，注册方式详见翻译器目录下的百度翻译注册方法')
        elif result['error_code'] == '54004':
            tkinter.messagebox.showerror(title='百度翻译错误：账户余额不足', message='请前往百度翻译API-管理控制台为账户充值')
        elif result['error_code'] == '54005':
            tkinter.messagebox.showerror(title='百度翻译错误：长query请求频繁', message='请降低长query的发送频率，3s后再试')
        elif result['error_code'] == '58000':
            tkinter.messagebox.showerror(title='百度翻译错误：客户端IP非法', message='检查个人资料里填写的IP地址是否正确\n可前往开发者信息-基本信息修改\nIP限制，IP可留空')
        elif result['error_code'] == '58001':
            tkinter.messagebox.showerror(title='百度翻译错误：译文语言方向不支持', message='检查译文语言是否在语言列表里')
        elif result['error_code'] == '58002':
            tkinter.messagebox.showerror(title='百度翻译错误：服务当前已关闭', message='请前往管理控制台开启服务')
        elif result['error_code'] == '90107':
            tkinter.messagebox.showerror(title='百度翻译错误：认证未通过或未生效', message='请前往我的认证查看认证进度')
        else:
            tkinter.messagebox.showerror(title='百度翻译错误：%s'%result['error_code'], message=result['error_msg'])
        string = ' '
    finally:
        if httpClient:
            httpClient.close()

    return string


def tencent(sentence):

    data = interface.get_config()
    secretId = data['TencentAPI']['Key']
    secretKey = data['TencentAPI']['Secret']

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
        result = findall(r'"TargetText": "(.+?)"', resp.to_json_string())[0]

    except TencentCloudSDKException as err: 
        err = str(err)
        code = findall(r'code:(.*?) message', err)[0]
        message = findall(r'message:(.+?) requestId', err)[0]
        if code == 'MissingParameter':
            pass
        elif code == 'FailedOperation.NoFreeAmount':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='本月免费额度已用完')
        elif code == 'FailedOperation.ServiceIsolate':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='账号因为欠费停止服务，请在腾讯云账户充值') 
        elif code == 'FailedOperation.UserNotRegistered':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='服务未开通，请在腾讯云官网机器翻译控制台开通服务')
        elif code == 'InternalError':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='内部错误')
        elif code == 'InternalError.BackendTimeout':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='后台服务超时，请稍后重试')
        elif code == 'InternalError.ErrorUnknown':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='未知错误')
        elif code == 'LimitExceeded':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='超过配额限制')
        elif code == 'UnsupportedOperation':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='操作不支持')
        elif code == 'InvalidCredential':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='secretId 或 secretKey 错误，请检查是否填写正确')
        elif code == 'AuthFailure.SignatureFailure':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='secretKey 错误，请检查是否填写正确')
        elif code == 'AuthFailure.SecretIdNotFound':
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message='secretId 错误，请检查是否填写正确')
        else:
            tkinter.messagebox.showerror(title='腾讯翻译错误：%s'%code, message=message)
        result = ' '
    except IndexError:
        result = ' '
    return result