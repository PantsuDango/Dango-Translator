import time
from PIL import Image
import base64
import os
import hashlib
from traceback import format_exc
import json
import io

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

    with open(image_path, "rb") as file :
        image = file.read()
    image_base64 = base64.b64encode(image).decode("utf-8")

    headers = {}
    host = object.yaml["dict_info"].get("ocr_host", "")
    if url != object.yaml["dict_info"]["ocr_server"] and host :
        headers["Host"] = host

    body = {
        "ImageB64": image_base64,
        "Language": language,
        "Verify": "Token",
        "Token": token
    }

    # 是否为试用在线ocr
    if object.settin_ui.online_ocr_probation_use == True :
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
def offlineOCR(object) :

    image_path = os.path.join(os.getcwd(), "config", "image.jpg")
    url = "http://127.0.0.1:6666/ocr/api"
    language = object.config["language"]
    body = {
        "ImagePath": image_path,
        "Language": language
    }

    res = utils.http.post(url, body, object.logger)
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


# 漫画OCR
def mangaOCR(object, filepath, image_base64=None, filtrate=True, check_permission=False) :

    token = object.config.get("DangoToken", "")
    if token == "" :
        return False, "图片文字识别失败: 未获取到token"

    if not image_base64 :
        # 如果是webp格式就转换为png
        _, ext = os.path.splitext(filepath)
        if ext.lower() == ".webp":
            data = imageWebpToPng(filepath)
        else :
            with open(filepath, "rb") as file :
                data = file.read()
        image_base64 = base64.b64encode(data).decode("utf-8")

    body = {
        "token": token,
        "mask": True,
        "refine": True,
        "filtrate": filtrate,
        "detect_scale": object.config.get("mangaDetectScale", 1),
        "image": image_base64
    }
    url = object.yaml["dict_info"].get("manga_ocr", "https://dl.ap-sh.starivercs.cn/v2/manga_trans/advanced/manga_ocr")
    # 试用
    if check_permission :
        url = object.yaml["dict_info"].get("manga_probate_ocr", "https://dl.ap-sh.starivercs.cn/v2/manga_probate/advanced/manga_ocr")

    sign = False
    result = "图片文字识别失败: "
    try :
        # 测试版本保留
        with open("ocr.json", "w", encoding="utf-8") as file:
            json.dump(body, file, indent=4)
        resp = utils.http.post(url=url, body=body, logger=object.logger, timeout=20)
        if resp.get("Code", -1) == 0 :
            result = resp.get("Data", {})
            sign = True
        else:
            result += resp.get("Message", "")
    except Exception as err :
        result += str(err)
    if not sign :
        object.logger.error(result)

    return sign, result


# 漫画文本消除
def mangaIPT(object, filepath, mask, image_base64=None, check_permission=False) :

    # 获取配置
    token = object.config.get("DangoToken", "")
    if token == "" :
        return False, "图片文字消除失败: 未获取到token"

    url = object.yaml["dict_info"].get("manga_text_inpaint", "https://dl.ap-sh.starivercs.cn/v2/manga_trans/advanced/text_inpaint")
    # 试用
    if check_permission :
        url = object.yaml["dict_info"].get("manga_probate_text_inpaint", "https://dl.ap-sh.starivercs.cn/v2/manga_probate/advanced/text_inpaint")

    if not image_base64 :
        # 如果是webp格式就转换为png
        _, ext = os.path.splitext(filepath)
        if ext.lower() == ".webp" :
            data = imageWebpToPng(filepath)
        else:
            with open(filepath, "rb") as file :
                data = file.read()
        image_base64 = base64.b64encode(data).decode("utf-8")

    body = {
        "token": token,
        "mask": mask,
        "image": image_base64
    }
    sign = False
    result = "图片文字消除失败: "
    try :
        # 测试版本保留
        with open("ipt.json", "w", encoding="utf-8") as file :
            json.dump(body, file, indent=4)
        resp = utils.http.post(url=url, body=body, logger=object.logger, timeout=20)
        if resp.get("Code", -1) == 0 :
            result = resp.get("Data", {})
            sign = True
        else:
            result += resp.get("Message", "")
    except Exception as err :
        result += str(err)
    if not sign :
        object.logger.error(result)

    return sign, result


# 漫画文本渲染
def mangaRDR(object, trans_list, inpainted_image, text_block, font, check_permission) :

    # 获取配置
    token = object.config.get("DangoToken", "")
    if token == "" :
        return False, "图片文字渲染失败: 未获取到token"
    url = object.yaml["dict_info"].get("manga_text_render", "https://dl.ap-sh.starivercs.cn/v2/manga_trans/advanced/text_render")
    # 试用
    if check_permission :
        url = object.yaml["dict_info"].get("manga_probate_text_render", "https://dl.ap-sh.starivercs.cn/v2/manga_probate/advanced/text_render")
    body = {
        "token": token,
        "inpainted_image": inpainted_image,
        "translated_text": trans_list,
        "text_block": text_block,
        "fast_render": object.config.get("mangaFastRenderUse", False)
    }
    if font and len(trans_list) > 0 :
        body["font_selector"] = []
        for _ in range(len(trans_list)) :
            body["font_selector"].append({font: None})

    sign = False
    result = "图片文字渲染失败: "
    try :
        # 测试版本保留
        with open("rdr.json", "w", encoding="utf-8") as file:
            json.dump(body, file, indent=4)
        resp = utils.http.post(url=url, body=body, logger=object.logger, timeout=20)
        if resp.get("Code", -1) == 0 :
            result = resp.get("Data", {})
            sign = True
        else:
            result += resp.get("Message", "")
    except Exception as err :
        result += str(err)
    if not sign :
        object.logger.error(result)

    return sign, result


# 获取漫画可用字体列表
def mangaFontList(object) :

    token = object.config.get("DangoToken", "")
    if token == "" :
        return False, "获取字体列表失败: 未获取到token"

    url = object.yaml["dict_info"].get("manga_font_list", "https://dl.ap-sh.starivercs.cn/v2/manga_trans/advanced/get_available_fonts")
    body = {"token": token}

    sign = False
    result = "获取字体列表失败: "
    try :
        resp = utils.http.post(url=url, body=body, logger=object.logger, timeout=5)
        if resp.get("Code", -1) == 0 :
            result = resp.get("Data", {})
            sign = True
        else :
            result += resp.get("Message", "")
    except Exception as err :
        result += str(err)
    if not sign :
        object.logger.error(result)

    return sign, result


# 私人团子翻译
def dangoTrans(object, sentence, language="auto") :

    token = object.config.get("DangoToken", "")
    if token == "":
        return False, "私人团子失败: 未获取到token"
    if not sentence :
        return True, ""

    url = object.yaml["dict_info"].get("dango_trans", "https://dl.ap-sh.starivercs.cn/v2/translate/sync_task")
    body = {
        "token": token,
        "texts": sentence.split("\n"),
        "from": language,
        "to": "CHS"
    }

    sign = False
    result = "私人团子: "
    try :
        resp = utils.http.post(url=url, body=body, logger=object.logger, timeout=5)
        if resp.get("Code", -1) == 0 :
            result = resp.get("Data", {}).get("texts", [])
            result = "\n".join(result)
            sign = True
        else :
            result += resp.get("Message", "我抽风啦, 请尝试重新翻译!")
    except Exception as err :
        result += str(err)
    if not sign :
        object.logger.error(result)

    return sign, result


# webp格式图片转png
def imageWebpToPng(filepath) :

    with Image.open(filepath) as im :
        im = im.convert('RGBA')
        img_bytes = io.BytesIO()
        im.save(img_bytes, format="png")
        img_bytes.seek(0)
        return img_bytes.read()