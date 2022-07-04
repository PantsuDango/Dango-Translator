import time
from win32 import win32api, win32gui, win32print
from win32.lib import win32con
# import win32gui
# import win32con
# from traceback import format_exc

# 全屏下置顶
def setWindowTop(object) :
    # 桌面分辨率
    rect_desk = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
    # 翻译界面句柄
    object.translation_ui_hwnd = int(object.translation_ui.winId())
    # 设置界面句柄
    object.settin_ui_hwnd = int(object.settin_ui.winId())
    # 范围界面句柄
    object.range_ui_hwnd = int(object.range_ui.winId())


    while True :
        time.sleep(3)
        # 判断当前激活窗体是否为全屏
        sign, hwnd = checkIsFullScreen(rect_desk)
        if not sign :
            continue

        # 设置窗口置顶且无焦点
        setTop(object.translation_ui_hwnd)
        setTop(object.settin_ui_hwnd)
        setTop(object.range_ui_hwnd)

        while True :
            # 如果退出全屏程序
            time.sleep(3)
            if win32gui.GetWindowRect(hwnd) != rect_desk :
                # 恢复翻译界面焦点
                releaseFocus(object.translation_ui_hwnd)
                releaseFocus(object.settin_ui_hwnd)
                releaseFocus(object.range_ui_hwnd)
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


# 设置窗口置顶且无焦点
def setTop(hwnd) :
    # 窗口无焦点
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_NOACTIVATE)
    # 窗口置顶
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


# 解除窗口焦点
def releaseFocus(hwnd) :
    # 恢复窗口焦点
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style &~ win32con.WS_EX_NOACTIVATE)