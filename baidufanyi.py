# 面向对象
# 百度翻译 -- 网页版(自动获取token,sign)
import requests
import js2py
import json
import re
from traceback import print_exc


class BaiduWeb():
    
    """百度翻译网页版爬虫"""
    
    def __init__(self, query_str):
        self.session = requests.session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        }
        self.session.headers = headers
        self.baidu_url = "https://www.baidu.com/"
        self.root_url = "https://fanyi.baidu.com/"
        self.lang_url = "https://fanyi.baidu.com/langdetect"
        self.trans_url = "https://fanyi.baidu.com/v2transapi"
        self.query_str = query_str


    def get_token_gtk(self):
        
        '''获取token和gtk(用于合成Sign)'''
        
        self.session.get(self.root_url)
        resp = self.session.get(self.root_url)
        html_str = resp.content.decode()
        token = re.findall(r"token: '(.*?)'", html_str)[0]
        gtk = re.findall(r"window.gtk = '(.*?)'", html_str)[0]
        
        return token,gtk


    def generate_sign(self,gtk):
        
        """生成sign"""
        # 1. 准备js编译环境
        
        context = js2py.EvalJs()
        with open('.\\config\\webtrans.js', encoding='utf8') as f:
            js_data = f.read()
            js_data = re.sub("window\[l\]",'"'+gtk+'"',js_data)
            # js_data = re.sub("window\[l\]", "\"{}\"".format(gtk), js_data)
            # print(js_data)
            context.execute(js_data)
        sign = context.e(self.query_str)
       
        return sign


    def lang_detect(self):
        
        '''获取语言转换类型.eg: zh-->en'''
        
        lang_resp = self.session.post(self.lang_url,data={"query":self.query_str})
        lang_json_str = lang_resp.content.decode()  # {"error":0,"msg":"success","lan":"zh"}
        lan = json.loads(lang_json_str)['lan']
        to = "en" if lan == "zh" else "zh"
        
        return lan,to


    def parse_url(self,post_data):
        
        trans_resp = self.session.post(self.trans_url,data=post_data)
        trans_json_str = trans_resp.content.decode()
        trans_json = json.loads(trans_json_str)
        self.result = trans_json["trans_result"]["data"][0]["dst"]


    def run(self):

        try:
            """实现逻辑"""
            # 1.获取百度的cookie,(缺乏百度首页的cookie会始终报错998)
            self.session.get(self.baidu_url)
            # 2. 获取百度翻译的token和gtk(用于合成sign)
            token, gtk = self.get_token_gtk()
            # 3. 生成sign
            sign = self.generate_sign(gtk)
            # 4. 获取语言转换类型.eg: zh-->en
            lan, to = self.lang_detect()
            # 5. 发送请求,获取响应,输出结果
            post_data = {
                #"from": lan,
                "from": lan,
                "to": to,
                "query": self.query_str,
                "transtype": "realtime",
                "simple_means_flag": 3,
                "sign": sign,
                "token": token
            }
            self.parse_url(post_data)
        
        except Exception:
            print_exc()
            self.result = '网页百度：我抽风啦！'
        
        return self.result


if __name__ == '__main__':
    
    webfanyi = BaiduWeb('一歩ひくと见えてくる 何かの中にどっぷり浸かっていると何がなんだか分からなくなってしまうことがある。')
    a = webfanyi.run()
    print(a)