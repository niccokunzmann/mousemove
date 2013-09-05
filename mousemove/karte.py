from .navigation import *
from .positionen import *

def ressourcen_positionen(*args):
    from . import ressourcen
    return ressourcen.ressourcen_positionen(*args)

def sign(i):
    if i == 0: return 0
    return i // abs(i)

def zerstöre_positionsbestimmung():
    global _pos
    _pos = []

zerstöre_positionsbestimmung()
_dorf = None

def starte_kartenpositionsbestimmung():
    global _pos, _dorf
    from .ressourcen import Ressource
    öffne_karte()
    öffne_dorf_auf_karte()
    x = breite_der_karte() // 2
    y = höhe_der_karte() // 2
    _dorf = Ressource('Dorf', x, y, [x, y])
    _pos = [dorf().x, dorf().y]

@im_menu('karte')
def scrolle_um(x, y):
    assert pos(), 'starte_kartenpositionsbestimmung() vorher'
    if x == 0 and y == 0: return
    from . import mouse
    *__, mittex, mittey = karten_koordinaten()
    max_scroll_x = breite_der_karte() // 2
    max_scroll_y = höhe_der_karte() // 2
    scroll_back = 0, 0
    while x != 0 or y != 0:
        sx = (x if abs(x) < max_scroll_x else max_scroll_x * sign(x))
        sy = (y if abs(y) < max_scroll_y else max_scroll_y * sign(y))
        if 0 < abs(sx) < 10 or 0 < abs(sy) < 10:
            sx += 30
            sy += 30
            assert scroll_back == (0, 0)
            scroll_back = -30, -30
        to_x = mittex - sx //2
        to_y = mittey - sy //2
        from_x = mittex + sx - sx //2
        from_y = mittey + sy - sy //2
        x-= sx
        y -= sy
        mouse.drag(from_x, from_y, to_x, to_y, sleep = 0.9)
        _pos[0]-= sx
        _pos[1]-= sy
    scrolle_um(*scroll_back)

def dorf():
    return _dorf

def pos():
    return _pos[:]

__all__ = 'dorf scrolle_um starte_kartenpositionsbestimmung'\
          ' zerstöre_positionsbestimmung pos'.split()
