"""
Rutas HTTP del add-on PPSSPP.

Se registran bajo el prefijo /game:
    GET /game/              → index.txt con la lista de juegos
    HEAD /game/<filename>   → obtener cabeceras HTTP
        - (existencia y soporte de rangos del servidor)
    GET /game/<filename>    → streaming del archivo
        - (soporta rangos)

Notas:
    - PPSSPP solo codifica espacios en las URLs (%20).
    - PPSSPP pide archivos con el prefijo que aparece en el index.txt.
    - Flask decodifica automáticamente los parámetros de la ruta.
    - Soportamos GET y HEAD (PPSSPP usa HEAD para verificar existencia).
"""

from pathlib import Path
from urllib.parse import quote

from flask import Blueprint, Response, abort, send_file

from .paths import get_games_directory


bp = Blueprint(
    "ppsspp",
    __name__,
    url_prefix="/game",
    template_folder="templates",
    static_folder="static",
)


# ==== Manejo de nombres de archivo ====
# class ServerUriEncode:
#    ReplaceAll(self, plain):
#        return quote(plain)


@bp.route("/", methods=["GET"])  # HEAD?
@bp.route("", methods=["GET", "HEAD"])  # /game
def index():
    """
    Devuelve la lista de juegos disponibles en formato index.txt.

    Cada línea debe empezar con '/' (PPSSPP lo requiere).
    Los nombres se codifican con quote() para que PPSSPP los
    solicite correctamente (espacios → %20).
    Formato de ejemplo:
        /dissidia.iso
        /god-of-war.cso
    """
    games_dir = Path(get_games_directory())
    lines = []

    if games_dir.is_dir():
        for entry in sorted(games_dir.iterdir()):
            if entry.is_file() and entry.suffix.lower() in {".iso", ".cso"}:
                encoded_name = quote(entry.name)
                lines.append(f"/{encoded_name}")

    content = "\n".join(lines) + "\n" if lines else ""
    return Response(content, mimetype="text/plain")


@bp.route("/<path:filename>", methods=["GET", "HEAD"])
def stream_game(filename):
    """
    Sirve un archivo de juego con soporte de peticiones de rango.
    PPSSPP requiere respuestas 206 Partial Content para el streaming.

    Flask decodifica automáticamente el percent-encoding del parámetro
    <path:filename>, así que aquí ya tenemos el nombre real del archivo.
    """
    games_dir = Path(get_games_directory()).resolve()
    file_path = (games_dir / filename).resolve()

    # Seguridad: evitar path traversal (../../etc/passwd)
    if not str(file_path).startswith(str(games_dir)):
        abort(403)

    if not file_path.is_file():
        abort(404)

    return send_file(
        file_path,
        conditional=True,  # habilita el manejo de cabeceras Range
        mimetype="application/octet-stream",
    )
