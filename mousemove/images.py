import os
import PIL.Image
import tkinter
import time

from . import files

_screenshot = (None, 0) # filename, time

def screenshot():
    from . import screenshot
    global _screenshot
    now = time.time()
    if now - 0.05 > _screenshot[1]:
        from . import screenshot
        filename = screenshot.screenshot()
        _screenshot = filename, now
    else:
        filename = _screenshot[0]
    return PIL.Image.open(filename)

def screenshot_with_size(left, top, width, height):
    from .screenshot import screenshot_with_size
    return PIL.Image.open(screenshot_with_size(left, top, width, height))

def last_screenshot_file_name():
    return _screenshot[0]

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

def open_image(image):
    if not os.path.isfile(image):
        image = name_zu_pfad[image]
    return PIL.Image.open(image)


def bild_positionen(*args, **kw):
    from .positionen import bild_positionen
    return bild_positionen(*args, **kw)

__all__ = 'screenshot last_screenshot_file_name pil2tkinter_image open_image'\
          ' bild_positionen screenshot_with_size'.split()



