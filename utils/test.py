import urllib.parse

from PyQt5.QtWidgets import *
import time
import os

import translator.ocr.dango
import translator.ocr.baidu
import translator.api
import utils.http
import utils.thread
import ui.desc


TEST_IMAGE_PATH = os.path.join(os.getcwd(), "config", "other", "image.jpg")
NEW_TEST_IMAGE_PATH = os.path.join(os.getcwd(), "config", "other", "new_image.jpg")


# 测试本地OCR
def testOfflineOCR(object):

    # 测试信息显示窗
    object.settin_ui.desc_ui = ui.desc.Desc(object)
    object.settin_ui.desc_ui.setWindowTitle("本地OCR测试")
    object.settin_ui.desc_ui.desc_text.append("\n开始测试, 共测试5次...")
    object.settin_ui.desc_ui.show()
    QApplication.processEvents()
    total_time = 0

    url = object.yaml["offline_ocr_url"]
    image_path = TEST_IMAGE_PATH
    body = {
        "Language": "JAP",
    }
    is_local = object.is_local_offline_ocr()
    if is_local:
        body["ImagePath"] = image_path

    for num in range(1, 6):
        start = time.time()
        # try :
        #     translator.ocr.dango.imageBorder(TEST_IMAGE_PATH, NEW_TEST_IMAGE_PATH, "a", 20, color=(255, 255, 255))
        # except Exception :
        #     body["ImagePath"] = TEST_IMAGE_PATH
        if is_local:
            res = utils.http.post(url, body, object.logger)
        else:
            with open(image_path, 'rb') as file:
                res = utils.http.post(url, body, object.logger, files={
                    'image': file
                })
        end = time.time()
        total_time += end-start
        if res.get("Code", -1) == 0:
            object.settin_ui.desc_ui.desc_text.append("\n第{}次, 成功, 耗时{:.2f}s".format(num, (end - start)))
        else:
            object.settin_ui.desc_ui.desc_text.append("\n第{}次, 失败".format(num))
        QApplication.processEvents()

    object.settin_ui.desc_ui.desc_text.append("\n测试完成, 平均耗时{:.2f}s".format(total_time/5))


# 测试私人腾讯
def testTencent(object) :

    # 测试信息显示窗
    object.settin_ui.desc_ui = ui.desc.Desc(object)
    object.settin_ui.desc_ui.setWindowTitle("私人腾讯翻译测试")
    object.settin_ui.desc_ui.desc_text.append("\n开始测试...")
    object.settin_ui.desc_ui.show()

    secret_id = object.config["tencentAPI"]["Key"]
    secret_key = object.config["tencentAPI"]["Secret"]
    original = "もし、今の状況が自分らしくないことの連続で、好きになれないなら、どうすれば、変えられるかを真剣に考えてみよう。そしないと問題はちっとも解決しない。"
    object.settin_ui.desc_ui.desc_text.append("\n原文: \n{}".format(original))
    QApplication.processEvents()
    result = translator.api.tencent(original, secret_id, secret_key, object.logger)
    object.settin_ui.desc_ui.desc_text.append("\n译文: \n{}".format(result))
    object.settin_ui.desc_ui.desc_text.append("\n测试结束!")


# 测试私人百度翻译
def testBaidu(object) :

    # 测试信息显示窗
    object.settin_ui.desc_ui = ui.desc.Desc(object)
    object.settin_ui.desc_ui.setWindowTitle("私人百度翻译测试")
    object.settin_ui.desc_ui.desc_text.append("\n开始测试...")
    object.settin_ui.desc_ui.show()

    original = "もし、今の状況が自分らしくないことの連続で、好きになれないなら、どうすれば、変えられるかを真剣に考えてみよう。そしないと問題はちっとも解決しない。"
    object.settin_ui.desc_ui.desc_text.append("\n原文: \n{}".format(original))
    QApplication.processEvents()
    secret_id = object.config["baiduAPI"]["Key"]
    secret_key = object.config["baiduAPI"]["Secret"]
    result = translator.api.baidu(original, secret_id, secret_key, object.logger)
    object.settin_ui.desc_ui.desc_text.append("\n译文: \n{}".format(result))
    object.settin_ui.desc_ui.desc_text.append("\n测试结束!")


# 测试私人彩云翻译
def testCaiyun(object) :

    # 测试信息显示窗
    object.settin_ui.desc_ui = ui.desc.Desc(object)
    object.settin_ui.desc_ui.setWindowTitle("私人彩云翻译测试")
    object.settin_ui.desc_ui.desc_text.append("\n开始测试...")
    object.settin_ui.desc_ui.show()

    original = "もし、今の状況が自分らしくないことの連続で、好きになれないなら、どうすれば、変えられるかを真剣に考えてみよう。そしないと問題はちっとも解決しない。"
    object.settin_ui.desc_ui.desc_text.append("\n原文: \n{}".format(original))
    QApplication.processEvents()
    secret_key = object.config["caiyunAPI"]
    result = translator.api.caiyun(original, secret_key, object.logger)
    object.settin_ui.desc_ui.desc_text.append("\n译文: \n{}".format(result))
    object.settin_ui.desc_ui.desc_text.append("\n测试结束!")


# 测试在线OCR
def testOnlineOCR(object) :

    # 测试信息显示窗
    object.settin_ui.desc_ui = ui.desc.Desc(object)
    object.settin_ui.desc_ui.setWindowTitle("团子在线OCR测试")
    object.settin_ui.desc_ui.desc_text.append("\n开始测试...")
    object.settin_ui.desc_ui.desc_text.insertHtml('<img src={} width="{}" >'.format(TEST_IMAGE_PATH, 245 * object.settin_ui.rate))
    object.settin_ui.desc_ui.show()
    QApplication.processEvents()

    ocr_sign, original = translator.ocr.dango.dangoOCR(object, test=True)
    object.settin_ui.desc_ui.desc_text.append("\n识别结果: \n{}".format(original))
    object.settin_ui.desc_ui.desc_text.append("\n测试结束!")


# 测试百度OCR
def testBaiduOCR(object) :

    # 测试信息显示窗
    object.settin_ui.desc_ui = ui.desc.Desc(object)
    object.settin_ui.desc_ui.setWindowTitle("百度OCR测试")
    object.settin_ui.desc_ui.desc_text.append("\n开始测试...")
    object.settin_ui.desc_ui.desc_text.insertHtml('<img src={} width="{}" >'.format(TEST_IMAGE_PATH, 245 * object.settin_ui.rate))
    object.settin_ui.desc_ui.show()
    QApplication.processEvents()

    translator.ocr.baidu.getAccessToken(object)
    ocr_sign, original = translator.ocr.baidu.baiduOCR(object, test=True)
    object.settin_ui.desc_ui.desc_text.append("\n识别结果: \n{}".format(original))
    object.settin_ui.desc_ui.desc_text.append("\n测试结束!")


# 测试私人ChatGPT翻译
def testChatGPT(object) :

    # 测试信息显示窗
    object.settin_ui.desc_ui = ui.desc.Desc(object)
    object.settin_ui.desc_ui.setWindowTitle("私人ChatGPT翻译测试")
    object.settin_ui.desc_ui.desc_text.append("\n开始测试...")
    object.settin_ui.desc_ui.show()

    original = "もし、今の状況が自分らしくないことの連続で、好きになれないなら、どうすれば、変えられるかを真剣に考えてみよう。そしないと問題はちっとも解決しない。"
    object.settin_ui.desc_ui.desc_text.append("\n原文: \n{}".format(original))
    QApplication.processEvents()
    def func() :
        start = time.time()
        result = translator.api.chatgpt(
            api_key=object.config["chatgptAPI"],
            language="JAP",
            proxy=object.config["chatgptProxy"],
            content=original,
            logger=object.logger,
        )
        object.settin_ui.desc_ui.desc_text.append("\n译文: \n{}".format(result))
        object.settin_ui.desc_ui.desc_text.append("\n耗时: {:.2f}s".format(time.time()-start))
        object.settin_ui.desc_ui.desc_text.append("测试结束!")
    utils.thread.createThread(func)