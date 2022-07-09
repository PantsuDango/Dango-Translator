import time
from win32 import win32api, win32gui, win32print
from win32.lib import win32con
from traceback import format_exc

import utils.thread


# 窗口句柄操作
class WindowHwnd() :

    def __init__(self, object) :

        self.object = object
        self.logger = object.logger
        self.rect_desk = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
        self.hwnd_list = [
            self.object.translation_ui,
            self.object.settin_ui,
            self.object.filter_ui,
            self.object.range_ui,
            self.object.settin_ui.desc_ui,
            self.object.settin_ui.hotkey_ui,
            self.object.settin_ui.key_ui,
        ]
        self.full_screen_sign = False


    # 判断当前激活窗体是否为全屏
    def checkIsFullScreen(self) :

        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        if hwnd == win32gui.GetDesktopWindow() or title == "" :
            return False
        if win32gui.GetWindowRect(hwnd) != self.rect_desk :
            return False

        self.full_screen_hwnd = hwnd
        return True


    # 设置窗口置顶且无焦点
    def setTop(self, window) :

        try :
            if not window.isVisible() :
                return  0
            hwnd = int(window.winId())
            if not hwnd :
                return 0
            if win32gui.IsWindow(hwnd) :
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_NOACTIVATE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
                return hwnd
        except Exception :
            self.logger.error(format_exc())

        return 0


    # 解除窗口焦点
    def releaseFocus(self, hwnd) :

        try :
            if not hwnd :
                return
            if not win32gui.IsWindow(hwnd) :
                return
            # 恢复窗口焦点
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style & ~ win32con.WS_EX_NOACTIVATE)
        except Exception :
            print_exc()
            self.logger.error(format_exc())


    # 监听窗体
    def windowMonitor(self, window) :

        # 用于判断是否执行过置顶语句, 避免重复执行
        sign = False
        hwnd = 0

        while True:
            time.sleep(0.1)
            # 如果退出全屏, 结束循环
            if not self.full_screen_sign :
                break

            # 如果句柄失效则退出
            if hwnd and not win32gui.IsWindow(hwnd) :
                sign = False
                hwnd = 0

            if not sign :
                # 设置窗口置顶且无焦点
                hwnd = self.setTop(window)
                if hwnd :
                    sign = True

        # 解除窗口焦点
        self.releaseFocus(hwnd)


    def run(self) :

        while True :
            time.sleep(0.1)
            if not self.checkIsFullScreen() :
                continue
            self.full_screen_sign = True
            for window in self.hwnd_list :
                utils.thread.createThread(self.windowMonitor, window)
            while True :
                time.sleep(0.1)
                if win32gui.GetWindowRect(self.full_screen_hwnd) != self.rect_desk :
                    self.full_screen_sign = False
                    break
