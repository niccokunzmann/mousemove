from tkinter import *
from concurrent.futures import ThreadPoolExecutor
from .lazy import FutureList
import win32gui
import threading

from . import images

m1 = Tk()
m1.overrideredirect(1)
m1.geometry("1x1-12-12")

screen_width = m1.winfo_screenwidth
screen_height = m1.winfo_screenheight
def spiel_height():
    return spiel_bbox()[3]
def spiel_width():
    return spiel_bbox()[2]
my_height = 738
my_width = 1366
breite_des_rechten_menus = 1365 - 1167
höhe_des_oberen_menus = 114
my_breite_der_karte = my_width - breite_des_rechten_menus
my_höhe_der_karte = my_height - höhe_des_oberen_menus
start_der_karte_y = höhe_des_oberen_menus

def höhe_der_karte():
    return spiel_height() - höhe_des_oberen_menus

def breite_der_karte():
    return spiel_width() - breite_des_rechten_menus

def rechts(x, y):
    return x - my_width + spiel_width(), y

def unten(x, y):
    return x, y - my_height + spiel_height()

def mitte(x, y):
    # x
    my_mitte = my_width // 2
    mitte = spiel_width() // 2
    x = x - my_mitte + mitte
    # y
    my_mitte = (my_height - höhe_des_oberen_menus) // 2
    mitte = (spiel_height() - höhe_des_oberen_menus) // 2
    y = y - my_mitte + mitte
    return x, y

def karte_mitte(x, y):
    # x
    my_mitte = my_breite_der_karte // 2
    mitte = breite_der_karte() // 2
    x = x - my_mitte + mitte
    # y
    my_mitte = my_höhe_der_karte // 2
    mitte = höhe_der_karte() // 2
    y = y - my_mitte + mitte
    return x, y

def spiel_koordinaten():
    from . import navigation
    left, top, right, bottom = win32gui.GetWindowRect(navigation.spiel_window_handle())
    return left, top ,right, bottom

def spiel_bbox():
    x, y, right, bottom = spiel_koordinaten()
    assert x < 0, str((x, y, right, bottom)) + " Ein anderes Fenster mit dem Titel 'Stronghold Kingdoms' ist offen." # wir brauchen einen rand!
    assert y < 0, str((x, y, right, bottom)) + " Ein anderes Fenster mit dem Titel 'Stronghold Kingdoms' ist offen." # wir brauchen einen rand!
    width = right + x # eigentlich - x aber wir ziehen den rand ab
    height = bottom + y
    x = 0
    y = 0
    return x, y, width, height

def ressourcen_positionen(*bilder):
    """Positionen der Ressourcen + zusätzliche bilder"""
    bilder += tuple(images.bilder_ressourcen)
    return karten_positionen(*bilder)

def karten_koordinaten():
    # wenn 1 und 2 gelten, gilt auch 3
    miny = start_der_karte_y # 3
    minx = 0 # 3
    maxx = minx + breite_der_karte() # 3
    maxy = miny + höhe_der_karte() # 3
    mittex = (minx + maxx) // 2
    mittey = (miny + maxy) // 2
    return minx, miny, maxx, maxy, mittex, mittey

def karten_positionen(*bilder):
    minx, miny, maxx, maxy, *x = karten_koordinaten()
    return bild_positionen(minx, miny, maxx, maxy, bilder)

def spiel_positionen(*bilder, **kw):
    left, top ,right, bottom = spiel_koordinaten()
    return bild_positionen(left, top ,right, bottom, bilder)
    

_search_executor = ThreadPoolExecutor(1)

submit_worker = _search_executor.submit

def neue_bildposition(bild, alt = None, box = None):
    if box is None:
        box = spiel_koordinaten()
    if not alt:
        print('schlechter weg')
        return bild_positionen(box[0], box[1], box[2], box[3], (bild,)).position_at(0)
    width, height = images.bildmaße(bild)
    x, y = alt.x, alt.y
##    print('masse', x, y, width, height, box)
    list = bild_positionen(x - width // 2, y - height // 2, x + width - width //2, y + height - height // 2, (bild,))
    position = list.position_at(0)
##    print(list)
##    print(bool(position))
    if position: return position
    print("langer weg")
    return neue_bildposition(bild, box = box)

def letzte_bildpositionen_speicher(box = None):
    from . import config
    config.letzte_bildpositionen.setdefault(box, {})
    positionen = config.letzte_bildpositionen[box]
    return positionen
    
def erneuere_position(bild, alt = None, box = None):
    from . import config
    bild = bild.lower()
    alte_position = letzte_bildpositionen_speicher(box).get(bild, None)
    if not alte_position: alte_position = alt
    neue_position = neue_bildposition(bild, alte_position, box)
    def update(neue_position):
        if not alte_position or neue_position != alte_position:
            print("position hat sich ge'ndert")
            config.load()
            letzte_bildpositionen_speicher(box)[bild] = neue_position
            config.save()
    neue_position.add_done_callback(update)
    return neue_position

def formationen_verwalten(relx, rely):
    pos = erneuere_position('Formationen Verwalten')
    return relx + pos.x, rely + pos.y

def bild_positionen(minx, miny, maxx, maxy, namen, debug_many_matches = True):
    from . import karte
    s = images.screenshot_with_size(minx, miny, maxx - minx, maxy - miny)
    karte_pos = karte.pos()
    future = submit_worker(_bild_positionen, minx, miny, maxx, maxy, namen, s,
                           karte_pos, debug_many_matches)
    return FutureList(future)

def _bild_positionen(minx, miny, maxx, maxy, namen, s, karte_pos, debug_many_matches):
    """mitte der bilder!"""
    from .ressourcen import Ressource
    bilder = [images.open_image(name) for name in namen]
    _s_getpixel = s.getpixel 
    def s_getpixel(x, y):
        try:
            return _s_getpixel((x0 + x, y0 + y))[:3]
        except IndexError as e:
            raise IndexError('x0={}, y0={}, x={}, y={}, maxx={}, maxy={},'\
                             ' xrange={}, yrange={}, in file {}'\
                             ''.format(x0, y0, x, y, maxx, maxy, xrange, yrange,
                                       images.last_screenshot_file_name()))
    x0, y0, maxx, maxy = s.getbbox()
##    print('x0', x0, y0, maxx, maxy)
##    print('minmax', minx, miny, maxx, maxy)
    ps1 = [(image.getpixel((0,0))[:3], image, image.getbbox()) for image in bilder]
    xrange = maxx - min([img[2][2] - img[2][0] for img in ps1]) - x0 + 1
    yrange = maxy - min([img[2][3] - img[2][1] for img in ps1]) - y0 + 1
##    print('pixels', xrange, yrange)
    positions = []
    matches = {img : 0 for img in ps1}
    for x in range(xrange):
        for y in range(yrange):
            px = s_getpixel(x, y)
            for img in ps1:
##                print('img[0] != px', img[0], '!=', px)
                if img[0] != px: continue
                matches[img] += 1
                bbox = img[2]
                matches[img]
##                print('match', x + minx, y + miny, bbox)
                if maxx - x < bbox[2] or maxy - y < bbox[3]:
                    continue
##                print(':)')
                image_getpixel = img[1].getpixel
                match = True
                i_x0, i_y0 = bbox[:2]
##                try:
                for dx in range(bbox[2] - i_x0):
                    for dy in range(bbox[3] - i_y0):
                        if s_getpixel(x + dx, y + dy) != \
                           image_getpixel((i_x0 + dx, i_y0 + dy))[:3]:
                            match = False
                            break
                    if not match: break
##                except IndexError: pass # image index out of range
                if match:
                    positions.append(Ressource(namen[ps1.index(img)],
                                      x0 + minx + x + (bbox[2] - bbox[0]) // 2,
                                      y0 + miny + y + (bbox[3] - bbox[1]) // 2,
                                      karte_pos))
    if debug_many_matches:
        for img, _matches in matches.items():
            if _matches > 20:
                print('[many matches', _matches, 'for', namen[ps1.index(img)], ']')
##    print('bildpositionen ende')
    return positions

def beep():
    m1.bell()

__all__ = 'screen_width screen_height spiel_height spiel_width '\
          'my_height my_width breite_des_rechten_menus '\
          'höhe_des_oberen_menus my_breite_der_karte my_höhe_der_karte '\
          'start_der_karte_y höhe_der_karte breite_der_karte '\
          'rechts unten karte_mitte spiel_koordinaten spiel_bbox '\
          'karten_koordinaten beep ressourcen_positionen '\
          'karten_positionen bild_positionen submit_worker '\
          'formationen_verwalten erneuere_position neue_bildposition '\
          'spiel_positionen'.split()
