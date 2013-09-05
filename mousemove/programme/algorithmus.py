andere_waren_nicht_dran_zeit = 0.5

def programm(funktion):
    def f(*args, **kw):
        schedule.schedule()
        iterator = funktion(*args, **kw)
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
            except KeyboardInterrupt: pass
            else: break
    f.__name__ = funktion.__name__
    f.__doc__ = funktion.__doc__
    return f
        
