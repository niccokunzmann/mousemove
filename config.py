import pickle as _pickle
import config
import os as _os

_config = config.__dict__
del config

_FILENAME = 'config.cfg'

def load():
    if not _os.path.isfile(_FILENAME):
        return
    d = _pickle.load(open(_FILENAME, 'rb'))
    print('load', d)
    for k, v in d.items():
        if k not in do_not_load_and_save and not k.startswith('_'):
            _config[k] = v

def save():
    d = _config.copy()
    for k in list(d.keys()):
        if k in do_not_load_and_save or k.startswith('_'):
            d.pop(k)
    print('save', d)
    _pickle.dump(d, open(_FILENAME, 'wb'))

do_not_load_and_save = dir() + [
    'do_not_load_and_save', '__initializing__', '__cached__'
    ]
# do not write anything behind this point
