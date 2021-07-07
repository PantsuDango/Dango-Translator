# -*- coding: utf-8 -*-

from win32 import win32api, win32gui, win32print
from win32.lib import win32con
from win32.win32api import GetSystemMetrics

from PIL import Image


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics (0)
    h = GetSystemMetrics (1)
    return w, h


def Background(screen_scale_rate):

    img = Image.open("./config/Background.jpg")
    weight = int(404*screen_scale_rate)
    height = int(576*screen_scale_rate)
    out = img.resize((weight, height))
    out.save("./config/Background%d.jpg"%(screen_scale_rate*100))


def get_screen_rate():

    real_resolution = get_real_resolution()
    screen_size = get_screen_size()
    screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
    
    if screen_scale_rate == 1.0 or screen_scale_rate == 1.25 or screen_scale_rate == 1.5 or screen_scale_rate == 1.75:
        pass
    else:
        Background(screen_scale_rate)

    return screen_scale_rate
    

if __name__ == '__main__':
   
    get_screen_rate()