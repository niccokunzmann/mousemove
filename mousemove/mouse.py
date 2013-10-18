import time
import win32api
import win32con

from .constants import wait
from .positionen import *

mouse_speed = 8

def move(x, y):
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

def drag(from_x, from_y, to_x, to_y, sleep = 0):
    move(from_x, from_y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,from_x,from_y,0,0)
    move(to_x, to_y)
    time.sleep(sleep)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,to_x,to_y,0,0)

def click(x, y):
    move(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    wait()

def click_again():
    x, y = win32api.GetCursorPos()
    click(x, y)

def right_click(x, y):
    move(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
    wait()

position = win32api.GetCursorPos

__all__ = 'mouse_speed move drag click click_again right_click position'\
          ''.split()
