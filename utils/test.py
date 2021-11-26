from PyQt5.QtWidgets import *
import time
import os

import translator.ocr.dango
import translator.api
import utils.http
import utils.thread
import ui.desc


TEST_IMAGE_PATH = os.path.join(os.getcwd(), "config", "other", "image.jpg")
NEW_TEST_IMAGE_PATH = os.path.join(os.getcwd(), "config", "other", "new_image.jpg")


# 测试离线OCR
def testOfflineOCR(object) :

    # 测试信息显示窗
    object.settin_ui.desc_ui = ui.desc.Desc(object)
    object.settin_ui.desc_ui.setWindowTitle("离线OCR测试")
    object.settin_ui.desc_ui.desc_text.append("\n开始测试, 共测试5次...")
    object.settin_ui.desc_ui.show()
    QApplication.processEvents()
    total_time = 0

    url = "http://127.0.0.1:6666/ocr/api"
    body = {
        "ImagePath": NEW_TEST_IMAGE_PATH,
        "Language": "JAP"
    }

    for num in range(1, 6) :
        start = time.time()
        try :
            translator.ocr.dango.imageBorder(TEST_IMAGE_PATH, NEW_TEST_IMAGE_PATH, "a", 20, color=(255, 255, 255))
        except Exception :
            body["ImagePath"] = TEST_IMAGE_PATH
        res = utils.http.post(url, body, object.logger)
        end = time.time()
        total_time += end-start
        if res.get("Code", -1) == 0 :
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
