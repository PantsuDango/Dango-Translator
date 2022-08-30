import utils.message
import utils.thread
import ui.progress_bar

from traceback import format_exc
import shutil
import os

OCR_INSTALL_PATH = "ocr"
OCR_ZIP_FILE_NAME = "ocr.zip"

# 判断本地ocr是否已安装
def check_offline_ocr_exist(object) :

    return os.path.exists(object.yaml["ocr_cmd_path"])


# 安装本地ocr
def install_offline_ocr(object) :

    # 判断本地ocr是否已安装
    if check_offline_ocr_exist(object) :
        utils.message.MessageBox("安装失败",
                                 "本地OCR已安装, 不需要重复安装!     ")
        return

    object.settin_ui.progress_bar.show()
    # 安装本地ocr
    thread = ui.progress_bar.InstallThread(object=object,
                                           file_name=OCR_ZIP_FILE_NAME,
                                           unzip_path=OCR_INSTALL_PATH)
    thread.progress_bar_sign.connect(object.settin_ui.progress_bar.paintProgressBar)
    utils.thread.runQThread(thread, mode=False)


# 卸载本地ocr
def uninstall_offline_ocr(object) :

    # 判断本地ocr是否已安装
    if check_offline_ocr_exist(object):
        utils.message.MessageBox("卸载本地OCR失败",
                                 "本地OCR未安装!     ")
        return

    try :
        shutil.rmtree(OCR_INSTALL_PATH)
    except Exception :
        object.logger.error(format_exc())
        utils.message.MessageBox("卸载本地OCR失败", "原因: %s"%format_exc())