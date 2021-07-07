# -*- coding:utf-8 -*-

import urllib.request
import urllib.parse
from requests import Session
from traceback import print_exc
from js2py import EvalJs


class GoogleTranslate():

    def __init__(self):

        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.session = Session()
        self.session.keep_alive = False
        

    def getTk(self, text):
        
        with open('.\\config\\GoogleJS.js', encoding='utf8') as f:
            js_data = f.read()

        context = EvalJs()
        context.execute(js_data)
        tk = context.TL(text)
        
        return tk


    def buildUrl(self, text ,tk):
        
        baseUrl = 'http://translate.google.cn/translate_a/single'
        baseUrl += '?client=webapp&'
        baseUrl += 'sl=auto&'
        baseUrl += 'tl=' + 'zh-CN' + '&'
        baseUrl += 'hl=zh-CN&'
        baseUrl += 'dt=at&'
        baseUrl += 'dt=bd&'
        baseUrl += 'dt=ex&'
        baseUrl += 'dt=ld&'
        baseUrl += 'dt=md&'
        baseUrl += 'dt=qca&'
        baseUrl += 'dt=rw&'
        baseUrl += 'dt=rm&'
        baseUrl += 'dt=ss&'
        baseUrl += 'dt=t&'
        baseUrl += 'ie=UTF-8&'
        baseUrl += 'oe=UTF-8&'
        baseUrl += 'clearbtn=1&'
        baseUrl += 'otf=1&'
        baseUrl += 'pc=1&'
        baseUrl += 'srcrom=0&'
        baseUrl += 'ssel=0&'
        baseUrl += 'tsel=0&'
        baseUrl += 'kc=2&'
        baseUrl += 'tk=' + str(tk) + '&'
        content = urllib.parse.quote(text)
        baseUrl += 'q=' + content
        
        return baseUrl


    def getHtml(self, session, url, headers):
        
        try:
            html = session.get(url, headers=headers, timeout=5)
            return html.json()
        except Exception:
            print_exc()
            return None


    def translate(self, text):
        
        try:
            tk = self.getTk(text)
            url = self.buildUrl(text, tk)
            result = self.getHtml(self.session, url, self.headers)
       
            if result != None:
                sentence = ''
                for i in result[0]:
                    if i[0] != None:
                        sentence += i[0]
            else:
                sentence = "谷歌：我抽风啦！"
        
        except Exception:
            print_exc()
            sentence = "谷歌：我抽风啦！"

        return sentence


if __name__ == '__main__':

    text = "そうすると、可笑しいことや変なこと、滑稽なことや正しくないこと、反対にやるべきことが见えてくるから。とにかく、何かにどっぷりはまっていると、周りのことが见えなくなってしまう。だから、时々一歩引くと物事が见えてくる。"
    google = GoogleTranslate()
    print(google.translate(text))