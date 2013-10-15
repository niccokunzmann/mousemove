from .configure_truppen import configure_truppen

class configure_wolfshöhlen(configure_truppen):
    titel = 'Mindestanzehl an Truppen für eine Wolfshöhle'
    hintergrundbildname = 'Wolfshöhlenformation'
    config_ziel_angreifen_attribut = 'wolfshöhlen_angreifen'
    angreifen_text = 'Wolfshöhlen angreifen'
    config_minimale_truppenstärke_attribut = 'minimale_wolfshöhlen_truppenstärken'

__all__ = ['configure_wolfshöhlen']
