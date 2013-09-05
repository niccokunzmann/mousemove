import time
from . import config
def wait():
    time.sleep(0.5)

def config_file_name():
    return 'config.cfg'

def DEFAULT_RESSOURCEN_PRIORITÄT():
    return 10

def DEFAULT_BANKETT_OPTION():
    return False

config.load()
if not hasattr(config, 'bankett_optionen'):
    config.bankett_optionen = collections.defaultdict(DEFAULT_BANKETT_OPTION)
    config.save()

if not hasattr(config, 'ressourcen_prioritäten'):
    config.ressourcen_prioritäten = collections.defaultdict(DEFAULT_RESSOURCEN_PRIORITÄT)
    config.save()

__all__ = 'wait DEFAULT_RESSOURCEN_PRIORITÄT config_file_name'\
          ' DEFAULT_BANKETT_OPTION'.split()
