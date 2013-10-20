from .programm import programm
from ..navigation import *
from ..ressourcen import *
from .. import config
import random
from collections import defaultdict



def greife_an(ziele, ziele_angegriffen):
    erschöpfte_dörfer = defaultdict(lambda: set())
    for ziel in ziele:
        if ziel.ist_zerstört():
            if ziel in ziele_angegriffen:
                ziele_angegriffen.remove(ziel)
                print(ziel, 'zerstört')
            continue
        if ziel.dorfname in erschöpfte_dörfer[ziel.angiffskategorie]:
            continue
        if not ziel.gibt_ehre_beim_angreifen(): continue
        if ziel in ziele_angegriffen: continue
        try:
            if ziel.angreifen():
                ziele_angegriffen.add(ziel)
                print('Angriff auf', ziel)
            else:
                erschöpfte_dörfer[ziel.angiffskategorie].add(ziel.dorfname)
        except RessourceVerschwunden:
            if ziel in ziele_angegriffen:
                ziele_angegriffen.remove(ziel)
            print(ziel, 'verschwunden!')

def plündere(alle_ressourcen, ressourcen_erkundet):
    for ressource in alle_ressourcen:
        if ressource.ist_bekannt() and ressource in ressourcen_erkundet:
            ressourcen_erkundet.remove(ressource)
            print(ressource, 'wurde erkundet.')
    alle_dörfer = dorfnamen()
    for dorfname in alle_dörfer:
        res = [r for r in alle_ressourcen if r.dorfname == dorfname and r.ist_ressource()]
        kundschafter = 8
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
                chosen_index0 = chosen_index = random.random() * \
                                all_preferences_sum 
                i = 0
                while chosen_index > all_preferences[i]:
                    chosen_index -= all_preferences[i]
                    i += 1
                r = res[i]
                # erkunden
                try:
                    if r.erkunde():
                        pass
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

def sichte_dorf_ressourcen(dorf):
    zusätzliche_ressourcen = []
    if config.wolfshöhlen_angreifen:
        zusätzliche_ressourcen.extend(['wolfshöhle', 'wolfshöhle zerstört'])
    if config.banditenlager_angreifen:
        zusätzliche_ressourcen.extend(['banditenlager', 'banditenlager zerstört'])
    return dorf.sichte_ressourcen(zusätzliche_ressourcen) 

@programm
def erkunde_ressourcen():
    # mit Keyboardinterrupt pausieren
    # anzahl der Kundschafter merken
    # wenn eine unerkannte ressource gefunden wird sofort losschicken
    # waren nur aufdecken, wenn es ehre gibt
    # wenn unerkannte ressource erneut erschient wird sie erkundet
    def start():
        öffne_spiel()
    ressourcen_erkundet = set()
    angegriffene_ziele = set()
    start()
    while 1:
        try:
            for dorf in alle_dörfer():
                ressourcen = sichte_dorf_ressourcen(dorf)
                plündere(ressourcen, ressourcen_erkundet)
                angriffsziele = [ziel for ziel in alle_ressourcen
                                 if ziel.ist_angreifbar()]
                greife_an(angriffsziele, angegriffene_ziele)
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


if __name__ == '__main__':
    erkunde_ressourcen()

