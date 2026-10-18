import re
import json
import socket
import subprocess
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


def get_lan_ip_udp() -> str:
    """Devuelve la IP local de la interfaz que conecta a la LAN."""
    # No envía datos reales, solo consulta al SO qué interfaz usaría
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conectar a una IP pública ficticia (no se envía nada)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        if not ip.startswith("127.") and not ip.startswith("10.0.8."):
            return ip
    except Exception:
        pass
    finally:
        s.close()
    return False


def get_lan_ip() -> str:
    """
    Devuelve la IP local del dispositivo (WiFi/Hotspot).

    Estrategia:
        1. Comando 'ip addr' (si está instalado).
        2. Truco de socket UDP (sin dependencias).
        3. Loopback como último recurso.
    """
    # 1. Intentar con 'ip addr' (más fiable en Termux)
    try:
        output = subprocess.check_output(
            ["ip", "-4", "addr", "show"], text=True, stderr=subprocess.DEVNULL, timeout=3
        )
        ips = re.findall(r"inet\s+(\d+\.\d+\.\d+\.\d+)", output)

        for ip in ips:
            if ip.startswith("127.") or ip.startswith("10.0.8."):
                continue
            return ip
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass  # 'ip' no está instalado o falló, pasamos al método 2

    # 2. Truco de socket UDP (Python puro)
    ip = get_lan_ip_udp()
    if ip:
        return ip

    # 3. Último recurso
    return "127.0.0.1"
