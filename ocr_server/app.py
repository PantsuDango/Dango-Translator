from paddleocr import PaddleOCR
from flask import Flask, request, jsonify

from traceback import print_exc
import json
import uuid
import yaml


japOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="japan", enable_mkldnn=True)
engOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="en", enable_mkldnn=True)
korOcr = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="korean", enable_mkldnn=True)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 打开本地配置文件
def openConfig(path) :

    try :
        with open(path, "r", encoding="utf-8") as file :
            config = yaml.load(file.read(), Loader=yaml.FullLoader)
        return int(config["port"])
    except Exception :
        return 6666


# 失败的返回
def jsonFail(message) :

    post_data = {
        "Code": -1,
        "Message": str(message),
        "RequestId": str(uuid.uuid4())
    }
    return jsonify(post_data)


# 成功的返回
def jsonSuccess(data) :

    post_data = {
        "Code": 0,
        "Message": "Success",
        "RequestId": str(uuid.uuid4()),
        "Data": data
    }
    return jsonify(post_data)


def ocrResultSort(ocr_result) :

    ocr_result.sort(key=lambda x: x[0][0][1])

    # 二次根据纵坐标数值分组（分行）
    allgroup = []
    newgroup = []
    flag = ocr_result[0][0][0][1]
    pram = max([int((i[0][3][1] - i[0][0][1]) / 2) for i in ocr_result])

    for sn, i in enumerate(ocr_result) :
        if abs(flag - i[0][0][1]) <= pram :
            newgroup.append(i)
        else:
            allgroup.append(newgroup)
            flag = i[0][0][1]
            newgroup = [i]
    allgroup.append(newgroup)

    # 单行内部按左上点横坐标排序
    allgroup = [sorted(i, key=lambda x: x[0][0][0]) for i in allgroup]
    # 去除分组，归一为大列表
    allgroup = [ii for i in allgroup for ii in i]
    # 列表输出为排序后txt
    allgroup = [ii for ii in allgroup]

    return allgroup


# ocr解析
def ocrProccess(imgPath, language) :

    if language == "JAP" :
        result = japOcr.ocr(imgPath, cls=False)
    elif language == "ENG" :
        result = engOcr.ocr(imgPath, cls=False)
    elif language == "KOR":
        result = korOcr.ocr(imgPath, cls=False)
    else :
        result = japOcr.ocr(imgPath, cls=False)

    try :
        result = ocrResultSort(result)
    except Exception :
        pass

    resMapList = []
    for line in result :
        print(line[1][0])
        resMap = {
            "Coordinate": {
                "UpperLeft": line[0][0],
                "UpperRight": line[0][1],
                "LowerRight": line[0][2],
                "LowerLeft": line[0][3]
            },
            "Words": line[1][0],
            "Score": float(line[1][1])
        }
        resMapList.append(resMap)
    print()

    return resMapList


# 接收请求
@app.route("/ocr/api", methods=["POST"])
def getPost() :

    try:
        post_data = request.get_data()
        post_data = json.loads(post_data.decode("utf-8"))

        languageList = ["JAP", "ENG", "KOR"]
        if post_data["Language"] not in languageList :
            return jsonFail("Language {} doesn't exist".format(post_data["Language"]))

        res = ocrProccess(post_data["ImagePath"], post_data["Language"])
        return jsonSuccess(res)

    except Exception as err:
        print_exc()
        return jsonFail(err)


if __name__ == "__main__" :

    port = openConfig("../config/config.yaml")
    app.run(debug=False, host="0.0.0.0", port=port, threaded=False)