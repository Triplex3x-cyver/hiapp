from pathlib import Path

# (...core)
from ...core.config import load_config, save_config


def get_games_directory() -> str:
    """Devuelve el directorio de juegos configurado, creándolo si no existe."""
    config = load_config()
    games_dir = config.get("games_dir", str(Path.home() / "PSP"))

    # Crear si no existe
    Path(games_dir).mkdir(parents=True, exist_ok=True)
    return games_dir


def save_games_directory(path: str) -> None:
    """Guarda el directorio de juegos en la configuración."""
    config = load_config()
    config["games_dir"] = str(path)
    save_config(config)
