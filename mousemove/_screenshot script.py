import win32gui, win32ui, win32con, win32api
import sys

left, top, width, height = map(int, sys.argv[1:5])
tempfilename = sys.argv[5]

hwin = win32gui.GetDesktopWindow()
hwindc = win32gui.GetWindowDC(hwin)
srcdc = win32ui.CreateDCFromHandle(hwindc)
memdc = srcdc.CreateCompatibleDC()
bmp = win32ui.CreateBitmap()
bmp.CreateCompatibleBitmap(srcdc, width, height)
memdc.SelectObject(bmp)
memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
bmp.SaveBitmapFile(memdc, tempfilename)
