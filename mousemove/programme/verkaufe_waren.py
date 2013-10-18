from .programm import programm
from ..navigation import alle_dörfer
from ..ressourcenstand import Ressourcenstand

MINUTEN = 60

@programm
def verkaufe_waren():
    while 1:
        for dorf in alle_dörfer():
            ressourcenstand = Ressourcenstand()
            ressourcenstand.auslesen()
            zu_verkaufen = ressourcenstand.waren_zum_verkauf()
            händler = zu_verkaufen.verkaufe_alles()
            print(händler, 'Händler wurden aus', dorf, 'losgeschickt.')
        yield 4 * MINUTEN

__all__ = ['verkaufe_waren']
