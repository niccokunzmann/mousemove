import time
from collections import defaultdict
import os

def wait():
    time.sleep(0.5)

def config_file_name():
    return 'config.cfg'

def DEFAULT_RESSOURCEN_PRIORITÄT():
    return 10

def DEFAULT_BANKETT_OPTION():
    return False

def default_configuration():
    return dict(bankett_optionen = defaultdict(DEFAULT_BANKETT_OPTION),
                ressourcen_prioritäten = defaultdict(DEFAULT_RESSOURCEN_PRIORITÄT),
                )    

def tesser_exe():
    path = os.path.join(os.environ['Programfiles'], 'Tesseract-OCR', 'tesseract.exe')
    if not os.path.exists(path):
        raise NotImplementedError('You must first install tesseract from https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-setup-3.02.02.exe&can=2&q=')
    return path
    

__all__ = 'wait DEFAULT_RESSOURCEN_PRIORITÄT config_file_name'\
          ' DEFAULT_BANKETT_OPTION default_configuration'.split()
