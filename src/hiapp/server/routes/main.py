"""
Blueprint principal de Hiapp.

Rutas del núcleo:
    /                → página principal (panel).
    /favicon.ico     → ícono del sitio.
"""
from ...core.config import load_config

from flask import Blueprint, render_template, send_from_directory


bp = Blueprint(
    "main",
    __name__,
    template_folder="../templates",
    static_folder="../static",
)


@bp.route("/")
def index():
    """
    Página principal de Hiapp.

    Muestra un panel con enlaces al estado, add-ons y
    (en el futuro) al sistema de seguridad.
    """
    lang = load_config().get("lang", "es")
    return render_template("index.html", lang=lang), 200


@bp.route("/favicon.ico")
def favicon():
    """Sirve el favicon del sitio."""
    return send_from_directory(
        bp.static_folder,
        "favicon.svg",
        mimetype="image/svg+xml",
    )
