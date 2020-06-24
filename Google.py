# -*- coding:utf-8 -*-

import urllib.request
import urllib.parse
from requests import Session
from traceback import print_exc
from js2py import EvalJs


class GoogleTranslate():

    def __init__(self, text):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.session = Session()
        self.session.keep_alive = False
        self.text = text

    def getTk(self, text):

        with open('.\\config\\GoogleJS.js', encoding='utf8') as f:
            js_data = f.read()

        context = EvalJs()
        context.execute(js_data)
        tk = context.TL(text)
        return tk

    def buildUrl(self, text, tk):

        baseUrl = 'http://translate.google.cn/translate_a/single'
        base_data = {
            'client': 'webapp',
            'sl': 'auto',
            'tl': 'zh-CN',
            'hl': 'zh-CN',
            'dt': ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't'],
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'clearbtn': '1',
            'otf': '1',
            'pc': '1',
            'srcrom': '0',
            'ssel': '0',
            'tsel': '0',
            'kc': '2',
            'tk': f'{tk}',
        }

        baseUrl = f'{baseUrl}?{"&".join([f"{x}={y}" if isinstance(y, str) else "&".join(map(lambda m : f"{x}={m}", y)) for x, y in base_data.items()])}'
        content = urllib.parse.quote(text)
        baseUrl += 'q=' + content

        return baseUrl

    def getHtml(self, session, url, headers):

        try:
            html = session.get(url, headers=headers)
            return html.json()
        except Exception:
            print_exc()
            return None

    def translate(self):

        tk = self.getTk(text)
        url = self.buildUrl(text, tk)

        try:
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
    google = GoogleTranslate(text)
    print(google.translate())
