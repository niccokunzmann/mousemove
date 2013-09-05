import collections
from . navigation import im_menu
from . import config
from .constants import *
from .positionen import *
from .navigation import *
from . import mouse

Ressource = collections.namedtuple('Ressource', ['name', 'x', 'y', 'pos'])

ressource_erkunden_click = lambda: mouse.click(*rechts(1270, 200))
ressource_erkunden_ausführen = lambda: mouse.click(*karte_mitte(824, 569))
ressource_erkunden_abbrechen = lambda: mouse.click(*karte_mitte(910, 210))

def ein_kundschafter():
    """=> ob ein kundschafter ausgewaehlt ist."""
    x, y = karte_mitte(309, 582)
    return bild_positionen(x - 50, y - 50, x + 50, y + 50, ('ein_kundschafter',))

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
    if karten_positionen('ein_kundschafter'):
        # ausführen is fehlgeschlagen
        ressource_erkunden_abbrechen()
        return False
    return True


config.load()

if not hasattr(config, 'ressourcen_prioritäten'):
    config.ressourcen_prioritäten = collections.defaultdict(DEFAULT_RESSOURCEN_PRIORITÄT)
    config.save()

class Ressource(Ressource):

    def __init__(self, *args, **kw):
        self.validate()

    def validate(self):
        if not isinstance(self.name, str): raise TypeError('name is {} but should be a string'.format(self.name))
        if not isinstance(self.x, int): raise TypeError('x is {} but should be an int'.format(self.x))
        if not isinstance(self.y, int): raise TypeError('y is {} but should be an int'.format(self.y))
        if not isinstance(self.pos, list): raise TypeError('pos is {} but should be a list'.format(self.pos))
        if len(self.pos) not in (0, 2): raise TypeError('pos is {} but should be of length 0 or 2'.format(self.pos))
        if self.pos and not isinstance(self.pos[0], int): raise TypeError('pos[0] is {} but should be an int'.format(self.pos[0]))
        if self.pos and not isinstance(self.pos[1], int): raise TypeError('pos[1] is {} but should be an int'.format(self.pos[1]))
    
    def scrolle_hin(self):
        assert pos(), 'starte_kartenpositionsbestimmung() vorher'
        assert self.pos, 'De ressource wurde aufgenommen, als karte.starte_kartenpositionsbestimmung() vergessen wurde'
        p = pos()
        scrolle_um(p[0] - self.pos[0], p[1] - self.pos[1])

    def erkunde(self):
        self.scrolle_hin()
        v = ressource_erkunden(self.x, self.y)
        starte_kartenpositionsbestimmung()
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
        return (self.relx - other.relx)**2 + (self.rely - other.rely)**2 < \
               differenz_pixel**2

    def __hash__(self):
        return 1

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

    def gibt_ehre_beim_erkunden(self):
        return self.name.lower() == 'ressourcen'

    def format_for_print(self, *args):
        return '{:<15} {:4.0f}({:4.2f}) {} {}'.format(self.name, \
                                                      self.abstand_zum_dorf, \
                                                      self.sortier_priorität,
                                                      ' '.join(map(str, args)),\
                                                      self)

def sichte_ressourcen(zahl = 1000):
    res = set()
    h = höhe_der_karte() - 20
    b = breite_der_karte() - 20
    last = None
    for dx, dy in [(0,0),(0,h),(0,-h),(-b,0),(b,0)]:#,(b,h),(-b,h),(b,-h),(-b,-h)]:
        if last != (0,0):
            starte_kartenpositionsbestimmung()
        last = (dx, dy)
        scrolle_um(dx, dy)
        res.update(ressourcen_positionen())
        if len(res) >= zahl:
            break
    res = list(res)
    res.sort()
    return res
    


__all__ = 'ressourcen_positionen Ressource sichte_ressourcen ein_kundschafter'\
          ''.split()
