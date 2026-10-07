"""
Blueprint de la API JSON de Hiapp.

Endpoints consumibles por la interfaz web o por clientes externos:
    /api/status      → estado general (versión, add-ons, config).
    /api/version     → solo la versión del paquete.
"""

from importlib.metadata import PackageNotFoundError, version

from flask import Blueprint, jsonify

from ...core.config import get_lan_ip, load_config


bp = Blueprint("api", __name__, url_prefix="/api")


def _get_version() -> str:
    """Devuelve la versión instalada de Hiapp."""
    try:
        return version("hiapp")
    except PackageNotFoundError:
        return "0.0.0+unknown"


@bp.route("/status")
def status():
    """
    Estado general de Hiapp.

    Devuelve un JSON con:
        - name:       nombre del paquete.
        - version:    versión instalada.
        - ip:         IP LAN detectada.
        - port:       puerto del servidor.
        - games_dir:  directorio de ISOs.
        - model:      nombre del modelo de voz configurado.
        - addons:     lista de add-ons cargados (futuro).
    """
    config = load_config()

    return jsonify({
        "name": "hiapp",
        "version": _get_version(),
        "ip": get_lan_ip(),
        "port": config.get("port", 5000),
        "games_dir": config.get("games_dir"),
        "model": config.get("lang_model_name"),
        "addons": [],  # Fase futura
    })


@bp.route("/version")
def version_endpoint():
    """Devuelve solo la versión del paquete."""
    return jsonify({"version": _get_version()})
