from selenium import webdriver
from difflib import SequenceMatcher
from traceback import format_exc
import re
import zipfile
import os
import json
import utils.http

CHROMEDRIVER_PATH = "./config/tools/chromedriver.exe"
DRIVER_DIR_PATH = "./config/tools"
DRIVER_ZIP_NAME = "chromedriver_win32.zip"

# 判断原文相似度
def getEqualRate(str1, str2) :

    return SequenceMatcher(None, str1, str2).quick_ratio()*100


# 获取浏览器版本号
def checkChromeVersion(object) :

    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    try:
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                         service_log_path="nul",
                         options=option)
        driver.close()
        driver.quit()
        object.chrome_driver_finish = 1
    except Exception as err :
        regex = re.findall("Current browser version is (.+?) with binary", str(err))
        if regex :
            return regex[0]
        else :
            object.chrome_driver_finish = 2


# 获取谷歌引擎文件下载信息
def getChromeVersionInfo(chrome_version, logger) :

    # 获取所有引擎版本
    url = "https://registry.npmmirror.com/-/binary/chromedriver/"
    res = utils.http.get(url, logger)
    if not res :
        return
    try :
        res = json.loads(res)
    except Exception :
        logger.error(format_exc())
        return

    driver_version = ""
    max_score = 0
    for val in res :
        # 正则过滤无关的内容
        regex = re.findall("\d{2,3}\.0\.\d{4}\.\d{1,3}", val["name"])
        if not regex :
            continue
        # 文本对比找出最匹配的引擎版本
        score = getEqualRate(regex[0], chrome_version)
        if score > max_score :
            max_score = score
            driver_version = regex[0]
        elif score == max_score :
            if regex[0] > driver_version :
                driver_version = regex[0]

    if driver_version :
        return driver_version


# 下载引擎文件
def downloadDriver(driver_version, object) :

    url = "https://registry.npmmirror.com/-/binary/chromedriver/{}/chromedriver_win32.zip".format(driver_version)
    if not utils.http.downloadFile(url, DRIVER_ZIP_NAME, object.logger) :
        object.chrome_driver_finish = 2
        return

    # 解压压缩包
    try :
        zip_file = zipfile.ZipFile(DRIVER_ZIP_NAME)
        zip_list = zip_file.namelist()
        for f in zip_list :
            if f != "chromedriver.exe" :
                continue
            zip_file.extract(f, DRIVER_DIR_PATH)
        zip_file.close()
        # 删除压缩包
        os.remove(DRIVER_ZIP_NAME)
        object.chrome_driver_finish = 1
    except Exception :
        object.logger.error(format_exc())
        object.chrome_driver_finish = 2


# 校验谷歌浏览器引擎文件
def updateChromeDriver(object) :

    # 获取浏览器版本
    chrome_version = checkChromeVersion(object)
    if not chrome_version :
        return

    # 获取谷歌引擎文件下载信息
    driver_version = getChromeVersionInfo(chrome_version, object.logger)
    if not driver_version :
        object.chrome_driver_finish = 2
        return

    # 下载引擎文件
    downloadDriver(driver_version, object)