"""
Servidor Flask del núcleo de Hiapp.

Crea la app con la configuración de Flask, registra los blueprints
del núcleo y los add-ons bundled (disponibles).
"""

import logging

from flask import Flask, cli

from ..core.i18n import translate
from .routes import register_blueprints
from .config import build_flask_config, _print_server_urls

from ..core.config import get_lan_ip, load_config


def _silence_flask_banner():
    """
    Silencia el banner de arranque de Flask y los logs de Werkzeug.

    Por defecto, Flask imprime muchas líneas al arrancar
    ('Serving Flask app', 'Debug mode', 'Running on ...').
    En Hiapp preferimos mostrar solo nuestros propios mensajes.
    """
    # Banner de arranque
    cli.show_server_banner = lambda *args, **kwargs: None

    # Logs de Werkzeug (peticiones HTTP, warnings del servidor de desarrollo)
    logging.getLogger("werkzeug").setLevel(logging.ERROR)


def create_app() -> Flask:
    """
    Crea y configura la app Flask con todos los blueprints del núcleo
    y los add-ons registrados.

    Returns:
        Instancia de Flask lista para ejecutar.
    """
    app = Flask(__name__)

    # Cargar configuración de Flask (SECRET_KEY, cookies, límites...)
    app.config.update(build_flask_config())

    # Inyectar translate en todas las plantillas
    # Ejemplo de uso:
    # <h2>{{ _('welcome', lang=lang) }}</h2>
    # <p class="muted">{{ _('index_intro', lang=lang) }}</p>
    app.jinja_env.globals["_"] = translate

    # --- Rutas del núcleo ---
    # Registrar blueprints del núcleo (main, api)
    register_blueprints(app)

    # --- Add-ons (bundled) ---
    # En 0.0.1, PPSSPP viene incluido con Hiapp.
    from ..addons.ppsspp.addon import PpssppAddon
    PpssppAddon().register(app)

    # En 0.0.2 pasaremos a descubrimiento dinámico desde ~/.hiapp/addons/.
    # from ..core.registry import discover_addons
    # for addon in discover_addons():
    #     addon.register(app)

    config = load_config()
    lan_ip = get_lan_ip()
    port = config.get("port", 5000)
    lang = config.get("lang", "es")
    _print_server_urls(lan_ip, port, lang)
    print("   Presiona Ctrl+C para detener.")

    return app


def main():
    """
    Punto de entrada del comando `hiapp-server`.

    Útil para desarrollo: arranca solo el servidor, sin voz.
    El comando principal `hiapp` usa create_app() dentro de main.py.
    """
    config = load_config()
    app = create_app()

    # Silenciar el banner de Flask antes de arrancar
    _silence_flask_banner()

    host = config.get("host", "0.0.0.0")
    port = config.get("port", 5000)
    # lan_ip = get_lan_ip()

    # lang = config.get("lang") para translate

    # print("Servidor HTTP levantado de forma independiente.")
    # print(translate("key", lang, lan_ip, port))
    # print(f"🌐 Hiapp escuchando en http://{lan_ip}:{port}/")
    # print(f"🎮 Servidor de juegos en http://{lan_ip}:{port}/game/")
    # print("   Presiona Ctrl+C para detener.")
    # print()

    app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)


# __name__ es "hiapp.server.app"
if __name__ == "__main__":
    main()
