import time
from win32 import win32api, win32gui, win32print
from win32.lib import win32con
# import win32gui
# import win32con
# from traceback import format_exc

# 全屏下置顶
def setWindowTop(object) :
    # 翻译界面句柄
    object.translation_ui_hwnd = int(object.translation_ui.winId())
    # 桌面分辨率
    rect_desk = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
    while True :
        time.sleep(3)
        # 判断当前激活窗体是否为全屏
        sign, hwnd_now = checkIsFullScreen(rect_desk)
        if not sign :
            continue
        # 翻译界面无焦点
        win32gui.SetWindowLong(object.translation_ui_hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_NOACTIVATE)
        while True :
            time.sleep(3)
            # 翻译界面置顶
            win32gui.SetWindowPos(object.translation_ui_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
            # 如果退出全屏程序
            if win32gui.GetWindowRect(hwnd_now) != rect_desk :
                # 恢复翻译界面焦点
                style = win32gui.GetWindowLong(object.translation_ui_hwnd, win32con.GWL_EXSTYLE)
                win32gui.SetWindowLong(object.translation_ui_hwnd, win32con.GWL_EXSTYLE, style &~ win32con.WS_EX_NOACTIVATE)
                break


# 判断当前激活窗体是否为全屏
def checkIsFullScreen(rect_desk) :

    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    if hwnd == win32gui.GetDesktopWindow() or title == "" :
        return False, hwnd
    if win32gui.GetWindowRect(hwnd) != rect_desk :
        return False, hwnd

    return True, hwnd