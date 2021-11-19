import yaml
import utils.http
from traceback import format_exc


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

    res = utils.http.post(url=url, body={}, logger=logger)
    result = res.get("Result", {})

    return result