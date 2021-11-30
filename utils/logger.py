import logging
import os
import time


# 设置日志文件
def setLog() :

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    log_file_name = date + ".log"
    logPath = "../logs/" + log_file_name

    try :
        os.makedirs("../logs")
    except FileExistsError :
        pass

    file_handler = logging.FileHandler(logPath, mode="a+", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s][%(pathname)s-line:%(lineno)d][%(levelname)s]\n%(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger