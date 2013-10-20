from .. import schedule
from ..navigation import beep
from ..errorhandling import report_exc, error_handling
from .. import config
from . import hanging_threads
from ..DorfWahlWidget import DorfWahlWidget
from tkinter import *

import collections
import time

andere_waren_nicht_dran_zeit = 0.5

def programm(funktion):
    def f(*args, **kw):
        try:
            schedule.schedule()
            config.load()
            iterator = funktion(*args, **kw)
            if isinstance(iterator, collections.Iterable):
                while 1:
                    try:
                        for timeout in iterator:
                            if not timeout: timeout = 0
                            letztes_scheduling = now = time.time()
                            ende = letztes_scheduling + timeout
                            schedule.schedule()
                            while now < ende:
                                # busy waiting
                                if letztes_scheduling + andere_waren_nicht_dran_zeit > now:
                                    sleep_time = (1 if ende - letztes_scheduling > 1 else ende - letztes_scheduling)
                                    time.sleep(sleep_time)
                                letztes_scheduling = now
                                schedule.schedule()
                                now = time.time()
                            config.load()
                    except KeyboardInterrupt: pass
                    except:
                        raise report_exc()
                    else: break
        finally:
            schedule.disconnect()
    f.__name__ = funktion.__name__
    f.__doc__ = funktion.__doc__
    return f

def configuration(funktion):
    def f(*args, **kw):
        with error_handling:
            funktion(*args, **kw)
    f.__name__ = funktion.__name__
    f.__doc__ = funktion.__doc__
    return f


def dorf_configuration(titel):
    def wrapper(function):
        @configuration
        def wrapper(*args, **kw):
            config.load()
            tk = Tk()
            tk.title(titel)
            tk.resizable(width=FALSE, height=FALSE)
            dorfwahl = DorfWahlWidget(tk)
            dorfwahl.pack(fill = X, expand = True)
            def alles_speichern():
                tk.quit()
                for dorf, (frame, save) in dorf_frames.items():
                    save(dorf)
                config.save()
            dorfwahl.alles_speichern = alles_speichern
            dorf_frames = {} # dorf : (frame, save)
            defaults = {}
            def default(**kw):
                assert len(kw) == 1
                for key, value in kw.items():
                    if key not in defaults:
                        defaults[key] = value()
                    return defaults[key]
            def aktualisieren(dorf):
                for frame, save in dorf_frames.values():
                    frame.pack_forget()
                if dorf in dorf_frames:
                    frame = dorf_frames[dorf][0]
                    frame.pack()
                    return 
                frame = Frame(tk)
                frame.pack(fill = BOTH, expand = True)
                save = function(frame, dorf, default, *args, **kw)
                dorf_frames[dorf] = (frame, save)
            dorfwahl.aktualisieren = aktualisieren
            def für_alle_übernehmen(dorf):
                frame, save = dorf_frames[dorf]
                for _dorf in dorfwahl.alle_dörfer:
                    save(_dorf)
                for _dorf in list(dorf_frames):
                    if _dorf != dorf: dorf_frames.pop(_dorf)
            dorfwahl.für_alle_übernehmen = für_alle_übernehmen
            tk.bind('<Escape>', lambda e: alles_speichern())
            tk.protocol("WM_DELETE_WINDOW", alles_speichern)
            tk.mainloop()
            tk.destroy()
        wrapper.__name__ = function.__name__
        wrapper.__qualname__ = function.__qualname__
        wrapper.__module__ = function.__module__
        return wrapper
    return wrapper

__all__ = 'configuration programm dorf_configuration'.split()
