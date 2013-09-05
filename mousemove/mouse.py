
from .constants import wait

mouse_speed = 4

def move_mouse(x, y):
    posx, posy = win32api.GetCursorPos()
    while posx != x or posy != y:
        if abs(x - posx) < mouse_speed: posx = x
        if x < posx: posx -= mouse_speed
        elif x > posx: posx += mouse_speed
        if abs(y - posy) < mouse_speed: posy = y
        if y < posy: posy -= mouse_speed
        elif y > posy: posy += mouse_speed
##        win32api.SetCursorPos((posx, posy))
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE |
                             win32con.MOUSEEVENTF_ABSOLUTE,
                             int(posx / screen_width() * 65535.0),
                             int(posy / screen_height() * 65535.0))
        time.sleep(0.01)
    win32api.SetCursorPos((posx, posy))

def mouse_drag(from_x, from_y, to_x, to_y, sleep = 0):
    move_mouse(from_x, from_y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,from_x,from_y,0,0)
    move_mouse(to_x, to_y)
    time.sleep(sleep)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,to_x,to_y,0,0)

def click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    wait()

def click_again():
    x, y = win32api.GetCursorPos()
    click(x, y)

def right_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
    wait()

__all__ = 'mouse_speed move_mouse mouse_drag click click_again right_click'.split()
