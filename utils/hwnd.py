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
        self.translation_ui_hwnd = self.object.translation_ui.winId()
        self.range_ui_hwnd = self.object.range_ui.winId()


    # 设置窗口置顶且无焦点
    def setTop(self, hwnd) :

        try :
            # 校验句柄是否有效
            if not win32gui.IsWindow(hwnd) :
                return
            while True :
                time.sleep(0.5)
                # 如果置顶开关被关闭则直接结束
                if not self.object.settin_ui.set_top_use :
                    return
                # 判断是否有全屏程序
                if not self.checkIsFullScreen() :
                    continue
                # 窗口无焦点
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_NOACTIVATE)
                # 防止黑屏
                if hwnd == self.range_ui_hwnd :
                    self.object.range_ui.drag_label.setStyleSheet("background-color:none")
                if hwnd == self.translation_ui_hwnd :
                    self.object.translation_ui.drag_label.setStyleSheet("{background-color:none}")
                while True :
                    time.sleep(0.5)
                    # 窗口置顶
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
                    # 如果退出了全屏
                    rect_desk = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
                    if win32gui.GetWindowRect(self.full_screen_hwnd) != rect_desk :
                        self.releaseFocus(hwnd)
                        break
                    # 如果置顶开关被关闭则直接结束
                    if not self.object.settin_ui.set_top_use :
                        self.releaseFocus(hwnd)
                        return
        except Exception :
            self.logger.error(format_exc())


    # 解除窗口焦点
    def releaseFocus(self, hwnd) :

        # 范围界面不需要显示焦点
        if hwnd == self.range_ui_hwnd :
            return
        try :
            if not win32gui.IsWindow(hwnd) :
                return
            # 恢复窗口焦点
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style & ~ win32con.WS_EX_NOACTIVATE)
        except Exception :
            self.logger.error(format_exc())


    # 判断当前激活窗体是否为全屏
    def checkIsFullScreen(self) :

        rect_desk = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        if hwnd == win32gui.GetDesktopWindow() or title == "":
            return False
        if win32gui.GetWindowRect(hwnd) != rect_desk :
            return False

        self.full_screen_hwnd = hwnd
        return True


    def run(self) :

        utils.thread.createThread(self.setTop, self.translation_ui_hwnd)
        utils.thread.createThread(self.setTop, self.range_ui_hwnd)
