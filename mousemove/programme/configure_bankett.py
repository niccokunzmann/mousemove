from tkinter import *
from ..images import pil2tkinter_image
from .programm import dorf_configuration

image = None

@dorf_configuration('Welche Bankette sollen abgehalten werden?')
def configure_bankett(t, dorf, default):
    image = default(image = lambda: pil2tkinter_image('BankettKonfigurationHintergrund', master = t))
    l = Label(t, image = image, border = 0)
    l.pack()
    def entry(x, y):
        spin = Checkbutton(t)
        v = BooleanVar(spin)
        spin.config(variable = v)
        spin.place(x = x, y = y, anchor = CENTER)
        return v
    # http://hilfe.strongholdkingdoms.de/index.php/Bankette
    entries = dict(
        Ärmlich = entry(591, 196),
        Bescheiden = entry(591, 236),
        Gut = entry(591, 276),
        Beeindruckend = entry(591, 316),
        Prächtig = entry(591, 356),
        Prunkvoll = entry(591, 396),
        Majestätisch = entry(591, 436),
        Erlesen = entry(591, 476),
        )
    for name, var in entries.items():
        prio = config.bankett_optionen[name]
        var.set(prio)
    def save(dorf):
        for name, var in entries.items():
            pass
##            config.bankett_optionen[name] = var.get()
    return save


__all__ = ['configure_bankett']
