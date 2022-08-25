import winreg
import utils.message

# 检查电脑是否安装chrome
def checkChrome():
    # 定义检测位置
    sub_key = [
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    ]

    software_name = []
    for i in sub_key:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            i,
            0,
            winreg.KEY_ALL_ACCESS
        )
        for j in range(0, winreg.QueryInfoKey(key)[0] - 1):
            try:
                key_name = winreg.EnumKey(key, j)
                key_path = i + '\\' + key_name
                each_key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    key_path,
                    0,
                    winreg.KEY_ALL_ACCESS
                )
                DisplayName, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                DisplayName = DisplayName.encode('utf-8')
                software_name.append(DisplayName)
            except WindowsError:
                pass

    software_name = list(set(software_name))
    software_name = sorted(software_name)

    for result in software_name:
        app_name = str(result, encoding='utf-8')
        if "Google Chrome" not in app_name:
            return True



def openChromeDownloadMessageBox():
    utils.message.checkChromeMessageBox("未安装Chrome浏览器",
                             "电脑未安装chrome浏览器，请前往chrome官网\nhttps://www.google.cn/chrome/index.html\n完成下载安装后，重启翻译器")