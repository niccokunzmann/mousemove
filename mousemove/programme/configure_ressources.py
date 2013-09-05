from tkinter import *
from ..images import pil2tkinter_image
from .. import config

def configure_ressources():
    t = Tk()
    t.title('Ressourcenprioritäten beim Erkunden')
    image = pil2tkinter_image('RessourcenKonfigurationHintergrund', t)
    l = Label(t, image = image)
    l.pack()
    b = Button(t, command = t.quit, text = 'OK')
    b.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    t.resizable(width=FALSE, height=FALSE)
    entry1 = lambda x: entry(x, 109)
    entry2 = lambda x: entry(x, 270)
    def entry(x, y):
        spin = Spinbox(t, width = 6, increment = 10,
                       validate = ALL,
                       justify = LEFT,
                       invalidcommand = t.bell,
                       to = 1000,
                       )
        v = IntVar(spin)
        spin.config({"from": 1}, textvariable = v)
        spin.place(x = x, y = y, anchor = CENTER)
        return v
    entries = dict(
        holz = entry1(45),
        stein = entry1(125),
        eisen = entry1(205),
        pech = entry1(285),
        wild = entry1(380),
        möbel = entry1(460),
        metallwaren = entry1(540),
        kleidung = entry1(620),
        wein = entry1(700),
        salz = entry1(780),
        gewürze = entry1(860),
        seide = entry1(940),
        
        äpfel = entry2(45),
        käse = entry2(125),
        fleisch = entry2(205),
        brot = entry2(285),
        gemüse = entry2(365),
        fisch = entry2(445),
        bier = entry2(530),)
    config.load()
    for name, var in entries.items():
        prio = config.ressourcen_prioritäten[name]
        var.set(prio)
    t.bind('<Escape>', lambda e: t.quit())
    t.protocol("WM_DELETE_WINDOW", t.quit)
    try:
        t.mainloop()
        config.load()
        for name, var in entries.items():
            config.ressourcen_prioritäten[name] = var.get()
        config.save()
    finally:
        t.destroy()

__all__ = ['configure_ressources']
