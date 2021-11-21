from PyQt5.QtCore import *
from selenium import webdriver
from traceback import format_exc
import time


# 翻译模块
class Webdriver(QObject) :

    message_sign = pyqtSignal(str)

    def __init__(self, object) :

        super(Webdriver, self).__init__()
        self.object = object
        self.logger = object.logger

        self.url_map = {
            "youdao" : "https://fanyi.youdao.com/",
            "baidu"  : "https://fanyi.baidu.com/?aldtype=16047#auto/zh",
            "tencent": "https://fanyi.qq.com/",
            "caiyun" : "https://fanyi.caiyunapp.com/#/",
            "google" : "https://translate.google.cn",
            "deepl"  : "https://www.deepl.com/translator",
            "xiaoniu": "https://niutrans.com/trans?type=text"
        }
        self.translater_map = {
            "youdao": "有道",
            "baidu": "百度",
            "tencent": "腾讯",
            "caiyun": "彩云",
            "google": "谷歌",
            "deepl": "DeepL",
            "xiaoniu": "小牛"
        }
        # 翻译引擎启动情况: 0-启动中, 1-启动成功, 2-启动失败
        self.browser_sign = 0
        # 用于对比前后翻译差异
        self.content = ""
        # 记录当前翻译源种类
        self.web_type = ""
        # 翻译网页是否准备就绪
        self.open_sign = False


    # 开启引擎
    def openWebdriver(self) :

        try:
            # 使用谷歌浏览器
            option = webdriver.ChromeOptions()
            option.add_argument("--headless")
            self.browser = webdriver.Chrome(executable_path="./config/tools/chromedriver.exe",
                                            service_log_path="./logs/geckodriver.log",
                                            options=option)
        except Exception:
            self.logger.error(format_exc())

            try:
                # 使用火狐浏览器
                option = webdriver.FirefoxOptions()
                option.add_argument("--headless")
                self.browser = webdriver.Firefox(executable_path="./config/tools/geckodriver.exe",
                                                 service_log_path="./logs/geckodriver.log",
                                                 options=option)
            except Exception:
                self.logger.error(format_exc())

                try:
                    # 使用Edge浏览器
                    EDGE = {
                        "browserName": "MicrosoftEdge",
                        "version": "",
                        "platform": "WINDOWS",
                        "ms:edgeOptions": {
                            'extensions': [],
                            'args': [
                                '--headless',
                                '--disable-gpu',
                                '--remote-debugging-port=9222',
                            ]}
                    }
                    self.browser = webdriver.Edge(executable_path="./config/tools/msedgedriver.exe",
                                                  service_log_path="./logs/geckodriver.log",
                                                  capabilities=EDGE)
                except Exception :
                    self.browser_sign = 2
                    self.logger.error(format_exc())
                    self.close()
                    self.message_sign.emit("翻译模块启动失败...")
                    return

        self.browser_sign = 1
        if not self.object.translation_ui.webdriver_type2 or not self.object.translation_ui.webdriver_type2 :
            self.message_sign.emit("翻译模块启动完成~")


    # 打开翻译页面
    def openWeb(self, web_type) :

        self.message_sign.emit("%s翻译引擎启动中, 请等待完成后再操作..."%self.translater_map[web_type])
        print("%s翻译引擎启动中, 请等待完成后再操作..."%self.translater_map[web_type])

        try :
            self.browser.get(self.url_map[web_type])
            self.browser.maximize_window()
            self.web_type = web_type
            self.open_sign = True
            self.message_sign.emit("%s翻译引擎启动完成~"%self.translater_map[web_type])
            print("%s翻译引擎启动完成~"%self.translater_map[web_type])

        except Exception :
            self.logger.error(format_exc())
            self.message_sign.emit("%s翻译引擎启动失败..."%self.translater_map[web_type])
            print("%s翻译引擎启动失败..."%self.translater_map[web_type])


    # 有道翻译
    def youdao(self, content) :

        try:
            try:
                self.browser.find_element_by_xpath(self.object.yaml["dict_info"]["youdao_xpath"]).click()
            except Exception:
                pass

            # 清空文本框
            self.browser.find_element_by_xpath('//*[@id="inputOriginal"]').clear()
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="inputOriginal"]').send_keys(content)
            self.browser.find_element_by_xpath('//*[@id="transMachine"]').click()

            start = time.time()
            while True:
                time.sleep(0.1)
                # 提取翻译信息
                outputText = self.browser.find_element_by_id("transTarget").get_attribute("textContent")
                if not outputText.isspace() and len(outputText.strip()) > 1 and "".join(
                        outputText.split()) != self.content:
                    self.content = "".join(outputText.split())
                    return self.content
                # 判断超时
                end = time.time()
                if (end - start) > 10:
                    self.browser.refresh()
                    return "公共有道: 我超时啦!"

        except Exception :
            self.browser.refresh()
            self.logger.error(format_exc())
            return "公共有道: 我抽风啦!"


    # 百度翻译
    def baidu(self, content):

        try :
            try :
                self.browser.find_element_by_xpath(self.object.yaml["dict_info"]["baidu_xpath"]).click()
            except Exception :
                pass

            # 清空翻译框
            self.browser.find_element_by_xpath('//*[@id="baidu_translate_input"]').clear()
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="baidu_translate_input"]').send_keys(content)
            self.browser.find_element_by_xpath('//*[@id="translate-button"]').click()

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    outputText = self.browser.find_element_by_xpath('//*[@id="main-outer"]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/p[2]').text
                    if outputText and outputText != self.content:
                        self.content = outputText
                        return self.content
                except Exception :
                    pass
                # 判断超时
                end = time.time()
                if (end - start) > 10 :
                    self.browser.refresh()
                    return "公共百度: 我超时啦!"

        except Exception :
            self.browser.refresh()
            self.logger.error(format_exc())
            return "公共百度: 我抽风啦!"


    # 腾讯翻译
    def tencent(self, content) :

        try :
            try :
                self.browser.find_element_by_xpath(self.object.yaml["dict_info"]["tencent_xpath"]).click()
            except Exception :
                pass

            # 清空翻译框
            self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/textarea').clear()
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/textarea').send_keys(content)
            self.browser.find_element_by_xpath('//*[@id="language-button-group-translate"]/div').click()

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    outputText = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[2]').text
                    if outputText and "".join(outputText.split()) != self.content :
                        self.content = "".join(outputText.split())
                        return self.content
                except Exception :
                    pass
                # 判断超时
                end = time.time()
                if (end - start) > 10 :
                    self.browser.refresh()
                    return "公共腾讯: 我超时啦!"

        except Exception :
            self.browser.refresh()
            self.logger.error(format_exc())
            return "公共腾讯: 我抽风啦!"


    # 彩云翻译
    def caiyun(self, content) :

        try :
            try:
                self.browser.find_element_by_xpath(self.object.yaml["dict_info"]["caiyun_xpath"]).click()
            except Exception:
                pass

            # 清空翻译框
            self.browser.find_element_by_xpath('//*[@id="textarea"]').clear()
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="textarea"]').send_keys(content)
            self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[2]').click()

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    # 提取翻译信息
                    outputText = self.browser.find_element_by_id("target-textblock").get_attribute("textContent")
                    if not outputText.isspace() and len(outputText.strip()) > 1 and "".join(outputText.split()) != self.content:
                        self.content = outputText.strip()
                        return self.content
                except Exception :
                    pass
                # 判断超时
                end = time.time()
                if (end - start) > 10 :
                    self.browser.refresh()
                    return "公共彩云: 我超时啦!"

        except Exception :
            self.browser.refresh()
            self.logger.error(format_exc())
            return "公共彩云: 我抽风啦!"


    # 谷歌翻译
    def google(self, content) :

        try :
            try:
                self.browser.find_element_by_xpath(self.object.yaml["dict_info"]["google_xpath"]).click()
            except Exception:
                pass

            # 清空翻译框
            self.browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[1]/span/span/div/textarea').clear()
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[1]/span/span/div/textarea').send_keys(content)

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    outputText = self.browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]').text
                    # 原文相似度
                    if outputText :
                        self.content = "".join(outputText.split())
                        return self.content
                except Exception :
                    pass
                # 判断超时
                end = time.time()
                if (end - start) > 10 :
                    self.browser.refresh()
                    return "公共谷歌: 我超时啦!"

        except Exception :
            self.browser.refresh()
            self.logger.error(format_exc())
            return "公共谷歌: 我抽风啦!"


    # deepl翻译
    def deepl(self, content) :

        try :
            try:
                self.browser.find_element_by_xpath(self.object.yaml["dict_info"]["deepl_xpath"]).click()
            except Exception:
                pass

            try :
                self.browser.find_element_by_xpath('//*[@id="dl_translator"]/div[3]/div[3]/div[1]/button/span').click()
            except Exception :
                pass
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="dl_translator"]/div[3]/div[3]/div[1]/div[2]/div[2]/textarea').send_keys(content)

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    # 提取翻译信息
                    outputText = self.browser.find_element_by_id("target-dummydiv").get_attribute("textContent")
                    if not outputText.isspace() \
                            and outputText.strip() \
                            and outputText.strip() != self.content \
                            and "[...]" not in "".join(outputText.split()) \
                            and (len(content) > 5 and len("".join(outputText.split())) > 3 ) :
                        self.content = outputText.strip()
                        return self.content
                except Exception :
                    pass
                # 判断超时
                end = time.time()
                if (end - start) > 10 :
                    self.browser.refresh()
                    return "公共DeepL: 我超时啦!"

        except Exception :
            self.browser.refresh()
            self.logger.error(format_exc())
            return "公共DeepL: 我抽风啦!"


    # 小牛翻译
    def xiaoniu(self, content):

        try:
            try:
                self.browser.find_element_by_xpath(self.object.yaml["dict_info"]["xiaoniu_xpath"]).click()
            except Exception:
                pass

            # 清空文本框
            self.browser.find_element_by_xpath('//*[@id="textarea"]').clear()
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="textarea"]').send_keys(content)
            self.browser.find_element_by_xpath('//*[@id="textTrans"]/div[2]/div/div[2]/div/div/div/p/button').click()

            start = time.time()
            while True:
                time.sleep(0.1)
                # 提取翻译信息
                outputText = self.browser.find_element_by_xpath('//*[@id="textTrans"]/div[3]/div/div[2]/div/div[1]').text
                if not outputText.isspace() and len(outputText.strip()) > 1 and "".join(
                        outputText.split()) != self.content:
                    self.content = "".join(outputText.split())
                    return self.content
                # 判断超时
                end = time.time()
                if (end - start) > 10:
                    self.browser.refresh()
                    return "公共小牛: 我超时啦!"

        except Exception:
            self.browser.refresh()
            self.logger.error(format_exc())
            return "公共小牛: 我抽风啦!"


    # 翻译主函数
    def translater(self, content) :

        if self.web_type == "youdao" :
            result = self.youdao(content)
        elif self.web_type == "baidu" :
            result = self.baidu(content)
        elif self.web_type == "tencent" :
            result = self.tencent(content)
        elif self.web_type == "caiyun" :
            result = self.caiyun(content)
        elif self.web_type == "google" :
            result = self.google(content)
        elif self.web_type == "deepl" :
            result = self.deepl(content)
        else :
            result = ""

        return result


    def close(self) :

        try :
            self.browser.close()
            self.browser.quit()
        except Exception :
            self.logger.error(format_exc())
        print("翻译模块关闭")


if __name__ == "__main__" :

    jap_content_list = [
        "ところで今日の最高気温、何度だと思う？37度だぜ、37度。夏にしても暑すぎる。これじゃオーブンだ。37度っていえば一人でじっとしてるより女の子と抱き合ってた方が涼しいくらいの温度だ。",
        "人生は生まれてきた家庭や环境によってみんな不平等である。それは自分で选択することはできません。しかし、一つだけ私たちにはみな平等なものがある。それは时间です。一年间365日、一日24时间はどの方にも平等に与えられています。",
        "人は幸せになるため生まれてきました。私たちはこの大切な时间を使って、幸せになっていくのです。私はいつも人生を一人旅と例えています。生まれてからは一人旅の始まりです。",
        "私たちは旅に出て、ゴールの见えない道をひたすら歩き続け、山や険しい道をいくつも乗り越え、自分のやりたいこと、したいことを探し、幸せになっていくのです。",
        "幸せになるには、失败を缲り返さなければいけません。时には自分の选択が间违って、 失败する场合があります。"
    ]

    eng_content_list = [
        "In a calm sea every man is a pilot.",
        "But all sunshine without shade, all pleasure without pain, is not life at all.Take the lot of the happiest - it is a tangled yarn.Bereavements and blessings,one following another, make us sad and blessed by turns. Even death itself makes life more loving. Men come closest to their true selves in the sober moments of life, under the shadows of sorrow and loss.",
        "In the affairs of life or of business, it is not intellect that tells so much as character, not brains so much as heart, not genius so much as self-control, patience, and discipline, regulated by judgment.",
        "I have always believed that the man who has begun to live more seriously within begins to live more simply without. In an age of extravagance and waste, I wish I could show to the world how few the real wants of humanity are.",
        "To regret one's errors to the point of not repeating them is true repentance.There is nothing noble in being superior to some other man. The true nobility is in being superior to your previous self.",
    ]

    kor_content_list = [
        "스무살이 되어야 이해하는 것",
        "밥은 엄마가 해주시는 집밥이 최고.",
        "그래도 교복 입고 다닐 때가 좋았던 것.",
        "친구의 관계가 아닌 사람사이 관계가 참 어렵고 힘들다는 것.",
        "돈 버는 것보다 쓰는게 훨씬 쉽다는 것."
    ]

    import utils
    logger = utils.logger.setLog()
    config = {}
    config["dictInfo"] = utils.config.getDictInfo()

    obj = Webdriver(config, logger)
    obj.openWebdriver()
    obj.openWeb("xiaoniu")

    for content in (jap_content_list+eng_content_list+kor_content_list) :
        start = time.time()
        result = obj.xiaoniu(content)
        print(content)
        print(result)
        print(time.time()-start)
        print()

    obj.close()