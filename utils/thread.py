from PyQt5.QtCore import *
import threading
import os
import utils.config
import utils.email
import utils.message
import utils.http
import traceback


# 创建线程
def createThread(func, *args) :

    thread = threading.Thread(target=func, args=args)
    thread.setDaemon(True)
    thread.start()

    return thread


# 不守护的线程
def createThreadDaemonFalse(func, *args) :

    thread = threading.Thread(target=func, args=args)
    thread.setDaemon(False)
    thread.start()

    return thread


# 运行QThread
def runQThread(qthread, mode=True) :

    def func() :
        qthread.start()
        qthread.wait()

    thread = threading.Thread(target=func)
    thread.setDaemon(mode)
    thread.start()

    return thread


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


# 检查版本线程
class createCheckVersionQThread(QThread) :

    signal = pyqtSignal(bool)

    def __init__(self, object):
        super(createCheckVersionQThread, self).__init__()
        self.object = object

    def run(self) :
        if self.object.yaml["version"] != self.object.yaml["dict_info"]["latest_version"] :
            self.signal.emit(False)


# 检查自动登录线程
class createCheckAutoLoginQThread(QThread) :

    signal = pyqtSignal(str)

    def __init__(self, object):
        super(createCheckAutoLoginQThread, self).__init__()
        self.object = object

    def run(self) :
        message = utils.http.loginCheck(self.object)
        if message :
            self.signal.emit(message)


# 漫画翻译进程
class createMangaTransQThread(QThread) :

    signal = pyqtSignal(str, bool)
    bar_signal = pyqtSignal(int, str)

    def __init__(self, window, image_paths, reload_sign=False):

        super(createMangaTransQThread, self).__init__()
        self.window = window
        self.logger = self.window.logger
        self.image_paths = image_paths
        self.reload_sign = reload_sign
        self.window.trans_process_bar.stop_sign = False
        self.window.trans_process_bar.finish_sign = False

    def run(self) :

        # 初始化进度条
        self.bar_signal.emit(0, "0/%d"%len(self.image_paths))
        try :
            for index, image_path in enumerate(self.image_paths) :
                # 翻译进程
                result = self.window.transProcess(image_path, self.reload_sign)
                # 如果失败记录日志
                if result :
                    self.logger.error(result)
                # # 发送刷新图片列表框信号
                # self.signal.emit(image_path, True)
                # 进度条
                self.bar_signal.emit(
                    int((index + 1) / len(self.image_paths) * 100),
                    "%d/%d"%(index + 1, len(self.image_paths))
                )
                # 如果停止
                if self.window.trans_process_bar.stop_sign :
                    break
        except Exception :
            self.logger.error(format_exc())
            self.signal.emit(traceback.format_exc(), False)
        # 结束
        self.window.trans_process_bar.finish_sign = True
        self.signal.emit("", False)


# 漫画翻译导入图片进程
class createInputImagesQThread(QThread) :

    bar_signal = pyqtSignal(float, int, str)
    image_widget_signal = pyqtSignal(str, bool)

    def __init__(self, window, images):

        super(createInputImagesQThread, self).__init__()
        self.window = window
        self.images = images
        self.window.input_images_progress_bar.stop_sign = False
        self.window.input_images_progress_bar.finish_sign = False

    def run(self) :

        # 初始化进度条
        self.bar_signal.emit(0, 0, "0/%d"%len(self.images))
        # 遍历文件列表, 将每个文件路径添加到列表框中
        for index, image_path in enumerate(self.images) :
            if image_path in self.window.image_path_list :
                continue
            self.image_widget_signal.emit(image_path, False)
            # 进度条
            self.bar_signal.emit(
                float((index + 1) / len(self.images) * 100),
                int((index + 1) / len(self.images) * 100),
                "%d/%d" % (index + 1, len(self.images))
            )
            # 如果停止
            if self.window.input_images_progress_bar.stop_sign :
                break
        self.window.input_images_progress_bar.finish_sign = True
        self.image_widget_signal.emit("", True)