from .configure_truppen import configure_truppen

class configure_banditenlager(configure_truppen):
    titel = 'Mindestanzehl an Truppen für ein Banditenlager'
    hintergrundbildname = 'Banditenlagerformation'
    config_ziel_angreifen_attribut = 'banditenlager_angreifen'
    angreifen_text = 'Banditenlager angreifen'
    config_minimale_truppenstärke_attribut = 'minimale_banditenlager_truppenstärken'

__all__ = ['configure_wolfshöhlen']
