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



# 检查是否绑定邮箱
def bindEmail(object, user="") :

    url = object.yaml["dict_info"]["dango_check_email"]
    if user :
        body = {"User": user}
    else :
        body = {"User": object.yaml["user"]}
    res = utils.http.post(url, body, object.logger)
    if res.get("Status", "") == "Success" :
        return res.get("Result", {}).get("Email", "")
    else :
        return False