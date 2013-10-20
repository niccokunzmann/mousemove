from .navigation import *
from .images import *
from . import constants

class Dorfkonfiguration:
    def __init__(self, dict):
        self.__dict__ = dict
        for name, value in constants.default_dorf_configuration().items():
            if name not in self.__dict__:
                self[name] = value
            
    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, item, value):
        self.__dict__[item] = value

class _Dorf:
    _dorfbilder = {}

    def __init__(self, name):
        self.name = name
        self._konfiguration = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert value.is_image_text(), 'Der Name muss ausgelesen sein.'
        self._image = open_image(value.image_file)
        self._name = value

    def pil_image(self):
        return self._image.copy()

    def tk_image(self, master = None, *args, **kw):
        if self in self._dorfbilder:
            return self._dorfbilder[self]
        bild = pil2tkinter_image(self.pil_image(), master = master, *args, **kw)
        self._dorfbilder[self] = bild
        return bild

    def ist_aktiv(self):
        return self.name == dorfname()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return '<{} name={}>'.format(self.__class__.__name__, repr(self.name))

    def __eq__(self, other):
        return other == str(self)

    def __hash__(self):
        return hash(str(self))

    def starte_kartenpositionsbestimmung(self):
        from . import karte
        karte.starte_kartenpositionsbestimmung(self.name)

    def sichte_ressourcen(self, zusätzliche_ressourcen = []):
        from . import config
        res = []
        height = höhe_der_karte() - 20
        width = breite_der_karte() - 20
        self.starte_kartenpositionsbestimmung()
        positionen = config.erkundungsmuster()
        while positionen:
            dx, dy = positionen.pop(0)
            scrolle_um(int(dx * width), int(dy * height))
            res.append(ressourcen_positionen(*zusätzliche_ressourcen))
        result = set()
        for rs in res:
            result.update(rs)
        result = list(result)
        result.sort()
        return result

    @property
    def config(self):
        return Dorfkonfiguration(self._konfiguration)

def _config_property(name):
    @property
    def _get_config(dorf):
        return dorf.config[name]
    @_get_config.setter
    def _set_config(dorf, value):
        dorf.config[name] = value
    _get_config.fget.__name__ = _set_config.fset.__name__ = name
    _get_config.fget.__qualname__ = _set_config.fset.__qualname__ = _Dorf.__qualname__ + '.' + name
    return _get_config

def update_dorf():
    for name, value in constants.default_dorf_configuration().items():
        if name in dir(_Dorf):
            raise ValueError('{} is already an attribute of _Dorf. '\
                             'The configuration is invalid.'.format(name))
        setattr(_Dorf, name, _config_property(name))
update_dorf()
del update_dorf, _config_property

def Dorf(name = None):
    from . import config
    if name is None:
        name = dorfname()
    if hasattr(config, 'alle_dörfer'):
        for dorf in config.alle_dörfer:
            if dorf.name == name:
                return dorf
    return _Dorf(name)

def speichere_alle_dörfer_in_config():
    from . import config
    config.alle_dörfer = set(alle_dörfer())

__all__ = 'Dorf speichere_alle_dörfer_in_config DorfWahlWidget'.split()
