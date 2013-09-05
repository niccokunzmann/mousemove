import pickle as _pickle
import os as _os

from . import files as _files

_config_file_name = _files.config_file_name

_config = globals()

def load():
    if not _os.path.isfile(_config_file_name()):
        return
    d = _pickle.load(open(_config_file_name(), 'rb'))
    print('load', d)
    for k, v in d.items():
        if k not in _do_not_load_and_save and not k.startswith('_'):
            _config[k] = v

def save():
    d = _config.copy()
    for k in list(d.keys()):
        if k in _do_not_load_and_save or k.startswith('_'):
            d.pop(k)
    print('save', d)
    _pickle.dump(d, open(_config_file_name(), 'wb'))



_do_not_load_and_save = dir()
# do not write anything behind this point
