from .navigation import alle_dörfer, dorfname, öffne_spiel, SpielNichtGestartet
from .images import *

class _Dorf:
    _dorfbilder = {}

    def __init__(self, name):
        self.name = name

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
        if self in self._dorfbilder[self]:
            return self._dorfbilder[self]
        bild = pil2tkinter_image(self.pil_image(), master = master, *args, **kw)
        self._dorfbilder[self] = bild

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

try:
    from tkinter import *
    from tkinter.messagebox import showerror
except:
    class DorfWahlWidget:
        def __init__(self, *args, **kw):
            raise NotImplementedError('need tkinter for this')
else:
    class DorfWahlWidget(Frame):

        def __init__(self, *args, **kw):
            super().__init__(*args, **kw)
            self.alles_speichern_button = Button(self, text = 'alle speichern',
                                                 command = self._alles_speichern)
            self.alles_speichern_button.pack(side = RIGHT, fill = Y)
            self.für_alle_übernehmen_button = Button(self, text = 'das für alle Dörfer',
                                                 command = self._für_alle_übernehmen)
            self.für_alle_übernehmen_button.pack(side = RIGHT, fill = Y)
            self.neuladen_bild = pil2tkinter_image('neu laden', master = self)
            self.neuladen_button = Button(self, image = self.neuladen_bild, 
                                          command = self.dörfer_laden)
            self.neuladen_button.pack(side = RIGHT, fill = Y)
            self.dorf_auswählen_button = Button(self,
                                command = self.klicke_dorfname)
            self.dorf_auswählen_button.pack(side = RIGHT, fill = BOTH,
                                            expand = True)
            self.aktives_dorf = None
            self.after(0, self.ändere_dorfname)

        @property
        def aktives_dorf(self):
            return self._aktives_dorf

        @aktives_dorf.setter
        def aktives_dorf(self, value):
            if value is None:
                self.für_alle_übernehmen_button.pack_forget()
            else:
                self.für_alle_übernehmen_button.pack()
            self._aktives_dorf = value

        def klicke_dorfname(self):
            if not self.ändere_dorfname():
                self.dörfer_laden()

        def ändere_dorfname(self):
            alle_dörfer = self.alle_dörfer
            if not alle_dörfer:
                self.dorf_auswählen_button['text'] = 'keine Dörfer'
                return False
            try: index = alle_dörfer.index(self.aktives_dorf)
            except: index = -1
            index += 1
            index %= len(alle_dörfer)
            self.aktives_dorf = dorf = alle_dörfer[index]
            self.dorf_auswählen_button['image'] = dorf.tk_image
            self._aktualisieren(dorf)
            return True

        def dörfer_laden(self):
            try:
                öffne_spiel()
            except SpielNichtGestartet:
                showerror('Spiel erst starten!', 'Das Spiel muss gestartet werden, \ndamit ich mich durchklicken kann und mir alle Dörfer merken.')
            else:
                speichere_alle_dörfer_in_config()
                self.ändere_dorfname()
            
        @property
        def alle_dörfer(self):
            from . import config
            dörfer = list(config.alle_dörfer)
            dörfer.sort(key = lambda dorf: dorf.name)
            return dörfer

        def _alles_speichern(self):
            self.alles_speichern()

        def _aktualisieren(self):
            self.aktualisieren()

        def _für_alle_übernehmen(self):
            if self.aktives_dorf:
                self.für_alle_übernehmen(self.aktives_dorf)

        ## zum überschreiben
        def aktualisieren(self, dorf):
            pass

        def alles_speichern(self):
            pass

        def für_alle_übernehmen(self):
            pass

__all__ = 'Dorf speichere_alle_dörfer_in_config DorfWahlWidget'.split()
