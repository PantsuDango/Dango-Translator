import re
import time
import requests
from traceback import print_exc

def get_filter(text):
    
    if isinstance(text, list):
        text = ''.join(text)
    text = str(text)
    text = text.strip()
    filter_list = [
        '\r', '\n', '\t', '\u3000', '\xa0', '\u2002',
        '<br>', '<br/>', '    ', '  ', '&nbsp;', '>>', '&quot;',
        '展开全部', ' '
    ]
    for fl in filter_list:
        text = text.replace(fl, '')
    return text


def get_qtv_qtk():
    
    api_url = 'https://fanyi.qq.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/73.0.3683.86 Safari/537.36', }

    res = requests.get(api_url, headers=headers)
    data = res.text
    fy_guid = res.cookies.get('fy_guid')
    reg = re.compile(r'var qtv = "(.*?)"')
    qtv = reg.search(data).group(1)
    reg = re.compile(r'var qtk = "(.*?)"')
    qtk = reg.search(data).group(1)

    return fy_guid, qtv, qtk


def getHtml(url,headers,data):

    html= requests.post(url=url,data= data,headers=headers, timeout=5)
    datas = html.json()['translate']['records']
        
    if html!=None and datas != None :
        trans_result = ''.join([data['targetText'] for data in datas])
  
    return trans_result


class TencentTrans(object):
    
    def __init__(self):
        
        self.api_url = 'https://fanyi.qq.com/api/translate'
        self.headers = {
            'Cookie': 'fy_guid=605ead81-f210-47eb-bd80-ac6ae5e7a2d8; '
                      'qtv=ed286a053ae88763; '
                      'qtk=wfMmjh3k/7Sr2xVNg/LtITgPRlnvGWBzP9a4FN0dn9PE7L5jDYiYJnW03MJLRUGHEFNCRhTfrp/V+wUj0dun1KkKNUUmS86A/wGVf6ydzhwboelTOs0hfHuF0ndtSoX+N3486tUMlm62VU4i856mqw==; ',
            'Host': 'fanyi.qq.com',
            'Origin': 'https://fanyi.qq.com',
            'Referer': 'https://fanyi.qq.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/73.0.3683.86 Safari/537.36', }

        self.fromlang = 'auto'
        self.tolang = 'zh'
        

    def get_trans_result(self, text):
        
        try:
            self.sessionUuid = str(int(time.time() * 1000))
            self.fy_guid, self.qtv, self.qtk = get_qtv_qtk()
            self.headers['Cookie'] = self.headers['Cookie'].replace(
                '605ead81-f210-47eb-bd80-ac6ae5e7a2d8', self.fy_guid)
            self.headers['Cookie'] = self.headers['Cookie'].replace(
                'ed286a053ae88763', self.qtv)
            self.headers['Cookie'] = self.headers['Cookie'].replace(
                'wfMmjh3k/7Sr2xVNg/LtITgPRlnvGWBzP9a4FN0dn9PE7L5jDYiYJnW03MJLRUGHEFNCRhTfrp/V+wUj0dun1KkKNUUmS86A/wGVf6ydzhwboelTOs0hfHuF0ndtSoX+N3486tUMlm62VU4i856mqw==',
                self.qtk)

            data = {
                    'source': self.fromlang,
                    'target': self.tolang,
                    'sourceText': text,
                    'qtv': self.qtv,
                    'qtk': self.qtk,
                    'sessionUuid': self.sessionUuid
                }

            trans_result = getHtml(self.api_url, self.headers, data)

        except Exception:
            print_exc()
            trans_result = '网页腾讯：我抽风啦！'
        
        return trans_result


if __name__ == '__main__':
    
    Tencent = TencentTrans()
    text = 'そうすると、可笑しいことや変なこと、滑稽なことや正しくないこと、反対にやるべきことが见えてくるから。とにかく、何かにどっぷりはまっていると、周りのことが见えなくなってしまう。だから、时々一歩引くと物事が见えてくる。'
    print(Tencent.get_trans_result(text))