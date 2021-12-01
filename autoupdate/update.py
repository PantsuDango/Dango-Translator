import requests
import json
import yaml
import os
import shutil
import sys

# 打开本地配置文件
def openConfig() :

    try :
        with open("./app/config/config.yaml", "r", encoding="utf-8") as file :
            config = yaml.load(file.read(), Loader=yaml.FullLoader)
    except Exception as err :
        return None, "获取本地版本号失败: %s"%err

    local_version = config.get("version", "")
    print("当前版本号:", local_version)

    return local_version, None


# 发送http请求
def post(url, body, timeout=5) :

    proxies = {
        "http": None,
        "https": None
    }

    try :
        # 消除https警告
        requests.packages.urllib3.disable_warnings()
    except Exception :
        pass

    try :
        with requests.post(url, data=json.dumps(body), proxies=proxies, verify=False, timeout=timeout) as response :
            try :
                response.encoding = "utf-8"
                result = json.loads(response.text)
            except Exception :
                response.encoding = "gb18030"
                result = json.loads(response.text)
    except Exception as err :
        return None, err

    return result, None


# 获取最新版本号
def getVersion() :

    res, err = post("https://trans.dango.cloud/DangoTranslate/ShowDict", {})
    if not res :
        res, err = post("https://dango.c4a15wh.cn/DangoTranslate/ShowDict", {})
    if err :
        return None, None, "获取最新版本号失败: %s"%err
    latest_version = res.get("Result", {}).get("latest_version", "")
    update_version = res.get("Result", {}).get("update_version", "")

    print("最新版本号:", latest_version)
    print("最新版本下载地址:", update_version)

    return latest_version, update_version, None


# 下载
def progressbar(url):

    size = 0
    chunk_size = 1024
    try :
        response = requests.get(url, stream=True)
        content_size = int(response.headers["content-length"])
        if response.status_code == 200 :
            print("文件大小:{size:.2f} MB".format(size=content_size/chunk_size/1024))
            with open("团子翻译器.exe", "wb") as file :
                for data in response.iter_content(chunk_size=chunk_size) :
                    file.write(data)
                    size +=len(data)
                    print("\r"+"[下载进度]:%s%.2f%%"%(">"*int(size*50/content_size), float(size/content_size * 100)) , end=" ")
        return None
    except Exception as err :
        try :
            os.remove("团子翻译器.exe")
        except Exception :
            pass
        return "下载失败: %s\n\n请尝试手动复制下载链接下载, 然后直接替换app目录内的'团子翻译器.exe'"%err


def main() :

    print(">>> 获取版本信息...")

    # 获取本地版本号
    local_version, err = openConfig()
    if err :
        return print(err)

    # 获取最新版本号
    latest_version, update_version, err = getVersion()
    if err :
        return print(err)
    if local_version == latest_version :
        return print("当前已是最新版本, 您无需更新")

    # 下载最新版本
    print("\n>>> 开始下载最新版本...")
    err = progressbar(update_version)
    if err :
        return print(err)

    # 替换版本文件
    print("\n>>> 替换新版本文件...")
    try :
        shutil.move("团子翻译器.exe", "./app/团子翻译器.exe")
        print("更新完成, 正在自动重启翻译器...")
        os.startfile("点我运行.exe")
        sys.exit()
    except Exception as err :
        return print("替换新版本文件失败: %s"%err)


if __name__ == "__main__" :

    main()
    input("\n请按任意键退出...")