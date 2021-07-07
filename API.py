# -*- coding: utf-8 -*-

import requests
from base64 import b64encode

from http.client import HTTPConnection
from hashlib import md5
from urllib import parse
from random import randint
import json
import os


from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from traceback import print_exc


# 出错时停止翻译状态
def error_stop():

    with open('.\\config\\settin.json') as file:
        data = json.load(file)
    if data["sign"] % 2 == 0:
        data["sign"] = 1
        with open('.\\config\\settin.json','w') as file:
            json.dump(data, file)


# 错误提示窗口
def MessageBox(title, text):

    error_stop()  # 停止翻译状态
    
    messageBox = QMessageBox()
    messageBox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    # 窗口图标
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("./config/图标.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
    messageBox.setWindowIcon(icon)
    # 设定窗口标题和内容
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.addButton(QPushButton('好滴'), QMessageBox.YesRole)
    # 显示窗口
    messageBox.exec_()


# 获取访问百度OCR用的token
def get_Access_Token():

    # 获取密钥id和secret
    with open('.\\config\\settin.json') as file:
        data = json.load(file)
    client_id = data['OCR']['Key']
    client_secret = data['OCR']['Secret']

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(client_id, client_secret)
    try:
        response = requests.get(host)
    
    except TypeError:
        print_exc()
        MessageBox('文件路径错误', '请将翻译器目录的路径设置为纯英文\n否则无法在非简中区的电脑系统下运行使用')
        return 0  # 返回失败标志
    
    except Exception:
        print_exc()
        MessageBox('OCR错误', '啊咧... Σ(っ°Д°;)っ OCR连接失败惹 (つД`)\n请打开“网络和Internet设置”的代理页面\n将其中的全部代理设置开关都关掉呢 (˘•ω•˘)')
        return 0  # 返回失败标志
    else:
        if response:
            try:
                access_token = response.json()['access_token']
            except Exception:
                print_exc()
                error = response.json()["error"]
                error_description = response.json()["error_description"]
                
                if error_description == 'unknown client id':
                    MessageBox("OCR错误", "你的OCR API Key填错啦 ヽ(#`Д´)ﾉ")
                
                elif error_description == 'Client authentication failed':
                    MessageBox("OCR错误", "你的OCR Secret Key填错啦 ヽ(#`Д´)ﾉ")
                
                else:
                     MessageBox("OCR错误", "啊咧... Σ(っ°Д°;)っ！！！  OCR连接失败惹... (つД`)\nerror：%s\nerror_description：%s"%(error, error_description))
                return 0  # 返回失败标志
            else:
                data['AccessToken'] = access_token
                with open('.\\config\\settin.json', 'w') as file:
                    json.dump(data, file)
                return 1  # 返回成功标志
        else:
            MessageBox("OCR错误", "啊咧... Σ(っ°Д°;)っ！！！  OCR连接失败惹... (つД`)\n好好检查一下你的OCR API Key和Secret Key哪里填错了喔 (˘•ω•˘)")
            return 0  # 返回失败标志


# 百度ocr
def baidu_orc(data):

    language = data["language"]  # 翻译语种
    access_token = data['AccessToken']  # token
    highPrecision = data["highPrecision"]  # 是否使用高精度模式
    showTranslateRow = data["showTranslateRow"]  # 是否使用竖排翻译
    
    if not access_token:
        sentence = 'OCR连接失败：还未注册OCR API，不可使用'
        error_stop()
        return None, sentence
    else:
        if showTranslateRow == 'True' or highPrecision == 'True':
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic" # 高精度
        else:
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic" # 普通
        
        f = open('.\\config\\image.jpg', 'rb')
        img = b64encode(f.read())
        params = {"image": img, "language_type": language}
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
    
        try:
            response = requests.post(request_url, data=params, headers=headers)
        
        except TypeError:
            print_exc()
            sentence = '路径错误：请将翻译器目录的路径设置为纯英文，否则无法在非简中区的电脑系统下运行使用'
            error_stop()
            return None, sentence
        
        except Exception:
            print_exc()
            sentence = 'OCR连接失败：请打开【网络和Internet设置】的【代理】页面，将其中的全部代理设置开关都关掉，保证关闭后请重试'
            #error_stop()
            return None, sentence
        else:
            if response:
                try:
                    words = response.json()['words_result']
                except Exception:
                    print()
                    error_code = response.json()["error_code"]
                    error_msg = response.json()["error_msg"]
                
                    if error_code == 6:
                        sentence = 'OCR错误：检查一下你的OCR注册网页，注册的类型是不是文字识别，你可能注册到语音技术还是其它什么奇怪的东西了'
                        error_stop()
                        return None, sentence

                    elif error_code == 17:
                        if showTranslateRow == 'True':
                            sentence = 'OCR错误：竖排翻译模式每日额度已用光，请取消竖排翻译模式'
                        elif  highPrecision == 'True':
                            sentence = 'OCR错误：高精度翻译模式每日额度已用光，请取消高精度翻译模式'
                        else:
                            sentence = 'OCR错误：OCR无额度，可使用团子离线ocr'
                        error_stop()
                        return None, sentence

                    elif error_code == 18:
                        sign, sentence = baidu_orc(data)
                        return sign, sentence
                    
                    elif error_code == 111:
                        sentence = 'OCR错误：密钥过期了，请进入设置页面后按一次保存设置，以重新生成密钥'
                        error_stop()
                        return None, sentence
                    
                    elif error_code == 216202:
                        sentence = 'OCR错误：范围截取过小无法识别，请重新框选一下你要翻译的区域'
                        error_stop()
                        return None, sentence
                    
                    else:
                        sentence = 'OCR错误：%s，%s'%(error_code, error_msg)
                        error_stop()
                        return None, sentence
                
                else:
                    sentence = ''
                    
                    # 竖排翻译模式
                    if showTranslateRow == 'True':
                        if words:
                            for word in words[::-1]:
                                sentence += word['words'] + '，'
                            sentence = sentence.replace(',','')
                    
                    # 普通翻译模式
                    else:
                        for word in words:
                            sentence += word['words']
                        if sentence :
                            print("百度OCR: %s"%sentence)
                    
                    return True, sentence
            else:
                sentence = 'OCR错误：response无响应'
                return None, sentence


def dango_ocr(data) :

    url = 'http://127.0.0.1:6666/ocr/api'
    imagePath = os.path.join(os.getcwd(), "config", "image.jpg")
    language = data["language"]

    data = {
        'ImagePath': imagePath,
        'Language': language
    }

    try :
        res = requests.post(url, data=json.dumps(data))
        res.encoding = "utf-8"
        result = json.loads(res.text)

    except Exception :
        print_exc()
        error_stop()
        return None, "OCR错误：团子离线ocr未启动或运行失败"

    if result["Code"] == -1 :
        error_stop()
        return None, "OCR错误：%s"%result["Message"]

    else :
        sentence = ""
        for tmp in result["Data"] :
            if language == "ENG" :
                sentence += tmp["Words"] + " "
            else :
                sentence += tmp["Words"]

        if sentence :
            print("团子OCR: %s"%sentence)
        return True, sentence


# 有道翻译
def youdao(sentence):
    
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    data = {
            'i':sentence,
            'from':'AUTO',
            'to':'zh',
            'smartresult':'dict',
            'client':'fanyideskweb',
            'doctype':'json',
            'version':'2.1',
            'keyfrom':'fanyi.web',
            'action':'FY_BY_REALTIME',
            'typoResult':'false'
           }
    try:
        res = requests.get(url, params=data, headers=headers)
        html = json.loads(res.text)
        result = ''
        for tgt in html['translateResult'][0]:
            result += tgt['tgt']
    
    except Exception:
        print_exc()
        result = "有道：我抽风啦！"
    
    return result


# 公共彩云翻译
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
        result = "公共彩云：我抽风啦！"

    return result


# 金山翻译
def jinshan(sentence):
    
    url = 'http://fy.iciba.com/ajax.php?a=fy'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    data = {
            'f': 'auto',
            't': 'zh',
            'w': sentence
           }
    try:
        response = requests.post(url, data=data, headers=headers)
        info = response.text
        data_list = json.loads(info)
        result = data_list['content']['out']
    
    except Exception:
        print_exc()
        result = "金山：我抽风啦！"

    return result


# yeekit翻译
def yeekit(sentence, data):

    url = 'https://www.yeekit.com/site/dotranslate' 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    data = {
            'content[]': sentence,
            'sourceLang': data["yeekitLanguage"],
            'targetLang': "nzh"
            }
    try:    
        res = requests.get(url, data=data, headers=headers)
        html = res.text.encode('utf-8').decode('unicode_escape')
        result = re.findall(r'"text": "(.+?)"translate time"', html, re.S)[0]
        result = result.replace('\\', '').replace('}', '').replace(']', '').replace('"', '').replace('\n', '').replace(' ', '')
        result = result[:-1]

    except Exception:
        print_exc()
        result = "yeekit：我抽风啦！"

    return result


def ALAPI(sentence):

    url = 'https://v1.alapi.cn/api/fanyi?q=%s&from=auto&to=zh'%sentence

    try:
        res = requests.post(url)
        html = json.loads(res.text)
        result = html["data"]["trans_result"][0]["dst"]

    except Exception:
        print_exc()
        result = "ALAPI：我抽风啦！"

    return result
   


# 私人百度翻译
def baidu(sentence, data):

    appid = data['baiduAPI']['Key']
    secretKey = data['baiduAPI']['Secret']
    
    if (not appid) or (not secretKey):
        string = '私人百度：还未注册私人百度API，不可使用'
    
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
                string = "私人百度：我抽风啦！"
            elif result['error_code'] == '52001':
                string = '私人百度：请求超时，请重试'
            elif result['error_code'] == '52002':
                string = '私人百度：系统错误，请重试'
            elif result['error_code'] == '52003':
                string = '私人百度：APPID 或 密钥 不正确'
            elif result['error_code'] == '54001':
                string = '私人百度：APPID 或 密钥 不正确'
            elif result['error_code'] == '54004':
                string = '私人百度：账户余额不足'
            elif result['error_code'] == '54005':
                string = '私人百度：请降低长query的发送频率，3s后再试'
            elif result['error_code'] == '58000':
                string = '私人百度：客户端IP非法，注册时错误填入服务器地址，请前往开发者信息-基本信息修改，服务器地址必须为空'
            elif result['error_code'] == '90107':
                string = '私人百度：认证未通过或未生效'
            else:
                string = '私人百度：%s，%s'%(result['error_code'], result['error_msg'])

        finally:
            if httpClient:
                httpClient.close()

    return string



# 私人腾讯翻译
def tencent(sentence, data):

    secretId = data['tencentAPI']['Key']
    secretKey = data['tencentAPI']['Secret']

    if (not secretId) or (not secretKey):
        result = '私人腾讯：还未注册私人腾讯API，不可使用'
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
            params = params.replace('\r', '\\r').replace('\n', '\\n')
            req.from_json_string(params)

            resp = client.TextTranslate(req)
            result = re.findall(r'"TargetText": "(.+?)"', resp.to_json_string())[0]

        except TencentCloudSDKException as err: 

            try :
                err = str(err)
                code = re.findall(r'code:(.*?) message', err)[0]
                error = re.findall(r'message:(.+?) requestId', err)[0]

            except Exception:
                print_exc()
                result = '私人腾讯：我抽风啦！'

            else :
                if code == 'MissingParameter':
                    pass

                elif code == 'FailedOperation.NoFreeAmount':
                    result = "私人腾讯：本月免费额度已经用完"

                elif code == 'FailedOperation.ServiceIsolate':
                    result = "私人腾讯：账号欠费停止服务"

                elif code == 'FailedOperation.UserNotRegistered':
                    result = "私人腾讯：还没有开通机器翻译服务"

                elif code == 'InternalError':
                    result = "私人腾讯：内部错误"

                elif code == 'InternalError.BackendTimeout':
                    result = "私人腾讯：后台服务超时，请稍后重试"

                elif code == 'InternalError.ErrorUnknown':
                    result = "私人腾讯：未知错误"

                elif code == 'LimitExceeded':
                    result = "私人腾讯：超过配额限制"

                elif code == 'UnsupportedOperation':
                    result = "私人腾讯：操作不支持"

                elif code == 'InvalidCredential':
                    result = "私人腾讯：secretId或secretKey错误"

                elif code == 'AuthFailure.SignatureFailure':
                    result = "私人腾讯：secretKey错误"

                elif code == 'AuthFailure.SecretIdNotFound':
                    result = "私人腾讯：secretId错误"

                elif code == 'AuthFailure.SignatureExpire':
                    result = "私人腾讯：签名过期，请将电脑系统时间调整至准确的时间后重试"

                else:
                    result = "私人腾讯：%s，%s"%(code, error)

        except Exception :
            print_exc()
            result = '私人腾讯：我抽风啦！'
    
    result = result.replace('\\r', '\r').replace('\\n', '\n')
    return result


def caiyunAPI(sentence, data):
    
    token = data["caiyunAPI"]
    if not token:
        result = '私人彩云：还未注册私人彩云API，不可使用'
    else:
        url = "http://api.interpreter.caiyunai.com/v1/translator" 
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
            result = "私人彩云：我抽风啦！"

    return result