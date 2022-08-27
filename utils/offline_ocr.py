import utils.message

# 判断本地ocr是否已安装
def check_offline_ocr_exist(object) :
    return os.path.exists(self.object.yaml["ocr_cmd_path"])


# 安装本地ocr
def install_offline_ocr(object) :

    # 判断本地ocr是否已安装
    if check_offline_ocr_exist(object) :
        utils.message.MessageBox("安装失败",
                                 "本地OCR已安装, 不需要重复安装!     ")
        return

    