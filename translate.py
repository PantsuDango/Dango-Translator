from PIL import ImageGrab

import requests
import base64

import http.client
import hashlib
import urllib
import random
import json
import os
import time

import tkinter
import tkinter.messagebox

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.tmt.v20180321 import tmt_client, models
import re


def get_Access_Token(path):

    with open(path+'ORC_Key.txt') as file:
        client_id,client_secret = file.read().split(',')

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(client_id, client_secret)
    response = requests.get(host)
    if response:
        try:
            access_token = response.json()['access_token']
        except Exception:
            error = response.json()["error"]
            error_description = response.json()["error_description"]
            tkinter.messagebox.showerror(title='error', message='error：%s\nerror_description：%s'%(error,error_description))

        else:
            with open(path+'Access_Token.txt','w') as file:
                file.write(access_token)
            return access_token
    else:
        tkinter.messagebox.showerror(title='error', message='未能连接获取ORC access_token，请检查ORC API设置！')


def image_cut(path):
   
    with open(path+'屏幕坐标.txt') as file:
        coordinates = file.read().split(',')
    bbox = tuple(int(coordinate) for coordinate in coordinates)

    image = ImageGrab.grab(bbox)
    image.save(path+'image.png')


def baidu_orc(path,access_token):

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    f = open(path+'image.png', 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img,
              "language_type":"JAP"}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        try:
            words = response.json()['words_result']
        
        except Exception:
            error_code = response.json()["error_code"]
            error_msg = response.json()["error_msg"]
            tkinter.messagebox.showerror(title='error', message='error_code：%s\nerror_msg：%s'%(error_code,error_msg))
        else:
            sentence = ''
            for word in words:
                sentence += word['words']
            return sentence
    else:
        tkinter.messagebox.showerror(title='error', message='未能连接ORC接口，请检查网络设置！')
    


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
        html = json.loads(res.text)
    except Exception:
        result = ' '
    else:
        result = ''
        for tgt in html['translateResult'][0]:
            result += tgt['tgt']
    return result


def baidu(sentence,path):

    with open(path+'Baidu_Key.txt') as file:  
        appid,secretKey = file.read().split(',')

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'jp'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    q = sentence
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
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
        tkinter.messagebox.showerror(title='error', message='百度翻译appid或secretKey设置错误！')
        string = ' '
    finally:
        if httpClient:
            httpClient.close()

    return string


def tencent(sentence,path):

    with open(path+'Tencent_Key.txt') as file:
        secretId,secretKey = file.read().split(',')

    try: 
        cred = credential.Credential(secretId, secretKey) 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile) 

        req = models.TextTranslateRequest()
        params = '{"SourceText":"%s","Source":"jp","Target":"zh","ProjectId":0}'%(sentence)
        req.from_json_string(params)

        resp = client.TextTranslate(req)
        result = re.findall(r'"TargetText": "(.+?)"', resp.to_json_string())[0]

    except TencentCloudSDKException as err: 
        result = ' '
    
    return result


def translate_main(Text,window):

    path = os.getcwd() + '\\config\\'
    try:
        with open(path+'Access_Token.txt') as file:
            access_token = file.read()
    except FileNotFoundError:
        get_Access_Token(path)
    
    with open(path+'Init.txt') as file:  
        value1,value2,value3,value4 = file.read().split(',')
    
    if access_token:
        
        if value2 == '1':
            image_cut(path)
            sentence = baidu_orc(path,access_token)

            if value1 == '1':
                result = youdao(sentence)
            elif value1 == '2':
                result = baidu(sentence,path)
            elif value1 == '3':
                result = tencent(sentence,path)

            if value4 == '1':
                result = result + '\n\n' + sentence
            
            Text.delete(1.0,tkinter.END)
            Text.insert(1.0,result)
        
        elif value2 == '2':
            
            while True:
                image_cut(path)
                sentence = baidu_orc(path,access_token)

                if value1 == '1':
                    result = youdao(sentence)
                elif value1 == '2':
                    result = baidu(sentence,path)
                elif value1 == '3':
                    result = tencent(sentence,path)
                if value4 == '1':
                    result = result + '\n\n' + sentence

                Text.delete(1.0,tkinter.END)
                Text.insert(1.0,result)
                window.update()
                sec = int(value3)
                time.sleep(sec-1)
                
    else:
        pass