'''
# Así lo hará Hiapp (importlib.util.spec_from_file_location):
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

import importlib.util as import_util
from pathlib import Path


def load_addon(addon_path: Path, context: dict):
    """
    Carga un add-on desde su carpeta.

    Args:
        addon_path: Ruta a la carpeta del add-on (ej. ~/.hiapp/addons/nombre_del_paquete/)
        context:    Diccionario con las herramientas de Hiapp
    """
    init_file = addon_path / "core" / "__init__.py"
    if not init_file.is_file():
        raise FileNotFoundError(f"No se encontró {init_file}")

    # Crear un nombre de módulo único para evitar colisiones
    module_name = f"hiapp_addon_{addon_path.name}"

    # Crear el spec apuntando al __init__.py
    spec = import_util.spec_from_file_location(
        module_name,
        init_file,
        # Tratar el directorio como un paquete
        submodule_search_locations=[str(addon_path / "core")],
    )
    module = import_util.module_from_spec(spec)

    # Registrar el módulo en sys.modules (necesario para imports relativos)
    import sys
    sys.modules[module_name] = module

    # Ejecutar el módulo (esto hace que los import relativos funcionen)
    spec.loader.exec_module(module)

    # Llamar al punto de entrada
    module.register(context)
