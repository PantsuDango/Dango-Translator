from selenium import webdriver
from traceback import format_exc
import re
import zipfile
import os
import utils.http
import shutil

EDGE_DRIVER_PATH = "./config/tools/msedgedriver.exe"
CHROMEDRIVER_DIR_PATH = "./config/tools"
DRIVER_ZIP_NAME = "edgedriver_win64.zip"


# 获取浏览器版本号
def checkEdgeVersion() :

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
    try:
        driver = webdriver.Edge(executable_path=EDGE_DRIVER_PATH,
                                service_log_path="nul",
                                capabilities=EDGE)
        driver.close()
        driver.quit()
    except Exception as err :
        regex = re.findall("[0-9.]+", str(err))
        if regex :
            return regex[0]


# 下载引擎文件
def downloadDriver(driver_version, logger) :

    url = "https://msedgedriver.azureedge.net/{}/edgedriver_win64.zip".format(driver_version)
    if not utils.http.downloadFile(url, DRIVER_ZIP_NAME, logger) :
        return

    # 解压压缩包
    try :
        zip_file = zipfile.ZipFile(DRIVER_ZIP_NAME)
        zip_list = zip_file.namelist()
        for f in zip_list :
            zip_file.extract(f, CHROMEDRIVER_DIR_PATH)
        zip_file.close()
        # 删除压缩包
        os.remove(DRIVER_ZIP_NAME)
        os.remove(os.path.join(CHROMEDRIVER_DIR_PATH, "Driver_Notes"))
    except Exception :
        logger.error(format_exc())


# 校验Edge浏览器引擎文件
def updateEdgeDriver(logger) :

    # 获取浏览器版本
    driver_version = checkEdgeVersion()
    if not driver_version :
        return

    # 下载引擎文件
    downloadDriver(driver_version, logger)