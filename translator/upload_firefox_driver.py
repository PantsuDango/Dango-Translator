from selenium import webdriver
from traceback import format_exc, print_exc
import re
import zipfile
import os
import utils.http

FIREFOX_DRIVER_PATH = "./config/tools/geckodriver.exe"
DRIVER_DIR_PATH = "./config/tools"
DRIVER_ZIP_NAME = "geckodriver-win64.zip"


# 获取浏览器版本号
def checkFirefoxVersion(object) :

    try:
        option = webdriver.FirefoxOptions()
        option.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH,
                                   service_log_path="nul",
                                   options=option)
        driver.close()
        driver.quit()
        object.firefox_driver_finish = 1
    except Exception :
        if "newSession" in format_exc() :
            return True
        else :
            object.firefox_driver_finish = 2


# 获取Firefox下载信息
def getFirefoxVersionInfo(logger) :

    url = "https://liushilive.github.io/github_selenium_drivers/search_plus_index.json"
    res = utils.http.get(url, logger)
    if not res :
        return
    try:
        res = eval(res)
        text = res["md/Firefox.html"]["body"]
    except Exception:
        logger.error(format_exc())
        return
    regex = re.findall("geckodriver-v[\d.]+-win64.zip", text)
    if not regex :
        return

    return regex[0]


# 下载浏览器引擎
def downloadDriver(driver_version, object) :

    # 下载引擎文件
    url = "https://npm.taobao.org/mirrors/geckodriver/v0.30.0/%s"%driver_version
    if not utils.http.downloadFile(url, DRIVER_ZIP_NAME, object.logger) :
        object.firefox_driver_finish = 2
        return

    # 解压压缩包
    try:
        zip_file = zipfile.ZipFile(DRIVER_ZIP_NAME)
        zip_list = zip_file.namelist()
        for f in zip_list:
            if f != "geckodriver.exe":
                continue
            zip_file.extract(f, DRIVER_DIR_PATH)
        zip_file.close()
        # 删除压缩包
        os.remove(DRIVER_ZIP_NAME)
        object.firefox_driver_finish = 1
    except Exception :
        object.logger.error(format_exc())
        object.firefox_driver_finish = 2


# 校验火狐浏览器引擎文件
def updateFirefoxDriver(object) :

    # 校验浏览器版本
    sign = checkFirefoxVersion(object)
    if not sign :
        return

    # 获取Firefox引擎信息
    driver_version = getFirefoxVersionInfo(object.logger)
    if not driver_version :
        object.firefox_driver_finish = 2
        return

    # 下载浏览器引擎
    downloadDriver(driver_version, object)