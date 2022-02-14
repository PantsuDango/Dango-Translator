import time
from selenium import webdriver
import re
import utils.http
from difflib import SequenceMatcher
import zipfile
import os
import sys

CHROMEDRIVER_PATH = "../config/tools/chromedriver.exe"
CHROMEDRIVER_DIR_PATH = "../config/tools"

# 判断原文相似度
def getEqualRate(str1, str2) :

    score = SequenceMatcher(None, str1, str2).quick_ratio()
    return score* 100


option = webdriver.ChromeOptions()
option.add_argument("--headless")
try:
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              service_log_path="nul",
                              chrome_options=option)
except Exception as err :
    regex = re.findall("Current browser version is (.+?) with binary", str(err))
    print("浏览器版本: ", regex[0])
else :
    sys.exit()


url = "https://registry.npmmirror.com/-/binary/chromedriver/"
logger = None
res = utils.http.get(url, logger)
if res :
    res = eval(res)
    res.reverse()

update_version = ""
max_score = 0
for val in res :
    version = re.findall("\d{2}\.0\.\d{4}\.\d{1,3}", val["name"])
    if version :
        score = getEqualRate(regex[0], version[0])
        if score > max_score :
            max_score = score
            update_version = version[0]

print("引擎最新版本: ", update_version)

url = "https://registry.npmmirror.com/-/binary/chromedriver/%s/chromedriver_win32.zip"%update_version
res = utils.http.downloadFile(url, "chromedriver_win32.zip", logger)

zip_file = zipfile.ZipFile("chromedriver_win32.zip")
zip_list = zip_file.namelist()
for f in zip_list:
    zip_file.extract(f, CHROMEDRIVER_DIR_PATH)

zip_file.close()
os.remove("chromedriver_win32.zip")