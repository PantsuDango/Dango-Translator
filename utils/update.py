import re
import os
import sys
from traceback import format_exc

import utils.http


OCR_SRC_FILE_PATH = "./ocr/resources/app.py"
PIL_FILE_PATH = "./PIL/_imagingft.cp38-win32.pyd"


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

    if not os.path.exists(PIL_FILE_PATH) :
        url = object.yaml["dict_info"]["pil_file_url"]
        if utils.http.downloadFile(url, PIL_FILE_PATH, object.logger) :
            sys.exit()