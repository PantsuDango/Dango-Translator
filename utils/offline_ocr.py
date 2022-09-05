from PyQt5.QtCore import *
from traceback import format_exc
import shutil
import os
import time
import requests
import zipfile

import utils.message
import utils.thread
import ui.progress_bar

OCR_INSTALL_PATH = "ocr"
OCR_ZIP_FILE_NAME = "ocr.zip"


# 安装本地ocr
def install_offline_ocr(object) :

    # 判断本地ocr是否已安装
    if os.path.exists(object.yaml["ocr_cmd_path"]) :
        utils.message.MessageBox("安装失败",
                                 "本地OCR已安装, 不需要重复安装!     ")
        return

    try :
        # 杀死本地ocr进程
        killOfflineOCR(object.yaml["port"])
        # 删除旧文件
        shutil.rmtree(OCR_INSTALL_PATH)
    except Exception :
        object.logger.error(format_exc())

    object.settin_ui.progress_bar.finish_sign = False
    object.settin_ui.progress_bar.show()
    # 安装本地ocr
    thread = InstallThread(object=object,
                           file_name=OCR_ZIP_FILE_NAME,
                           unzip_path=OCR_INSTALL_PATH)
    thread.progress_bar_sign.connect(object.settin_ui.progress_bar.paintProgressBar)
    thread.progress_bar_modify_title_sign.connect(object.settin_ui.progress_bar.modifyTitle)
    thread.progress_bar_close_sign.connect(object.settin_ui.closeProcessBar)
    thread = utils.thread.runQThread(thread)


# 杀死本地ocr进程
def killOfflineOCR(port) :

    popen_content = os.popen("netstat -ano |findstr %s"%port).read()
    if popen_content :
        print(popen_content)
        pid = popen_content.split(" ")[-1]
        os.popen("taskkill /f /t /im %s"%pid)


# 卸载本地ocr
def uninstall_offline_ocr(object) :

    # 判断本地ocr是否已安装
    if not os.path.exists(OCR_INSTALL_PATH):
        utils.message.MessageBox("卸载本地OCR失败",
                                 "本地OCR未安装!     ")
        return

    # 杀死本地ocr进程解除占用
    killOfflineOCR(object.yaml["port"])

    # 删除本地ocr
    try :
        shutil.rmtree(OCR_INSTALL_PATH)
        object.logger.error(format_exc())
        utils.message.MessageBox("卸载本地OCR", "卸载完成!      ")
    except PermissionError :
        utils.message.MessageBox("卸载本地OCR", "卸载失败了, 请先关闭本地ocr后再尝试卸载!        ")
    except Exception :
        object.logger.error(format_exc())
        utils.message.MessageBox("卸载本地OCR", "卸载失败了, 原因: %s"%format_exc())


# 下载
class InstallThread(QThread) :

    progress_bar_sign = pyqtSignal(float, int, str)
    progress_bar_modify_title_sign = pyqtSignal(str)
    progress_bar_close_sign = pyqtSignal(str, str)

    def __init__(self, object, file_name, unzip_path) :

        super(InstallThread, self).__init__()
        self.object = object
        self.logger = object.logger
        self.url = object.yaml["dict_info"]["ocr_install_url"]
        self.file_name = file_name
        self.unzip_path = unzip_path
        self.object.settin_ui.progress_bar.stop_sign = False


    # 下载
    def download(self) :

        size = 0
        chunk_size = 1024
        try :
            response = requests.get(self.url, stream=True, timeout=5)
            content_size = int(response.headers["content-length"])
            if response.status_code != 200 :
                return "下载链接失效, 原因:\nhttp.status_code %d"%response.status_code

            # 显示文件大小
            file_size = content_size / chunk_size / 1024
            file_size_content = "{:.2f} MB".format(content_size / chunk_size / 1024)
            with open(self.file_name, "wb") as file :
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    # 显示当前进度
                    now_size_content = "{:.2f} MB".format(size / content_size * file_size)
                    self.progress_bar_sign.emit(float(size / content_size * 100),
                                                int(size / content_size * 100),
                                                "%s/%s"%(now_size_content, file_size_content))
                    # 如果收到停止信号
                    if self.object.settin_ui.progress_bar.stop_sign :
                        break
            response.close()
            return None

        except Exception :
            self.logger.error(format_exc())
            try :
                os.remove(file_name)
            except Exception :
                pass

            return "下载被中断, 原因:\n%s"%format_exc()


    # 编码转换
    def decode(self, str) :

        try :
            string = str.encode("cp437").decode("gbk")
        except Exception :
            string = str.encode("utf-8").decode("utf-8")

        return string


    # 解压
    def unzip(self) :

        try :
            zip_file = zipfile.ZipFile(self.file_name)
            zip_list = zip_file.infolist()
            # 先计算总解压大小
            all_size = 0
            for f in zip_list :
                all_size += f.file_size
            all_size_content = "{:.2f} MB".format(all_size / 1024 / 1024)
            # 执行解压
            now_size = 0
            for f in zip_list :
                zip_file.extract(f, self.unzip_path)
                # 中文乱码重命名
                old_name = os.path.join("ocr", f.filename)
                new_name = old_name.encode('cp437').decode('gbk')
                os.rename(old_name, new_name)
                # 显示当前进度
                now_size += f.file_size
                now_size_content = "{:.2f} MB".format(now_size / 1024 / 1024)
                self.progress_bar_sign.emit(float(now_size / all_size * 100),
                                            int(now_size / all_size * 100),
                                            "%s/%s"%(now_size_content, all_size_content))
                # 如果收到停止信号
                if self.object.settin_ui.progress_bar.stop_sign :
                    break
            zip_file.close()
            # 删除压缩包
            os.remove(self.file_name)
        except Exception :
            self.logger.error(format_exc())
            return format_exc()


    def run(self) :

        # 下载
        self.progress_bar_modify_title_sign.emit("下载本地OCR -- 下载中请勿关闭此窗口")
        err = self.download()
        if err :
            utils.message.MessageBox("安装本地ocr失败", "原因: %s"%err)
            return

        # 如果收到停止信号
        if self.object.settin_ui.progress_bar.stop_sign :
            os.remove(self.file_name)
            return

        # 解压
        self.progress_bar_modify_title_sign.emit("解压本地OCR -- 解压中请勿关闭此窗口")
        err = self.unzip()
        if err :
            utils.message.MessageBox("安装本地ocr失败",
                                     "解压%s失败, 原因:\n%s"%(self.file_name, format_exc()))
            return

        # 如果收到停止信号
        if self.object.settin_ui.progress_bar.stop_sign :
            shutil.rmtree(OCR_INSTALL_PATH)
            return

        self.object.settin_ui.progress_bar.finish_sign = True
        self.progress_bar_close_sign.emit("安装本地ocr完成",
                                          "请点击本地ocr的运行按钮, 待运行完毕后再打开本地ocr的开关, 使用过程中切勿关闭本地ocr的运行小黑窗")