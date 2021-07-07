import urllib.request
import urllib.parse
from traceback import print_exc


class BingTranslate(object):
    
    def __init__(self):
        
        self.url = "http://api.microsofttranslator.com/v2/ajax.svc/TranslateArray2?"

  
    def translate(self, content, data):

        Language = data["BingLanguage"]
        data = {}
        data['from'] = '"' + Language + '"'
        data['to'] = '"' + 'zh' + '"'
        data['texts'] = '["'
        data['texts'] += content
        data['texts'] += '"]'
        data['options'] = "{}"
        data['oncomplete'] = 'onComplete_3'
        data['onerror'] = 'onError_3'
        data['_'] = '1430745999189'
        
        try:
            data = urllib.parse.urlencode(data).encode('utf-8')
            strUrl = self.url + data.decode() + "&appId=%223DAEE5B978BA031557E739EE1E2A68CB1FAD5909%22"
            response = urllib.request.urlopen(strUrl, timeout=5)
            str_data = response.read().decode('utf-8')
            print(str_data)
            tmp, str_data = str_data.split('"TranslatedText":')
            translate_data = str_data[1:str_data.find('",', 1)].replace('\\"','')

        except Exception:
            print_exc()
            translate_data = "Bing：我抽风啦！"
        
        return translate_data


if __name__ == '__main__':

    content = 'そうすると、可笑しいことや変なこと、滑稽なことや正しくないこと、反対にやるべきことが见えてくるから。とにかく、何かにどっぷりはまっていると、周りのことが见えなくなってしまう。だから、时々一歩引くと物事が见えてくる。'
    #content = "Hooray! It's snowing! It's time to make a snowman.James runs out. He makes a big pile of snow. He puts a big snowball on top. He adds a scarf and a hat. He adds an orange for the nose. He adds coal for the eyes and buttons.In the evening, James opens the door. What does he see? The snowman is moving! James invites him in. The snowman has never been inside a house. He says hello to the cat. He plays with paper towels.A moment later, the snowman takes James's hand and goes out.They go up, up, up into the air! They are flying! What a wonderful night!The next morning, James jumps out of bed. He runs to the door.He wants to thank the snowman. But he's gone."
    #content = "낙성대는 ‘별이 떨어진 곳’ 이라는 뜻이다.고려시대 때 어는 날 하늘에서 가장 크고 빛나는 별 하나가 땅에 떨어졌는데 그 곳에서 명장 강감찬 장군이 태어났다.그 후부터 그 곳을 낙성대라고 불렀다."
    # ja en ko
    bing = BingTranslate()
    print(bing.translate('ja', content))