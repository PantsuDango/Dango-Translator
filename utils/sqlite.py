import os.path
import sqlite3
import re
import datetime
import time
import traceback
import csv

DB_PATH = "../db/"
HISTORY_FILE_PATH = "../翻译历史.txt"
TRANSLATION_DB = None
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
    "私人阿里云": "aliyun_private",
    "私人有道": "youdao_private",
    "私人小牛": "xiaoniu_private",
    "私人火山": "huoshan_private"
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
    "youdao_private": "私人有道",
    "xiaoniu_private": "私人小牛",
    "huoshan_private": "私人火山"
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
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (`src`, `trans_type`));
        '''
        TRANSLATION_DB.execute(sql)
        sql = '''
            CREATE INDEX IF NOT EXISTS src ON translations (src);
        '''
        TRANSLATION_DB.execute(sql)
        TRANSLATION_DB.commit()
    except Exception :
        logger.error(traceback.format_exc())


# 写入翻译历史数据库
def insertTranslationDB(logger, src, trans_type, tgt, create_time=None) :

    # 原文不能为空
    if not tgt :
        return
    # 校验数据库连接
    global TRANSLATION_DB
    if not TRANSLATION_DB :
        return
    # 过滤是否是异常的翻译结果
    if trans_type in TRANS_MAP_INVERSION :
        trans_type = TRANS_MAP_INVERSION[trans_type]
    if re.match("^{}[:：]".format(trans_type), tgt) :
        return
    # 统一翻译类型基于TRANS_MAP
    if trans_type in TRANS_MAP :
        trans_type = TRANS_MAP[trans_type]
    # 使用当前时间
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
        sql = '''
            UPDATE translations SET tgt = ? WHERE src =? AND trans_type = ?;
        '''
        TRANSLATION_DB.execute(sql, (tgt, src, trans_type))
        TRANSLATION_DB.commit()
    except Exception :
        logger.error(traceback.format_exc())


# 查询翻译历史数据库
def selectTranslationDBList(src, tgt, limit, offset, logger) :

    rows = []
    global TRANSLATION_DB
    if not TRANSLATION_DB :
        return rows

    try :
        if src :
            if tgt :
                sql = '''SELECT id, trans_type, src, tgt FROM translations WHERE src LIKE '%{}%' AND tgt LIKE '%{}%' ORDER BY id DESC LIMIT ? OFFSET ?;'''.format(src, tgt)
            else :
                sql = '''SELECT id, trans_type, src, tgt FROM translations WHERE src LIKE '%{}%' ORDER BY id DESC LIMIT ? OFFSET ?;'''.format(src)
        else:
            if tgt :
                sql = '''SELECT id, trans_type, src, tgt FROM translations WHERE tgt LIKE '%{}%' ORDER BY id DESC LIMIT ? OFFSET ?;'''.format(tgt)
            else :
                sql = '''SELECT id, trans_type, src, tgt FROM translations ORDER BY id DESC LIMIT ? OFFSET ?;'''
        cursor = TRANSLATION_DB.execute(sql, (limit, offset))
        rows = cursor.fetchall()
        cursor.close()
    except Exception :
        logger.error(traceback.format_exc())

    return rows


# 查询翻译历史数据库
def selectTranslationDBBySrcAndTransType(src, logger) :

    rows = []
    trans_map = {}
    global TRANSLATION_DB
    if not TRANSLATION_DB:
        return trans_map

    try :
        sql = '''SELECT * FROM translations WHERE src = ?;'''
        cursor = TRANSLATION_DB.execute(sql, (src,))
        rows = cursor.fetchall()
        cursor.close()
    except Exception :
        logger.error(traceback.format_exc())

    for row in rows :
        trans_map[row[2]] = row[3]

    return trans_map


# 同步旧翻译历史文件
def SyncTranslationHistory(logger) :

    global TRANSLATION_DB
    if not TRANSLATION_DB :
        return

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

    global TRANSLATION_DB
    if not TRANSLATION_DB :
        return

    if not object.yaml["sync_db"] :
        SyncTranslationHistory(object.logger)
        object.yaml["sync_db"] = True


# 查询翻译历史总数
def selectTranslationDBTotal(src, tgt, logger) :

    result = 0
    global TRANSLATION_DB
    if not TRANSLATION_DB :
        return result

    try :
        if src :
            if tgt :
                sql = '''SELECT count(*) FROM translations WHERE src LIKE '%{}%' AND tgt LIKE '%{}%';'''.format(src, tgt)
            else :
                sql = '''SELECT count(*) FROM translations WHERE src LIKE '%{}%';'''.format(src)
        else :
            if tgt :
                sql = '''SELECT count(*) FROM translations WHERE tgt LIKE '%{}%';'''.format(tgt)
            else :
                sql = '''SELECT count(*) FROM translations;'''
        cursor = TRANSLATION_DB.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()
    except Exception :
        logger.error(traceback.format_exc())

    return result


# 导出所有数据
def outputTranslationDB(file_path, logger) :

    global TRANSLATION_DB
    if not TRANSLATION_DB :
        return

    sql = '''SELECT src, trans_type, tgt, create_time FROM translations;'''
    try :
        cursor = TRANSLATION_DB.execute(sql)
        titles = [description[0] for description in cursor.description]

        with open(file_path, "w", encoding="utf-8", newline="") as file :
            writer = csv.writer(file)
            writer.writerow(titles)
            while True:
                rows = cursor.fetchmany(10000)
                if not rows :
                    break
                writer.writerows(rows)
        cursor.close()
    except Exception :
        logger.error(traceback.format_exc())
        return traceback.format_exc()


# 修改原文翻译数据
def modifyTranslationDBSrc(id, src, logger) :

    global TRANSLATION_DB
    if not TRANSLATION_DB :
        return

    sql = '''UPDATE translations SET src = ? WHERE id = ?;'''
    try :
        TRANSLATION_DB.execute(sql, (src, id,))
        TRANSLATION_DB.commit()
    except Exception :
        logger.error(traceback.format_exc())
        return traceback.format_exc()


# 修改原文翻译数据
def modifyTranslationDBTgt(id, tgt, logger) :

    global TRANSLATION_DB
    if not TRANSLATION_DB :
        return

    sql = '''UPDATE translations SET tgt = ? WHERE id = ?;'''
    try :
        TRANSLATION_DB.execute(sql, (tgt, id,))
        TRANSLATION_DB.commit()
    except Exception :
        logger.error(traceback.format_exc())
        return traceback.format_exc()


# 删除翻译数据
def deleteTranslationDBByID(id, logger) :

    global TRANSLATION_DB
    if not TRANSLATION_DB :
        return

    sql = '''DELETE FROM translations WHERE id = ?;'''
    try :
        TRANSLATION_DB.execute(sql, (id,))
        TRANSLATION_DB.commit()
    except Exception :
        logger.error(traceback.format_exc())
        return traceback.format_exc()