from tkinter import *

import win32gui

import mousemove.navigation
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
    assert x < 0 # wir brauchen einen rand!
    assert y < 0
    width = right + x # eigentlich - x aber wir ziehen den rand ab
    height = bottom + y
    x = 0
    y = 0
    return x, y, width, height

def ressourcen_positionen(*bilder):
    if not bilder: bilder = images.bilder_ressourcen
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

def bild_positionen(minx, miny, maxx, maxy, namen):
    from .ressourcen import Ressource
    from . import karte
    bilder = [images.open_image(name) for name in namen]
    s = images.screenshot()
    s_getpixel = s.getpixel
    x0, y0, maxx, maxy = s.getbbox()
    assert x0 == 0, x0
    assert y0 == 0, y0
    assert maxx == screen_width() #1
    assert maxy == screen_height() #2
    ps1 = [(image.getpixel((0,0))[:3], image, image.getbbox()) for image in bilder]
    maxx -= min([img[2][2] for img in ps1])
    maxy -= min([img[2][3] for img in ps1])
    positions = []
    matches = {img : 0 for img in ps1}
##    print(minx, '-->',maxx, '|', miny, '-->', maxy)
    for x in range(minx, maxx):
        for y in range(miny, maxy):
            match = True
            px = s_getpixel((x, y))[:3]
            for img in ps1:
                if img[0] != px: continue
                matches[img] += 1
                bbox = img[2]
                matches[img]
                if maxx - x < bbox[2] or maxy - y < bbox[3]:
                    continue
                image_getpixel = img[1].getpixel
                for dx in range(bbox[2]):
                    for dy in range(bbox[3]):
                        if s_getpixel((x + dx, y + dy))[:3] != \
                           image_getpixel((dx, dy))[:3]:
                            match = False
                            break
                    if not match: break
                if match:
                    positions.append(Ressource(namen[ps1.index(img)],
                                      x + bbox[2] // 2,
                                      y + bbox[3] // 2,
                                      karte.pos()))
    for img, _matches in matches.items():
        if _matches > 20:
            print('many matches', _matches, 'for', bilder[ps1.index(img)])
    return positions

def beep():
    m1.bell()

__all__ = 'screen_width screen_height spiel_height spiel_width '\
          'my_height my_width breite_des_rechten_menus '\
          'höhe_des_oberen_menus my_breite_der_karte my_höhe_der_karte '\
          'start_der_karte_y höhe_der_karte breite_der_karte '\
          'rechts unten karte_mitte spiel_koordinaten spiel_bbox '\
          'karten_koordinaten beep ressourcen_positionen '\
          'karten_positionen bild_positionen'.split()
