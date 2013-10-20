from .configure_ressources import *

class configure_ressourcen_verkauf(configure_ressources):
    titel = 'Ab welchem Wert werden Ressourcen verkauft'
    hintergrundbildname = 'RessourcenKonfigurationHintergrund'
    config_aktivieren_attribut = ''
    aktivieren_text = 'XXXXXXXXXXXXXX'
    config_ressourcen_attribut = 'waren_verkaufs_schwellwert'
    auch_waffen_anzeigen = True
    lagerwerte = True
    

__all__ = ['configure_ressourcen_verkauf']
