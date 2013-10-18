from . import mouse
from .navigation import dorfname
from . import config
from .positionen import markt_positionen as _markt_positionen
from .positionen import mitte

def markt_reihenfolge():
    key = dorfname()
    # reihenfolge = [index von markt, ...]
    config.markt_reihenfolge.setdefault(key, [])
    return config.markt_reihenfolge[key]

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

def falscher_markt():
    '''Bestrafe den zuletzt gewählten Markt für das Dorf'''
    # bester markt ist schlecht!
    reihenfolge = markt_reihenfolge()
    if reihenfolge:
        reihenfolge.append(reihenfolge.pop(0))

def markt_positionen():
    positionen = _markt_positionen()
    positionen.sort(key = lambda position: position.y)
    result = []
    for position in positionen:
        result.append((position.x + 30, position.y))
    return result

def öffne_märktemenu():
    mouse.click(*mitte(800, 254))

def wechsele_markt():
    '''Wechsele zu dem Markt, der am besten für das Dorf geeignet ist.
    !!! nur falscher_markt() und wechsele_markt() können zur Endlosschelife führen.
    benutze die Anzahl der Märkte als Rückgabe dieser Funktion.'''
    öffne_märktemenu()
    positionen = markt_positionen()
    assert len(positionen), 'Es muss ein Markt zur Verfügung stehen.'
    mouse.click(*wähle_markt_position(positionen))
    assert not markt_positionen(), 'Das Menu "Märkte" muss geschlossen sein.'
    return len(positionen)
    
__all__ = 'wechsele_markt falscher_markt'.split()
