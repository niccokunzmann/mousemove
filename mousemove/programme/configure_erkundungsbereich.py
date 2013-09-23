from tkinter import *
from ..images import pil2tkinter_image
from .. import config
import collections
import mousemove.constants
from .programm import configuration

@configuration
def configure_erkundungsbereich():
    t = Tk()
    t.title('Wo soll erkundet werden?')
    t.resizable(width=FALSE, height=FALSE)
    einträge = [[[(0, 0)], "Dorf mit 1"], 
                [[(.5, .5), (.5, -.5), (-.5, .5), (-.5, -.5)], "Dorf mit 4"],
                [[(.5, .5), (.5, -.5), (-.5, .5), (-.5, -.5), (0, -1.5), (0, 1.5)], "Dorf mit 6"],
                [[(-.5, 0), (.5, 0), (-.5, 1), (.5, 1), (-.5, -1), (.5, -1)], "Dorf mit 6.2"],
                [[(0, 0), (-1, 0), (1, 0), (-.5, -1), (.5, -1), (-5., 1), (.5, 1)], "Dorf mit 7"], 
                [[(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (-1, -1), (1, 1), (1, -1)], "Dorf mit 9"], 
                ]

    chosen_index = IntVar(t, -1)
    max_grid_width = int(round(len(einträge) **.5))
    for index, eintrag in enumerate(einträge):
        image = pil2tkinter_image(eintrag[1], master = t)
        eintrag.append(image)
        if config.erkundungsmuster() == eintrag[0]:
            chosen_index.set(index)
        rb = Radiobutton(t, value = index, variable = chosen_index, image = image)
        rb.grid(row = index // max_grid_width, column = index % max_grid_width)
    
    b = Button(t, command = t.quit, text = 'OK')
    b.place(relx = 0.5, rely = 1, anchor = S)
    t.bind('<Escape>', lambda e: t.quit())
    t.protocol("WM_DELETE_WINDOW", t.quit)
    try:
        t.mainloop()
        config.load()
        if chosen_index.get() != -1:
            config.erkundungsmuster(einträge[chosen_index.get()][0])
        config.save()
    finally:
        t.destroy()

__all__ = ['configure_erkundungsbereich']
