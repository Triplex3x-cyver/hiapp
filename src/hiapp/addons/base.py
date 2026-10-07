"""
Clase base para todos los add-ons de Hiapp.

Un add-on es una funcionalidad opcional que se registra en el núcleo.
Puede ser gratuito (viene con Hiapp) o PRO (instalado desde el servidor de licencias).

Cada add-on debe:
    - Definir `name` (identificador único).
    - Definir `prefix` (prefijo de URL si expone rutas Flask).
    - Definir `free` (True si es gratuito, False si es PRO).
    - Implementar `register(app)` si expone rutas HTTP.
    - Opcionalmente sobrescribir `start()` y `stop()` si gestiona recursos.
"""


class Addon:
    """Clase base para todos los add-ons de Hiapp."""

    # --- Atributos que cada subclase debe sobrescribir ---
    name: str = "unnamed"
    prefix: str = ""  # Prefijo de URL (ej. "/game")
    free: bool = True

    # --- Ciclo de vida ---

    def register(self, app):
        """
        Registra los blueprints y rutas del add-on en la app Flask.

        Args:
            app: Instancia de Flask donde registrar el add-on.
        """
        pass

    def start(self):
        """Inicia recursos propios (hilos, procesos). Opcional."""
        pass

    def stop(self):
        """Detiene recursos propios. Opcional."""
        pass

    # --- Estado ---

    def status(self) -> dict:
        """
        Devuelve un diccionario con el estado actual del add-on.
        Las subclases pueden sobrescribirlo para dar más información.
        """
        return {
            "name": self.name,
            "prefix": self.prefix,
            "free": self.free,
        }

    # --- Utilidades ---

    def __repr__(self) -> str:
        kind = "free" if self.free else "PRO"
        return f"<Addon {self.name} ({kind}) prefix={self.prefix!r}>"
