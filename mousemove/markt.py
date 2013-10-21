from . import mouse
from .navigation import dorfname, schließe_error_dialog
from . import config
from .positionen import markt_positionen as _markt_positionen
from .positionen import mitte
import time

def markt_reihenfolge(dorf = None):
    if dorf is None:
        dorf = dorfname()
    # reihenfolge = [index von markt, ...]
    config.markt_reihenfolge.setdefault(dorf, [])
    return config.markt_reihenfolge[dorf]

def wähle_markt_position(positionen):
    reihenfolge = markt_reihenfolge()
    if len(reihenfolge) < len(positionen):
        # reihenfolge länger machen
        reihenfolge.extend(range(len(reihenfolge), len(positionen)))
    else:
        # reihenfolge kürzer machen
        for index in range(len(positionen), len(reihenfolge)):
            reihenfolge.remove(index)
    return positionen[reihenfolge[0]]

def markt_positionen():
    positionen = _markt_positionen()
    positionen.sort(key = lambda position: position.y)
    result = []
    for position in positionen:
        result.append((position.x + 30, position.y))
    return result

def öffne_märktemenu():
    mouse.click(*mitte(800, 254))

def markt_lässt_sich_öffnen():
    return _wähle_einen_markt()

_letztes_verkaufsdorf = None

def _wähle_einen_markt():
    öffne_märktemenu()
    t = time.time()
    positionen = markt_positionen()
    if not positionen:
        sleeping = 0.5 - time.time() + t
        if sleeping > 0: time.sleep(sleeping)
        positionen = markt_positionen()
    if positionen:
        mouse.click(*wähle_markt_position(positionen))
    return positionen


def wechsele_markt():
    '''Wechsele zu dem Markt, der am besten für das Dorf geeignet ist.
    !!! nur falscher_markt() und wechsele_markt() können zur Endlosschelife führen.
    benutze die Anzahl der Märkte als Rückgabe dieser Funktion.'''
    global _letztes_verkaufsdorf
    positionen = _wähle_einen_markt()
    if not positionen:
        schließe_error_dialog()
        positionen = _wähle_einen_markt()
    assert len(positionen), 'Es muss ein Markt zur Verfügung stehen.'
    assert not markt_positionen(), 'Das Menu "Märkte" muss geschlossen sein.'
    _letztes_verkaufsdorf = dorfname()
    # plus 1 wegen falscher verwendung von falscher_markt()
    return len(positionen) + 1 
    
def falscher_markt():
    '''Bestrafe den zuletzt gewählten Markt für das Dorf'''
    # bester markt ist schlecht!
    if _letztes_verkaufsdorf != dorfname(): return
    reihenfolge = markt_reihenfolge()
    if reihenfolge:
        reihenfolge.append(reihenfolge.pop(0))

__all__ = 'wechsele_markt falscher_markt markt_lässt_sich_öffnen'.split()
