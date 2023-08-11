import yaml
import json
import time
from traceback import format_exc
import utils.http
import utils.sqlite
import translator.api


YAML_PATH = "./config/config.yaml"
HISTORY_FILE_PATH = "../翻译历史.txt"
CLOUD_CONFIG_PATH = "./config/cloud_config.json"


# 打开本地配置文件
def openConfig(logger) :

    try :
        with open(YAML_PATH, "r", encoding="utf-8") as file :
            config = yaml.load(file.read(), Loader=yaml.FullLoader)

    except Exception :
        logger.error(format_exc())
        config = {
            "user": "",
            "password": "",
            "dict_info_url": "https://trans.dango.cloud/DangoTranslate/ShowDict",
            "ocr_cmd_path": ".\ocr\startOCR.cmd",
            "port": 6666,
        }
    # 2022.02.19 添加新参数
    if "auto_login" not in config.keys() :
        config["auto_login"] = False
    # 2022.09.26 添加新参数
    if "agree_collect_time" not in config.keys() :
        config["agree_collect_time"] = "2022-09-25"
    # 2022.10.30 添加新参数
    if "selenium_debug" not in config.keys() :
        config["selenium_debug"] = False
    # 2022.11.13 添加新参数
    if "range" in config.keys() :
        del config["range"]
    if "range1" not in config.keys():
        config["range1"] = {"x": 0, "y": 0, "w": 0, "h": 0}
    if "range2" not in config.keys():
        config["range2"] = {"x": 0, "y": 0, "w": 0, "h": 0}
    if "range3" not in config.keys():
        config["range3"] = {"x": 0, "y": 0, "w": 0, "h": 0}
    if "range4" not in config.keys():
        config["range4"] = {"x": 0, "y": 0, "w": 0, "h": 0}
    # 2022.03.08 修改参数
    if "dict_info_url" in config.keys() :
        config["dict_info_url"] = "https://trans.dango.cloud/DangoTranslate/ShowDict"
    # 2023.07.03 自动打开图片翻译界面
    if "auto_open_manga_use" not in config.keys() :
        config["auto_open_manga_use"] = False
    # 2023.07.30 翻译历史数据同步
    if "sync_db" not in config.keys() :
        config["sync_db"] = False

    return config


# 保存配置文件
def saveConfig(config, logger) :

    config = config.copy()
    try :
        with open(YAML_PATH, "w", encoding="utf-8") as file :
            yaml.dump(config, file, allow_unicode=True, default_flow_style=False, sort_keys=False, Dumper=yaml.SafeDumper)
    except Exception :
        logger.error(format_exc())


# 获取字典表
def getDictInfo(url, logger) :

    res = utils.http.post(url, {}, logger)
    if not res :
        res = utils.http.post("https://43.154.0.93/DangoTranslate/ShowDict", {}, logger)
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

    # 修复开关采用字符串存值的问题
    use_map = {
        "True": True,
        "False": False
    }
    ################### OCR设定 ###################
    # 本地OCR开关
    object.config["offlineOCR"] = object.config.get("offlineOCR", False)
    # 在线OCR开关
    object.config["onlineOCR"] = object.config.get("onlineOCR", False)
    # 团子云Token
    object.config["DangoToken"] = object.config.get("DangoToken", "")
    # 试用在线OCR开关
    object.config["onlineOCRProbation"] = object.config.get("onlineOCRProbation", False)
    # 在线OCR节点
    object.config["nodeURL"] = object.config.get("nodeURL", object.yaml["dict_info"]["ocr_server"])
    node_info = json.loads(object.yaml["dict_info"]["ocr_node"])
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
    # 字体颜色 私人团子
    object.config["fontColor"]["dango"] = object.config["fontColor"].get("dango", "#5B8FF9")
    # 字体颜色 私人腾讯
    object.config["fontColor"]["tencent"] = object.config["fontColor"].get("tencent", "#5B8FF9")
    # 字体颜色 私人百度
    object.config["fontColor"]["baidu"] = object.config["fontColor"].get("baidu", "#5B8FF9")
    # 字体颜色 私人彩云
    object.config["fontColor"]["caiyunPrivate"] = object.config["fontColor"].get("caiyunPrivate", "#5B8FF9")
    # 字体颜色 私人ChatGPT
    object.config["fontColor"]["chatgptPrivate"] = object.config["fontColor"].get("chatgptPrivate", "#5B8FF9")
    # 字体颜色 私人阿里云
    object.config["fontColor"]["aliyunPrivate"] = object.config["fontColor"].get("aliyunPrivate", "#5B8FF9")
    # 字体颜色 私人有道
    object.config["fontColor"]["youdaoPrivate"] = object.config["fontColor"].get("youdaoPrivate", "#5B8FF9")
    # 字体颜色 私人小牛
    object.config["fontColor"]["xiaoniuPrivate"] = object.config["fontColor"].get("xiaoniuPrivate", "#5B8FF9")
    # 字体颜色 私人火山
    object.config["fontColor"]["huoshanPrivate"] = object.config["fontColor"].get("huoshanPrivate", "#5B8FF9")
    # 原文颜色
    object.config["fontColor"]["original"] = object.config["fontColor"].get("original", "#5B8FF9")

    # 公共有道翻译开关
    object.config["youdaoUse"] = object.config.get("youdaoUse", False)
    if object.config["youdaoUse"] in use_map :
        object.config["youdaoUse"] = use_map[object.config["youdaoUse"]]
    # 公共百度翻译开关
    object.config["baiduwebUse"] = object.config.get("baiduwebUse", False)
    if object.config["baiduwebUse"] in use_map :
        object.config["baiduwebUse"] = use_map[object.config["baiduwebUse"]]
    # 公共腾讯翻译开关
    object.config["tencentwebUse"] = object.config.get("tencentwebUse", False)
    if object.config["tencentwebUse"] in use_map :
        object.config["tencentwebUse"] = use_map[object.config["tencentwebUse"]]
    # 公共DeepL翻译开关
    object.config["deeplUse"] = object.config.get("deeplUse", False)
    if object.config["deeplUse"] in use_map :
        object.config["deeplUse"] = use_map[object.config["deeplUse"]]
    # 公共bing翻译开关
    object.config["bingUse"] = object.config.get("bingUse", False)
    if object.config["bingUse"] in use_map :
        object.config["bingUse"] = use_map[object.config["bingUse"]]
    # 公共彩云翻译开关
    object.config["caiyunUse"] = object.config.get("caiyunUse", False)
    if object.config["caiyunUse"] in use_map :
        object.config["caiyunUse"] = use_map[object.config["caiyunUse"]]
    # 私人团子翻译开关
    object.config["dangoUse"] = object.config.get("dangoUse", False)
    if object.config["dangoUse"] in use_map :
        object.config["dangoUse"] = use_map[object.config["dangoUse"]]
    # 私人腾讯翻译开关
    object.config["tencentUse"] = object.config.get("tencentUse", False)
    if object.config["tencentUse"] in use_map :
        object.config["tencentUse"] = use_map[object.config["tencentUse"]]
    # 私人百度翻译开关
    object.config["baiduUse"] = object.config.get("baiduUse", False)
    if object.config["baiduUse"] in use_map :
        object.config["baiduUse"] = use_map[object.config["baiduUse"]]
    # 私人彩云翻译开关
    object.config["caiyunPrivateUse"] = object.config.get("caiyunPrivateUse", False)
    if object.config["caiyunPrivateUse"] in use_map :
        object.config["caiyunPrivateUse"] = use_map[object.config["caiyunPrivateUse"]]
    # 私人ChatGPT翻译开关
    object.config["chatgptPrivateUse"] = object.config.get("chatgptPrivateUse", False)
    if object.config["chatgptPrivateUse"] in use_map :
        object.config["chatgptPrivateUse"] = use_map[object.config["chatgptPrivateUse"]]
    # 私人阿里云翻译开关
    object.config["aliyunPrivateUse"] = object.config.get("aliyunPrivateUse", False)
    if object.config["aliyunPrivateUse"] in use_map :
        object.config["aliyunPrivateUse"] = use_map[object.config["aliyunPrivateUse"]]
    # 私人有道翻译开关
    object.config["youdaoPrivateUse"] = object.config.get("youdaoPrivateUse", False)
    # 私人小牛翻译开关
    object.config["xiaoniuPrivateUse"] = object.config.get("xiaoniuPrivateUse", False)
    # 私人火山翻译开关
    object.config["huoshanPrivateUse"] = object.config.get("huoshanPrivateUse", False)

    # 确保版本转换后至多只有3个翻译源能被同时开始
    tmp = []
    for val in ["youdaoUse", "baiduwebUse", "tencentwebUse", "deeplUse", "bingUse", "caiyunUse", "tencentUse",
                "baiduUse", "caiyunPrivateUse", "chatgptPrivateUse", "dangoUse", "aliyunPrivateUse", "youdaoPrivateUse",
                "xiaoniuPrivateUse", "huoshanPrivateUse"] :
        if object.config[val] == True :
            tmp.append(val)
    if len(tmp) > 3 :
        count = 0
        for val in tmp :
            object.config[val] = False
            count += 1
            if len(tmp) - count <= 3 :
                break

    # 私人腾讯翻译密钥
    object.config["tencentAPI"] = object.config.get("tencentAPI", {})
    object.config["tencentAPI"]["Key"] = object.config["tencentAPI"].get("Key", "")
    object.config["tencentAPI"]["Secret"] = object.config["tencentAPI"].get("Secret", "")
    # 私人百度翻译密钥
    object.config["baiduAPI"] = object.config.get("baiduAPI", {})
    object.config["baiduAPI"]["Key"] = object.config["baiduAPI"].get("Key", "")
    object.config["baiduAPI"]["Secret"] = object.config["baiduAPI"].get("Secret", "")
    # 私人彩云翻译密钥
    object.config["caiyunAPI"] = object.config.get("caiyunAPI", "")
    # 私人ChatGPT翻译密钥
    object.config["chatgptAPI"] = object.config.get("chatgptAPI", "")
    # 私人阿里云翻译密钥
    object.config["aliyunAPI"] = object.config.get("aliyunAPI", {})
    object.config["aliyunAPI"]["Key"] = object.config["aliyunAPI"].get("Key", "")
    object.config["aliyunAPI"]["Secret"] = object.config["aliyunAPI"].get("Secret", "")
    # 私人有道翻译密钥
    object.config["youdaoAPI"] = object.config.get("youdaoAPI", {})
    object.config["youdaoAPI"]["Key"] = object.config["youdaoAPI"].get("Key", "")
    object.config["youdaoAPI"]["Secret"] = object.config["youdaoAPI"].get("Secret", "")
    # 私人小牛翻译密钥
    object.config["xiaoniuAPI"] = object.config.get("xiaoniuAPI", "")
    # 私人火山翻译密钥
    object.config["huoshanAPI"] = object.config.get("huoshanAPI", {})
    object.config["huoshanAPI"]["Key"] = object.config["huoshanAPI"].get("Key", "")
    object.config["huoshanAPI"]["Secret"] = object.config["huoshanAPI"].get("Secret", "")

    # 私人ChatGPT翻译代理
    object.config["chatgptProxy"] = object.config.get("chatgptProxy", "")
    # 私人ChatGPT接口地址
    object.config["chatgptApiAddr"] = object.config.get("chatgptApiAddr", "https://api.openai.com/v1/chat/completions")
    # 私人ChatGPT模型
    object.config["chatgptModel"] = object.config.get("chatgptModel", "gpt-3.5-turbo-0613")
    # chatgpt prompt
    object.config["chatgptPrompt"] = object.config.get("chatgptPrompt", translator.api.CHATGPT_PROMPT)
    # chatgpt联系上下文开关
    object.config["chatgptContextUse"] = object.config.get("chatgptContextUse", True)
    # chatgpt联系上下文句子数
    object.config["chatgptContextCount"] = object.config.get("chatgptContextCount", 5)

    ################### 其他设定 ###################
    # 翻译界面透明度
    object.config["horizontal"] = object.config.get("horizontal", 30)
    # 字体大小
    object.config["fontSize"] = object.config.get("fontSize", 15)
    # 字体
    object.config["fontType"] = object.config.get("fontType", "华康方圆体W7")
    # 字体样式开关
    object.config["showColorType"] = object.config.get("showColorType", False)
    if object.config["showColorType"] in use_map :
        object.config["showColorType"] = use_map[object.config["showColorType"]]
    # 自动翻译时间间隔
    object.config["translateSpeed"] = object.config.get("translateSpeed", 0.5)
    # 显示原文开关
    object.config["showOriginal"] = object.config.get("showOriginal", False)
    if object.config["showOriginal"] in use_map :
        object.config["showOriginal"] = use_map[object.config["showOriginal"]]
    # 原文自动复制到剪贴板开关
    object.config["showClipboard"] = object.config.get("showClipboard", False)
    if object.config["showClipboard"] in use_map :
        object.config["showClipboard"] = use_map[object.config["showClipboard"]]
    # 文字方向
    object.config["showTranslateRow"] = object.config.get("showTranslateRow", False)
    if object.config["showTranslateRow"] in use_map :
        object.config["showTranslateRow"] = use_map[object.config["showTranslateRow"]]
    # 文字换行
    object.config["BranchLineUse"] = object.config.get("BranchLineUse", False)
    # 翻译快捷键
    object.config["translateHotkeyValue1"] = object.config.get("translateHotkeyValue1", "ctrl")
    object.config["translateHotkeyValue2"] = object.config.get("translateHotkeyValue2", "d")
    # 翻译快捷键开关
    object.config["showHotKey1"] = object.config.get("showHotKey1", False)
    if object.config["showHotKey1"] in use_map :
        object.config["showHotKey1"] = use_map[object.config["showHotKey1"]]
    # 范围快捷键
    object.config["rangeHotkeyValue1"] = object.config.get("rangeHotkeyValue1", "ctrl")
    object.config["rangeHotkeyValue2"] = object.config.get("rangeHotkeyValue2", "f")
    # 范围快捷键开关
    object.config["showHotKey2"] = object.config.get("showHotKey2", False)
    if object.config["showHotKey2"] in use_map :
        object.config["showHotKey2"] = use_map[object.config["showHotKey2"]]
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
    object.config["hideRangeHotkeyValue2"] = object.config.get("hideRangeHotkeyValue2", "e")

    # 隐藏范围快捷键开关
    object.config["showHotKey3"] = object.config.get("showHotKey3", False)
    if object.config["showHotKey3"] in use_map :
        object.config["showHotKey3"] = use_map[object.config["showHotKey3"]]

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
    object.config["choiceRangeHotKeyUse"] = object.config.get("choiceRangeHotKeyUse", False)
    # 自动朗读开关
    object.config["autoPlaysoundUse"] = object.config.get("autoPlaysoundUse", False)
    # 图片翻译所使用的翻译源
    object.config["mangaTrans"] = object.config.get("mangaTrans", "私人团子")
    object.config["mangaLanguage"] = object.config.get("mangaLanguage", "JAP")
    # 图片翻译高级设置
    object.config["mangaDetectScale"] = object.config.get("mangaDetectScale", 1)
    object.config["mangaMergeThreshold"] = object.config.get("mangaMergeThreshold", 5.0)
    object.config["mangaFontColor"] = object.config.get("mangaFontColor", "#83AAF9")
    object.config["mangaBgColor"] = object.config.get("mangaBgColor", "#83AAF9")
    object.config["mangaFontColorUse"] = object.config.get("mangaFontColorUse", False)
    object.config["mangaBgColorUse"] = object.config.get("mangaBgColorUse", False)
    object.config["mangaFontType"] = object.config.get("mangaFontType", "Noto_Sans_SC/NotoSansSC-Regular")
    object.config["mangaOutputRenameUse"] = object.config.get("mangaOutputRenameUse", False)
    object.config["mangaFastRenderUse"] = object.config.get("mangaFastRenderUse", False)
    object.config["mangaShadowSize"] = object.config.get("mangaShadowSize", 4)
    object.config["mangaFiltrateUse"] = object.config.get("mangaFiltrateUse", True)
    object.config["mangaFontSizeUse"] = object.config.get("mangaFontSizeUse", False)
    object.config["mangaFontSize"] = object.config.get("mangaFontSize", 36)
    object.config["mangaChatgptDelayUse"] = object.config.get("mangaChatgptDelayUse", False)
    object.config["mangaChatgptDelayTime"] = object.config.get("mangaChatgptDelayTime", 1)

    # 允许写入的key
    allow_keys = [
        "dictInfo", "offlineOCR", "onlineOCR", "DangoToken", "onlineOCRProbation", "nodeURL", "baiduOCR", "OCR", "AccessToken",
        "language", "fontColor", "youdaoUse", "baiduwebUse", "tencentwebUse", "deeplUse", "bingUse", "caiyunUse",
        "tencentUse", "baiduUse", "caiyunPrivateUse", "chatgptPrivateUse", "dangoUse", "aliyunPrivateUse", "tencentAPI",
        "baiduAPI", "caiyunAPI", "chatgptAPI", "aliyunAPI","chatgptProxy", "chatgptApiAddr", "chatgptModel",
        "horizontal", "fontSize", "fontType", "showColorType", "translateSpeed", "showOriginal", "showClipboard",
        "showTranslateRow", "BranchLineUse", "translateHotkeyValue1", "translateHotkeyValue2", "showHotKey1",
        "rangeHotkeyValue1", "rangeHotkeyValue2", "showHotKey2", "Filter", "imageSimilarity", "textSimilarity",
        "showStatusbarUse", "drawImageUse", "hideRangeHotkeyValue1", "hideRangeHotkeyValue2", "showHotKey3", "setTop",
        "agreeCollectUse", "switch1Use", "switch2Use", "switch3Use", "switch4Use", "choiceRangeHotkeyValue",
        "choiceRangeHotKeyUse", "autoPlaysoundUse", "mangaTrans", "mangaLanguage", "mangaDetectScale",
        "mangaMergeThreshold", "mangaFontColor", "mangaBgColor", "mangaFontColorUse", "mangaBgColorUse",
        "mangaFontType", "mangaOutputRenameUse", "mangaFastRenderUse", "mangaShadowSize", "mangaFiltrateUse",
        "mangaFontSizeUse", "mangaFontSize", "youdaoPrivateUse", "youdaoAPI", "chatgptPrompt", "xiaoniuPrivateUse",
        "xiaoniuAPI", "huoshanPrivateUse", "huoshanAPI", "mangaChatgptDelayUse", "mangaChatgptDelayTime",
        "chatgptContextUse", "chatgptContextCount"
    ]
    # 删除多余的key
    delete_keys = []
    for key in object.config.keys() :
        if key not in allow_keys :
            delete_keys.append(key)
    for key in delete_keys :
        del object.config[key]


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
        with open(CLOUD_CONFIG_PATH, "r", encoding="utf-8") as file :
            config = json.loads(file.read())
    except Exception :
        logger.error(format_exc())

    return config


# 保存云端配置文件至本地
def saveCloudConfigToLocal(object) :

    try :
        with open(CLOUD_CONFIG_PATH, "w", encoding="utf-8") as file :
            json.dump(object.config, file, indent=4, ensure_ascii=False)
    except Exception :
        object.logger.error(format_exc())