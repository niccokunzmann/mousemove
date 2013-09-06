from tkinter.messagebox import showinfo
from .programm import programm

@programm
def programme_anhalten():
    showinfo("Weiter machen?", "Die Programme wurden angehalten.\n OK klicken zum weitermachen.")

__all__ = 'programme_anhalten'.split()
