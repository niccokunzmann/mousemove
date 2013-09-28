from tkinter import *
from ..images import pil2tkinter_image
from .. import config
import collections
import mousemove.constants
from .programm import configuration

@configuration
def configure_wolfshöhlen():
    t = Tk()
    t.title('Mindestanzehl an Truppen für eine Wolfshöhle')
    image = pil2tkinter_image('Wolfshöhlenformation', master = t)
    l = Label(t, image = image, border = 0)
    l.pack()
    b = Button(t, command = t.quit, text = 'OK')
    b.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    t.resizable(width=FALSE, height=FALSE)
    def entry(x, y):
        spin = Spinbox(t, width = 6, increment = 5,
                       validate = ALL,
                       justify = LEFT,
                       invalidcommand = t.bell,
                       to = 1000,
                       )
        v = IntVar(spin)
        spin.config({'from' : 1}, textvariable = v)
        spin.place(x = x, y = y, anchor = CENTER)
        return v
    c_value = BooleanVar(t, value = config.wolfshöhlen_erkunden)
    c = Checkbutton(t, text = 'Wolfshöhlen angreifen', \
                    variable = c_value, onvalue = True, offvalue = False)
    c.place(x = 5, rely = 0.5, anchor = W)
    entries = dict(
        Bauern = entry(62, 81),
        Bogenschützen = entry(145, 81),
        Pikeniere = entry(62, 156),
        Schwertkämpfer = entry(145, 156),
        Katapulte = entry(62, 232),
        Hauptmänner = entry(145, 232),
        )
    config.load()
    for name, var in entries.items():
        prio = config.minimale_wolfshöhlen_truppenstärken[name]
        var.set(prio)
    t.bind('<Escape>', lambda e: t.quit())
    t.protocol("WM_DELETE_WINDOW", t.quit)
    try:
        t.mainloop()
        config.load()
        for name, var in entries.items():
            config.minimale_wolfshöhlen_truppenstärken[name] = var.get()
        config.save()
    finally:
        t.destroy()

__all__ = ['configure_wolfshöhlen']
