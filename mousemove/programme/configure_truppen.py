from tkinter import *
from ..images import pil2tkinter_image
from .. import config
import collections
import mousemove.constants
from .programm import configuration
import abc

to_be_defined = abc.abstractstaticmethod(lambda:0)

class configure_truppen(metaclass = abc.ABCMeta):
    titel = to_be_defined
    hintergrundbildname = to_be_defined
    config_ziel_angreifen_attribut = to_be_defined
    angreifen_text = to_be_defined
    config_minimale_truppenstärke_attribut = to_be_defined

    @property
    def ziel_angreifen(self):
        return getattr(config, self.config_ziel_angreifen_attribut)
    @ziel_angreifen.setter
    def ziel_angreifen(self, value):
        setattr(config, self.config_ziel_angreifen_attribut, value)
    
    @property
    def minimale_truppenstärke(self):
        return getattr(config, self.config_minimale_truppenstärke_attribut)
    @minimale_truppenstärke.setter
    def minimale_truppenstärke(self, value):
        setattr(config, self.config_minimale_truppenstärke_attribut, value)

    load = staticmethod(config.load)
    save = staticmethod(config.save)

    @configuration
    def __init__(self):
        t = Tk()
        t.title(self.titel)
    ##    t.tk_setPalette(background = '#b8ae91')
        image = pil2tkinter_image(self.hintergrundbildname, master = t)
        l = Label(t, image = image, border = 0)
        l.pack()
        b = Button(t, command = t.quit, text = 'OK')
        b.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        t.resizable(width=FALSE, height=FALSE)
        def entry(x, y, bg):
            spin = Spinbox(t, width = 6, increment = 5,
                           validate = ALL,
                           justify = LEFT,
                           invalidcommand = t.bell,
                           to = 500,
                           bg = bg
                           )
            v = IntVar(spin)
            spin.config({'from' : 1}, textvariable = v)
            spin.place(x = x, y = y, anchor = CENTER)
            return v
        c_value = BooleanVar(t, value = self.ziel_angreifen)
        c = Checkbutton(t, text = self.angreifen_text, \
                        variable = c_value, onvalue = True, offvalue = False,
                        bg = '#a5997f')
        c.place(relx = .5, y = 265, anchor = CENTER)
        entries = dict(
            Bauern = entry(62, 81, '#b8ae91'),
            Bogenschützen = entry(145, 81, '#b8ae91'),
            Pikeniere = entry(62, 156, '#b2a78b'),
            Schwertkämpfer = entry(145, 156, '#b2a78b'),
            Katapulte = entry(62, 232, '#ab9f85'),
            Hauptmann = entry(145, 232, '#ab9f85'),
            )
        self.load()
        for name, var in entries.items():
            prio = self.minimale_truppenstärke[name]
            var.set(prio)
        t.bind('<Escape>', lambda e: t.quit())
        t.protocol("WM_DELETE_WINDOW", t.quit)
        try:
            t.mainloop()
            self.load()
            for name, var in entries.items():
                self.minimale_truppenstärke[name] = var.get()
            self.ziel_angreifen = c_value.get()
            self.save()
        finally:
            t.destroy()

__all__ = ['configure_truppen', 'to_be_defined']
