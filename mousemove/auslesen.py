from concurrent.futures import ThreadPoolExecutor
from .screenshot import screenshot_with_size, last_screenshot_file_name
from .navigation import *
from .positionen import mitte, rechts
from . import files
import subprocess
import time
import PIL.Image

import re
import collections
from threading import Lock
import sys

PARAMETER_ONLY_DIGITS = ['nobatch', 'digits']

class ImageText(str):
    @staticmethod
    def is_image_text(): return True

def text_from_image_file(image_name, parameters = []):
    assert image_name.lower().endswith('.bmp')
    output_name = files.tempfilename('', 'tesser_output')
    exe_file = files.tesser_exe()
    return_code = subprocess.call([exe_file, image_name, output_name, '-psm', '7'] + parameters, shell = True)
    output_name += '.txt'
    if return_code != 0:
        raise NotImplementedError('Errorbehandlung für tesseract; code {}; '\
                                  'input {} ; output {}'.format(return_code,
                                                                image_name,
                                                                output_name))
##    time.sleep(0.5) # öffnet sich ein blödes Fenster
    result = ImageText(open(output_name, encoding = 'utf8').read().strip())
    result.image_file = image_name
    result.text_file = output_name
    return result

def text(x, y, width, height, *args, **kw):
    image_name = screenshot_with_size(x, y, width, height)
    return text_from_image_file(image_name, *args, **kw)

def text2(left, top, right, bottom):
    return text(left, top, right - left, bottom - top)

def schwarzer_text(x, y, width, height, schwelle = 200, parameters = []):
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
    return text_from_image_file(image_name, parameters)

def heller_text(x, y, width, height, parameters = []):
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
    return text_from_image_file(image_name, parameters)

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

def _dorfname():
    x, y = rechts(970, 56)
    return schwarzer_text(x, y, 1340 - 970, 69 - 56, schwelle = 330)

def dorfname():
    from .navigation import dorfname_ist_bekannt, dorfname
    if dorfname_ist_bekannt():
        return dorfname()
    return _dorfname()

_debug_numbers_lock = Lock()

DEBUG_INTO_STDERR = False

def debug_numbers(imageText):
    string = 'number {} in screenshot {}'.format(repr(imageText), imageText.image_file)
    with _debug_numbers_lock:
        with open('debug numbers.out', 'a', encoding = 'utf8') as f:
            print(string, file = f)
            if DEBUG_INTO_STDERR:
                print(string, file = sys.stderr)

map_numbers = {'.' : 0, '1.21': 101, '2.2' : 20, '1.35' : 105,
               '1 5' : 105}
def _tesseract_format_number(imageText):
    number = imageText.replace(' ', '').strip()
    if len(number) > 3 and number[-4] == '.':
        # remove .
        number = number[:-4] + number[-3:]
    number = number.replace('.3', '0').replace('.2', '0')
    if number in map_numbers:
        return map_numbers[number]
    if not number.isdigit():
        debug_numbers(imageText)
        return 0
    return int(number)

def _angriffszahl(x, y):
    x1, y1 = rechts(x + 1, y + 2)
    filename = screenshot_with_size(x1, y1, 21, 11)
    text = text_from_image_file(filename, PARAMETER_ONLY_DIGITS)
    return _tesseract_format_number(text)

def angriff_bauern():
    return _angriffszahl(1224, 224)

def angriff_bogenschützen():
    return _angriffszahl(1307, 224)

def angriff_pikeniere():
    return _angriffszahl(1224, 299)

def angriff_schwertkämpfer():
    return _angriffszahl(1307, 299)

def angriff_katapulte():
    return _angriffszahl(1224, 374)

def angriff_hauptmann():
    return _angriffszahl(1307, 374)

def angriffstruppen():
    spiel_window_handle() # sonst blockiert es
    fut = _submit_angriffstruppen_worker
    d = dict(Bauern = fut(angriff_bauern),
             Bogenschützen = fut(angriff_bogenschützen),
             Hauptmann = fut(angriff_hauptmann),
             Pikeniere = fut(angriff_pikeniere),
             Schwertkämpfer = fut(angriff_schwertkämpfer),
             Katapulte = fut(angriff_katapulte),
             )
    result = {}
    for k, v in d.items():
        result[k] = v.result()
    return result



ressourcen_speicher_positionen = dict(
    Holz = (200, 307), Stein = (280, 307), Eisen = (360, 307), Pech = (440, 307),
    Wild = (535, 307), Möbel = (615, 307), Metallwaren = (695, 307), Gewänder = (775, 307), Wein = (855, 307), Salz = (935, 307), Gewürze = (1015, 307), Seide = (1092, 307),
    Äpfel = (200, 467), Käse = (280, 467), Fleisch = (360, 467), Brot = (440, 467), Gemüse = (520, 467), Fisch = (600, 467),
    Bier = (685, 467),
    Bögen = (775, 467), Piken = (855, 467), Rüstung = (935, 467), Schwerter = (1015, 467), Katapulte = (1092, 467), )

_auslesen_pool = ThreadPoolExecutor(len(ressourcen_speicher_positionen))

_submit_angriffstruppen_worker = _auslesen_pool.submit
_submit_ressourcen_speicher_worker = _auslesen_pool.submit

def ressourcen_zahl(name):
    x, y = mitte(*ressourcen_speicher_positionen[name.capitalize()])
    _text = text(x + 5, y, 70, 20, parameters = PARAMETER_ONLY_DIGITS)
    return _tesseract_format_number(_text)


def ressourcenstand():
    spiel_window_handle() # sonst blockiert es
    fut = _submit_ressourcen_speicher_worker
    futures = []
    for name in ressourcen_speicher_positionen:
        futures.append((name, fut(ressourcen_zahl, name)))
    result = {}
    for name, future in futures:
        result[name] = future.result()
    return result

def warenmenge_im_handel(index):
    x, y = mitte(423, 344)
    y += 40 * index
    _text = text(x, y, 95, 28, parameters = PARAMETER_ONLY_DIGITS)
    return _tesseract_format_number(_text)
    
    
__all__ = 'schwarzer_text heller_text dorfname PARAMETER_ONLY_DIGITS'\
          ' schwarzer_text heller_text angriff_bauern angriff_bogenschützen'\
          ' angriff_pikeniere angriff_schwertkämpfer angriff_katapulte'\
          ' angriff_hauptmann angriffstruppen ressourcen_zahl'\
          ' ressourcen_speicher_positionen ressourcenstand text'\
          ' warenmenge_im_handel text2'.split()
