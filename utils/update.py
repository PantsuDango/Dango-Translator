import re
import requests
from traceback import format_exc


OCR_SRC_FILE_PATH = "./ocr/resources/app.py"


# 更新本地ocr源码文件
def updateOCRSrcFile(url, logger) :

    try:
        with open(OCR_SRC_FILE_PATH, "r", encoding="utf-8") as file :
            src = file.read()

        regex = "paddleocr.paddleocr.BASE_DIR"
        if len(re.findall(regex, src)) > 0 :
            res = requests.get(url, stream=True)
            content = res.content
            with open(OCR_SRC_FILE_PATH, "wb") as file :
                file.write(content)

    except Exception:
        logger.error(format_exc())