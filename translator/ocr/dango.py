import base64
from PIL import Image
import os

import utils.http


IMAGE_PATH = "./config/image.jpg"
NEW_IMAGE_PATH = "./config/new_image.jpg"
TEST_IMAGE_PATH = os.path.join(os.getcwd(), "config", "other", "image.jpg")
NEW_TEST_IMAGE_PATH = os.path.join(os.getcwd(), "config", "other", "new_image.jpg")


# 图片四周加白边
def imageBorder(src, dst, loc="a", width=3, color=(0, 0, 0)):

    # 读取图片
    img_ori = Image.open(src)
    w = img_ori.size[0]
    h = img_ori.size[1]

    # 添加边框
    if loc in ["a", "all"]:
        w += 2*width
        h += 2*width
        img_new = Image.new("RGB", (w, h), color)
        img_new.paste(img_ori, (width, width))
    elif loc in ["t", "top"]:
        h += width
        img_new = Image.new("RGB", (w, h), color)
        img_new.paste(img_ori, (0, width, w, h))
    elif loc in ["r", "right"]:
        w += width
        img_new = Image.new("RGB", (w, h), color)
        img_new.paste(img_ori, (0, 0, w-width, h))
    elif loc in ["b", "bottom"]:
        h += width
        img_new = Image.new("RGB", (w, h), color)
        img_new.paste(img_ori, (0, 0, w, h-width))
    elif loc in ["l", "left"]:
        w += width
        img_new = Image.new("RGB", (w, h), color)
        img_new.paste(img_ori, (width, 0, w, h))
    else:
        pass

    # 保存图片
    img_new.save(dst)


# 团子在线OCR服务
def dangoOCR(object, test=False) :

    if not test :
        try :
            # 四周加白边
            imageBorder(IMAGE_PATH, NEW_IMAGE_PATH, "a", 10, color=(255, 255, 255))
            path = NEW_IMAGE_PATH
        except Exception:
            path = IMAGE_PATH
    else :
        try :
            # 四周加白边
            imageBorder(TEST_IMAGE_PATH, NEW_TEST_IMAGE_PATH, "a", 10, color=(255, 255, 255))
            path = NEW_TEST_IMAGE_PATH
        except Exception:
            path = TEST_IMAGE_PATH


    with open(path, "rb") as file :
        image = file.read()
    imageBase64 = base64.b64encode(image).decode("utf-8")

    token = object.config["DangoToken"]
    url = object.yaml["dict_info"]["ocr"]
    language = object.config["language"]

    body = {
        "ImageB64": imageBase64,
        "Language": language,
        "Verify": "Token",
        "Token": token
    }

    res = utils.http.post(url, body, object.logger, timeout=2.5)
    if not res :
        return False, "团子OCR错误: 错误未知, 请尝试重试, 如果频繁出现此情况请联系团子"

    code = res.get("Code", -1)
    message = res.get("Message", "")
    if code == 0 :
        content = ""
        for val in res.get("Data", []) :
            content += val.get("Words", "")
        return True, content
    else :
        object.logger.error(message)
        return False, "团子OCR错误: %s"%message


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
        imageBorder(image_path, new_image_path, "a", 10, color=(255, 255, 255))
    except Exception :
        body["ImagePath"] = image_path
    res = utils.http.post(url, body, object.logger)
    if not res :
        return False, "离线OCR错误: 错误未知, 请尝试重试, 如果频繁出现此情况请联系团子"

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