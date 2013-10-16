from .programm import programm


MINUTEN = 60

@programm
def verkaufe_waren():
    while 1:
        
        yield 15 * MINUTEN
