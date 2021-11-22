import requests
import json
import base64
from traceback import format_exc
from PIL import Image
import urllib3
import os

import utils.http

IMAGE_PATH = "./config/image.jpg"
new_image_path = "./config/new_image.jpg"


# 图片四周加白边
def imageBorder(src, dst, loc='a', width=3, color=(0, 0, 0)):

    # 读取图片
    img_ori = Image.open(src)
    w = img_ori.size[0]
    h = img_ori.size[1]

    # 添加边框
    if loc in ['a', 'all']:
        w += 2*width
        h += 2*width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (width, width))
    elif loc in ['t', 'top']:
        h += width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (0, width, w, h))
    elif loc in ['r', 'right']:
        w += width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (0, 0, w-width, h))
    elif loc in ['b', 'bottom']:
        h += width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (0, 0, w, h-width))
    elif loc in ['l', 'left']:
        w += width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (width, 0, w, h))
    else:
        pass

    # 保存图片
    img_new.save(dst)


# 团子在线OCR服务
def dangoOCR(config, logger) :

    # 忽略接口警告
    urllib3.disable_warnings()
    # 图片四周加白边
    imageBorder(IMAGE_PATH, new_image_path, "a", 20, color=(255, 255, 255))

    with open(new_image_path, "rb") as file :
        image = file.read()
    imageBase64 = base64.b64encode(image).decode("utf-8")

    token = config.get("DangoToken", "")
    url = config["dictInfo"].get("ocr_server", "https://stariver.c4a15wh.cn/OCR/Admin/OCRService")
    url = url + "?Token=" + token
    language = config.get("language", "")

    data = {
        "ImageB64": imageBase64,
        "Language": language,
        "Verify": "Token",
        "Token": token
    }
    proxies = {"http": None, "https": None}

    try :
        with requests.post(url, data=json.dumps(data), proxies=proxies, verify=False, timeout=10) as res :
            res.encoding = "utf-8"
            result = json.loads(res.text)

        if result["Code"] == 0 :
            content = ""
            for val in result["Result"] :
                content += val["Words"]
                return True, content
        else :
            logger.error(result["ErrorMsg"])
            return False, "团子OCR错误: %s"%result["ErrorMsg"]

    except Exception :
        logger.error(format_exc())
        print(res.text)
        return False, "团子OCR错误: 请求服务出错, 具体请查看错误日志"


# 离线OCR
def offlineOCR(object) :

    image_path = os.path.join(os.getcwd(), "config", "image.jpg")
    new_image_path = os.path.join(os.getcwd(), "config", "new_image.jpg")
    language = object.config["language"]
    url = "http://127.0.0.1:6666/ocr/api"
    body = {
        "ImagePath": new_image_path,
        "Language": language
    }

    # 四周加白边
    try :
        imageBorder(image_path, new_image_path, "a", 20, color=(255, 255, 255))
    except Exception :
        body["ImagePath"] = image_path
    res = utils.http.post(url, body, object.logger)
    code = res.get("Code", -1)
    message = res.get("Message", "")
    if code == -1 :
        return False, "离线OCR错误: %s"%message
    else :
        sentence = ""
        for tmp in res.get("Data", []) :
            if language == "ENG" :
                sentence += tmp["Words"] + " "
            else :
                sentence += tmp["Words"]

        return True, sentence