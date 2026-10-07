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

import secrets

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


def build_flask_config() -> dict:
    """
    Devuelve un diccionario con la configuración de Flask,
    listo para pasar a app.config.update().

    Uso:
        from .config import build_flask_config
        app.config.update(build_flask_config())
    """
    hiapp_config = load_config()

    # ¿Hay TLS configurado? (afecta al envío de cookies)
    has_tls = bool(
        hiapp_config.get("tls_cert") and hiapp_config.get("tls_key")
    )

    return {
        # ─── Seguridad ────────
        # Firma de las cookies de sesión.
        "SECRET_KEY": _get_or_create_secret_key(),

        # Nombre de la cookie de sesión.
        "SESSION_COOKIE_NAME": "hiapp_sess",

        # Solo enviar la cookie por HTTPS.
        # Si el usuario no ha configurado TLS, se permite HTTP.
        "SESSION_COOKIE_SECURE": has_tls,

        # JavaScript NUNCA debe leer la cookie de sesión.
        # Previene XSS que robe la sesión.
        "SESSION_COOKIE_HTTPONLY": True,

        # "Lax" envía la cookie en navegaciones top-level (links)
        # pero no en peticiones cross-site automáticas.
        # Equilibrio entre seguridad y usabilidad.
        "SESSION_COOKIE_SAMESITE": "Lax",

        # ─── Comportamiento ───────────
        # Recargar plantillas al cambiar (útil en desarrollo).
        "TEMPLATES_AUTO_RELOAD": True,

        # Límite de subida: 2 GB (para ISOs de PSP).
        "MAX_CONTENT_LENGTH": 2 * 1024 * 1024 * 1024,

        # No usar X-Sendfile (no aplica en Termux/Android).
        "USE_X_SENDFILE": False,
    }
