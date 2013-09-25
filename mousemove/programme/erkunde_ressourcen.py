from .programm import programm
from ..navigation import *
from ..ressourcen import *
from .. import config
import random

@programm
def erkunde_ressourcen(kundschafter_pro_dorf = 4):
    # mit Keyboardinterrupt pausieren
    # anzahl der Kundschafter merken
    # wenn eine unerkannte ressource gefunden wird sofort losschicken
    # waren nur aufdecken, wenn es ehre gibt
    # wenn unerkannte ressource erneut erschient wird sie erkundet
    def start():
        öffne_spiel()
    ressourcen_erkundet = set()
    start()
    while 1:
        try:
            alle_ressourcen = sichte_ressourcen()
            for ressource in alle_ressourcen:
                if ressource.ist_bekannt() and ressource in ressourcen_erkundet:
                    ressourcen_erkundet.remove(ressource)
                    print(ressource, 'wurde erkundet.')
            alle_dörfer = dorfnamen()
            for dorfname in alle_dörfer:
                res = [r for r in alle_ressourcen if r.dorfname == dorfname]
                kundschafter = kundschafter_pro_dorf
                if res:
                    print(len(res), 'Ressourcen gefunden:')
                    for r in res:
                        if r in ressourcen_erkundet: erk = '(erkundet)'
                        else: erk = ''
                        print(r.format_for_print(erk))
                unbekannte = [r for r in res if r.soll_zuerst_erkundet_werden() \
                                            and r not in ressourcen_erkundet]
                i = 0
                kein_kundschater_mehr = False
                for unbekannt in unbekannte:
                    try:
                        if unbekannt.erkunde():
                            ressourcen_erkundet.add(unbekannt)
                            kundschafter -= 1
                            print('erkunde unbekanntes', unbekannt)
                        else:
                            kein_kundschater_mehr = True
                            break
                    except RessourceVerschwunden:
                        print('Ressource verschwunden!')
                        continue
                    i += 1
                if res and not kein_kundschater_mehr:
                    all_preferences = [r.preferenz for r in res]
                    all_preferences_sum = sum(all_preferences)
                    gesendete_kundschafter = 0
                    while gesendete_kundschafter < kundschafter and res:
                        # roulette wheel
                        chosen_index0 = chosen_index = random.random() * all_preferences_sum 
                        i = 0
                        while chosen_index > all_preferences[i]:
                            chosen_index -= all_preferences[i]
                            i += 1
                        r = res[i]
                        # erkunden
                        try:
                            if r.erkunde():
                                print('erkunde', r)
                            else:
                                break
                        except RessourceVerschwunden:
                            all_preferences.pop(res.index(r))
                            res.remove(r)
                            all_preferences_sum -= r.preferenz
                            print('Ressource verschwunden!')
                        else:
                            gesendete_kundschafter += 1
                
                print('kein Kundschafter mehr in {}'.format(dorfname))
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

@programm
def erkunde_ressourcen2(kundschafter = 4):
    def start():
        öffne_spiel()
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

