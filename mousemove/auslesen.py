from .screenshot import screenshot_with_size
from .navigation import *
from .positionen import mitte, rechts
from . import files
import subprocess
import time
import PIL.Image

import re
import collections


def text_from_image_file(image_name):
    assert image_name.lower().endswith('.bmp')
    output_name = files.tempfilename('', 'tesser_output')
    exe_file = files.tesser_exe()
    return_code = subprocess.call([exe_file, image_name, output_name, '-psm', '7'])
    if return_code != 0:
        raise NotImplementedError('Errorbehandlung für tesseract')
    time.sleep(0.5) # öffnet sich ein blödes Fenster
    return open(output_name + '.txt', encoding = 'utf8').read()

def text(x, y, width, height):
    image_name = screenshot_with_size(x, y, width, height)
    return text_from_image_file(image_name)

def schwarzer_text(x, y, width, height, schwelle = 200):
    image_name = screenshot_with_size(x, y, width, height)
    img = PIL.Image.open(image_name)
    x0, y0, width, height = img.getbbox()
    for x in range(x0, width + x0):
        for y in range(y0, height + y0):
            rgba = img.getpixel((x, y))
            if sum(rgba[:3]) > schwelle:
                img.putpixel((x, y), (255,255,255) + rgba[3:])
            else:
                img.putpixel((x, y), (0, 0, 0) + rgba[3:])
    img.save(image_name)
    return text_from_image_file(image_name)

def heller_text(x, y, width, height):
    image_name = screenshot_with_size(x, y, width, height)
    img = PIL.Image.open(image_name)
    x0, y0, width, height = img.getbbox()
    for x in range(x0, width + x0):
        for y in range(y0, height + y0):
            rgba = img.getpixel((x, y))
            if sum(rgba[:3]) > 255*3 - 200:
                img.putpixel((x, y), (0,0,0) + rgba[3:])
            else:
                img.putpixel((x, y), (255,255,255) + rgba[3:])
    img.save(image_name)
    return text_from_image_file(image_name)


read_width = 120 # pixel
read_height = 22 # pixel
def maximalzahl_in_klammern(x, y):
    left = x - read_width // 2
    top =  y - read_height // 2
    txt = heller_text(left, top, read_width, read_height)
##    print('text:', repr(txt))
    txt = txt.strip()[1:-1]
    zahl = re.findall('(?:\\d+\\.)*\\d+', txt)
    assert len(zahl) == 1, zahl
    zahl = zahl[0]
    zahl = zahl.replace('.', '')
##    print('Zahl:', zahl)
    return int(zahl)

def ressourcenzahlen(x, y, width, height):
    text = schwarzer_text(x, y, width, height)
##    print('text:', repr(text))
    zahl = re.findall('(?:\\d+\\.)*\\d+', text)
##    print('Zahl:', zahl)
    return map(int, map(lambda z: z.replace('.', ''), zahl))

Lager = collections.namedtuple('Lager', ('holz', 'stein', 'eisen', 'pech', 'max'))

class Lager(Lager):
    pass

def lager():
    öffne_ressourcen()
    x, y = mitte(213, 305)
    holz, stein, eisen, pech = ressourcenzahlen(x, y, 503 - 213, 327 - 305)
    max = maximalzahl_in_klammern(*mitte(362, 249))
    return Lager(holz, stein, eisen, pech, max)

Dorfhalle = collections.namedtuple('Dorfhalle', ('wild', 'möbel', 'metallwaren', 'kleidung', 'wein', 'salz', 'gewürze', 'seide', 'max'))

class Dorfhalle(Dorfhalle):
    pass

def dorfhalle():
    öffne_ressourcen()
    x, y = mitte(550, 305)
    ressources = ressourcenzahlen(x, y, 1149 - 550, 327 - 305)
    max = maximalzahl_in_klammern(*mitte(852, 248))
    return Dorfhalle(*ressources, max = max)

Kornspeicher = collections.namedtuple('Kornspeicher', ('äpfel', 'käse', 'fleisch', 'brot', 'gemüse', 'fisch', 'max'))

class Kornspeicher(Kornspeicher):
    pass

def kornspeicher():
    öffne_ressourcen()
    x, y = mitte(205, 465)
    ressources = ressourcenzahlen(x, y, 667 - 205, 490 - 465)
    max = maximalzahl_in_klammern(*mitte(442, 412))
    return Kornspeicher(*ressources, max = max)

Kornspeicher = collections.namedtuple('Kornspeicher', ('äpfel', 'käse', 'fleisch', 'brot', 'gemüse', 'fisch', 'max'))

class Kornspeicher(Kornspeicher):
    pass

def kornspeicher():
    öffne_ressourcen()
    x, y = mitte(205, 465)
    ressources = ressourcenzahlen(x, y, 667 - 205, 490 - 465)
    max = maximalzahl_in_klammern(*mitte(442, 412))
    return Kornspeicher(*ressources, max = max)

def erkundungszeit():
    s = heller_text(482, 528, 590-482, 559-528)
    s.replace('D', '0') # 0 wird manchmal als D erkannt
    
def _dorfname():
    x, y = rechts(970, 56)
    return schwarzer_text(x, y, 1340 - 970, 69 - 56, schwelle = 330).strip()

def dorfname():
    from .navigation import dorfname_ist_bekannt, dorfname
    if dorfname_ist_bekannt():
        return dorfname()
    return _dorfname()

__all__ = 'Lager lager Kornspeicher kornspeicher'\
          ' dorfhalle Dorfhalle schwarzer_text heller_text dorfname'.split()
