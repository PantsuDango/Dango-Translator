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


# 横排结果排序组包
def resultSortTD(ocr_result, language) :

    # ocr结果归类文本块
    new_words_list = []
    filter_words_list = []
    for index, val in enumerate(ocr_result):
        if val in filter_words_list:
            continue
        tmp_words_list = []
        tmp_words_list.append(val)

        # 以字高作为碰撞阈值
        word_height = val["Coordinate"]["LowerRight"][1] - val["Coordinate"]["UpperRight"][1]
        rr1 = utils.range.createRectangularTD(val, word_height)
        utils.range.findRectangularTD(rr1, ocr_result, index, tmp_words_list)

        # 文本块聚类
        x1 = tmp_words_list[0]["Coordinate"]["UpperLeft"][0]
        y1 = tmp_words_list[0]["Coordinate"]["UpperLeft"][1]
        x2 = tmp_words_list[0]["Coordinate"]["LowerRight"][0]
        y2 = tmp_words_list[0]["Coordinate"]["LowerRight"][1]
        text = ""
        for val in tmp_words_list :
            if val["Coordinate"]["UpperLeft"][0] < x1 :
                x1 = val["Coordinate"]["UpperLeft"][0]
            if val["Coordinate"]["UpperLeft"][1] < y1 :
                y1 = val["Coordinate"]["UpperLeft"][1]
            if val["Coordinate"]["LowerRight"][0] > x2 :
                x2 = val["Coordinate"]["LowerRight"][0]
            if val["Coordinate"]["LowerRight"][1] > y2 :
                y2 = val["Coordinate"]["LowerRight"][1]
            text += val["Words"]
            filter_words_list.append(val)

        if language == "ENG":
            word_width = int(val["Coordinate"]["LowerRight"][1] - val["Coordinate"]["UpperRight"][1]) + 3
        else :
            word_width = int(val["Coordinate"]["LowerRight"][1] - val["Coordinate"]["UpperRight"][1]) - 3
        new_words_list.append({
            "Coordinate": {
                "UpperLeft": [x1, y1],
                "UpperRight": [x2, y1],
                "LowerRight": [x2, y2],
                "LowerLeft": [x1, y2]
            },
            "Words": text,
            "WordWidth": word_width
        })

    # 结果组包
    text = ""
    for val in new_words_list :
        if val == new_words_list[-1] :
            text += val["Words"]
        else :
            text += val["Words"] + "\n"

    return text, new_words_list


# 竖排结果排序组包
def resultSortMD(ocr_result, language) :

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
        word_width = (val["Coordinate"]["UpperRight"][0] - val["Coordinate"]["UpperLeft"][0]) // 2
        rr1 = utils.range.createRectangularMD(val, word_width)
        utils.range.findRectangularMD(rr1, ocr_result, index, tmp_words_list)

        # 文本块聚类
        x1 = tmp_words_list[-1]["Coordinate"]["UpperLeft"][0]
        x2 = tmp_words_list[0]["Coordinate"]["UpperRight"][0]
        y1 = tmp_words_list[0]["Coordinate"]["UpperRight"][1]
        y2 = tmp_words_list[0]["Coordinate"]["LowerRight"][1]
        text = ""
        for val in tmp_words_list:
            if val["Coordinate"]["UpperRight"][1] < y1:
                y1 = val["Coordinate"]["UpperRight"][1]
            if val["Coordinate"]["LowerRight"][1] > y2:
                y2 = val["Coordinate"]["LowerRight"][1]
            text += val["Words"]
            filter_words_list.append(val)

        if language == "ENG":
            word_width = val["Coordinate"]["UpperRight"][0] - val["Coordinate"]["UpperLeft"][0] + 3
        else :
            word_width = val["Coordinate"]["UpperRight"][0] - val["Coordinate"]["UpperLeft"][0] - 3
        new_words_list.append({
            "Coordinate": {
                "UpperLeft": [x1, y1],
                "UpperRight": [x2, y1],
                "LowerRight": [x2, y2],
                "LowerLeft": [x1, y2]
            },
            "Words": text,
            "WordWidth": word_width
        })

    # 二次文本块聚类, 水平方向
    word_width = ocr_result[0]["Coordinate"]["UpperRight"][0]
    new_words_list2 = []
    filter_words_list2 = []
    for index, val in enumerate(new_words_list):
        if val in filter_words_list2:
            continue
        tmp_words_list = []
        tmp_words_list.append(val)
        rr1 = utils.range.createRectangularMD(val, word_width)
        utils.range.findRectangular2MD(rr1, new_words_list, index, tmp_words_list, word_width)
        for val in tmp_words_list:
            filter_words_list2.append(val)
        new_words_list2.append(tmp_words_list)

    # 文字顺序由上至下排序
    new_words_list2.sort(
        key=lambda x: x[0]["Coordinate"]["UpperRight"][1], reverse=False
    )
    # 整理文本块结果
    text = ""
    for val in new_words_list2:
        for v in val:
            if val == new_words_list2[-1] and v == val[-1]:
                text += v["Words"]
            else:
                text += v["Words"] + "\n"

    ocr_result = []
    for val in new_words_list2 :
        for v in val :
            ocr_result.append(v)

    return text, ocr_result


# 团子在线OCR服务
def dangoOCR(object, test=False) :

    token = object.config["DangoToken"]
    host = re.findall(r"//(.+?)/", object.yaml["dict_info"]["ocr_server"])[0]
    url = object.config["nodeURL"]
    language = object.config["language"]
    showTranslateRow = object.config["showTranslateRow"]
    if language == "JAP" and showTranslateRow == "True":
        language = "Vertical_JAP"
    if test :
        path = TEST_IMAGE_PATH
    else :
        path = IMAGE_PATH

    with open(path, "rb") as file :
        image = file.read()
    imageBase64 = base64.b64encode(image).decode("utf-8")

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
    ocr_result = res.get("Data", [])
    if code == 0 :
        if language == "Vertical_JAP" :
            content, ocr_result = resultSortMD(ocr_result, language)
        else :
            content, ocr_result = resultSortTD(ocr_result, language)
        object.ocr_result = ocr_result
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