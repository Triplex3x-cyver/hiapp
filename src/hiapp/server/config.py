"""
Configuración de Flask para Hiapp.

Los valores propios de Hiapp (puerto, host, modelo, etc.) viven en
~/.hiapp/config.json y los gestiona core.config.

Esta clase solo cubre los ajustes específicos de Flask:
    - Firma de sesiones (SECRET_KEY).
    - Cookies de sesión (seguridad).
    - Límite de subidas.
    - Comportamiento del servidor de plantillas.
"""
# Para activar el modo debug
# production o development
# FLASK_ENV="development"

import os
import secrets
# from datetime import timedelta

from ..core.i18n import translate
from ..core.config import load_config, save_config


def _get_or_create_secret_key() -> str:
    """
    Obtiene la SECRET_KEY del archivo de configuración.
    Si no existe, la genera y la guarda.

    La clave es única por instalación y persistente entre reinicios.
    Si cambia, todas las sesiones activas se invalidan, así que
    debe guardarse en ~/.hiapp/config.json.
    """
    config = load_config()

    if not config.get("secret_key"):
        config["secret_key"] = secrets.token_hex(32)
        save_config(config)

    return config["secret_key"]


def _print_server_urls(lan_ip, port, lang):
    if lan_ip == "127.0.0.1":
        # Modo solo-local
        print(translate("server_local_only", lang=lang, port=port))
        print(translate("server_local_hint", lang=lang))

    else:
        print(translate("server_running", lang=lang, ip=lan_ip, port=port))
        print(translate("game_running", lang=lang, ip=lan_ip, port=port))
    # print()


def build_flask_config() -> dict:
    """
    Devuelve un diccionario con la configuración de Flask,
    listo para pasar a app.config.update().

    Uso:
        from .config import build_flask_config
        app.config.update(build_flask_config())
    """
    hiapp_config = load_config()
    # server_name = os.environ.get("SERVER_NAME", None)
    # users_json_file = os.path.join(os.path.dirname(__file__), "server/json/users.json")
    # database_url = os.environ.get(
    #    "DATABASE_URL", f"mysql+pymysql://{db_cred['user']}:"
    #    + f"{db_cred['pass']}@{db_cred['host']}/"
    #    + f"{db_cred['name']}")  # = "sqlite:///project.db"
    # db_cred = hiapp_config.get("db_cred")

    # ¿Hay TLS configurado? (afecta al envío de cookies)
    has_tls = bool(
        hiapp_config.get("tls_cert") and hiapp_config.get("tls_key")
    )

    return {
        # --- Seguridad -----------
        # Firma de las cookies de sesión.
        # Do not reveal the secret key
        "SECRET_KEY": _get_or_create_secret_key(),
        #
        # Implement key rotation without invalidating active sessions
        # or other recently-signed secrets
        # "SECRET_KEY_FALLBACKS": [],
        # "APP_API_KEY": "",

        # Nombre de la cookie de sesión.
        "SESSION_COOKIE_NAME": "hiapp_sess",

        # Solo enviar la cookie por HTTPS.
        # Si el usuario no ha configurado TLS, se permite HTTP.
        "SESSION_COOKIE_SECURE": has_tls,

        # JavaScript NUNCA debe leer la cookie de sesión.
        # Previene XSS que robe la sesión.
        "SESSION_COOKIE_HTTPONLY": True,

        # "Lax" envía la cookie en navegaciones top-level (enlaces)
        # pero no en peticiones cross-site automáticas (como imágenes o enlaces).
        # Equilibrio entre seguridad y usabilidad.
        # Opciones: Strict o Lax
        "SESSION_COOKIE_SAMESITE": "Lax",

        # "PERMANENT_SESSION_LIFETIME": int(
        #   timedelta(days=31).total_seconds())  # 2678400 (en segundos)

        # La cookie se envía con cada respuesta (True)
        # "SESSION_REFRESH_EACH_REQUEST": False,

        # Evitar host falsificado del cliente.
        # Bloquear alguna ip (permitir solo localhost?)
        # "TRUSTED_HOSTS": ["0.0.0.0", "127.0.0.1"],

        # Lista de IPs permitidas (vacía = todas)
        "ALLOWED_IPS": [],  # ejemplo: ['192.168.1.100', '127.0.0.1']

        # --- Comportamiento -----------
        # Nombre o ip real
        # "SERVER_NAME": server_name,  # def None
        "PREFERRED_URL_SCHEME": "https" if has_tls else "http",
        # Recargar plantillas al cambiar (útil en desarrollo).
        "TEMPLATES_AUTO_RELOAD": os.environ.get("FLASK_ENV") == "development",

        # Límite de subida: 2 GB (para ISOs de PSP).
        # puede usarse Request.max_content_length en la vista.
        "MAX_CONTENT_LENGTH": 2 * 1024 * 1024 * 1024,

        # No usar X-Sendfile (no aplica en Termux/Android).
        # Apache reconoce esto y sirve los datos de manera más eficiente. (False).
        "USE_X_SENDFILE": False,

        # --- Base de datos -----------
        # (útil para negocios)
        # "DATABASE_URI": "mysql://user@localhost/dir",  # sqlite/mysql
        # "DB_SERVER": "localhost",
        #
        # Conector SQLAlchemy, controlador pymysql
        # "SQLALCHEMY_DATABASE_URI": database_url,
        # "SQLALCHEMY_TRACK_MODIFICATIONS": False,

        # --- Usuarios -----------
        # Backend de usuarios: 'json' o 'mariadb'
        # "USER_BACKEND": "mariadb",  # Por defecto json, 'mariadb' para usar base de datos
        #
        # Archivo JSON para usuarios
        # "USERS_JSON_FILE": users_json_file,

        # "DB_SECRET_KEY": "",
        # "DB_TABLES_WITH_KEY": "",
    }
