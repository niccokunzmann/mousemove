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
##    t.tk_setPalette(background = '#b8ae91')
    image = pil2tkinter_image('Wolfshöhlenfomation', master = t)
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
    c_value = BooleanVar(t, value = config.wolfshöhlen_angreifen)
    c = Checkbutton(t, text = 'Wolfshöhlen angreifen', \
                    variable = c_value, onvalue = True, offvalue = False,
                    bg = '#a5997f')
    c.place(relx = .5, y = 265, anchor = CENTER)
    entries = dict(
        Bauern = entry(62, 81, '#b8ae91'),
        Bogenschützen = entry(145, 81, '#b8ae91'),
        Pikeniere = entry(62, 156, '#b2a78b'),
        Schwertkämpfer = entry(145, 156, '#b2a78b'),
        Katapulte = entry(62, 232, '#ab9f85'),
        Hauptmänner = entry(145, 232, '#ab9f85'),
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
        config.wolfshöhlen_angreifen = c_value.get()
        config.save()
    finally:
        t.destroy()

__all__ = ['configure_wolfshöhlen']
