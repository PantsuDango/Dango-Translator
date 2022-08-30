from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ui.static.icon
import utils.thread
import utils.message
import zipfile

import sys
import os
import base64
import requests
from traceback import format_exc


# 进度条
class ProgressBar(QWidget) :

    def __init__(self, rate) :

        super().__init__()
        self.rate = rate

        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        # 窗口图标
        icon = QIcon()
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(ui.static.icon.APP_LOGO))
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)
        # 设置字体
        self.setStyleSheet("font: %spt '%s'; background-color: rgb(255, 255, 255);}"%(self.font_size, self.font_type))

        self.progress_bar = QProgressBar(self)
        self.customSetGeometry(self.progress_bar, 20, 10, 260, 10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: rgba(62, 62, 62, 0.2); "
                                        "border-radius: 6px;}"
                                        "QProgressBar::chunk { background-color: %s; border-radius: 5px;}"
                                        %(self.color_2))

        self.progress_label = QLabel(self)
        self.customSetGeometry(self.progress_label, 240, 25, 150, 20)
        self.progress_label.setStyleSheet("color: %s"%self.color_2)

        self.file_size_label = QLabel(self)
        self.customSetGeometry(self.file_size_label, 20, 25, 150, 20)
        self.file_size_label.setStyleSheet("color: %s" % self.color_2)


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate),
                                 int(w * self.rate),
                                 int(h * self.rate)))


    # 初始化配置
    def getInitConfig(self):

        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 10
        # 灰色
        self.color_1 = "#595959"
        # 蓝色
        self.color_2 = "#5B8FF9"
        # 界面尺寸
        self.window_width = int(300 * self.rate)
        self.window_height = int(50 * self.rate)


    # 绘制进度信息
    def paintProgressBar(self, float_val, int_val, str_val) :

        self.progress_label.setText("{:.2f}%".format(float_val))
        self.progress_bar.setValue(int_val)
        self.file_size_label.setText(str_val)


    # 窗口关闭处理
    def closeEvent(self, event) :

        utils.message.MessageBox("这是来自团子的提示~",
                                 "安装进行中, 关闭将会在后台进行      ")


# 下载
class InstallThread(QThread) :

    progress_bar_sign = pyqtSignal(float, int, str)

    def __init__(self, object, file_name, unzip_path) :

        super(InstallThread, self).__init__()
        self.object = object
        self.logger = object.logger
        self.url = object.yaml["dict_info"]["ocr_install_url"]
        self.file_name = file_name
        self.unzip_path = unzip_path


    def download(self) :

        size = 0
        chunk_size = 1024
        try :
            response = requests.get(self.url, stream=True)
            content_size = int(response.headers["content-length"])
            if response.status_code != 200 :
                return "下载链接失效, 原因:\nhttp.status_code %d"%response.status_code

            # 显示文件大小
            file_size = content_size / chunk_size / 1024
            file_size_content = "{:.2f} MB".format(content_size / chunk_size / 1024)
            with open(self.file_name, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    # 显示当前进度
                    now_size_content = "{:.2f} MB".format(size / content_size * file_size)
                    self.progress_bar_sign.emit(float(size / content_size * 100),
                                                int(size / content_size * 100),
                                                "%s/%s" % (now_size_content, file_size_content))
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
                self.progress_bar_sign.emit(float(now_size / all_size*100),
                                            int(now_size / all_size*100),
                                            "%s/%s"%(now_size_content, all_size_content))
            zip_file.close()
            # 删除压缩包
            os.remove(self.file_name)
        except Exception :
            self.logger.error(format_exc())
            return format_exc()


    def run(self) :

        # 下载
        self.object.settin_ui.progress_bar.setWindowTitle("下载本地OCR -- 下载中请勿关闭此窗口")
        err = self.download()
        if err :
            utils.message.MessageBox("安装本地ocr失败", "原因: %s"%err)
            return

        # 解压
        self.object.settin_ui.progress_bar.setWindowTitle("解压本地OCR -- 解压中请勿关闭此窗口")
        err = self.unzip()
        if err :
            utils.message.MessageBox("安装本地ocr失败",
                                     "解压%s失败, 原因:\n%s"%(self.file_name, format_exc()))
            return

        utils.message.MessageBox("安装本地ocr完成",
                                 "请点击本地ocr的运行按钮, 待运行完毕后再打开本地ocr的开关, 使用过程中切勿关闭本地ocr的运行小黑窗")
        self.object.settin_ui.progress_bar.close()



if __name__ == "__main__" :

    app = QApplication(sys.argv)
    obj = ProgressBar(1.5)
    obj.show()
    sys.exit(app.exec_())