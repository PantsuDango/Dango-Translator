import requests
import hashlib
import time
import random

# 有道翻译
class YDDict():

    # 获取加密参数
    @staticmethod
    def get_data(keyword):
        md = hashlib.md5()
        lts = str(int(time.time() * 1000))
        salt = lts + str(random.randrange(10))
        md.update("fanyideskweb{}{}Tbh5E8=q6U3EXe+&L[4c@".format(keyword, salt).encode("utf8"))
        sign = md.hexdigest()
        return lts, salt, sign

    # 翻译
    def translate(self, keyword):
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
            "Referer": "https://fanyi.youdao.com/",
            "Host": "fanyi.youdao.com",
            "Origin": "https://fanyi.youdao.com",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
        lts, salt, sign = self.get_data(keyword)
        data = {
            "i": keyword,
            "from": "AUTO",
            "to": "zh-CHS",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": lts,
            "bv": "1744f6d1b31aab2b4895998c6078a934",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }

        content = "公共有道: 我抽风啦, 请尝试重新翻译! 如果频繁出现, 建议直接注册使用私人翻译"
        try :
            resp = requests.post(url, headers=headers, data=data).json()
            error_code = resp["errorCode"]
            if error_code == 0 :
                trans = resp["translateResult"][0]
                content = ""
                for val in trans :
                    content += val["tgt"]

        except Exception :
            pass

        return content

if __name__ == "__main__" :

    jap = "に傍にいてくれるものではありません。ちょっとしたきっかけで、いなくなってしまうものです。"
    eng = "Time goes by so fast, people go in and out of your life. You must never miss the opportunity to tell these people how much they mean to you"
    kor = "어느 날 임금님께서 신하들 과 나라의 이곳저곳 을 시찰하게 됐습니다. 그러던 중 어느 시골의 넓은 들판에 이르렀는데, 그곳에는 많은 염소 떼가 있었습니다."
    rus = "Я понял, что и я получил подаяние от моего брата."
    youdao = YDDict()
    content = youdao.translate(eng)
    print(content)