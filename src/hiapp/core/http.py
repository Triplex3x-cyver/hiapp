
import importlib.metadata


def get_user_agent() -> str:
    """
    Devuelve el User-Agent con nombre, versión y contacto del desarrollador.
    Se usa en todas las peticiones de red salientes de Hiapp.
    """
    try:
        version = importlib.metadata.version("hiapp")
    except importlib.metadata.PackageNotFoundError:
        version = "dev"  # No instalado
    return (
        f"hiapp/{version} "
        "(+https://github.com/Triplex3x-cyver/hiapp; "
        "triplex3x.cyver@gmail.com)"
    )


# Cabeceras por defecto para requests
DEFAULT_HEADERS = {"User-Agent": get_user_agent()}
