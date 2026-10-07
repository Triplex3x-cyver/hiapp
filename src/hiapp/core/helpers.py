"""
Utilidades del núcleo de Hiapp.

Funciones auxiliares que se usan en varios módulos del proyecto.
"""

import math
from pathlib import Path


def load_file(path: str, mode: str = "rt") -> str | None:
    """
    Lee un archivo de texto.

    Args:
        path: Ruta al archivo.
        mode: Modo de apertura (por defecto "rt" = texto lectura).

    Returns:
        El contenido como string, o None si el archivo no existe
        o hay un error de lectura.
    """
    p = Path(path)
    if not p.is_file():
        print(f"⚠️  Archivo no encontrado: {path}")
        return None

    try:
        with open(p, mode, encoding="utf-8", newline=None) as fh:
            return fh.read()
    except OSError as e:
        print(f"⚠️  Error al leer {path}: {e}")
        return None


def format_size(size_bytes: int, decimals: int = 2) -> str:
    """
    Formatea un tamaño en bytes a formato legible (KB, MB, GB...).

    Args:
        size_bytes: Tamaño en bytes.
        decimals: Número de decimales a mostrar.

    Returns:
        Cadena formateada. Ejemplos:
            format_size(0)         -> "0 Bytes"
            format_size(1500)      -> "1.46 KB"
            format_size(1500000)   -> "1.43 MB"
    """
    if size_bytes == 0:
        return "0 Bytes"

    power = 1024
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB"]
    i = int(math.floor(math.log(size_bytes, power)))

    if units[i] == "Bytes":
        return f"{size_bytes} {units[i]}"
    return f"{size_bytes / (power ** i):.{decimals}f} {units[i]}"
