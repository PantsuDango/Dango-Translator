import re
import os
import sys
from traceback import format_exc
import hashlib

import utils.http


OCR_SRC_FILE_PATH = "./ocr/resources/app.py"
PIL_FILE_PATH = "./PIL/_imagingft.cp38-win32.pyd"
AUTO_UPDATE_FILE_PATH = "../自动更新程序.exe"


# 更新本地ocr源码文件
def updateOCRSrcFile(url, logger) :

    try:
        with open(OCR_SRC_FILE_PATH, "r", encoding="utf-8") as file :
            src = file.read()

        regex = "paddleocr.paddleocr.BASE_DIR"
        if len(re.findall(regex, src)) > 0 :
            utils.http.downloadFile(url, OCR_SRC_FILE_PATH, logger)

    except Exception:
        logger.error(format_exc())


# 更新贴字翻译所需的文件
def updatePilFile(object) :

    if not os.path.exists(PIL_FILE_PATH)  :
        url = object.yaml["dict_info"]["pil_file_url"]
        if utils.http.downloadFile(url, PIL_FILE_PATH, object.logger) :
            sys.exit()


# 更新自动更新程序
def updateAutoUpdateFile(object) :

    if not os.path.exists(AUTO_UPDATE_FILE_PATH) :
        return
    auto_update_file_md5 = object.yaml["dict_info"].get("auto_update_file_md5", "")
    if not auto_update_file_md5 :
        return
    # 计算当前自动更新程序的MD5
    hash_md5 = hashlib.md5()
    with open(AUTO_UPDATE_FILE_PATH, "rb") as file :
        for chunk in iter(lambda: file.read(4096), b"") :
            hash_md5.update(chunk)
    file_md5 = hash_md5.hexdigest()
    # 比较MD5, 判断是否需要更新
    if file_md5 == auto_update_file_md5 :
        return
    # 下载新的自动更新程序
    url = object.yaml["dict_info"].get("auto_update_file_url", "")
    if not url :
        return
    utils.http.downloadFile(url, AUTO_UPDATE_FILE_PATH, object.logger)