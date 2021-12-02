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
                                            service_log_path="nul",
                                            options=option)
        except Exception :
            self.logger.error(format_exc())

            try:
                # 使用火狐浏览器
                option = webdriver.FirefoxOptions()
                option.add_argument("--headless")
                self.browser = webdriver.Firefox(executable_path="./config/tools/geckodriver.exe",
                                                 service_log_path="nul",
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
                                                  service_log_path="nul",
                                                  capabilities=EDGE)
                except Exception :
                    self.browser_sign = 2
                    self.logger.error(format_exc())
                    self.close()
                    self.message_sign.emit("翻译模块启动失败, 无法使用公共翻译, 详见公共翻译教程说明")
                    return

        self.browser_sign = 1
        self.message_sign.emit("翻译模块启动完成~")
        if self.object.translation_ui.webdriver1.browser_sign == 1 \
                and self.object.translation_ui.webdriver2.browser_sign == 1 \
                and self.object.translation_ui.webdriver3.browser_sign == 1 :
            self.message_sign.emit("翻译模块启动完成~")


    # 打开翻译页面
    def openWeb(self, web_type) :

        self.web_type = web_type
        self.message_sign.emit("%s翻译引擎启动中, 请等待完成后再操作..."%self.translater_map[web_type])

        try :
            self.browser.get(self.url_map[web_type])
            self.browser.maximize_window()
            self.open_sign = True
            self.message_sign.emit("%s翻译引擎启动完成~"%self.translater_map[web_type])
            print("%s翻译引擎启动完成~"%self.translater_map[web_type])

        except Exception :
            self.logger.error(format_exc())
            self.message_sign.emit("%s翻译引擎启动失败, 详见公共翻译教程说明"%self.translater_map[web_type])


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
                    return "公共有道: 我超时啦!"

        except Exception :
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
                    return "公共百度: 我超时啦!"

        except Exception :
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
                    return "公共腾讯: 我超时啦!"

        except Exception :
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
                    if not outputText.isspace() and len(outputText.strip()) > 1 and "".join(outputText.split()) != self.content :
                        self.content = outputText.strip()
                        return self.content
                except Exception :
                    pass
                # 判断超时
                end = time.time()
                if (end - start) > 10 :
                    return "公共彩云: 我超时啦!"

        except Exception :
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
                    return "公共谷歌: 我超时啦!"

        except Exception :
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
                    return "公共DeepL: 我超时啦!"

        except Exception :
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
                    return "公共小牛: 我超时啦!"

        except Exception :
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