import re
import subprocess
from traceback import format_exc


# 检查端口是否被占用
def detectPort(port, logger) :

    cmd = ("netstat", "-a", "-n")
    try :
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        for line in p.stdout :
            if re.findall("0\.0\.0\.0:%d"%port, str(line)) :
                return True

        p.kill()

    except Exception :
        logger.error(format_exc())

    return False