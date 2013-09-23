from tkinter import *
from ..images import pil2tkinter_image
from .. import config
import collections
import mousemove.constants
from .programm import configuration

@configuration
def configure_bankett():
    t = Tk()
    t.title('Welche Bankette sollen abgehalten werden?')
    image = pil2tkinter_image('BankettKonfigurationHintergrund', master = t)
    l = Label(t, image = image, border = 0)
    l.pack()
    b = Button(t, command = t.quit, text = 'OK')
    b.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    t.resizable(width=FALSE, height=FALSE)
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
    config.load()
    for name, var in entries.items():
        prio = config.bankett_optionen[name]
        var.set(prio)
    t.bind('<Escape>', lambda e: t.quit())
    t.protocol("WM_DELETE_WINDOW", t.quit)
    try:
        t.mainloop()
        config.load()
        for name, var in entries.items():
            config.bankett_optionen[name] = var.get()
        config.save()
    finally:
        t.destroy()

__all__ = ['configure_bankett']
