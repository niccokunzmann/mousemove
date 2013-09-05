import collections
import .positionen

def ressourcen_positionen(*args):
    return positionen.ressourcen_positionen()

Ressource = collections.namedtuple('Ressource', ['name', 'x', 'y', 'pos'])

ressource_erkunden_click = lambda: click(*rechts(1270, 200))
ressource_erkunden_ausführen = lambda: click(*karte_mitte(824, 569))
ressource_erkunden_abbrechen = lambda: click(*karte_mitte(910, 210))

def ein_kundschafter():
    """=> ob ein kundschafter ausgewaehlt ist."""
    x, y = karte_mitte(309, 582)
    return bild_positionen(x - 50, y - 50, x + 50, y + 50, ('ein_kundschafter',))

@im_menu('karte')
def ressource_erkunden(x, y):
    """erkunde eine ressource => ob geklappt"""
    zerstöre_positionsbestimmung()
    click(x, y)
    ressource_erkunden_click()
    for i in range(10):
        if not ein_kundschafter():
            click(*karte_mitte(309, 582))
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
    def scrolle_hin(self):
        assert pos, 'starte_kartenpositionsbestimmung() vorher'
        scrolle_um(pos[0] - self.pos[0], pos[1] - self.pos[1])

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
        return self.x - self.pos[0]

    @property
    def rely(self):
        return self.y - self.pos[1]

    def abstand_zu(self, other):
        return ((self.relx - other.relx)**2 + (self.rely - other.rely)**2)**0.5

    @property
    def abstand_zum_dorf(self):
        return self.abstand_zu(dorf)

    @property
    def sortier_priorität(self):
        return self.abstand_zum_dorf / self.priorität

    def __lt__(self, other):
        return self.abstand_zum_dorf < other.abstand_zum_dorf

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
        

def sichte_ressourcen(zahl = 1000):
    res = set()
    h = höhe_der_karte() - 20
    b = breite_der_karte() - 20
    last = None
    for dx, dy in [(0,0),(0,h),(0,-h),(-b,0),(b,0),(b,h),(-b,h),(-b,h),(-b,-h)]:
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
    


__all__ = 'ressourcen_positionen Ressource'.split()
