from .navigation import *
from .images import *
from tkinter import *
from tkinter.messagebox import showerror, askyesnocancel
from .dorf import speichere_alle_dörfer_in_config



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
            self.dorf_auswählen_button['background'] = None
            self.dorf_auswählen_button['activebackground'] = None
            self.dorf_auswählen_button['text'] = 'keine Dörfer'
            return False
        try: index = alle_dörfer.index(self.aktives_dorf)
        except: index = -1
        index += 1
        index %= len(alle_dörfer)
        self.aktives_dorf = dorf = alle_dörfer[index]
        image = dorf.tk_image(self)
        background = self.image_background(image)
        self.dorf_auswählen_button['image'] = image
        self.dorf_auswählen_button['background'] = background
        self.dorf_auswählen_button['activebackground'] = background
        self._aktualisieren()
        return True

    def image_background(self, image):
        return '#%02X%02X%02X' % tuple(map(int, image.get(0, 0).split()))

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
        self.aktualisieren(self.aktives_dorf)

    def _für_alle_übernehmen(self):
        if self.aktives_dorf and self.ask_okay_für_alle_übernehmen():
            self.für_alle_übernehmen(self.aktives_dorf)

    def ask_okay_für_alle_übernehmen(self):
        return askyesnocancel("Alle anderen überschreiben?",
                              "Soll die Konfiguration für alle anderen "\
                              "Dörfer gelöscht und überschrieben werden?")

    ## zum überschreiben
    def aktualisieren(self, dorf):
        pass

    def alles_speichern(self):
        pass

    def für_alle_übernehmen(self):
        pass

__all__ = 'DorfWahlWidget'.split()
