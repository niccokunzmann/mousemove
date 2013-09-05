from .programm import programm
from ..navigation import *
from ..ressourcen import *

@programm
def erkunde_ressourcen(kundschafter = 3):
    def start():
        öffne_spiel()
        öffne_karte()
    ressourcen_erkundet = []
    start()
    while 1:
        try:
            res = sichte_ressourcen()
            if res:
                print(len(res), 'ressourcen gefunden:')
                for r in res:
                    if r in ressourcen_erkundet: erk = '(erkundet)'
                    else: erk = ''
                    print(r.format_for_print(erk))
            unbekannte = [r for r in res if r.gibt_ehre_beim_erkunden() and \
                                            r not in ressourcen_erkundet]
            i = 0
            kein_kundschater_mehr = False
            for unbekannt in unbekannte:
                if unbekannt.erkunde():
                    ressourcen_erkundet.append(unbekannt)
                    print('erkunde unbekanntes', unbekannt)
                else:
                    kein_kundschater_mehr = True
                    break
                i += 1
            if res and not kein_kundschater_mehr:
                r = res[0]
                for i in range(i, kundschafter):
                    if r.erkunde():
                        ressourcen_erkundet.append(r)
                        print('erkunde', r)
                    else:
                        break
            print('kein Kundschafter mehr')
            yield 60
        except KeyboardInterrupt:
            while 1:
                try:
                    rrr = input('Keyboardinterrupt - pausiert. zum fortsetzen ENTER, zum beenden etwas anderes und ENTER')
                except KeyboardInterrupt: continue                
                if rrr:
                    return
                start()
                break
                

def test_erkunde_ressourcen1():
    öffne_spiel()
    öffne_karte()
    while 1:
        rp = ressourcen_positionen()
        if rp:
            for r in rp:
                print(r)
                if ressource_erkunden(r.x, r.y):
                    print('hingesendet')
                else:
                    print('kein kundschafter mehr')
                    time.sleep(300)
                öffne_dorf_auf_karte()
        else:
            time.sleep(10) # aktualisierungszeit



if __name__ == '__main__':
    erkunde_ressourcen()

