import time
import os
import win32gui
import pywintypes
from .mouse import *

from .files import forschungsordner
from .positionen import *

wo = 'spiel geöffnet'

def öffnen(f):
    assert 'öffne' in f.__name__
    l = f.__name__.split('_')
    ort = l[l.index('öffne') + 1]
    def x(*args, **kw):
        global wo
        wo = ort
        return f(*args, **kw)
    x.__name__ = f.__name__
    return x

def im_menu(ort):
    def xx(f):
        def x(*args, **kw):
            assert wo == ort, '"{}" ist im Modus "{}" und nicht im Modus "{}". "öffne_{}()" davor fehlt.'.format(f.__name__, wo, ort, ort)
            return f(*args, **kw)
        x.__name__ = f.__name__
        return x
    return xx


windowhandle = None

class SpielNichtGestartet(Exception):
    pass

@öffnen
def öffne_spiel():
    global windowhandle
    # GetWindowRect(handle) # koordinaten des spieles
    name = "Stronghold Kingdoms - Welt"
    handles = []
    def append_handle(handle, handles):
        handles.append(handle)
    win32gui.EnumWindows(append_handle, handles)
    for handle in handles:
        text = win32gui.GetWindowText(handle)
        if name.lower() in text.lower():
            for i in range(30):
                try:
                    win32gui.SetForegroundWindow(handle)
                    windowhandle = handle
                    return
                except pywintypes.error: pass
    raise SpielNichtGestartet('Spiel nicht gestartet')

def spiel_window_handle():
    if windowhandle == None:
        öffne_spiel()
    return windowhandle

@im_menu('karte')
def zoom_raus():
    for i in range(5):
        right_click(378, 367)
        time.sleep(0.5)

_dorfnamen = set()
_dorfname = None
def dorfname_ist_bekannt():
    return _dorfname is not None

def click_dorf_nach_rechts():
    global _dorfname
    _dorfname = None
    click(*rechts(933, 61))
    
def click_dorf_nach_links():
    global _dorfname
    _dorfname = None
    click(*rechts(917, 61))

ZOOM_ZUM_DORF_ZEIT = 2

def öffne_dorf_auf_karte(name = ''):
    global _dorfname
    from .auslesen import dorfname
    assert name is not None
    if name == _dorfname:
        click_dorf_nach_links()
        t = ZOOM_ZUM_DORF_ZEIT + time.time()
        click_dorf_nach_rechts()
        now = time.time()
        if now < t: time.sleep(t - now)
        _dorfname = dorfname()
        assert _dorfname == name, (_dorfname, name)
        return 
    dorfnamen = set()
    for i in range(20):
        click_dorf_nach_rechts()
        t = time.time()
        time.sleep(0.5)
        _dorfname = dorfname()
        dorfnamen.add(_dorfname)
        if name == _dorfname or not name: break
    if name and name != _dorfname:
        raise ValueError('Dorf {} konnte nicht unter den Dörfern {} '\
                         'gefunden werden.'.format(repr(name), dorfnamen))
    s = ZOOM_ZUM_DORF_ZEIT - time.time() + t
    if s > 0: time.sleep(s) # warten bis er zum dorf gescrollt hat

def dorfname():
    global _dorfname
    from .auslesen import dorfname
    if not dorfname_ist_bekannt():
        _dorfname = dorfname()
    _dorfnamen.add(_dorfname)
    return _dorfname

def dorfnamen():
    return _dorfnamen.copy()

def alle_dörfer():
    '''Iterator über alle Dörfer'''
    from . import config
    from .dorf import Dorf
    dörfer = []
    while 1:
        öffne_dorf_auf_karte()
        dorf = Dorf()
        if dorf in dörfer: break
        dörfer.append(dorf)
        yield dorf

@öffnen
def öffne_karte():
    click(*rechts(932, 91))
@öffnen
def öffne_dorf():
    click(*rechts(977, 96))
@öffnen
def öffne_gemeinde():
    click(*rechts(1027, 92))
@öffnen
def öffne_forschung():
    click(*rechts(1084, 95))
@öffnen
def öffne_rang():
    click(*rechts(1142, 94))
@öffnen
def öffne_quests():
    click(*rechts(1194, 94))
@öffnen
def öffne_angriffe():
    click(*rechts(1252, 95))
@öffnen
def öffne_berichte():
    click(*rechts(1286, 94))
@öffnen
def öffne_fraktion():
    click(*rechts(1345, 95))

@im_menu('forschung')
def öffne_forschungsliste():
    click(*rechts(1234, 341))

@im_menu('forschung')
@öffnen
def öffne_gewerbe():
    öffne_forschungsliste()
    click(112, 347)
    
@im_menu('forschung')
@öffnen
def öffne_militär():
    öffne_forschungsliste()
    click(260, 346)
    
@im_menu('forschung')
@öffnen
def öffne_landwirtschaft():
    öffne_forschungsliste()
    click(420, 345)
    
@im_menu('forschung')
@öffnen
def öffne_bildung():
    öffne_forschungsliste()
    click(626, 336)

def funktion(kathegorie, name, bildpfad):
    def erforsche_():
        öffne_forschung()
        locals()['öffne_' + kathegorie]()
        click_bild(bildpfad)
    erforsche_.__name__ += name
    erforsche_.__doc__ = "Erforsche {name} in der Kathegorie {kathegorie}".format(**locals())
    return im_menu('Forschung')(erforsche_)

_names = []

for kathegorie in os.listdir(forschungsordner):
    kathegorieordner = os.path.join(forschungsordner, kathegorie)
    for bild in os.listdir(kathegorieordner):
        bildpfad = os.path.join(kathegorieordner, bild)
        name = os.path.splitext(bild)[0]
        f = funktion(kathegorie, name, bildpfad)
        locals()[f.__name__] = f
        _names.append(f.__name__)

del funktion

def dorf():
    from . import karte
    return karte.dorf()

def pos():
    from . import karte
    return karte.pos()

def scrolle_um(x, y):
    from . import karte
    return karte.scrolle_um(x, y)

def starte_kartenpositionsbestimmung(*args, **kw):
    from . import karte
    return karte.starte_kartenpositionsbestimmung(*args, **kw)

def zerstöre_positionsbestimmung():
    from . import karte
    return karte.zerstöre_positionsbestimmung()

def öffne_dorfkarte():
    öffne_dorf()
    click(*rechts(977, 123))

def öffne_burgkarte():
    öffne_dorf()
    click(*rechts(1027, 123))

def öffne_ressourcen():
    öffne_dorf()
    time.sleep(0.5)
    click(*rechts(1084, 123))

def öffne_handel():
    öffne_dorf()
    click(*rechts(1142, 123))

def öffne_truppen():
    öffne_dorf()
    click(*rechts(1194, 123))

def öffne_einheiten():
    öffne_dorf()
    click(*rechts(1252, 123))

def öffne_bankett():
    öffne_dorf()
    click(*rechts(1286, 123))

def öffne_vasallen():
    öffne_dorf()
    click(*rechts(1345, 123))

def schließe_error_dialog():
    from .positionen import erneuere_position
    from . import mouse
    p1 = erneuere_position('handelsfehler links')
    p2 = erneuere_position('handelsfehler rechts')
    assert bool(p1) == bool(p2), 'Das Fenster muss vollständig sein'
    if p1 and p2:
        assert p1.y == p2.y, (p1.y, p2.y)
        mouse.click((p1.x + p2.x) // 2, p1.y + 109)
        return False
    return True

__all__ = 'zoom_raus spiel_window_handle öffne_spiel öffne_dorf_auf_karte'\
          ' öffne_karte öffne_dorf öffne_gemeinde öffne_forschung öffne_rang'\
          ' öffne_quests öffne_angriffe öffne_berichte öffne_fraktion'\
          ' öffne_forschungsliste öffne_gewerbe öffne_militär öffne_landwirtschaft'\
          ' öffne_bildung scrolle_um starte_kartenpositionsbestimmung'\
          ' zerstöre_positionsbestimmung dorf im_menu pos beep öffne_dorfkarte'\
          ' öffne_burgkarte öffne_ressourcen öffne_handel öffne_truppen'\
          ' öffne_einheiten öffne_bankett öffne_vasallen dorfname_ist_bekannt'\
          ' dorfname dorfnamen alle_dörfer SpielNichtGestartet'\
          ' schließe_error_dialog'.split()

__all__.extend(_names)

del _names
