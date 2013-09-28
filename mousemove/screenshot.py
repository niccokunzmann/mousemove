#!/usr/bin/python3
import win32gui, win32ui, win32con, win32api
try: from . import files
except SystemError: import files
import time
import multiprocessing

def _screenshot_with_size(left, top, width, height, tempfilename):
    hwin = win32gui.GetDesktopWindow()
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    bmp.SaveBitmapFile(memdc, tempfilename)

def screenshot_with_size(left, top, width, height):
    # using a pool makes no performance difference
    tempfilename = files.tempfilename('.bmp')
    with _some_lock:
        _screenshot_with_size(left, top, width, height, tempfilename)
    return tempfilename

def screenshot():
    hwin = win32gui.GetDesktopWindow()
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return screenshot_with_size(left, top, width, height)

def last_screenshot_file_name():
    from . import images
    return images.last_screenshot_file_name()

__all__ = 'screenshot screenshot_with_size last_screenshot_file_name'\
          ''.split()


if __name__ == '__main__':
    print(screenshot())
