from .configure_ressources import *

class configure_ressourcen_erkundung(configure_ressources):
    titel = 'Ressourcenprioritäten beim Erkunden'
    hintergrundbildname = 'RessourcenKonfigurationHintergrund'
    config_aktivieren_attribut = 'erkunde_alle_unbekannten_ressourcen'
    aktivieren_text = 'Ressourcen ohne Ehre aufdecken'
    config_ressourcen_attribut = 'ressourcen_prioritäten'
    auch_waffen_anzeigen = False
    lagerwerte = False
    

__all__ = ['configure_ressourcen_erkundung']
