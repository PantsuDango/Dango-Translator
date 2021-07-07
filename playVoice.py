import urllib.parse
from requests import Session
from playsound import playsound
from traceback import print_exc
import json
from js2py import EvalJs


class Voice():

    def __init__(self, text):

        self.text = text
        self.session = Session()
        self.session.keep_alive = False

        self.headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
                        "Referer": "https://translate.google.cn/"
                       }

        self.play_voice()


    def getTk(self):
        
        with open('.\\config\\GoogleJS.js', encoding='utf8') as f:
            js_data = f.read()

        context = EvalJs()
        context.execute(js_data)
        tk = context.TL(self.text)
        
        return tk


    def play_voice(self):

        with open('.\\config\\settin.json') as file:
            data = json.load(file)

        try:
            content = urllib.parse.quote(self.text)
            tk = self.getTk()
            url = "https://translate.google.cn/translate_tts?ie=UTF-8&q="+content+"&tl=" +data["BingLanguage"]+ "&total=1&idx=0&textlen=107&tk="+tk+"&client=webapp&prev=input"
            res = self.session.get(url, headers=self.headers)
    
            with open('.\\config\\voice.mp3', 'wb') as file:
                file.write(res.content)
            playsound('.\\config\\voice.mp3')
        
        except Exception:
            print_exc()


if __name__ == '__main__' :

    # ja en ko 
    #Voice("다음은 서울에 있는 동네 이름에 얽힌 이야기이다.")
    #Voice("Hooray! It's snowing! It's time to make a snowman.James runs out. He makes a big pile of snow. He puts a big snowball on top.")
    Voice("そうすると、可笑しいことや変なこと、滑稽なことや正しくないこと、反対にやるべきことが见えてくるから。とにかく、何かにどっぷりはまっていると、周りのことが见えなくなってしまう。だから、时々一歩引くと物事が见えてくる。")     