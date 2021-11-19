import yaml
import json
from traceback import format_exc

import utils.http


YAML_PATH = "./config/config.yaml"


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
            "dict_info_url": "http://120.24.146.175:3000/DangoTranslate/ShowDict",
        }


    return config


# 保存配置文件
def saveConfig(config, logger) :

    try :
        with open(YAML_PATH, "w", encoding="utf-8") as file :
            yaml.dump(config, file)
    except Exception :
        logger.error(format_exc())


# 获取字典表
def getDictInfo(url, logger) :

    res = utils.http.post(url, {}, logger)
    result = res.get("Result", {})

    return result


# 从服务器获取用户配置信息
def getSettin(object) :

    url = object.yaml["dict_info"]["dango_get_config"]
    body = {
        "User": object.yaml["user"]
    }

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

    #config = configConvert(config, json.loads(result))


