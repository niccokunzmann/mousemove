from .navigation import *
from .auslesen import ressourcenstand as ressourcenstand_auslesen
from .positionen import mitte, erneuere_position, bild_positionen
from . import mouse
from . import config
from . import auslesen
from .markt import *

dorf_ist_offen = None

def öffnen(öffner):
    def wrap(function):
        def _function(self, *args, **kw):
            global dorf_ist_offen
            if dorf_ist_offen == öffner:
                return function(self, *args, **kw)
            alt = dorf_ist_offen
            dorf_ist_offen = öffner
            try:
                öffner()
                öffne_dorf_auf_karte(self.dorfname)
                return function(self, *args, **kw)
            finally:
                if callable(alt):
                    alt()
                dorf_ist_offen = alt
        _function.__name__ = function.__name__
        _function.__qualname__ = function.__qualname__
        _function.__doc__ = function.__doc__
        return _function
    return wrap

class Ressourcenstand(dict):
    def __init__(self, für_dorf = None, other = {}):
        if für_dorf is None:
            für_dorf = dorfname()
        self.dorfname = für_dorf
        self.update(other)

    def update(self, other):
        for name, value in other.items():
            self[name.lower()] = value

    @öffnen(öffne_ressourcen)
    def auslesen(self):
        self.update(ressourcenstand_auslesen())

    def __repr__(self):
        super_string = super().__repr__()
        return '{}({}, {})'.format(self.__class__.__name__,
                                   repr(self.dorfname), super_string)

    def waren_zum_verkauf(self):
        d = WarenZuVerkaufen(self.dorfname)
        for ware, stand in self.items():
            if config.waren_verkaufs_schwellwert[ware] < stand:
                d[ware] = stand - config.waren_verkaufs_schwellwert[ware]
        return d

_handelspositionen = None
def handelspositionen():
    global _handelspositionen
    if _handelspositionen is not None:
        return _handelspositionen
    
    RESSOURCEN = mitte(255, 250)
    NAHRUNG = mitte(329, 250)
    WAFFEN = mitte(412, 250)
    BANKETTWAREN = mitte(485, 248)

    eintrag = [(245, 357), (250, 396), (252, 439), (257, 473), (254, 516), (257, 558), (259, 600), (261, 631)]
    handelspositionen = {}
    for MENUPOSITION, waren in [(RESSOURCEN, 'holz stein eisen pech'),
                                     (NAHRUNG, 'äpfel käse fleisch brot gemüse fisch bier'),
                                     (WAFFEN, 'bögen piken rüstung schwerter katapulte'),
                                     (BANKETTWAREN, 'wild möbel metallwaren gewänder wein salz gewürze seide')
                                     ]:
        for i, ware in enumerate(waren.split()):
            handelspositionen[ware.lower()] = (MENUPOSITION, eintrag[i], i)
    _handelspositionen = handelspositionen
    return handelspositionen

def vorhandene_warenmenge(name):
    mengen_position = handelspositionen()[name][2]
    

def ziehe_verkaufsschieber_nach_links():
    args = mitte(835, 457) + mitte(991, 494) + (('Verkaufsschieber',),)
    schieber = bild_positionen(*args)
    if not schieber:
        return False
    schieber = schieber[0]
    mouse.drag(schieber.x, schieber.y, args[0], schieber.y)

def verkauf_einen_händler_mehr():
    mouse.click(*mitte(963, 481))

def es_gibt_noch_händler():
    return erneuere_position('Verkaufsbutton aktiv', box = mitte(995, 521) + mitte(1029, 564))

def click_verkaufen():
    mouse.click(*mitte(1073, 542))
    return richtige_börse()

def richtige_börse():
    p1 = erneuere_position('handelsfehler links')
    p2 = erneuere_position('handelsfehler rechts')
    assert bool(p1) == bool(p2), 'Das Fenster muss vollständig sein'
    if p1 and p2:
        assert p1.y == p2.y, (p1.y, p2.y)
        mouse.click((p1.x + p2.x) // 2, p1.y + 109)
        return False
    return True

def vorhandene_warenmenge_im_handel(ware):
    index = handelspositionen()[ware][2]
    warenmenge = auslesen.warenmenge_im_handel(index) # nur für delta, liest nicht richtig
    return warenmenge

def setze_auf_einen_händler():
    ziehe_verkaufsschieber_nach_links()
    verkauf_einen_händler_mehr()

class WarenZuVerkaufen(dict):
    def __init__(self, dorfname, other = {}):
        self.dorfname = dorfname
        self.update(other)

    @öffnen(öffne_handel)
    def öffne_ware(self, ware):
        menuposition, warenposition = handelspositionen()[ware.lower()][:2]
        mouse.click(*menuposition)
        mouse.click(*warenposition)

    @öffnen(öffne_handel)
    def verkaufe_ware(self, ware):
        """=> Anzahl der losgeschickten Händler"""
        if ware not in self:
            return 0
        self.öffne_ware(ware)
        setze_auf_einen_händler()
        if not es_gibt_noch_händler():
            return 0
        for i in range(wechsele_markt()):
            if click_verkaufen():
                # börse stimmt
                return 1
            else:
                # börse wechseln
                falscher_markt()
                wechsele_markt()

    @öffnen(öffne_handel)
    def verkaufe_alles(self):
        händler = 0
        for ware in self:
            gesendete_händler = self.verkaufe_ware(ware)
            if not gesendete_händler:
                break
            händler += gesendete_händler
        return händler

    def __repr__(self):
        super_string = super().__repr__()
        return '{}({}, {})'.format(self.__class__.__name__,
                                   repr(self.dorfname), super_string)

    def __iter__(self):
        keys = list(super().keys())
        keys.sort(key = lambda ware: self[ware])
        return iter(keys)

__all__ = ['Ressourcenstand', 'WarenZuVerkaufen', 'es_gibt_noch_händler', 
           'ziehe_verkaufsschieber_nach_links', 'richtige_börse']


