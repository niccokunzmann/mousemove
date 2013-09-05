import pickle as _pickle
import config

_config = config.__dict__
del config

def load():
    d = _pickle.load(open('config.cfg', 'rb'))
    print('load', d)
    for k, v in d.items():
        if k not in do_not_load_and_save and not k.startswith('_'):
            _config[k] = v

def save():
    d = _config.copy()
    for k in list(d.keys()):
        if k in do_not_load_and_save:
            d.pop(k)
    _pickle.dump(d, open('config.cfg', 'wb'))

do_not_load_and_save = dir() + [
    'do_not_load_and_save', '__initializing__', '__cached__'
    ]
# do not write anything behind this point
