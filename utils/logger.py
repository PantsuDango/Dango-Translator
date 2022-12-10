import logging
import os
import time
import datetime

LOG_PATH = "../logs/"

# 设置日志文件
def setLog() :

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    log_file_name = date + ".log"
    logPath = LOG_PATH + log_file_name

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


# 清理日志
def clearLog() :
    log_list = os.listdir(LOG_PATH)
    for filename in log_list :
        if ".log" not in filename :
            continue
        log_date = filename.split(".log")[0]
        time_point = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d")
        if log_date < time_point :
            os.remove(LOG_PATH+filename)
