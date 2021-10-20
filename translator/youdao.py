from selenium import webdriver
from traceback import format_exc
import time


# 有道翻译模块实例化
def createYoudao(obj, logger) :

    obj.youdao = Youdao(logger)


# 有道翻译模块
class Youdao() :

    def __init__(self, logger) :

        self.content = ""
        self.logger = logger
        url = "https://fanyi.youdao.com/"

        try :
            # 使用谷歌浏览器
            option = webdriver.ChromeOptions()
            option.add_argument("--headless")
            self.browser = webdriver.Chrome(executable_path="../config/tools/chromedriver.exe",
                                            service_log_path="../logs/geckodriver.log",
                                            options=option)
        except Exception :
            self.logger.error(format_exc())

            try :
                # 使用火狐浏览器
                option = webdriver.FirefoxOptions()
                option.add_argument("--headless")
                self.browser = webdriver.Firefox(executable_path="../config/tools/geckodriver.exe",
                                                 service_log_path="../logs/geckodriver.log",
                                                 options=option)
            except Exception :
                self.logger.error(format_exc())

                try :
                    # 使用Edge浏览器
                    EDGE = {
                        "browserName": "MicrosoftEdge",
                        "version": "",
                        "platform": "WINDOWS",

                        # 关键是下面这个
                        "ms:edgeOptions": {
                            'extensions': [],
                            'args': [
                                '--headless',
                                '--disable-gpu',
                                '--remote-debugging-port=9222',
                            ]}
                    }
                    self.browser = webdriver.Edge(executable_path="../config/tools/msedgedriver.exe",
                                                     service_log_path="../logs/geckodriver.log",
                                                     capabilities=EDGE)
                except Exception:
                    self.logger.error(format_exc())
                    self.close()

        self.browser.get(url)
        self.browser.maximize_window()


    # 翻译
    def translater(self, content) :

        try :
            # 清空文本框
            self.browser.find_element_by_xpath('//*[@id="inputOriginal"]').clear()
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="inputOriginal"]').send_keys(content)
            self.browser.find_element_by_xpath('//*[@id="transMachine"]').click()

            start = time.time()
            while True:
                # 提取翻译信息
                outputText = self.browser.find_element_by_id("transTarget").get_attribute("textContent")
                if not outputText.isspace() and len(outputText.strip()) > 1 and "".join(outputText.split()) != self.content :
                    self.content = "".join(outputText.split())
                    return self.content
                # 判断超时
                end = time.time()
                if (end - start) > 10 :
                    return "公共有道: 我超时啦!"

        except Exception :
            self.logger.error(format_exc())
            return "公共有道: 我抽风啦!"


    def close(self) :

        self.browser.close()
        self.browser.quit()


if __name__ == "__main__" :

    jap_content_list = [
        "ところで今日の最高気温、何度だと思う？37度だぜ、37度。夏にしても暑すぎる。これじゃオーブンだ。37度っていえば一人でじっとしてるより女の子と抱き合ってた方が涼しいくらいの温度だ。",
        "人生は生まれてきた家庭や环境によってみんな不平等である。それは自分で选択することはできません。しかし、一つだけ私たちにはみな平等なものがある。それは时间です。一年间365日、一日24时间はどの方にも平等に与えられています。",
        "人は幸せになるため生まれてきました。私たちはこの大切な时间を使って、幸せになっていくのです。私はいつも人生を一人旅と例えています。生まれてからは一人旅の始まりです。",
        "私たちは旅に出て、ゴールの见えない道をひたすら歩き続け、山や険しい道をいくつも乗り越え、自分のやりたいこと、したいことを探し、幸せになっていくのです。",
        "幸せになるには、失败を缲り返さなければいけません。时には自分の选択が间违って、 失败する场合があります。",
        "それも幸せになるための道のりです。なかなかうまくいかないのが人生です。うまくいかない时を顽张って越えるから、成长していく のです。",
        "先ほどいいました。人生は一人旅です。私たちはこの旅で大切な仲间と出会い、一绪に幸せになるため、お互い助けあい、励ましていくのです。仲间はとても大 切です。",
        "家族も人です、特别な仲间かもしれませんが、感谢することは当たり前です。しかし、この世に利益を求めるため、出会った仲间を好きなように利用する人がたくさんいます。",
        "人间はみんな幸せの道を探しています。自分が助けてほしいなら、まず相手を助けましょう。何よりも私たちは常に感谢の気持ちを忘れず、生きていくことはとても大事なのです。なぜならいつも大切な仲间が贵重な时间を使っ て、自分が困った时、助けてくれるからです。",
        "みなさんは楽しい时间を过ごしたいから旅行にいくのではありませんか？人生も同じです。常 に楽しく生きることが大事なのです。一度に一回の人生です。自分が生きている间、时间も进みます。自分が立ち止っている间、时间は待ってくれません。",
    ]

    eng_content_list = [
        "In a calm sea every man is a pilot.",
        "But all sunshine without shade, all pleasure without pain, is not life at all.Take the lot of the happiest - it is a tangled yarn.Bereavements and blessings,one following another, make us sad and blessed by turns. Even death itself makes life more loving. Men come closest to their true selves in the sober moments of life, under the shadows of sorrow and loss.",
        "In the affairs of life or of business, it is not intellect that tells so much as character, not brains so much as heart, not genius so much as self-control, patience, and discipline, regulated by judgment.",
        "I have always believed that the man who has begun to live more seriously within begins to live more simply without. In an age of extravagance and waste, I wish I could show to the world how few the real wants of humanity are.",
        "To regret one's errors to the point of not repeating them is true repentance.There is nothing noble in being superior to some other man. The true nobility is in being superior to your previous self.",
        "In the eternal universe, every human being has a one-off chance to live --his existence is unique and irretrievable, for the mold with which he was made, as Rousseau said, was broken by God immediately afterwards.",
        "Fame, wealth and knowledge are merely worldly possessions that are within the reach of anybody striving for them. But your experience of and feelings about life are your own and not to be shared. No one can live your life over again after your death. ",
        "A full awareness of this will point out to you that the most important thing in your existence is your distinctive individuality or something special of yours. What really counts is not your worldly success but your peculiar insight into the meaning of life and your commitment to it, which add luster to your personality.",
        "It is not easy to be what one really is. There is many a person in the world who can be identified as anything either his job, his status or his social role that shows no trace about his individuality. It does do him justice to say that he has no identity of his own, if he doesn't know his own mind and all his things are either arranged by others or done on others' sugg estions; if his life, always occupied by external things, is completely void of an inner world.",
        "You won't be able to find anything whatever, from head to heart, that truly belongs to him. He is, indeed, no more than a shadow cast by somebody else or a machine capable of doing business."
    ]

    kor_content_list = [
        "스무살이 되어야 이해하는 것",
        "밥은 엄마가 해주시는 집밥이 최고.",
        "그래도 교복 입고 다닐 때가 좋았던 것.",
        "친구의 관계가 아닌 사람사이 관계가 참 어렵고 힘들다는 것.",
        "돈 버는 것보다 쓰는게 훨씬 쉽다는 것.",
        "부모님,선생님의 눈을 피해 했던 일들이 더 신나고 즐거웠다는것.",
        "알 수 없는 것이 사람 마음이라는 것.",
        "지금 내지갑 만원짜리보다 교복주머니속 천원짜리 한장이 더 행복이라는 것.",
        "마지막으로 더 크고 더 많고 더 자유롭고 더 편한것이 행복지수와 비례하지 않다는 것."
    ]

    obj = Youdao(None)
    for content in jap_content_list+eng_content_list+kor_content_list :
        start = time.time()
        result = obj.translater(content)
        print(content)
        print(result)
        print(time.time()-start)
        print()
    obj.close()