from win32 import win32api, win32gui, win32print
from win32.lib import win32con
from win32.win32api import GetSystemMetrics


def getRealResolution():

    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def getScreenSize():

    """获取缩放后的分辨率"""
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


def getScreenRate(config) :

    real_resolution = getRealResolution()
    screen_size = getScreenSize()
    screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
    config["screenScaleRate"] = screen_scale_rate

    return config