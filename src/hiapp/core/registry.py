'''
Registro y cargador de add-ons para Hiapp.

Escanea la carpeta de add-ons instalados (~/.hiapp/addons/),
valida su estructura y los carga dinámicamente en la aplicación.

Así lo hará Hiapp (importlib.util.spec_from_file_location):
import importlib.util as import_util

spec = import_util.spec_from_file_location(
    "hiapp_addon_ppsspp",
    "core/__init__.py"   # ← el __init__, no paths.py
)
module = import_util.module_from_spec(spec)
spec.loader.exec_module(module)

# Y luego llama a la función:
module.register(context)   # ← esto registra el blueprint
'''

import sys
import json
# from pathlib import Path
import importlib.util as import_util

from .config import HIAPP_DIR

# Directorio donde viven los add-ons instalados
ADDONS_DIR = HIAPP_DIR / "addons"


def discover_addons() -> list[dict]:
    """
    Escanea el directorio de add-ons y devuelve una lista con los
    metadatos de los add-ons válidos encontrados.

    No carga el código, solo lee los `addon.json`.
    """
    addons = []
    if not ADDONS_DIR.is_dir():
        return addons

    for entry in sorted(ADDONS_DIR.iterdir()):
        if not entry.is_dir():
            continue

        manifest_path = entry / "addon.json"
        core_init = entry / "core" / "__init__.py"

        # Validación básica de estructura
        if not manifest_path.is_file() or not core_init.is_file():
            print(f"⚠️  Add-on ignorado (estructura inválida): {entry.name}")
            continue

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                meta = json.load(f)

            # Añadir la ruta física para usarla al cargar
            meta["_path"] = entry
            addons.append(meta)
        except Exception as e:
            print(f"⚠️  Error leyendo addon.json en {entry.name}: {e}")

    return addons


def load_addon(addon: dict, context: dict):
    """
    Carga un add-on en la app Flask.

    Args:
        addon: diccionario con los metadatos (debe incluir "_path")
        context: herramientas de Hiapp para el add-on
    """
    name = addon.get("name")
    addon_path = addon.get("_path")
    core_path = addon_path / "core"

    # 1. Crear un nombre de módulo único para evitar colisiones
    module_name = f"hiapp_addon_{name}"

    # 2. Preparar la importación dinámica
    # Al usar submodule_search_locations, permitimos que el add-on
    # haga imports relativos internos (from . import algo)
    spec = import_util.spec_from_file_location(
        module_name,
        # Crear el spec apuntando al __init__.py
        core_path / "__init__.py",
        # Tratar el directorio como un paquete
        submodule_search_locations=[str(core_path)]
    )
    if not spec or not spec.loader:
        raise ImportError(f"No se pudo crear el spec para {name}")

    module = import_util.module_from_spec(spec)

    # 3. Registrar en sys.modules (necesario para que los imports relativos funcionen)
    sys.modules[module_name] = module

    # 4. Ejecutar el código del add-on (esto hace que los import relativos funcionen)
    spec.loader.exec_module(module)

    # 5. Llamar a la función de entrada estándar
    if hasattr(module, "register"):
        module.register(context)
    else:
        raise AttributeError(f"El add-on '{name}' no tiene la función register(context)")


def load_all_addons(app, config, load_config, save_config, logger):
    """
    Descubre y carga todos los add-ons instalados.
    Se llama desde create_app() en server/app.py.
    """
    import hiapp  # Para obtener la versión actual

    # Construir el contexto que recibirán todos los add-ons
    context = {
        "app": app,
        "config": config,
        "load_config": load_config,
        "save_config": save_config,
        "logger": logger,
        "hiapp_dir": HIAPP_DIR,
        "hiapp_version": getattr(hiapp, "__version__", "unknown"),
    }

    addons = discover_addons()
    if not addons:
        return

    for addon in addons:
        try:
            load_addon(addon, context)
            print(f"✅ Add-on cargado: {addon['name']} v{addon.get('version', '?')}")
        except Exception as e:
            print(f"❌ Error cargando add-on '{addon['name']}': {e}")
