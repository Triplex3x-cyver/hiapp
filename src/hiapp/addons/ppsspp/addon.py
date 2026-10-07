"""
Add-on gratuito: servidor de juegos para PPSSPP.
"""

# ..
from ..base import Addon
# .
from .routes import bp


class PpssppAddon(Addon):
    """Servidor HTTP de streaming para PPSSPP (soporta rangos)."""

    name = "ppsspp"
    prefix = "/game"
    free = True

    def register(self, app):
        """Registra el blueprint /game en la app Flask."""
        app.register_blueprint(bp)
