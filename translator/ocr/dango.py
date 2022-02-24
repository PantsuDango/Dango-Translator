from PIL import Image
import base64
import os
import re

import utils.http
import utils.range


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
    img_new = None

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

    # 保存图片
    img_new.save(dst)


# 结果排序组包
def resultSort(ocr_result, branchLineUse):
    # 文字顺序由右至左排序
    ocr_result.sort(key=lambda x: x["Coordinate"]["UpperRight"][0], reverse=True)
    # ocr结果归类文本块
    new_words_list = []
    filter_words_list = []
    for index, val in enumerate(ocr_result):
        if val in filter_words_list:
            continue
        tmp_words_list = []
        tmp_words_list.append(val)
        # 以字宽作为碰撞阈值
        word_width = val["Coordinate"]["UpperRight"][0] - val["Coordinate"]["UpperLeft"][0]
        rr1 = utils.range.createRectangular(val, word_width)
        utils.range.findRectangular(rr1, ocr_result, index, tmp_words_list)
        new_words_list.append(tmp_words_list)
        for val in tmp_words_list:
            filter_words_list.append(val)

    # 文字顺序由上至下排序
    filter_words_list = []
    new_ocr_result = []
    ocr_result.sort(key=lambda x: x["Coordinate"]["UpperRight"][1], reverse=False)
    for val in ocr_result:
        if val in filter_words_list:
            continue
        for tmp in new_words_list:
            if val in tmp:
                filter_words_list += tmp
                new_ocr_result.append(tmp)

    # 整理文本块结果
    text = ""
    for val in new_ocr_result:
        content = ""
        for x in val:
            content += x["Words"]
        if val != new_ocr_result[-1] and branchLineUse :
            text += content + "\n"
        else :
            text += content

    return text


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
    host = re.findall(r"//(.+?)/", object.yaml["dict_info"]["ocr_server"])[0]
    url = object.config["nodeURL"]
    language = object.config["language"]
    showTranslateRow = object.config["showTranslateRow"]
    if language == "JAP" and showTranslateRow == "True" :
        language = "Vertical_JAP"

    headers = {"Host": host}
    body = {
        "ImageB64": imageBase64,
        "Language": language,
        "Verify": "Token",
        "Token": token
    }

    res = utils.http.post(url, body, object.logger, headers)
    # 如果出错就直接结束
    if not res :
        return False, "团子OCR错误: 错误未知, 请尝试重试, 如果频繁出现此情况请联系团子"

    code = res.get("Code", -1)
    message = res.get("Message", "")
    if code == 0 :
        # 竖排识别
        if language == "Vertical_JAP" :
            content = resultSort(res.get("Data", []), object.config["BranchLineUse"])
            return True, content
        else :
            content = ""
            for index, val in enumerate(res.get("Data", [])) :
                if (index+1 != len(res.get("Data", []))) and object.config["BranchLineUse"] :
                    if language == "ENG" :
                        content += (val.get("Words", "") + " \n")
                    else :
                        content += (val.get("Words", "") + "\n")
                else :
                    if language == "ENG" :
                        content += val.get("Words", "") + " "
                    else :
                        content += val.get("Words", "")
            return True, content
    else :
        object.logger.error(message)
        return False, "团子OCR错误: %s"%message


# 本地OCR
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
        return False, "本地OCR错误: 错误未知, 请尝试重试, 如果频繁出现此情况请联系团子"

    code = res.get("Code", -1)
    message = res.get("Message", "")
    if code == -1 :
        return False, "本地OCR错误: %s"%message
    else :
        sentence = ""
        for index, tmp in enumerate(res.get("Data", [])) :
            if index+1 != len(res.get("Data", [])) and object.config["BranchLineUse"] :
                if language == "ENG" :
                    sentence += (tmp["Words"] + " \n")
                else :
                    sentence += (tmp["Words"] + "\n")
            else :
                if language == "ENG" :
                    sentence += (tmp["Words"] + " ")
                else :
                    sentence += tmp["Words"]

        return True, sentence