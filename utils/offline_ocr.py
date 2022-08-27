import utils.message
import utils.thread
import ui.progress_bar

import os


# 判断本地ocr是否已安装
def check_offline_ocr_exist(object) :

    return os.path.exists(object.yaml["ocr_cmd_path"])


# 下载本地ocr
def download_offline_ocr(object) :

    # 判断本地ocr是否已安装
    if check_offline_ocr_exist(object) :
        utils.message.MessageBox("安装失败",
                                 "本地OCR已安装, 不需要重复安装!     ")
        return

    object.settin_ui.progress_bar.setWindowTitle("下载本地OCR -- 下载中请勿关闭此窗口")
    object.settin_ui.progress_bar.show()
    thread = ui.progress_bar.Download(object.yaml["dict_info"]["ocr_install_url"], "ocr.zip")
    thread.progress_bar_sign.connect(object.settin_ui.progress_bar.paintProgressBar)
    utils.thread.runQThread(thread, mode=False)