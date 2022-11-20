import yaml
import json
import time
from traceback import format_exc

import utils.http


YAML_PATH = "./config/config.yaml"
HISTORY_FILE_PATH = "../翻译历史.txt"
CLOUD_CONFIG_PATH = "./config/cloud_config.json"


# 打开本地配置文件
def openConfig(logger) :

    try :
        with open(YAML_PATH, "r", encoding="utf-8") as file :
            config = yaml.load(file.read(), Loader=yaml.FullLoader)

        # 2022.02.19 添加新参数
        if "auto_login" not in config.keys() :
            config["auto_login"] = False
        # 2022.03.08 修改参数
        if "dict_info_url" in config.keys():
            config["dict_info_url"] = "https://dango.c4a15wh.cn/DangoTranslate/ShowDict"
        # 2022.09.26 添加新参数
        if "agree_collect_time" not in config.keys() :
            config["agree_collect_time"] = "2022-09-25"
        # 2022.10.30 添加新参数
        if "selenium_debug" not in config.keys() :
            config["selenium_debug"] = False
        # 2022.11.13 添加新参数
        if "range" in config.keys() :
            del config["range"]
        if "range1" not in config.keys() :
            config["range1"] = {"x": 0, "y": 0, "w": 0, "h": 0}
        if "range2" not in config.keys() :
            config["range2"] = {"x": 0, "y": 0, "w": 0, "h": 0}
        if "range3" not in config.keys() :
            config["range3"] = {"x": 0, "y": 0, "w": 0, "h": 0}
        if "range4" not in config.keys() :
            config["range4"] = {"x": 0, "y": 0, "w": 0, "h": 0}

    except Exception :
        logger.error(format_exc())
        config = {
            "user": "",
            "password": "",
            "dict_info_url": "https://dango.c4a15wh.cn/DangoTranslate/ShowDict",
            "ocr_cmd_path": ".\ocr\startOCR.cmd",
            "port": 6666,
            "auto_login": False
        }

    return config


# 保存配置文件
def saveConfig(config, logger) :

    config = config.copy()
    del config["dict_info"]
    try :
        with open(YAML_PATH, "w", encoding="utf-8") as file :
            yaml.dump(config, file)
    except Exception :
        logger.error(format_exc())


# 获取字典表
def getDictInfo(url, logger) :

    res = utils.http.post(url, {}, logger)
    if not res :
        res = utils.http.post("https://trans.dango.cloud/DangoTranslate/ShowDict", {}, logger)
    result = res.get("Result", {})

    return result


# 从服务器获取用户配置信息
def getDangoSettin(object) :

    url = object.yaml["dict_info"]["dango_get_config"]
    body = {
        "User": object.yaml["user"]
    }

    res = utils.http.post(url, body, object.logger)
    if not res:
        url = "https://trans.dango.cloud/DangoTranslate/GetSettin"
        res = utils.http.post(url, body, object.logger)
    result = res.get("Result", {})
    try :
        result = json.loads(result)
    except Exception :
        return {}
    if result == "User dose not exist" :
        return {}
    elif type(result) != dict :
        return {}

    return result


# 配置转换
def configConvert(object) :

    ################### OCR设定 ###################
    # 本地OCR开关
    object.config["offlineOCR"] = object.config.get("offlineOCR", False)
    # 在线OCR开关
    object.config["onlineOCR"] = object.config.get("onlineOCR", False)
    # 在线OCR节点
    object.config["nodeURL"] = object.config.get("nodeURL", object.yaml["dict_info"]["ocr_server"])
    node_info = eval(object.yaml["dict_info"]["ocr_node"])
    if object.config["nodeURL"] not in node_info.values() :
        object.config["nodeURL"] = object.yaml["dict_info"]["ocr_server"]
    # 百度OCR开关
    object.config["baiduOCR"] = object.config.get("baiduOCR", False)
    # 百度OCR密钥
    object.config["OCR"] = object.config.get("OCR", {})
    object.config["OCR"]["Secret"] = object.config["OCR"].get("Secret", "")
    object.config["OCR"]["Key"] = object.config["OCR"].get("Key", "")
    object.config["AccessToken"] = object.config.get("AccessToken", "")
    # 百度OCR高精度开关
    object.config["OCR"]["highPrecision"] = object.config["OCR"].get("highPrecision", False)
    # 翻译语种
    object.config["language"] = object.config.get("language", "JAP")

    ################### 翻译设定 ###################
    # 字体颜色
    object.config["fontColor"] = object.config.get("fontColor", {})
    # 字体颜色 公共有道
    object.config["fontColor"]["youdao"] = object.config["fontColor"].get("youdao", "#5B8FF9")
    # 字体颜色 公共百度
    object.config["fontColor"]["baiduweb"] = object.config["fontColor"].get("baiduweb", "#5B8FF9")
    # 字体颜色 公共腾讯
    object.config["fontColor"]["tencentweb"] = object.config["fontColor"].get("tencentweb", "#5B8FF9")
    # 字体颜色 公共DeepL
    object.config["fontColor"]["deepl"] = object.config["fontColor"].get("deepl", "#5B8FF9")
    # 字体颜色 公共Bing
    object.config["fontColor"]["bing"] = object.config["fontColor"].get("bing", "#5B8FF9")
    # 字体颜色 公共彩云
    object.config["fontColor"]["caiyun"] = object.config["fontColor"].get("caiyun", "#5B8FF9")
    # 字体颜色 私人腾讯
    object.config["fontColor"]["tencent"] = object.config["fontColor"].get("tencent", "#5B8FF9")
    # 字体颜色 私人百度
    object.config["fontColor"]["baidu"] = object.config["fontColor"].get("baidu", "#5B8FF9")
    # 字体颜色 私人彩云
    object.config["fontColor"]["caiyunPrivate"] = object.config["fontColor"].get("caiyunPrivate", "#5B8FF9")
    # 原文颜色
    object.config["fontColor"]["original"] = object.config["fontColor"].get("original", "#5B8FF9")

    # 公共有道翻译开关
    object.config["youdaoUse"] = object.config.get("youdaoUse", "False")
    # 公共百度翻译开关
    object.config["baiduwebUse"] = object.config.get("baiduwebUse", "False")
    # 公共腾讯翻译开关
    object.config["tencentwebUse"] = object.config.get("tencentwebUse", "False")
    # 公共DeepL翻译开关
    object.config["deeplUse"] = object.config.get("deeplUse", "False")
    # 公共bing翻译开关
    object.config["bingUse"] = object.config.get("bingUse", "False")
    # 公共彩云翻译开关
    object.config["caiyunUse"] = object.config.get("caiyunUse", "False")
    # 私人腾讯翻译开关
    object.config["tencentUse"] = object.config.get("tencentUse", "False")
    # 私人百度翻译开关
    object.config["baiduUse"] = object.config.get("baiduUse", "False")
    # 私人彩云翻译开关
    object.config["caiyunPrivateUse"] = object.config.get("caiyunPrivateUse", "False")

    # 确保版本转换后至多只有2个翻译源能被同时开始
    tmp = []
    for val in ["youdaoUse", "baiduwebUse", "tencentwebUse", "deeplUse", "bingUse",
                "caiyunUse", "tencentUse", "baiduUse", "caiyunPrivateUse"] :
        if object.config[val] == "True" :
            tmp.append(val)
    if len(tmp) > 3 :
        count = 0
        for val in tmp :
            object.config[val] = "False"
            count += 1
            if len(tmp) - count <= 3 :
                break

    # 私人腾讯翻译密钥
    object.config["tencentAPI"] = object.config.get("tencentAPI", {})
    object.config["tencentAPI"]["Secret"] = object.config["tencentAPI"].get("Secret", "")
    object.config["tencentAPI"]["Key"] = object.config["tencentAPI"].get("Key", "")
    # 私人百度翻译密钥
    object.config["baiduAPI"] = object.config.get("baiduAPI", {})
    object.config["baiduAPI"]["Secret"] = object.config["baiduAPI"].get("Secret", "")
    object.config["baiduAPI"]["Key"] = object.config["baiduAPI"].get("Key", "")
    # 私人彩云翻译密钥
    object.config["caiyunAPI"] = object.config.get("caiyunAPI", "")

    ################### 其他设定 ###################
    # 翻译界面透明度
    object.config["horizontal"] = object.config.get("horizontal", 30)
    # 字体大小
    object.config["fontSize"] = object.config.get("fontSize", 15)
    # 字体
    object.config["fontType"] = object.config.get("fontType", "华康方圆体W7")
    # 字体样式开关
    object.config["showColorType"] = object.config.get("showColorType", "False")
    # 自动翻译时间间隔
    object.config["translateSpeed"] = object.config.get("translateSpeed", 0.5)
    # 显示原文开关
    object.config["showOriginal"] = object.config.get("showOriginal", "False")
    # 原文自动复制到剪贴板开关
    object.config["showClipboard"] = object.config.get("showClipboard", "False")
    # 文字方向
    object.config["showTranslateRow"] = object.config.get("showTranslateRow", "False")
    # 文字换行
    object.config["BranchLineUse"] = object.config.get("BranchLineUse", False)
    # 翻译快捷键
    object.config["translateHotkeyValue1"] = object.config.get("translateHotkeyValue1", "ctrl")
    object.config["translateHotkeyValue2"] = object.config.get("translateHotkeyValue2", "d")
    # 翻译快捷键开关
    object.config["showHotKey1"] = object.config.get("showHotKey1", "False")
    # 范围快捷键
    object.config["rangeHotkeyValue1"] = object.config.get("rangeHotkeyValue1", "ctrl")
    object.config["rangeHotkeyValue2"] = object.config.get("rangeHotkeyValue2", "f")
    # 范围快捷键开关
    object.config["showHotKey2"] = object.config.get("showHotKey2", "False")
    # 屏蔽词
    object.config["Filter"] = object.config.get("Filter", [])
    # 图像相似度
    object.config["imageSimilarity"] = object.config.get("imageSimilarity", 98)
    # 文字相似度
    object.config["textSimilarity"] = object.config.get("textSimilarity", 90)
    # 显示消息栏
    object.config["showStatusbarUse"] = object.config.get("showStatusbarUse", True)
    # 贴字翻译开关
    object.config["drawImageUse"] = object.config.get("drawImageUse", False)
    # 隐藏范围快捷键
    object.config["hideRangeHotkeyValue1"] = object.config.get("hideRangeHotkeyValue1", "ctrl")
    object.config["hideRangeHotkeyValue2"] = object.config.get("hideRangeHotkeyValue2", "x")
    # 隐藏范围快捷键开关
    object.config["showHotKey3"] = object.config.get("showHotKey3", False)
    # 是否全屏下置顶开关
    object.config["setTop"] =  object.config.get("setTop", False)
    # 是否同步翻译历史开关
    object.config["agreeCollectUse"] = object.config.get("agreeCollectUse", True)

    # 范围状态开关
    object.config["switch1Use"] = object.config.get("switch1Use", True)
    object.config["switch2Use"] = object.config.get("switch2Use", False)
    object.config["switch3Use"] = object.config.get("switch3Use", False)
    object.config["switch4Use"] = object.config.get("switch4Use", False)
    # 切换范围快捷键
    object.config["choiceRangeHotkeyValue"] = object.config.get("choiceRangeHotkeyValue", "ctrl")
    # 切换范围快捷键开关
    object.config["choiceRangeHotKey"] = object.config.get("choiceRangeHotKey", False)


# 保存配置至服务器
def postSaveSettin(object) :

    url = object.yaml["dict_info"]["dango_save_settin"]
    body = {
        "User": object.yaml["user"],
        "Data": json.dumps(object.config)
    }
    res = utils.http.post(url, body, object.logger)
    if not res:
        url = "https://trans.dango.cloud/DangoTranslate/SaveSettin"
        utils.http.post(url, body, object.logger)


# 保存识别到的原文
def saveOriginalHisTory(original) :

    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    with open(HISTORY_FILE_PATH, "a+", encoding="utf-8") as file :
        file.write("\n\n[原文][%s]\n%s\n"%(date, original))


# 保存翻译历史
def saveTransHisTory(text, translate_type) :

    if translate_type == "youdao" :
        content = "[公共有道]\n%s\n"%text
    elif translate_type == "caiyun" :
        content = "[公共彩云]\n%s\n"%text
    elif translate_type == "deepl" :
        content = "[公共DeepL]\n%s\n"%text
    elif translate_type == "baidu" :
        content = "[公共百度]\n%s\n"%text
    elif translate_type == "tencent" :
        content = "[公共腾讯]\n%s\n"%text
    elif translate_type == "bing" :
        content = "[公共Bing]\n%s\n"%text
    elif translate_type == "baidu_private" :
        content = "[私人百度]\n%s\n"%text
    elif translate_type == "tencent_private" :
        content = "[私人腾讯]\n%s\n"%text
    elif translate_type == "caiyun_private" :
        content = "[私人彩云]\n%s\n"%text
    else:
        return

    with open(HISTORY_FILE_PATH, "a+", encoding="utf-8") as file :
        file.write(content)


# 获取版本广播信息
def getVersionMessage(object) :

    url = object.yaml["dict_info"]["dango_get_inform"]
    body = {
        "version": object.yaml["version"]
    }
    res = utils.http.post(url, body, object.logger)
    if not res:
        url = "https://trans.dango.cloud/DangoTranslate/Getinform"
        res = utils.http.post(url, body, object.logger)
    return res.get("Result", "")



# 从本地获取配置信息
def readCloudConfigFormLocal(logger) :

    config = None
    try :
        with open(CLOUD_CONFIG_PATH, "r", encoding="utf-8") as file:
            config = json.loads(file.read())
    except Exception :
        logger.error(format_exc())

    return config


# 保存云端配置文件至本地
def saveCloudConfigToLocal(object) :

    try :
        with open(CLOUD_CONFIG_PATH, "w", encoding="utf-8") as file:
            json.dump(object.config, file, indent=4, ensure_ascii=False)
    except Exception :
        object.logger.error(format_exc())