"""
Rutas HTTP del add-on PPSSPP.

Se registran bajo el prefijo /game:
    /game/            → index.txt con la lista de juegos
    /game/<filename>  → streaming del archivo (soporta rangos)
"""

from pathlib import Path

from flask import Blueprint, Response, abort, send_file

# (.)
from .paths import get_games_directory


bp = Blueprint(
    "ppsspp",
    __name__,
    url_prefix="/game",
    template_folder="templates",
    static_folder="static",
)


@bp.route("/", methods=["GET"])
def index():
    """
    Devuelve la lista de juegos disponibles en formato index.txt.

    Cada línea debe empezar con '/' (PPSSPP lo requiere).
    Formato de ejemplo:
        /dissidia.iso
        /god-of-war.cso
    """
    games_dir = Path(get_games_directory())
    lines = []

    if games_dir.is_dir():
        for entry in sorted(games_dir.iterdir()):
            if entry.is_file() and entry.suffix.lower() in {".iso", ".cso"}:
                lines.append(f"/{entry.name}")

    content = "\n".join(lines) + "\n" if lines else ""
    return Response(content, mimetype="text/plain")


@bp.route("/<path:filename>", methods=["GET"])
def stream_game(filename):
    """
    Sirve un archivo de juego con soporte de peticiones de rango.
    PPSSPP requiere respuestas 206 Partial Content.
    """
    games_dir = Path(get_games_directory()).resolve()
    file_path = (games_dir / filename).resolve()

    # Seguridad: evitar path traversal (../../etc/passwd)
    if not str(file_path).startswith(str(games_dir)):
        abort(403)

    if not file_path.is_file():
        abort(404)

    # conditional=True habilita el manejo de cabeceras Range
    return send_file(
        file_path,
        conditional=True,
        mimetype="application/octet-stream",
    )
