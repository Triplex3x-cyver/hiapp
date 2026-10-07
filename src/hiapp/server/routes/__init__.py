"""
Registro central de blueprints de Hiapp.

Cada blueprint agrupa un conjunto de rutas relacionadas:
    - main: página principal, favicon.
    - api:  endpoints JSON (estado, versión).

Uso:
    from .routes import register_blueprints
    register_blueprints(app)
"""

from flask import Flask


def register_blueprints(app: Flask) -> None:
    """
    Registra todos los blueprints del núcleo en la aplicación Flask.

    Args:
        app: Instancia de Flask donde registrar los blueprints.
    """
    # Importaciones locales para evitar ciclos al cargar el módulo
    from .main import bp as main_bp
    from .api import bp as api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
