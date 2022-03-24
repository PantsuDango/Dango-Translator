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
            #option.add_argument("--headless")
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
                    self.message_sign.emit("公共翻译启动失败, 若需使用公共翻译请下载安装谷歌浏览器后重启翻译器, 若使用私人翻译请忽视此提示")
                    return

        self.browser_sign = 1
        if self.object.translation_ui.webdriver1.browser_sign == 1 \
                and self.object.translation_ui.webdriver2.browser_sign == 1 \
                and self.object.translation_ui.webdriver3.browser_sign == 1 :
            self.message_sign.emit("翻译模块启动完成~")


    # 打开翻译页面
    def openWeb(self, web_type) :

        self.web_type = web_type
        self.content = ""

        # 判断当前准备启动的所有翻译源
        web_type_list = [
            self.object.translation_ui.webdriver1.web_type,
            self.object.translation_ui.webdriver2.web_type,
            self.object.translation_ui.webdriver3.web_type
        ]
        content = ""
        for val in web_type_list :
            if not val :
                continue
            content += "[公共%s]"%self.translater_map[val]
        self.message_sign.emit("%s翻译启动中, 请等待完成后再操作..."%content)

        try :
            self.browser.get(self.url_map[web_type])
            self.browser.maximize_window()
            self.open_sign = True
            self.transInit(web_type)
        except Exception :
            import traceback
            traceback.print_exc()
            self.logger.error(format_exc())

        open_sign_list = [
            self.object.translation_ui.webdriver1.open_sign,
            self.object.translation_ui.webdriver2.open_sign,
            self.object.translation_ui.webdriver3.open_sign
        ]
        web_type_list = [
            self.object.translation_ui.webdriver1.web_type,
            self.object.translation_ui.webdriver2.web_type,
            self.object.translation_ui.webdriver3.web_type
        ]

        success_content, fail_content = "", ""
        for val1, val2 in zip(web_type_list, open_sign_list) :
            if not val1 :
                continue
            if val2 :
                success_content += "[公共%s]"%self.translater_map[val1]
            else :
                fail_content += "[公共%s]"%self.translater_map[val1]

        if not success_content :
            self.message_sign.emit("%s启动中..."%fail_content)
        elif not fail_content :
            self.message_sign.emit("%s翻译启动成功" %success_content)
        else :
            self.message_sign.emit("%s翻译启动成功, %s启动中..."%(success_content, fail_content))


    # 点击动作延时
    def browserClickTimeout(self, xpath, timeout=1) :

        start = time.time()
        while True :
            try :
                self.browser.find_element_by_xpath(xpath).click()
                break
            except Exception :
                if time.time()-start > timeout :
                    break
            time.sleep(0.1)


    # 翻译页面初始化
    def transInit(self, web_type) :

        try :
            # 去弹窗广告
            self.browser.find_element_by_xpath(self.object.yaml["dict_info"]["%s_xpath"%web_type]).click()
        except Exception:
            pass
        language = self.object.config["language"]

        # 有道
        if web_type == "youdao" :
            self.browserClickTimeout('//*[@id="langSelect"]')
            if language == "JAP" :
                self.browserClickTimeout('//*[@id="languageSelect"]/li[5]/a')
            elif language == "ENG" :
                self.browserClickTimeout('//*[@id="languageSelect"]/li[3]/a')
            elif language == "KOR" :
                self.browserClickTimeout('//*[@id="languageSelect"]/li[7]/a')

        # 百度
        if web_type == "baidu" :
            self.browserClickTimeout('//*[@id="main-outer"]/div/div/div[1]/div[1]/div[1]/a[1]/span/span')
            if language == "JAP" :
                self.browserClickTimeout('//*[@id="lang-panel-container"]/div/div[5]/div[1]/div[16]/div/span[1]')
            elif language == "ENG" :
                self.browserClickTimeout('//*[@id="lang-panel-container"]/div/div[5]/div[1]/div[21]/div/span[1]')
            elif language == "KOR" :
                self.browserClickTimeout('//*[@id="lang-panel-container"]/div/div[5]/div[1]/div[8]/div/span[1]')


        # 腾讯
        if web_type == "tencent" :
            self.browserClickTimeout('//*[@id="language-button-group-source"]/div[1]')
            if language == "JAP" :
                self.browserClickTimeout('//*[@id="language-button-group-source"]/div[2]/ul/li[4]/span')
            elif language == "ENG" :
                self.browserClickTimeout('//*[@id="language-button-group-source"]/div[2]/ul/li[3]/span')
            elif language == "KOR" :
                self.browserClickTimeout('//*[@id="language-button-group-source"]/div[2]/ul/li[5]/span')
            self.browserClickTimeout('//*[@id="language-button-group-target"]/div[1]')
            self.browserClickTimeout('//*[@id="language-button-group-target"]/div[2]/ul/li[1]/span')

        # DeepL
        if web_type == "deepl" :
            self.browserClickTimeout('//*[@id="dl_translator"]/div[3]/div[3]/div[1]/div[1]/div/button/div')
            if language == "JAP" :
                self.browserClickTimeout('//*[@id="dl_translator"]/div[3]/div[3]/div[1]/div[2]/div[4]/div/div[2]/button[7]/div')
            elif language == "ENG" :
                self.browserClickTimeout('//*[@id="dl_translator"]/div[3]/div[3]/div[1]/div[2]/div[4]/div/div[3]/button[6]/div')
            elif language == "KOR" :
                self.browserClickTimeout('//*[@id="dl_translator"]/div[3]/div[3]/div[1]/div[2]/div[4]/div/div[1]/button[1]/div[1]')
            self.browserClickTimeout('//*[@id="dl_translator"]/div[3]/div[3]/div[3]/div[1]/div[2]/div[1]/button/div')
            self.browserClickTimeout('//*[@id="dl_translator"]/div[3]/div[3]/div[3]/div[3]/div[7]/div/div[3]/button[8]/div[1]')

        # google
        if web_type == "google" :
            self.browserClickTimeout('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/button/div[2]')
            if language == "JAP" :
                self.browserClickTimeout('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[3]/c-wiz/div[1]/div/div[3]/div/div[3]/div[67]/div[2]')
            elif language == "ENG" :
                self.browserClickTimeout('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[3]/c-wiz/div[1]/div/div[3]/div/div[3]/div[106]/div[2]')
            elif language == "KOR" :
                self.browserClickTimeout('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[3]/c-wiz/div[1]/div/div[3]/div/div[3]/div[30]/div[2]')
            self.browserClickTimeout('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[5]/button/div[2]')
            self.browserClickTimeout('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[3]/c-wiz/div[2]/div/div[3]/div/div[2]/div[110]/div[2]')

        # 彩云
        if web_type == "caiyun" :
            self.browserClickTimeout('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/div/div[1]')
            if language == "JAP" :
                self.browserClickTimeout('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/div[2]/div[4]')
            elif language == "ENG" :
                self.browserClickTimeout('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/div[2]/div[3]')
            elif language == "KOR" :
                self.browserClickTimeout('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/div[2]/div[1]')
            self.browserClickTimeout('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/div/div[3]')
            self.browserClickTimeout('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]')


    # 有道翻译
    def youdao(self, content) :

        try :
            # 清空文本框
            if self.content :
                self.browserClickTimeout('//*[@id="inputDelete"]')
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="inputOriginal"]').send_keys(content)
            self.browser.find_element_by_xpath('//*[@id="transMachine"]').click()

            start = time.time()
            while True:
                time.sleep(0.1)
                # 提取翻译信息
                text = self.browser.find_element_by_xpath('//*[@id="transTarget"]').text
                if text :
                    self.content = text
                    return self.content
                # 判断超时
                end = time.time()
                if (end - start) > 10 :
                    return "公共有道: 我超时啦!"

        except Exception :
            self.logger.error(format_exc())
            return "公共有道: 我抽风啦!"


    # 百度翻译
    def baidu(self, content):

        try :
            # 清空翻译框
            if self.content :
                self.browserClickTimeout('//*[@id="main-outer"]/div/div/div[1]/div[2]/div[1]/div[1]/div/div[2]/a')
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="baidu_translate_input"]').send_keys(content)
            self.browser.find_element_by_xpath('//*[@id="translate-button"]').click()

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    text = self.browser.find_element_by_xpath('//*[@id="main-outer"]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/p[2]').text
                    if text :
                        self.content = text
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
            # 清空翻译框
            if self.content :
                self.browserClickTimeout('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]')
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/textarea').send_keys(content)
            self.browser.find_element_by_xpath('//*[@id="language-button-group-translate"]/div').click()

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    text = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[2]').text
                    if text :
                        self.content = text.replace("\n", "")
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
            # 清空翻译框
            if self.content :
                self.browserClickTimeout('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[2]/div/a')
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="textarea"]').send_keys(content)
            self.browserClickTimeout('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[2]')

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    # 提取翻译信息
                    text = self.browser.find_element_by_xpath('//*[@id="texttarget"]').text
                    if text :
                        self.content = text
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
            # 清空翻译框
            if self.content :
                self.browserClickTimeout('/html[1]/body[1]/c-wiz[1]/div[1]/div[2]/c-wiz[1]/div[2]/c-wiz[1]/div[1]/div[2]/div[2]/c-wiz[1]/div[1]/div[1]/div[1]/span[1]/button[1]/div[2]')
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea').send_keys(content)

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    try :
                        # 可能出出现重试按钮
                        self.browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[4]/div[2]/button/span').click()
                    except Exception :
                        pass
                    text = self.browser.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[6]/div/div[1]').text
                    if text :
                        self.content = text
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
            # 清空翻译框
            if self.content:
                self.browserClickTimeout('//*[@id="dl_translator"]/div[3]/div[3]/div[1]/button/span')
            # 输入要翻译的文本
            self.browser.find_element_by_xpath('//*[@id="dl_translator"]/div[3]/div[3]/div[1]/div[2]/div[2]/textarea').send_keys(content)

            start = time.time()
            while True :
                time.sleep(0.1)
                # 提取翻译信息
                try :
                    # 提取翻译信息
                    text = self.browser.find_element_by_id("target-dummydiv").get_attribute("textContent")
                    if not text.isspace() \
                            and text.strip() \
                            and "[...]" not in "".join(text.split()) \
                            and (len(content) > 5 and len("".join(text.split())) > 3 ) :
                        self.content = text.strip()
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