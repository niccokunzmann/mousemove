from .programm import programm
from ..navigation import alle_dörfer
from ..ressourcenstand import Ressourcenstand
from ..navigation import schließe_error_dialog

MINUTEN = 60

@programm
def verkaufe_waren():
##    import sys
##    sys.stdout = sys.stderr = open('debug.out', 'w', encoding = 'utf8')
    while 1:
        try:
            for dorf in alle_dörfer():
                ressourcenstand = Ressourcenstand()
                ressourcenstand.auslesen()
                zu_verkaufen = ressourcenstand.waren_zum_verkauf()
                händler = zu_verkaufen.verkaufe_alles()
                print(händler, 'Händler wurden aus', dorf, 'losgeschickt.')
        finally:
            if schließe_error_dialog():
                print('Errordialog war offen.')
        yield 4 * MINUTEN

__all__ = ['verkaufe_waren']
