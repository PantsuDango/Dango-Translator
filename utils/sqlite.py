import os.path
import sqlite3
import re
import datetime
import traceback

DB_PATH = "../db/"
HISTORY_FILE_PATH = "../翻译历史.txt"


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
        create_translations_sql = '''
            CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            src TEXT NOT NULL,
            trans_type TEXT NOT NULL,
            tgt TEXT NOT NULL,
            create_time DATATIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (`src`, `trans_type`, `tgt`));
        '''
        TRANSLATION_DB.execute(create_translations_sql)
    except Exception :
        logger.error(traceback.format_exc())


# 写入翻译历史数据库
def insertTranslationDB(logger, src, trans_type, tgt, create_time=None) :

    if not create_time :
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try :
        insert_translation_sql = '''
            INSERT INTO translations (src, trans_type, tgt, create_time)
            VALUES (?, ?, ?, ?);
        '''
        TRANSLATION_DB.execute(insert_translation_sql, (src, trans_type, tgt, create_time))
        TRANSLATION_DB.commit()
    except sqlite3.IntegrityError :
        pass
    except Exception :
        logger.error(traceback.format_exc())


# 同步旧翻译历史文件
def SyncTranslationHistory(logger) :

    time_pattern = r'''\[原文\]\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]'''
    original_pattern = r'''\[原文\]\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'''
    text = ""
    trans_type_list = [
        "公共有道", "公共彩云", "公共DeepL", "公共百度", "公共腾讯", "公共Bing", "私人团子",
        "私人百度", "私人腾讯", "私人彩云", "私人ChatGPT", "私人阿里云", "私人有道"
    ]
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
                    for trans_type in trans_type_list :
                        trans_pattern = r'''\[{}\]'''.format(trans_type)
                        re_result = re.findall(trans_pattern+r"\n(.+?)\n", text, re.S)
                        if re_result :
                            trans = re_result[0]
                            if re.match("^{}[:：]".format(trans_type), trans) :
                                continue
                            trans_map[trans_type] = trans
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
