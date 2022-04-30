import os
from traceback import print_exc

LOCK_FILE_PATH = os.path.join(os.getcwd(), "config", "dango.lock")

# 创建锁文件
def createLock() :
    with open(LOCK_FILE_PATH, "w") :
        pass

# 删除锁文件
def deleteLock() :
    try :
        os.remove(LOCK_FILE_PATH)
    except Exception :
        print_exc()
        pass

# 校验锁文件是否存在
def checkLock() :
    return os.path.exists(LOCK_FILE_PATH)