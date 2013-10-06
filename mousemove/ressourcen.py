import collections
from . navigation import im_menu
from . import config
import mousemove.constants
from .positionen import *
from .navigation import *
from . import mouse
from . screenshot import last_screenshot_file_name
from . import config
from .constants import EHRENRADIUS

import time

Ressource = collections.namedtuple('Ressource', ['name', 'x', 'y', 'pos'])

ressource_erkunden_click = lambda: mouse.click(*rechts(1270, 200))
ressource_erkunden_ausführen = lambda: mouse.click(*karte_mitte(824, 569))
ressource_erkunden_abbrechen = lambda: mouse.click(*karte_mitte(910, 210))

def ein_kundschafter():
    """=> ob ein kundschafter ausgewaehlt ist."""
    x, y = karte_mitte(306, 582)
    return bild_positionen(x - 20, y -20, x + 20, y + 20, ('ein_kundschafter',))

def kann_nur_erkundet_werden():
    """=> ob nur die Erkundungsoption zur Verfügung steht.
Best benutzt, wenn die Ressource angewählt wurde"""
##    click(1184, 178)
##    # 166x38
    x1, y1 = rechts(1184, 178)
    x2, y2 = rechts(1350, 216)
    return bild_positionen(x1-2, y1-2, x2+2, y2+2, ('nur Kundschafterbutton',), \
                           debug_many_matches = False)

def wolfshöhle_existiert():
    x1, y1 = rechts(1189, 148)
    x2, y2 = rechts(1341, 234)
    return bild_positionen(x1-2, y1-2, x2+2, y2+2, ('Wolfshöhle ausgewählt',), \
                           debug_many_matches = False)

class RessourceVerschwunden(Exception):
    pass

@im_menu('karte')
def ressource_erkunden(x, y):
    """erkunde eine ressource => ob geklappt"""
    zerstöre_positionsbestimmung()
    mouse.click(x, y)
    if not kann_nur_erkundet_werden():
        raise RessourceVerschwunden('Ressource an der Stelle ({},{}) nicht gefunden.'.format(x, y))
    ressource_erkunden_click()
    for i in range(10):
        if not ein_kundschafter():
            mouse.click(*karte_mitte(309, 582))
        else:
            break
    if i >= 9:
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

    def ist_bekannt(self):
        return not self.ist_unbekannt()

    def ist_ressource(self):
        from . import images
        return self.name.capitalize() in images.bilder_ressourcen

    def gibt_ehre_beim_erkunden(self):
        # 768 ist die groesse des radius in dem es ehre gibt
        return self.ist_unbekannt() and self.ist_im_ehrenradius()

    def ist_im_ehrenradius(self):
        return self.abstand_zum_dorf <= EHRENRADIUS

    def gibt_ehre_beim_angreifen(self):
        return self.ist_wolfshöhle() and self.ist_im_ehrenradius()

    def ist_wolfshöhle(self):
        return self.name.lower() in ('wolfshöhle', 'wolfshöhle zerstört')

    def ist_zerstört(self):
        return self.name.lower() in ('wolfshöhle zerstört',)

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

    @property
    def preferenz(self):
        return 1 / self.sortier_priorität

    def angreifen(self):
        assert self.name.lower() == 'wolfshöhle'
        self.scrolle_hin()
        return wolfshöhle_angreifen(self.x, self.y, self)

wolfshöhle_angreifen_click = lambda: mouse.click(*rechts(1254, 233))

def formationen_verwalten_click():
    mouse.click(*rechts(1276, 649))
    formationen_verwalten_position()

erste_formation_auswählen_position = lambda: formationen_verwalten(137, -63 - 106)
erste_formation_auswählen_click = lambda: mouse.click(*erste_formation_auswählen_position())
formation_setzen_click = lambda: mouse.click(*formationen_verwalten(137, 47))
formation_schließen_click = lambda: mouse.click(*formationen_verwalten(430, 92))
angriff_losschicken_click = lambda: mouse.click(*rechts(1267, 537))
angreifen_ausführen_click = lambda: mouse.click(*karte_mitte(833, 628))
angriff_abbrechen_click = lambda: mouse.click(*rechts(1266, 601))

def formation_auswählen():
    mouse.move(*erste_formation_auswählen_position())
    formationen_verwalten_position()
    erste_formation_auswählen_click()
    formation_setzen_click()
    formation_schließen_click()
        
def wolfshöhle_angreifen(x, y, wolfshöhle = ''):
    """greife eine wolfshhle an => ob geklappt"""
    zerstöre_positionsbestimmung()
    mouse.click(x, y)
    if not wolfshöhle_existiert():
        raise RessourceVerschwunden('Die Wolfshöhle an der Stelle ({},{}) nicht gefunden.'.format(x, y))
    wolfshöhle_angreifen_click()
    time.sleep(0.7)
    if not genug_truppen_für_wolfshöhlen(wolfshöhle):
        angriff_abbrechen_click()
        return False
    formationen_verwalten_click()
    formation_auswählen()
    angriff_losschicken_click()
    angreifen_ausführen_click()
    return True

def genug_truppen_für_wolfshöhlen(wolfshöhle):
    from . import auslesen
    for name, stärke in auslesen.angriffstruppen().items():
        minimal_stärke = config.minimale_wolfshöhlen_truppenstärken[name]
        if minimal_stärke > stärke:
            print('Nur {} {} aber {} benötigt in {}.'.format(stärke, name, minimal_stärke, wolfshöhle.dorfname))
            return False
    return True
    
def sichte_ressourcen(zusätzliche_ressourcen = []):
    res = []
    height = höhe_der_karte() - 20
    width = breite_der_karte() - 20
    dörfer = {}
    schon_mal_doppelt = False
    while not schon_mal_doppelt or any(dörfer.values()):
        starte_kartenpositionsbestimmung()
        if dorfname() in dörfer:
            positionen = dörfer[dorfname()]
            schon_mal_doppelt = True
        else:
            dörfer[dorfname()] = positionen = config.erkundungsmuster()
        if positionen:
            dx, dy = positionen.pop(0)
            scrolle_um(int(dx * width), int(dy * height))
            res.append(ressourcen_positionen(*zusätzliche_ressourcen))
    result = set()
    for rs in res:
        result.update(rs)
    result = list(result)
    result.sort()
    return result
    


__all__ = 'ressourcen_positionen Ressource sichte_ressourcen ein_kundschafter'\
          ' RessourceVerschwunden kann_nur_erkundet_werden '\
          'wolfshöhle_existiert wolfshöhle_angreifen'.split()
