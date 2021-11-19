from PyQt5.QtCore import *

import utils.http
import utils.message


# 发送邮件线程
class SendEmail(QThread) :

    signal = pyqtSignal(bool, str)

    def __init__(self, url, user, email, code_key, logger) :

        super(SendEmail, self).__init__()
        self.url = url
        self.user = user
        self.email = email
        self.code_key = code_key
        self.logger = logger


    def run(self) :

        body = {
            "User": self.user,
            "Email": self.email,
            "CodeKey": self.code_key
        }

        # 请求注册服务器
        res = utils.http.post(self.url, body, self.logger)
        result = res.get("Status", "")
        error = res.get("Error", "")
        if result != "Success" :
            self.logger.error(error)
            self.signal.emit(False, error)
        else :
            self.signal.emit(True, error)



# 发送邮件线程
class BindEmail(QThread) :

    signal = pyqtSignal(bool)

    def __init__(self, object) :

        super(BindEmail, self).__init__()
        self.object = object


    def run(self) :

        url = self.object.yaml["dict_info"]["dango_check_email"]
        body = {
            "User": self.object.yaml["user"]
        }
        # 请求注册服务器
        res = utils.http.post(url, body, self.object.logger)
        result = res.get("Message", "")
        if result == "未绑定邮箱" :
            self.signal.emit(False)