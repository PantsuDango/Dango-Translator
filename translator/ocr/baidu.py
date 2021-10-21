import requests
from base64 import b64encode
import json

from utils import MessageBox, saveConfig
from traceback import print_exc




# 获取访问百度OCR用的token
def get_Access_Token(config):

    # 获取密钥id和secret
    client_id = config["OCR"]["Key"]
    client_secret = config["OCR"]["Secret"]

    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"%(client_id, client_secret)
    try:
        response = requests.get(host)

    except TypeError :
        print_exc()
        MessageBox("文件路径错误", "请将翻译器目录的路径设置为纯英文\n否则无法在非简中区的电脑系统下运行使用")
        return False

    except Exception :
        print_exc()
        MessageBox("OCR错误", "啊咧... Σ(っ°Д°;)っ OCR连接失败惹 (つД`)\n请打开[网络和Internet设置]的代理页面\n将其中的全部代理设置开关都关掉呢 (˘•ω•˘)")
        return False
    else:
        if response:
            try:
                access_token = response.json()['access_token']
            except Exception :
                print_exc()
                error = response.json()["error"]
                error_description = response.json()["error_description"]

                if error_description == 'unknown client id':
                    MessageBox("OCR错误", "你的OCR API Key填错啦 ヽ(#`Д´)ﾉ")

                elif error_description == 'Client authentication failed':
                    MessageBox("OCR错误", "你的OCR Secret Key填错啦 ヽ(#`Д´)ﾉ")

                else:
                    MessageBox("OCR错误", "啊咧... Σ(っ°Д°;)っ！！！  OCR连接失败惹... (つД`)\nerror：%s\nerror_description：%s"%(error, error_description))

                return False

            else :
                # 保存AccessToken
                config["AccessToken"] = access_token
                saveConfig(config)
                return True
        else:
            MessageBox("OCR错误", "啊咧... Σ(っ°Д°;)っ！！！  OCR连接失败惹... (つД`)\n好好检查一下你的OCR API Key和Secret Key哪里填错了喔 (˘•ω•˘)")
            return False


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
            # error_stop()
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
                        sentence = 'OCR错误：%s，%s ' %(error_code, error_msg)
                        error_stop()
                        return None, sentence

                else:
                    sentence = ''

                    # 竖排翻译模式
                    if showTranslateRow == 'True':
                        if words:
                            for word in words[::-1]:
                                sentence += word['words'] + '，'
                            sentence = sentence.replace(',' ,'')

                    # 普通翻译模式
                    else:
                        for word in words:
                            sentence += word['words']
                        if sentence :
                            print("百度OCR: %s " %sentence)

                    return True, sentence
            else:
                sentence = 'OCR错误：response无响应'
                return None, sentence