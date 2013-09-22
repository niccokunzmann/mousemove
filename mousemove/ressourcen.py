import collections
from . navigation import im_menu
from . import config
import mousemove.constants
from .positionen import *
from .navigation import *
from . import mouse
from . screenshot import last_screenshot_file_name
from . import config
import time

Ressource = collections.namedtuple('Ressource', ['name', 'x', 'y', 'pos'])

ressource_erkunden_click = lambda: mouse.click(*rechts(1270, 200))
ressource_erkunden_ausführen = lambda: mouse.click(*karte_mitte(824, 569))
ressource_erkunden_abbrechen = lambda: mouse.click(*karte_mitte(910, 210))

def ein_kundschafter():
    """=> ob ein kundschafter ausgewaehlt ist."""
    x, y = karte_mitte(306, 582)
    return bild_positionen(x - 20, y -20, x + 20, y + 20, ('ein_kundschafter',))

@im_menu('karte')
def ressource_erkunden(x, y):
    """erkunde eine ressource => ob geklappt"""
    zerstöre_positionsbestimmung()
    mouse.click(x, y)
    ressource_erkunden_click()
    for i in range(10):
        if not ein_kundschafter():
            mouse.click(*karte_mitte(309, 582))
        else:
            break
    if i > 1:
        print(i, 'mal gebraucht, um den kundschafter auf 1 zu setzen', last_screenshot_file_name())
    ressource_erkunden_ausführen()
    time.sleep(0.5) # wegen netzwerklatzenz kann das hier schon mal schiefgehen
    if ein_kundschafter():
        # ausführen ist fehlgeschlagen
        ressource_erkunden_abbrechen()
        return False
    return True

class Ressource(Ressource):

    def __init__(self, *args, **kw):
        self.validate()

    def validate(self):
        if not isinstance(self.name, str): raise TypeError('name is {} but should be a string'.format(self.name))
        if not isinstance(self.x, int): raise TypeError('x is {} but should be an int'.format(self.x))
        if not isinstance(self.y, int): raise TypeError('y is {} but should be an int'.format(self.y))
        if not isinstance(self.pos, list): raise TypeError('pos is {} but should be a list'.format(self.pos))
        if len(self.pos) not in (0, 3): raise TypeError('pos is {} but should be of length 0 or 2'.format(self.pos))
        if self.pos and not isinstance(self.pos[0], int): raise TypeError('pos[0] is {} but should be an int'.format(self.pos[0]))
        if self.pos and not isinstance(self.pos[1], int): raise TypeError('pos[1] is {} but should be an int'.format(self.pos[1]))
    
    def scrolle_hin(self):
        assert self.pos, 'Die ressource wurde aufgenommen, als karte.starte_kartenpositionsbestimmung() vergessen wurde'
        starte_kartenpositionsbestimmung(self.dorfname)
        assert pos(), 'starte_kartenpositionsbestimmung() vorher'
        p = pos()
        scrolle_um(p[0] - self.pos[0], p[1] - self.pos[1])

    def erkunde(self):
        print("erkunde", self)
        self.scrolle_hin()
        v = ressource_erkunden(self.x, self.y)
        return v

    @property
    def priorität(self):
        prio = config.ressourcen_prioritäten[self.name.lower()]
        if prio <= 1:
            return 1
        return prio

    @property
    def relx(self):
        assert self.pos, 'De ressource wurde aufgenommen, als karte.starte_kartenpositionsbestimmung() vergessen wurde'
        return self.x - self.pos[0]

    @property
    def rely(self):
        assert self.pos, 'De ressource wurde aufgenommen, als karte.starte_kartenpositionsbestimmung() vergessen wurde'
        return self.y - self.pos[1]

    def abstand_zu(self, other):
        return ((self.relx - other.relx)**2 + (self.rely - other.rely)**2)**0.5

    @property
    def abstand_zum_dorf(self):
        return self.abstand_zu(dorf())

    @property
    def sortier_priorität(self):
        return self.abstand_zum_dorf / self.priorität

    def __lt__(self, other):
        return self.sortier_priorität < other.sortier_priorität

    def __eq__(self, other):
        differenz_pixel = 70 # 100 vielleicht?
        return self.dorfname == other.dorfname and \
               (self.relx - other.relx)**2 + (self.rely - other.rely)**2 < \
               differenz_pixel**2

    def __hash__(self):
        return hash(self.dorfname)

    def set_pos(self, pos):
        while self.pos:
            self.pos.pop()
        self.pos.extend(pos)

    def abstand_zu_gerade_zwischen(self, a, b):
        if a == b: return self.abstand_zu(a)
        dx = a.relx - b.relx
        dy = a.rely - b.rely
        u = ((a.relx - self.relx) * dy + (self.rely - a.rely) * dx) / (dy*dy + dx*dx)
        return abs(u) * (dy*dy + dx*dx)**0.5

    def ist_unbekannt(self):
        return self.name.lower() == 'ressourcen'

    def gibt_ehre_beim_erkunden(self):
        # 768 ist die groesse des radius in dem es ehre gibt
        return self.ist_unbekannt() and self.abstand_zum_dorf <= 768

    def soll_zuerst_erkundet_werden(self):
        if config.erkunde_alle_unbekannten_ressourcen:
            return self.ist_unbekannt()
        return self.gibt_ehre_beim_erkunden()

    def format_for_print(self, *args):
        return '{:<15} {:4.0f}({:4.2f}) {} {}'.format(self.name, \
                                                      self.abstand_zum_dorf, \
                                                      self.sortier_priorität,
                                                      ' '.join(map(str, args)),\
                                                      self)
    @property
    def dorfname(self):
        return self.pos[2]
    
def sichte_ressourcen():
    res = []
    h = höhe_der_karte() - 20
    b = breite_der_karte() - 20
    dörfer = {}
    # erste Positionen abarbeiten um die Dorfzalh heauszufinden
    while 1:
        starte_kartenpositionsbestimmung()
        if dorfname() in dörfer: break
        dörfer[dorfname()] = positionen = config.erkundungsbereich()
        dx, dy = positionen.pop(0)
        scrolle_um(dx, dy)
        res.append(ressourcen_positionen())
    # andere Positionen abarbeiten
    while dörfer:
        starte_kartenpositionsbestimmung()
        positionen = dörfer.get(dorfname(), None)
        if positionen:
            dx, dy = positionen.pop(0)
            scrolle_um(dx, dy)
            res.append(ressourcen_positionen())
            if not positionen:
                dörfer.pop(dorfname())
    result = set()
    for rs in res:
        result.update(rs)
    result = list(result)
    result.sort()
    return result
    


__all__ = 'ressourcen_positionen Ressource sichte_ressourcen ein_kundschafter'\
          ''.split()
