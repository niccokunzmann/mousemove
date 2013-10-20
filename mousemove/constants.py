import time
from collections import defaultdict
import os
import threading

EHRENRADIUS = 768

def wait():
    time.sleep(0.5)

def config_file_name():
    return 'config.cfg'

def DEFAULT_RESSOURCEN_PRIORITÄT():
    return 10

def DEFAULT_BANKETT_OPTION():
    return False

def DEFAULT_TRUPPENSTÄRKE():
    return 500

DEFAULT_WOLFSHÖHLEN_TRUPPENSTÄRKE = DEFAULT_TRUPPENSTÄRKE
DEFAULT_BANDITENLAGER_TRUPPENSTÄRKE = DEFAULT_TRUPPENSTÄRKE

def DEFAULT_RESSOURCEN_VERKAUF_SCHWELLWERT():
    return 1000000

class _erkundungsmusterClass:
    def __init__(self):
        self.muster = [(.5, .5), (.5, -.5), (-.5, .5), (-.5, -.5)]
        
    def __call__(self, wert = None):
        if wert is None:
            return self.muster[:]
        self.muster = wert

def default_configuration():
    return dict(ressourcen_prioritäten = defaultdict(DEFAULT_RESSOURCEN_PRIORITÄT),
                waren_verkaufs_schwellwert = defaultdict(DEFAULT_RESSOURCEN_VERKAUF_SCHWELLWERT),
                erkunde_alle_unbekannten_ressourcen = False,
                erkundungsmuster = _erkundungsmusterClass(),
                wolfshöhlen_angreifen = False,
                minimale_wolfshöhlen_truppenstärken = defaultdict(DEFAULT_WOLFSHÖHLEN_TRUPPENSTÄRKE),
                banditenlager_angreifen = False,
                minimale_banditenlager_truppenstärken = defaultdict(DEFAULT_BANDITENLAGER_TRUPPENSTÄRKE),
                letzte_bildpositionen = {},
                markt_reihenfolge = {},
                alle_dörfer = [],
                )

def default_dorf_configuration():
    return dict(
        bankett_optionen = defaultdict(DEFAULT_BANKETT_OPTION),
        )

def tesser_exe():
    path = os.path.join(os.environ['Programfiles'], 'Tesseract-OCR', 'tesseract.exe')
    if not os.path.exists(path):
        raise NotImplementedError('You must first install tesseract from https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-setup-3.02.02.exe&can=2&q=')
    return path
    

__all__ = 'wait DEFAULT_RESSOURCEN_PRIORITÄT config_file_name'\
          ' DEFAULT_BANKETT_OPTION default_configuration'.split()
