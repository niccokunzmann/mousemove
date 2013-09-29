#!/usr/bin/python3

try: from . import files
except SystemError: import files
import win32gui, win32ui, win32con, win32api
import time
import subprocess
import sys

class ScreenshotError(Exception):
    pass

def _screenshot_with_size(left, top, width, height, tempfilename):
    scriptpath = files.screenshot_script_path()
    p = subprocess.Popen([sys.executable, scriptpath, str(left), str(top), 
                          str(width), str(height), tempfilename],
                         stdout = subprocess.PIPE, stderr = subprocess.PIPE,
                         stdin = subprocess.PIPE)
    stdout, stderr = p.communicate()
    code = p.wait()
    if code != 0:
        s = "Screenshotting exited with error code {}\n".format(code) + \
            stdout.decode("latin-1") + stderr.decode("latin-1")
        raise ScreenshotError(s)

def screenshot_with_size(left, top, width, height):
    # using a pool makes no performance difference
    tempfilename = files.tempfilename('.bmp')
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
