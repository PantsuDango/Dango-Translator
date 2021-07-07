'''
    @author: harumonia
    :@url: http://harumonia.top
    :copyright: © 2020 harumonia<zxjlm233@gmail.com>
    :@site:
    :@datetime: 2020/7/9 21:05
    :@software: PyCharm
    :@description: None
'''

import ctypes
import math
import re
from traceback import print_exc

import requests


class BaiduTranslator:
    """
    通过JS解密实现的百度翻译
    """

    def __init__(self):
        self.req = requests.Session()
        self.req.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'cookie': 'BAIDUID=B27294F1569BB6465ED40FF870EF88C8:FG=1;',
        }

    def run(self, query):
        """
        执行函数
        @param query: 查询的语句 （一行）
        @return:
        """
        try:
            # 尚未明确cookie的生命周期，暂且写死，观察后续
            # req.get('https://www.baidu.com/')
            response_gtk = self.req.get('https://fanyi.baidu.com/')
            gtk = re.findall(r"gtk = '(\d+.\d+)'", response_gtk.text)[0]
            token = re.findall(r"token: '(.*)'", response_gtk.text)[0]

            lan, to = self.lang_detect(query)

            params = (
                ('from', lan),
                ('to', to),
            )

            data = {
                'from': lan,
                'to': 'zh',
                'query': query,
                'transtype': 'realtime',
                'simple_means_flag': '3',
                'sign': self.e_encryption(query, gtk),
                'token': token,
                'domain': 'common'
            }

            response = self.req.post('https://fanyi.baidu.com/v2transapi', params=params, data=data, timeout=5)
            result = response.json()["trans_result"]["data"][0]["dst"]
        except Exception as _e:
            print(_e)
            print_exc()
            result = '网页百度：我抽风啦！'

        return result

    def lang_detect(self, query):
        """
        获取带翻译语种
        @param query:
        @return:
        """

        lang_resp = self.req.post("https://fanyi.baidu.com/langdetect", data={"query": query})
        lan = lang_resp.json()["lan"]
        to = "en" if lan == "zh" else "zh"

        return lan, to

    @staticmethod
    def int_overflow(val):
        maxint = 2147483647
        if not -maxint - 1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val

    @staticmethod
    def unsigned_left_shitf(n, i):
        if n < 0:
            n = ctypes.c_uint32(n).value
        if i < 0:
            return -(BaiduTranslator.int_overflow(n >> abs(i)))
        return BaiduTranslator.int_overflow(n << i)

    def e_encryption(self, r_mat, gtk):
        """
        js解密
        @param r_mat:
        @param gtk:
        @return:
        """

        def n_encryption(r_sub, o):
            for t in range(0, len(o) - 2, 3):
                a = o[t + 2]
                a = ord(a) - 87 if a >= "a" else int(a)
                a = r_sub >> a if o[t + 1] == "+" else BaiduTranslator.unsigned_left_shitf(r_sub, a)
                r_sub = r_sub + a & 4294967295 if o[t] == "+" else r_sub ^ a
            return r_sub

        if len(r_mat) > 30:
            r_mat = "" + r_mat[:10] + r_mat[math.floor(len(r_mat) / 2) - 5: math.floor(len(r_mat) / 2) + 5] + r_mat[
                                                                                                              -10:]
        u = gtk
        m, s = u.split('.')
        ss, c, v = [], 0, 0
        while v < len(r_mat):
            aa = ord(r_mat[v])
            if aa < 128:
                ss.append(aa)
            else:
                if 2048 > aa:
                    ss.append(aa >> 6 | 192)  # 考虑无符号
                else:
                    if 55296 == (64512 & aa) and v + 1 < len(r_mat) and 56320 == (64512 & ord(r_mat[v + 1])):
                        v += 1
                        aa = 65536 + ((1023 & aa) << 10) + (1023 & ord(r_mat[v]))
                        ss.append(aa >> 18 | 240)
                        ss.append(aa >> 12 & 64 | 128)
                    else:
                        ss.append(aa >> 12 | 224)
                        ss.append(aa >> 6 & 63 | 128)
                        ss.append(63 & aa | 128)
            v += 1
        F = "+-a^+6"
        D = "+-3^+b+-f"
        p = int(m)
        for b in range(len(ss)):
            p += ss[b]
            p = n_encryption(p, F)
        p = n_encryption(p, D)
        p ^= int(s)
        if 0 > p:
            p = (2147483647 & p) + 2147483648
        p %= int(1e6)
        return str(p) + "." + str(p ^ int(m))


if __name__ == '__main__':
    r = "ブリテンの伝説の王。騎士王とも。アルトリアは幼名であり、王として起ってからは アーサー王と呼ばれる事になった。"

    res = BaiduTranslator().run(r)
    print(res)