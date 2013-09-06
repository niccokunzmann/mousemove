import time
from collections import defaultdict

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

__all__ = 'wait DEFAULT_RESSOURCEN_PRIORITÄT config_file_name'\
          ' DEFAULT_BANKETT_OPTION default_configuration'.split()
