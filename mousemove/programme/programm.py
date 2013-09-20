from .. import schedule, disconnect
from ..navigation import beep
from ..errorhandling import report_exc, error_handling
from .. import config

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
            disconnect()
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
        
__all__ = 'configuration programm'.split()
