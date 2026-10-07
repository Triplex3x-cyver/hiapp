import json
import socket
from pathlib import Path

# Rutas base (fijas)
HIAPP_DIR = Path.home() / ".hiapp"
CONFIG_FILE = HIAPP_DIR / "config.json"

# Configuración de usuario (resetable con --all)
USER_DEFAULTS = {
    "models_dir": str(HIAPP_DIR / "models"),
    "games_dir": str(Path.home() / "PSP"),
    "port": 5000,
    "host": "0.0.0.0",
    "aliases": [],
}

# Estado de la aplicación (NO resetable con --all)
APP_DEFAULTS = {
    "lang": None,
    "lang_model_name": None,
}

# Todas las claves válidas (para validación en CLI)
ALL_DEFAULTS = {**USER_DEFAULTS, **APP_DEFAULTS}


def load_config() -> dict:
    """Carga la configuración aplicando esta prioridad:
        1. Valores por defecto (USER_DEFAULTS + APP_DEFAULTS).
        2. Valores del archivo ~/.hiapp/config.json (si existen).

    Solo se cargan las claves que existen en ALL_DEFAULTS.
    """
    result = {**USER_DEFAULTS, **APP_DEFAULTS}

    # 1. Cargar del archivo json
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                # config.update(json.load(f))
                saved = json.load(f)

            for key in ALL_DEFAULTS:
                if key in saved:  # Solo carga las que estén en ALL_KEYS
                    result[key] = saved[key]
        except (json.JSONDecodeError, OSError):
            pass  # Usar valores por defecto

    return result


def save_config(config: dict):
    """Guarda la configuración en ~/.hiapp/config.json."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_lan_ip() -> str:
    """Devuelve la IP local de la interfaz que conecta a la LAN."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No envía nada, solo consulta la ruta de salida hacia internet
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()
