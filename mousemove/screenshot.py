#!/usr/bin/python3
import win32gui, win32ui, win32con, win32api
import subprocess
from . import files


def screenshot_with_size(left, top, width, height):
    hwin = win32gui.GetDesktopWindow()
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    tempfilename = files.tempfilename('.bmp')
    bmp.SaveBitmapFile(memdc, tempfilename)
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

class Tesser_General_Exception(Exception):
    pass

def text(x, y, width, height):
    image_name = screenshot_with_size(x, y, width, height)
    output_name = files.tempfilename('', 'tesser_output')
    exe_file = files.tesser_exe()
    return_code = subprocess.call([exe_file, image_name, output_name])
    if return_code != 0:
        text = open("tesseract.log").read()
	# All error conditions result in "Error" somewhere in logfile
        if "Error" in text:
            raise Tesser_General_Exception(text)
    return open(output_name + '.txt', encoding = 'utf8').read()
    

__all__ = 'screenshot text screenshot_with_size last_screenshot_file_name'\
          ''.split()


if __name__ == '__main__':
    print(screenshot())
