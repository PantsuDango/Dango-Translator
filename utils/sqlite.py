import os.path
import sqlite3
import re
import datetime
import traceback

DB_PATH = "../db/"
HISTORY_FILE_PATH = "../翻译历史.txt"
TRANS_MAP = {
    "公共有道": "youdao",
    "公共彩云": "caiyun",
    "公共DeepL": "deepl",
    "公共百度": "baidu",
    "公共腾讯": "tencent",
    "公共Bing": "bing",
    "私人团子": "dango_private",
    "私人百度": "baidu_private",
    "私人腾讯": "tencent_private",
    "私人彩云": "caiyun_private",
    "私人ChatGPT": "chatgpt_private",
    "私人阿里": "aliyun_private",
    "私人有道": "youdao_private",
}
TRANS_MAP_INVERSION = {
    "youdao": "公共有道",
    "caiyun": "公共彩云",
    "deepl": "公共DeepL",
    "baidu": "公共百度",
    "tencent": "公共腾讯",
    "bing": "公共Bing",
    "dango_private": "私人团子",
    "baidu_private": "私人百度",
    "tencent_private": "私人腾讯",
    "caiyun_private": "私人彩云",
    "chatgpt_private": "私人ChatGPT",
    "aliyun_private": "私人阿里",
    "youdao_private": "私人有道"
}


# 连接翻译历史数据库
def connectTranslationDB(logger) :

    try :
        os.makedirs(DB_PATH)
    except FileExistsError :
        pass

    try :
        # 连接数据库
        global TRANSLATION_DB
        db_path = os.path.join(DB_PATH, "translation.db")
        TRANSLATION_DB = sqlite3.connect(db_path, check_same_thread=False)
        # 初始化翻译记录表
        sql = '''
            CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            src TEXT NOT NULL,
            trans_type TEXT NOT NULL,
            tgt TEXT NOT NULL,
            create_time DATATIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (`src`, `trans_type`));
        '''
        TRANSLATION_DB.execute(sql)
    except Exception :
        logger.error(traceback.format_exc())


# 写入翻译历史数据库
def insertTranslationDB(logger, src, trans_type, tgt, create_time=None) :

    if trans_type in TRANS_MAP_INVERSION :
        trans_type = TRANS_MAP_INVERSION[trans_type]
    if re.match("^{}[:：]".format(trans_type), tgt) :
        return
    if trans_type in TRANS_MAP :
        trans_type = TRANS_MAP[trans_type]
    if not create_time :
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try :
        sql = '''
            INSERT INTO translations (src, trans_type, tgt, create_time)
            VALUES (?, ?, ?, ?);
        '''
        TRANSLATION_DB.execute(sql, (src, trans_type, tgt, create_time))
        TRANSLATION_DB.commit()
    except sqlite3.IntegrityError :
        pass
    except Exception :
        logger.error(traceback.format_exc())


# 查询翻译历史数据库
def selectTranslationDBList(count) :

    sql = '''SELECT * FROM translations ORDER BY id DESC LIMIT ?;'''
    cursor = TRANSLATION_DB.execute(sql, (count,))
    rows = cursor.fetchall()
    cursor.close()

    return rows


# 同步旧翻译历史文件
def SyncTranslationHistory(logger) :

    time_pattern = r'''\[原文\]\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]'''
    original_pattern = r'''\[原文\]\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'''
    text = ""

    # 读取翻译历史文件
    with open(HISTORY_FILE_PATH, "r", encoding="utf-8") as file :
        for line in file :
            re_result = re.findall(time_pattern, line)
            if re_result :
                create_time = re_result[0]
                trans_map = {}
                src = ""
                # 提取原文
                re_result = re.findall(original_pattern+r"\n(.+?)\n\[", text, re.S)
                if re_result :
                    src = re_result[0]
                    # 提取译文
                    for trans_type in TRANS_MAP.keys() :
                        trans_pattern = r'''\[{}\]'''.format(trans_type)
                        re_result = re.findall(trans_pattern+r"\n(.+?)\n", text, re.S)
                        if re_result :
                            trans_map[trans_type] = re_result[0]
                # 写入翻译历史数据库
                if src and len(trans_map) >= 1 :
                    values = []
                    for trans_type, tgt in trans_map.items() :
                        insertTranslationDB(logger, src, trans_type, tgt, create_time)

                text = line
            else :
                text += line


# 数据库初始化
def initTranslationDB(object) :

    if not object.yaml["sync_db"] :
        SyncTranslationHistory(object.logger)
        object.yaml["sync_db"] = True
