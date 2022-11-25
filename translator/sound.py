from selenium import webdriver
from traceback import format_exc
import utils.thread
# import winsound
import time


# 快捷键按键音
# def playButtonSound() :
#     def func() :
#         try :
#             winsound.Beep(440, 500)
#         except Exception :
#             pass
#     utils.thread.createThread(func)


# 音乐朗读模块
class Sound() :

    def __init__(self, object) :

        self.object = object
        self.logger = object.logger
        self.content = ""
        self.url = "https://fanyi.qq.com/"


    # 开启引擎
    def openWebdriver(self):

        try:
            # 使用谷歌浏览器
            option = webdriver.ChromeOptions()
            option.add_argument("--headless")
            self.browser = webdriver.Chrome(executable_path="./config/tools/chromedriver.exe",
                                            service_log_path="nul",
                                            options=option)
        except Exception:
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
                except Exception:
                    self.logger.error(format_exc())
                    self.close()

        self.refreshWeb()


    # 刷新页面
    def refreshWeb(self) :

        self.content = ""
        try :
            self.browser.get(self.url)
            self.browser.maximize_window()
            self.transInit()
        except Exception :
            self.logger.error(format_exc())
            self.close()


    # 点击动作延时
    def browserClickTimeout(self, xpath, timeout=1):

        start = time.time()
        while True:
            try:
                self.browser.find_element_by_xpath(xpath).click()
                break
            except Exception:
                if time.time() - start > timeout:
                    break
            time.sleep(0.1)


    # 翻译页面初始化
    def transInit(self) :

        try:
            self.browser.find_element_by_xpath(self.object.yaml["dict_info"]["tencent_xpath"]).click()
        except Exception:
            pass
        language = self.object.config["language"]

        self.browserClickTimeout('//*[@id="language-button-group-source"]/div[1]')
        if language == "JAP":
            self.browserClickTimeout('//*[@id="language-button-group-source"]/div[2]/ul/li[4]/span')
        elif language == "ENG":
            self.browserClickTimeout('//*[@id="language-button-group-source"]/div[2]/ul/li[3]/span')
        elif language == "KOR":
            self.browserClickTimeout('//*[@id="language-button-group-source"]/div[2]/ul/li[5]/span')


    # 播放音乐
    def playSound(self, content) :

        try :
            if content != self.content :
                # 清空文本框
                self.browserClickTimeout('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]')
                # 输入要朗读的文本
                self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/textarea').send_keys(content)
                self.browser.find_element_by_xpath('//*[@id="language-button-group-translate"]/div').click()
                self.content = content

            # 判断是否已经开始朗读
            while True :
                start = time.time()
                # 点击朗读键
                self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]').click()
                time.sleep(0.1)
                try :
                    # 通过播放图标的css属性判断是否已经开始朗读
                    self.browser.find_element_by_css_selector('body > div.layout-container > div.textpanel > div.textpanel-container.clearfix > div.textpanel-source.active > div.textpanel-tool.tool-voice.ani')
                    break
                except Exception :
                    # 设置如果5s都无法播放就超时
                    now = time.time()
                    if now - start >= 5 :
                        return

            # 判断朗读是否结束
            while True :
                start = time.time()
                time.sleep(0.1)
                try :
                    # 通过播放图标的css属性判断是否已经结束朗读
                    self.browser.find_element_by_css_selector('body > div.layout-container > div.textpanel > div.textpanel-container.clearfix > div.textpanel-source.active > div.textpanel-tool.tool-voice.ani')
                    # 这是如果60s都无法结束就超时
                    now = time.time()
                    if now - start >= 60 :
                        return
                except Exception :
                    break

        except Exception :
            self.logger.error(format_exc())


    def close(self) :

        try :
            self.browser.close()
            self.browser.quit()
        except Exception :
            self.logger.error(format_exc())