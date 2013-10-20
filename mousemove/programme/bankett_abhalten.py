from .programm import programm
from ..navigation import *
from ..positionen import mitte
from ..ressourcen import *
from ..mouse import click
from .. import config

qualitäten = ['Ärmlich', 
              'Bescheiden',
              'Gut',
              'Beeindruckend',
              'Prächtig',
              'Prunkvoll',
              'Majestätisch',
              'Erlesen',]

positionen = []

x, y = 960, 389
for qualität in qualitäten:
    positionen.append((qualität, x, y))
    y += 40

@programm
def bankett_abhalten():
    öffne_spiel()
    while 1:
        for dorf in alle_dörfer():
            öffne_bankett()
            for qualität, x, y in positionen:
                if dorf.bankett_optionen[qualität]:
                    click(*mitte(x, y))
                    print('Halte in', dorf, 'Bankett ab', qualität)
        yield 2 * 60 * 60


__all__ = 'qualitäten bankett_abhalten positionen'
