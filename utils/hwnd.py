import time
from win32 import win32api, win32gui, win32print
from win32.lib import win32con
# import win32gui
# import win32con
from traceback import format_exc, print_exc

# 全屏下置顶
def setWindowTop(hwnd) :

    # 桌面分辨率
    rect_desk = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
    time.sleep(3)

    try :
        while True :
            time.sleep(0.1)

            # 如果句柄失效则退出
            if not win32gui.IsWindow(hwnd) :
                return

            # 判断当前激活窗体是否为全屏
            sign, full_screen_hwnd = checkIsFullScreen(rect_desk)
            if not sign :
                continue

            # 设置窗口置顶且无焦点
            setTop(hwnd)

            while True :
                time.sleep(0.1)

                # 如果句柄失效则退出
                if not win32gui.IsWindow(hwnd) :
                    return

                # 如果退出全屏程序
                if win32gui.GetWindowRect(full_screen_hwnd) != rect_desk :
                    # 恢复窗口焦点
                    releaseFocus(hwnd)
                    break
    except Exception :
        print_exc()


# 判断当前激活窗体是否为全屏
def checkIsFullScreen(rect_desk) :

    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    if hwnd == win32gui.GetDesktopWindow() or title == "" :
        return False, hwnd
    if win32gui.GetWindowRect(hwnd) != rect_desk :
        return False, hwnd

    return True, hwnd


# 窗口置顶
def setWindowPos(hwnd) :

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


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