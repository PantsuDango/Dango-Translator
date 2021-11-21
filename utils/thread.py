from PyQt5.QtCore import *
import threading

import utils.config
import utils.email
import utils.message


# 创建线程
def createThread(func, *args) :

    thread = threading.Thread(target=func, args=args)
    thread.setDaemon(True)
    thread.start()


# 不守护的线程
def createThreadDaemonFalse(func, *args) :

    thread = threading.Thread(target=func, args=args)
    thread.setDaemon(False)
    thread.start()


# 运行QThread
def runQThread(qthread) :

    def func() :
        qthread.start()
        qthread.wait()

    thread = threading.Thread(target=func)
    thread.setDaemon(True)
    thread.start()


# 检查绑定邮箱线程
class createCheckBindEmailQThread(QThread) :

    signal = pyqtSignal(bool)

    def __init__(self, object):

        super(createCheckBindEmailQThread, self).__init__()
        self.object = object


    def run(self) :

        if not utils.email.bindEmail(self.object):
            self.signal.emit(False)



# 打印翻译框默认信息线程
class createShowTranslateTextQThread(QThread) :

    signal = pyqtSignal(str)

    def __init__(self, object):

        super(createShowTranslateTextQThread, self).__init__()
        self.object = object


    def run(self) :

        # 获取版本广播信息
        result = utils.config.getVersionMessage(self.object)
        if result != "" and result != "No" :
            self.signal.emit(result)
        else :
            self.signal.emit("")