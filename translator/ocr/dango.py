import time

from PIL import Image
import base64
import os
import hashlib
from traceback import format_exc

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
        word_height = (val["Coordinate"]["LowerRight"][1] - val["Coordinate"]["UpperRight"][1]) * 1.5
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

        # 获取字宽
        word_width = val["Coordinate"]["LowerRight"][1] - val["Coordinate"]["UpperRight"][1]
        if language == "ENG":
            word_width = val["Coordinate"]["LowerRight"][1] - val["Coordinate"]["UpperRight"][1] + 3

        new_words_list.append({
            "Coordinate": {
                "UpperLeft": [x1, y1],
                "UpperRight": [x2, y1],
                "LowerRight": [x2, y2],
                "LowerLeft": [x1, y2]
            },
            "Words": text,
            "WordWidth": int(word_width)
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
            "WordWidth": int(word_width)
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

    # 获取配置
    token = object.config.get("DangoToken", "")
    url = object.config.get("nodeURL", object.yaml["dict_info"]["ocr_server"])
    language = object.config.get("language", "JAP")
    show_translate_row = object.config.get("showTranslateRow", "False")
    branch_line_use = object.config.get("BranchLineUse", False)
    if language == "JAP" and show_translate_row == "True":
        language = "Vertical_JAP"
    if test :
        image_path = TEST_IMAGE_PATH
        language = "JAP"
    else :
        image_path = IMAGE_PATH

    # if not test :
    #     try :
    #         # 四周加白边
    #         imageBorder(image_path, image_path, "a", 10, color=(255, 255, 255))
    #     except Exception :
    #         object.logger.error(format_exc())

    with open(image_path, "rb") as file :
        image = file.read()
    imageBase64 = base64.b64encode(image).decode("utf-8")

    headers = {}
    host = object.yaml["dict_info"].get("ocr_host", "")
    if url != object.yaml["dict_info"]["ocr_server"] and host :
        headers["Host"] = host

    body = {
        "ImageB64": imageBase64,
        "Language": language,
        "Verify": "Token",
        "Token": token
    }

    # 是否为试用在线ocr
    if object.settin_ui.online_ocr_probation_use == True and test == False :
        url = object.yaml["dict_info"]["ocr_probation"]
    res = utils.http.post(url=url, body=body, logger=object.logger, headers=headers)
    if not res :
        return False, "在线OCR错误: 网络超时, 请尝试重试\n如果频繁出现, 请于[设置]-[识别设定]-[在线OCR]页面内, 切换延迟最低的节点并重新翻译"

    code = res.get("Code", -1)
    message = res.get("Message", "")
    ocr_result = res.get("Data", [])
    if code == 0 :
        # 如果开启了贴字翻译就去掉白边
        if object.config["drawImageUse"] :
            try :
                # 去掉白边
                image = Image.open(image_path)
                coordinate = (10, 10, image.width - 10, image.height - 10)
                region = image.crop(coordinate)
                region.save(image_path)
                # 裁剪后复位坐标参数
                for index, val in enumerate(ocr_result) :
                    UpperLeft = val["Coordinate"]["UpperLeft"]
                    UpperRight = val["Coordinate"]["UpperRight"]
                    LowerRight = val["Coordinate"]["LowerRight"]
                    LowerLeft = val["Coordinate"]["LowerLeft"]
                    ocr_result[index]["Coordinate"]["UpperLeft"] = [UpperLeft[0]-10, UpperLeft[1]-10]
                    ocr_result[index]["Coordinate"]["UpperRight"] = [UpperRight[0]-10, UpperRight[1]-10]
                    ocr_result[index]["Coordinate"]["LowerRight"] = [LowerRight[0]-10, LowerRight[1]-10]
                    ocr_result[index]["Coordinate"]["LowerLeft"] = [LowerLeft[0]-10, LowerLeft[1]-10]
            except Exception :
                object.logger.error(message)

        content = ""
        # 竖向翻译
        if language == "Vertical_JAP" :
            content, ocr_result = resultSortMD(ocr_result, language)
            if object.config["drawImageUse"] :
                object.ocr_result = ocr_result

        # 横向翻译
        else :
            # 贴字翻译采用文本聚类
            if object.config["drawImageUse"] :
                # 开启了自动换行
                if branch_line_use :
                    for index, val in enumerate(ocr_result) :
                        # 获取字宽
                        word_width = val["Coordinate"]["LowerRight"][1] - val["Coordinate"]["UpperRight"][1]
                        if language == "ENG":
                            word_width += 3
                        ocr_result[index]["WordWidth"] = int(word_width)
                        # 自动换行
                        if val != ocr_result[-1] :
                            content += val["Words"] + "\n"
                        else :
                            content += val["Words"]
                else :
                    content, ocr_result = resultSortTD(ocr_result, language)
                object.ocr_result = ocr_result
            # 普通翻译文字直接拼接
            else :
                for val in ocr_result :
                    # 开启了自动换行
                    if branch_line_use and val != ocr_result[-1] :
                        content += val["Words"] + "\n"
                    else :
                        content += val["Words"]
        return True, content
    else :
        if code == -3 :
            return False, "在线OCR错误: 在线OCR需购买才可使用\n请于[设置]-[识别设定]-[在线OCR]页面内, 点击购买按钮完成支付后再使用\n若您已经购买但仍出现此提示, 请直接通过交流群联系客服"
        else :
            object.logger.error(message)
            return False, "在线OCR错误: %s"%message


# 本地OCR
def offlineOCR(object):

    image_path = os.path.join(os.getcwd(), "config", "image.jpg")
    # try :
    #     # 四周加白边
    #     imageBorder(image_path, image_path, "a", 10, color=(255, 255, 255))
    # except Exception :
    #     object.logger.error(format_exc())

    url = object.yaml["offline_ocr_url"]
    language = object.config["language"]
    body = {
        "Language": language
    }

    if object.is_local_offline_ocr():
        body["ImagePath"] = image_path
        res = utils.http.post(url, body, object.logger)
    else:
        with open(image_path, 'rb') as file:
            res = utils.http.post(url, body, object.logger, files={
                'Image': file
            })

    if not res :
        return False, "本地OCR错误: 本地OCR所使用的端口可能被占用, 请重启电脑以释放端口后重试\n如果频繁出现, 建议切换其他OCR使用"

    code = res.get("Code", -1)
    message = res.get("Message", "")
    ocr_result = res.get("Data", [])

    if code == 0 :
        if object.config["drawImageUse"] :
            try :
                # 去掉白边
                image = Image.open(image_path)
                coordinate = (10, 10, image.width - 10, image.height - 10)
                region = image.crop(coordinate)
                region.save(image_path)
                # 裁剪后复位坐标参数
                for index, val in enumerate(ocr_result) :
                    UpperLeft = val["Coordinate"]["UpperLeft"]
                    UpperRight = val["Coordinate"]["UpperRight"]
                    LowerRight = val["Coordinate"]["LowerRight"]
                    LowerLeft = val["Coordinate"]["LowerLeft"]
                    ocr_result[index]["Coordinate"]["UpperLeft"] = [UpperLeft[0]-10, UpperLeft[1]-10]
                    ocr_result[index]["Coordinate"]["UpperRight"] = [UpperRight[0]-10, UpperRight[1]-10]
                    ocr_result[index]["Coordinate"]["LowerRight"] = [LowerRight[0]-10, LowerRight[1]-10]
                    ocr_result[index]["Coordinate"]["LowerLeft"] = [LowerLeft[0]-10, LowerLeft[1]-10]
            except Exception :
                object.logger.error(message)

        if language == "Vertical_JAP" :
            content, ocr_result = resultSortMD(ocr_result, language)
        else :
            content, ocr_result = resultSortTD(ocr_result, language)

        object.ocr_result = ocr_result
        return True, content
    else :
        object.logger.error(message)
        if message == "Language RU doesn't exist":
            return False, "本地OCR错误: 当前本地OCR版本尚未支持俄语\n请于[设置]-[识别设定]-[本地OCR]页面内, 通过卸载和安装功能, 更新最新版本的本地OCR后重试"
        else :
            return False, "本地OCR错误: %s\n如果频繁出现, 建议切换其他OCR使用"%message
