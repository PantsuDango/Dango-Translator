from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import os
import re

import translator.ocr.dango
import translator.ocr.baidu
import translator.api
import utils.http
import utils.thread
import ui.desc
import traceback


TEST_IMAGE_PATH = os.path.join(os.getcwd(), "config", "other", "image.jpg")
TEST_ORIGINAL = "もし、今の状況が自分らしくないことの連続で、好きになれないなら、どうすれば、変えられるかを真剣に考えてみよう。そしないと問題はちっとも解決しない。"


# 测试本地OCR
def testOfflineOCR(object) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("本地OCR测试")
    desc_ui.desc_text.append("\n开始测试...")
    desc_ui.desc_text.insertHtml('<img src={} width="{}" >'.format(TEST_IMAGE_PATH, 245 * object.settin_ui.rate))
    QApplication.processEvents()

    def func():
        start = time.time()
        sign, result = translator.ocr.dango.offlineOCR(object, True)
        if sign :
            signal.emit("\n识别结果:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time() - start))
        else :
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试私人腾讯
def testTencent(object, secret_id, secret_key) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("私人腾讯翻译测试")
    signal.emit("\n开始测试...\n\n原文: \n{}".format(TEST_ORIGINAL))
    QApplication.processEvents()

    def func() :
        start = time.time()
        result = translator.api.tencent(TEST_ORIGINAL, secret_id, secret_key, object.logger)
        if not re.match("^私人腾讯[:：]", result) :
            signal.emit("\n译文:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time() - start))
        else:
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试私人百度翻译
def testBaidu(object, secret_id, secret_key) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("私人百度翻译测试")
    signal.emit("\n开始测试...\n\n原文: \n{}".format(TEST_ORIGINAL))
    QApplication.processEvents()

    def func() :
        start = time.time()
        result = translator.api.baidu(TEST_ORIGINAL, secret_id, secret_key, object.logger)
        if not re.match("^私人百度[:：]", result):
            signal.emit("\n译文:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time() - start))
        else:
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试私人彩云翻译
def testCaiyun(object, secret_key) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("私人彩云翻译测试")
    signal.emit("\n开始测试...\n\n原文: \n{}".format(TEST_ORIGINAL))
    QApplication.processEvents()

    def func() :
        start = time.time()
        result = translator.api.caiyun(TEST_ORIGINAL, secret_key, object.logger)
        if not re.match("^私人彩云[:：]", result) :
            signal.emit("\n译文:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time() - start))
        else:
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试在线OCR
def testOnlineOCR(object) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("团子在线OCR测试")
    desc_ui.desc_text.append("\n开始测试...")
    desc_ui.desc_text.insertHtml('<img src={} width="{}" >'.format(TEST_IMAGE_PATH, 245 * object.settin_ui.rate))
    QApplication.processEvents()

    def func() :
        start = time.time()
        sign, result = translator.ocr.dango.dangoOCR(object, test=True)
        if sign :
            signal.emit("\n识别结果:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time()-start))
        else :
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试百度OCR
def testBaiduOCR(object) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("百度OCR测试")
    desc_ui.desc_text.append("\n开始测试...")
    desc_ui.desc_text.insertHtml('<img src={} width="{}" >'.format(TEST_IMAGE_PATH, 245 * object.settin_ui.rate))
    QApplication.processEvents()

    def func() :
        start = time.time()
        translator.ocr.baidu.getAccessToken(object)
        sign, result = translator.ocr.baidu.baiduOCR(object, test=True)
        if sign :
            signal.emit("\n识别结果:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time()-start))
        else :
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试私人ChatGPT翻译
def testChatGPT(object, api_key, proxy, url, model, prompt) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("私人ChatGPT翻译测试")
    signal.emit("\n开始测试...\n\n原文: \n{}".format(TEST_ORIGINAL))
    QApplication.processEvents()

    def func():
        start = time.time()
        result = translator.api.chatgpt(
            api_key=api_key,
            language="JAP",
            proxy=proxy,
            url=url,
            model=model,
            prompt=prompt,
            content=TEST_ORIGINAL,
            logger=object.logger,
        )
        if not re.match("^私人ChatGPT[:：]", result) :
            signal.emit("\n译文:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time() - start))
        else:
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试私人团子
def testDango(object) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("私人团子翻译测试")
    signal.emit("\n开始测试...\n\n原文: \n{}".format(TEST_ORIGINAL))
    QApplication.processEvents()

    def func() :
        start = time.time()
        sign, result = translator.ocr.dango.dangoTrans(
            object=object,
            sentence=TEST_ORIGINAL,
            language="JAP"
        )
        if sign :
            signal.emit("\n译文:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time()-start))
        else :
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试私人阿里云翻译
def testAliyun(object, access_key_id, access_key_secret) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("私人有道翻译测试")
    signal.emit("\n开始测试...\n\n原文: \n{}".format(TEST_ORIGINAL))
    QApplication.processEvents()

    def func() :
        start = time.time()
        sign, result = translator.api.aliyun(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            source_language="JAP",
            text_to_translate=TEST_ORIGINAL,
            logger=object.logger
        )
        if sign :
            signal.emit("\n译文:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time()-start))
        else :
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试私人有道翻译
def testYoudao(object, app_key, app_secret) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("私人有道翻译测试")
    signal.emit("\n开始测试...\n\n原文: \n{}".format(TEST_ORIGINAL))
    QApplication.processEvents()

    def func():
        start = time.time()
        sign, result = translator.api.youdao(
            text=TEST_ORIGINAL,
            app_key=app_key,
            app_secret=app_secret,
            logger=object.logger
        )
        if sign :
            signal.emit("\n译文:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time()-start))
        else :
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试私人小牛翻译
def testXiaoniu(object, secret_key) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("私人小牛翻译测试")
    signal.emit("\n开始测试...\n\n原文: \n{}".format(TEST_ORIGINAL))
    QApplication.processEvents()

    def func():
        start = time.time()
        sign, result = translator.api.xiaoniu(secret_key, TEST_ORIGINAL, "JAP", object.logger)
        if sign :
            signal.emit("\n译文:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time()-start))
        else :
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)


# 测试私人火山
def testHuoshan(object, secret_id, secret_key) :

    desc_ui = object.settin_ui.desc_ui
    signal = object.settin_ui.desc_signal
    desc_ui.desc_text.clear()
    desc_ui.show()

    desc_ui.setWindowTitle("私人火山翻译测试")
    signal.emit("\n开始测试...\n\n原文: \n{}".format(TEST_ORIGINAL))
    QApplication.processEvents()

    def func() :
        start = time.time()
        sign, result = translator.api.huoshan(secret_id, secret_key, TEST_ORIGINAL, object.logger)
        if sign :
            signal.emit("\n译文:\n{}\n\n耗时: {:.2f}s\n测试成功!".format(result, time.time() - start))
        else:
            signal.emit("\n测试出错:\n{}\n\n测试失败, 请排查完错误后重试!".format(result))

    utils.thread.createThread(func)