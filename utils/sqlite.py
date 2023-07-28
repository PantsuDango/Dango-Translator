import os.path
import sqlite3
import re


DB_PATH = "../db/"
HISTORY_FILE_PATH = "../../翻译历史.txt"
TRANSLATION_DB = None


# 连接翻译历史数据库
def connectTranslationDB() :

    try :
        os.makedirs(DB_PATH)
    except FileExistsError :
        pass

    db_path = os.path.join(DB_PATH, "translation.db")
    TRANSLATION_DB = sqlite3.connect(db_path)

    # 创建翻译记录表
    create_translations_sql = '''
        CREATE TABLE IF NOT EXISTS translations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        src TEXT NOT NULL,
        trans_type TEXT NOT NULL,
        tgt TEXT NOT NULL,
        UNIQUE (`src`, `trans_type`, `tgt`));
    '''
    TRANSLATION_DB.execute(create_translations_sql)


# 读取旧翻译历史文件
def ReadTranslationHistory() :

    original_pattern = r'''\[原文\]\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'''
    text = ""
    trans_type_list = [
        "公共有道", "公共彩云", "公共DeepL", "公共百度", "公共腾讯", "公共Bing", "私人团子", "私人百度", "私人腾讯", "私人彩云",
        "私人ChatGPT", "私人阿里云", "私人有道"
    ]

    # 读取翻译历史文件
    with open(HISTORY_FILE_PATH, "r", encoding="utf-8") as file :
        for line in file :
            if re.match(original_pattern, line) :
                trans_map = {}
                # 提取原文
                re_result = re.findall(original_pattern+r"\n(.+?)\n\[", text, re.S)
                if re_result :

                    trans_map["src"] = re_result[0]
                    # 提取译文
                    for trans_type in trans_type_list :
                        trans_pattern = r'''\[{}\]'''.format(trans_type)
                        re_result = re.findall(trans_pattern+r"\n(.+?)\n", text, re.S)
                        if re_result :
                            trans_map[trans_type] = re_result[0]

                print(trans_map)
                print("------------------------------------------")
                text = line
            else :
                text += line


ReadTranslationHistory()