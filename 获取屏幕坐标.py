from pyautogui import position


while True:
    print('\n请把鼠标放置于需要检测坐标的位置，然后按下回车键获取坐标值：')
    input()
    x,y = position()
    print('x=',x,'y=',y)