from tkinter import *
from ..images import pil2tkinter_image
from .. errorhandling import error_handling
from .programm import dorf_configuration
import abc

to_be_defined = abc.abstractstaticmethod(lambda:0)

class configure_ressources(metaclass = abc.ABCMeta):
    titel = to_be_defined
    hintergrundbildname = to_be_defined
    config_aktivieren_attribut = to_be_defined
    aktivieren_text = to_be_defined
    config_ressourcen_attribut = to_be_defined
    auch_waffen_anzeigen = to_be_defined
    lagerwerte = to_be_defined

    def __init__(self):
        method = dorf_configuration(self.titel)(self._configure_ressources)
        method(self)

    @staticmethod
    def _configure_ressources(t, dorf, default, self):
        image = default(image = lambda: pil2tkinter_image(self.hintergrundbildname, master = t))
        l = Label(t, image = image, border = 0)
        l.pack()
        if self.config_aktivieren_attribut:
            c_value = BooleanVar(t, value = dorf.config[self.config_aktivieren_attribut])
            c = Checkbutton(t, text = self.aktivieren_text, \
                            variable = c_value, onvalue = True, offvalue = False)
            c.place(x = 5, rely = 0.5, anchor = W)
        entry1 = lambda x, step: entry(x, 109, step)
        entry2 = lambda x, step: entry(x, 270, step)
        def entry(x, y, step):
            if not self.lagerwerte: step = 5
            spin = Spinbox(t, width = 6, increment = step,
                           validate = ALL,
                           justify = LEFT,
                           invalidcommand = t.bell,
                           to = 66001,
                           )
            v = IntVar(spin)
            spin.config({'from' : 1}, textvariable = v)
            spin.place(x = x, y = y, anchor = CENTER)
            return v
        entries = dict(
            holz = entry1(45, 1000),
            stein = entry1(125, 1000),
            eisen = entry1(205, 1000),
            pech = entry1(285, 1000),
            
            wild = entry1(380, 20),
            möbel = entry1(460, 20),
            metallwaren = entry1(540, 20),
            kleidung = entry1(620, 20),
            wein = entry1(700, 20),
            salz = entry1(780, 20),
            gewürze = entry1(860, 20),
            seide = entry1(940, 20),
            
            äpfel = entry2(45, 500),
            käse = entry2(125, 500),
            fleisch = entry2(205, 500),
            brot = entry2(285, 500),
            gemüse = entry2(365, 500),
            fisch = entry2(445, 500),
            
            bier = entry2(530, 200),
            )
        if self.auch_waffen_anzeigen:
            entries.update(dict(
            bögen = entry2(615, 5),
            piken = entry2(695, 5),
            rüstung = entry2(775, 5),
            schwerter = entry2(855, 5),
            katapulte = entry2(935, 5),
            ))
        for name, var in entries.items():
            prio = dorf.config[self.config_ressourcen_attribut][name]
            var.set(prio)
        def save(dorf):
            if self.config_aktivieren_attribut:
                dorf.config[self.config_aktivieren_attribut] = bool(c_value.get())
            for name, var in entries.items():
                dorf.config[self.config_ressourcen_attribut][name] = var.get()
        return save

__all__ = ['configure_ressources']
