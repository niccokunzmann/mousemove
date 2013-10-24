import os
import PIL.Image
import tkinter
import time
import subprocess

from . import files

_screenshot = None # filename

def screenshot():
    from . import screenshot
    global _screenshot
    filename = screenshot.screenshot()
    _screenshot = filename
    return PIL.Image.open(filename)

def screenshot_with_size(left, top, width, height):
    global _screenshot
    from .screenshot import screenshot_with_size
    filename = screenshot_with_size(left, top, width, height)
    _screenshot = filename
    return PIL.Image.open(filename)

def last_screenshot_file_name():
    return _screenshot

def pil2tkinter_image(img, *args, **kw):
    if isinstance(img, str):
        img = open_image(img)
    x0, y0, width, height = img.getbbox()
    l = []
    for y in range(y0, height):
        l.append('{')
        for x in range(x0, width):
            l.append('#%02X%02X%02X' % img.getpixel((x, y))[:3])
        l.append('}')
    data = ' '.join(l)
    pi = tkinter.PhotoImage(*args, **kw)
    pi.put(data, (0,0))
    return pi

name_zu_pfad = {}
namen = []

image_folder = files.image_folder

for dirpath, dirnames, filenames in os.walk(image_folder):
    for filename in filenames:
        name = os.path.splitext(filename)[0]
        if name.lower() in name_zu_pfad:
            raise ValueError('name {} kommt doppelt vor'.format(name))
        path = os.path.join(dirpath, filename)
        namen.append(name.capitalize())
        kathegorie = os.path.basename(dirpath)
        if kathegorie == 'geht':
            kathegorie = os.path.basename(os.path.dirname(dirpath))
        kathegorie = 'bilder_' + kathegorie.lower()
        name_zu_pfad[name] = name_zu_pfad[name.capitalize()] = \
                             name_zu_pfad[name.lower()] = \
                             name_zu_pfad[name.upper()] = path
        locals().setdefault(kathegorie, [])
        locals()[kathegorie].append(name.capitalize())
        locals()[kathegorie].sort()

assert PIL.Image.Image.__reduce__ is object.__reduce__

def _Image_reduce(self):
    return PIL.Image.frombytes, (self.mode, self.size, self.tobytes())
# monkeypatch the __reduce__ function of images
PIL.Image.Image.__reduce__ = _Image_reduce

def image_path(image):
    if not os.path.isfile(image):
        image = name_zu_pfad[image]
    return image

def open_image(image):
    return PIL.Image.open(image_path(image))

def mspaint(image_file):
    return subprocess.Popen(['mspaint', image_path(image)], shell = True)

def bildmaße(image):
    left, upper, right, lower = open_image(image).getbbox()
    return right - left, lower - upper

def bild_positionen(*args, **kw):
    from .positionen import bild_positionen
    return bild_positionen(*args, **kw)


__all__ = 'screenshot last_screenshot_file_name pil2tkinter_image open_image'\
          ' bild_positionen screenshot_with_size bildmaße'.split()



