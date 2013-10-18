from tkinter import *
from .programm import programm

@programm
def programme_anhalten():
    t = Tk()
    t.title("Weiter machen?")
    l = Label(t, text = "Die Programme wurden angehalten.\n OK klicken zum weitermachen.")
    l.pack()
    b = Button(t, text = 'OK', command = t.quit)
    b.pack()
    t.mainloop()
    t.destroy()

__all__ = 'programme_anhalten'.split()
