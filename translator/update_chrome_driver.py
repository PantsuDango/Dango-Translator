from selenium import webdriver
import re
import utils.http
from difflib import SequenceMatcher
import zipfile
import os
from traceback import format_exc

CHROMEDRIVER_PATH = "./config/tools/chromedriver.exe"
CHROMEDRIVER_DIR_PATH = "./config/tools"

# 判断原文相似度
def getEqualRate(str1, str2) :

    return SequenceMatcher(None, str1, str2).quick_ratio()*100


# 获取浏览器版本号
def checkChromeVersion() :

    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    try:
        webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                         service_log_path="nul",
                         chrome_options=option)
    except Exception as err :
        regex = re.findall("Current browser version is (.+?) with binary", str(err))
        if regex :
            return regex[0]


# 获取谷歌引擎文件下载信息
def getChromeVersionInfo(chrome_version, logger) :

    url = "https://registry.npmmirror.com/-/binary/chromedriver/"
    res = utils.http.get(url, logger)
    if not res :
        return
    try :
        res = eval(res)
        res.reverse()
    except Exception :
        return

    driver_version = ""
    max_score = 0
    for val in res :
        regex = re.findall("\d{2}\.0\.\d{4}\.\d{1,3}", val["name"])
        if not regex :
            continue
        score = getEqualRate(regex[0], chrome_version)
        if score > max_score :
            max_score = score
            driver_version = regex[0]

    if driver_version :
        return driver_version


# 下载引擎文件
def downloadDriver(driver_version, logger) :

    url = "https://registry.npmmirror.com/-/binary/chromedriver/{}/chromedriver_win32.zip".format(driver_version)
    utils.http.downloadFile(url, "chromedriver_win32.zip", logger)

    try :
        zip_file = zipfile.ZipFile("chromedriver_win32.zip")
        zip_list = zip_file.namelist()
        for f in zip_list:
            zip_file.extract(f, CHROMEDRIVER_DIR_PATH)
        zip_file.close()
        os.remove("chromedriver_win32.zip")
    except Exception :
        logger.error(format_exc())


# 校验谷歌浏览器引擎文件
def updateChromeDriver(logger) :

    # 获取浏览器版本
    chrome_version = checkChromeVersion()
    if not chrome_version :
        return

    # 获取谷歌引擎文件下载信息
    driver_version = getChromeVersionInfo(chrome_version, logger)
    if not driver_version :
        return

    # 下载引擎文件
    downloadDriver(driver_version, logger)