import re
import os
from traceback import format_exc
import utils.http


OCR_SRC_FILE_PATH = "./ocr/resources/app.py"
FUNCTION_ICON_PATH = "./config/icon/function.png"
OPEN_STATUSBAR_IMG_PATH = "./config/other/显示消息栏.png"
CLOSE_STATUSBAR_IMG_PATH = "./config/other/屏蔽消息栏.png"


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


# 一些新增图标的更新
def updateIcon(yaml, logger) :

    if not os.path.exists(FUNCTION_ICON_PATH) :
        url = yaml["dict_info"]["function_icon_url"]
        utils.http.downloadFile(url, FUNCTION_ICON_PATH, logger)

    if not os.path.exists(OPEN_STATUSBAR_IMG_PATH) :
        url = yaml["dict_info"]["open_statusbar_url"]
        utils.http.downloadFile(url, OPEN_STATUSBAR_IMG_PATH, logger)

    if not os.path.exists(CLOSE_STATUSBAR_IMG_PATH) :
        url = yaml["dict_info"]["close_statusbar_url"]
        utils.http.downloadFile(url, CLOSE_STATUSBAR_IMG_PATH, logger)
