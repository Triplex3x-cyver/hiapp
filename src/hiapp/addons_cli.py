"""
CLI para la gestión de add-ons (instalar, listar, eliminar).
"""

import json
import shutil
import zipfile
import hashlib
# from pathlib import Path

import requests

from .core.config import HIAPP_DIR
from .core.http import DEFAULT_HEADERS

CATALOG_URL = "https://raw.githubusercontent.com/Triplex3x-cyver/hiapp-addons/main/addons.json"
ADDONS_DIR = HIAPP_DIR / "addons"


def _fetch_catalog() -> dict:
    """Descarga el catálogo addons.json desde GitHub."""
    print("📡 Obteniendo catálogo de add-ons...")
    try:
        response = requests.get(CATALOG_URL, headers=DEFAULT_HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error al conectar con el catálogo: {e}")
        return {}


def list_addons():
    """Muestra los add-ons instalados actualmente."""
    ADDONS_DIR.mkdir(parents=True, exist_ok=True)

    print("🧩 Add-ons instalados:")
    count = 0
    for entry in ADDONS_DIR.iterdir():
        if entry.is_dir() and (entry / "addon.json").exists():
            with open(entry / "addon.json", "r", encoding="utf-8") as f:
                meta = json.load(f)
            print(f"  - {meta.get('name')} (v{meta.get('version')}): {meta.get('description')}")
            count += 1

    if count == 0:
        print("  (Ninguno)")


def install_addon(name: str):
    """Descarga, verifica e instala un add-on desde el catálogo."""
    catalog = _fetch_catalog()
    if not catalog:
        return

    target = next((a for a in catalog.get("addons", []) if a["name"] == name), None)
    if not target:
        print(f"❌ Add-on '{name}' no encontrado en el catálogo.")
        return

    if target.get("free") is False:
        print(f"💳 El add-on '{name}' es de pago. Visita la web para adquirirlo.")
        return

    dest_dir = ADDONS_DIR / name
    if dest_dir.exists():
        print(f"⚠️  El add-on '{name}' ya está instalado.")
        return

    print(f"📥 Descargando {name} v{target['version']}...")
    zip_path = HIAPP_DIR / f"{name}.zip"

    try:
        # 1. Descargar con requests y el User-Agent de Hiapp
        with requests.get(
                target["download_url"], headers=DEFAULT_HEADERS, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # 2. Verificar SHA256 (Seguridad)
        print("🔒 Verificando integridad del archivo...")
        sha256_hash = hashlib.sha256()
        with open(zip_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        file_hash = sha256_hash.hexdigest()
        expected_hash = target.get("sha256", "").strip()

        if expected_hash and file_hash != expected_hash:
            zip_path.unlink()
            raise ValueError(
                "El hash SHA256 no coincide. El archivo podría estar corrupto o alterado.")

        # 3. Descomprimir
        print("📦 Instalando...")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(ADDONS_DIR)

        print(f"✅ Add-on '{name}' instalado correctamente en {dest_dir}")
        print("   Reinicia Hiapp para cargarlo.")

    except Exception as e:
        print(f"❌ Error durante la instalación: {e}")
    finally:
        if zip_path.exists():
            zip_path.unlink()  # Limpiar el ZIP descargado


def remove_addon(name: str):
    """Elimina un add-on instalado."""
    dest_dir = ADDONS_DIR / name
    if not dest_dir.exists():
        print(f"❌ El add-on '{name}' no está instalado.")
        return

    confirm = input(f"¿Estás seguro de que quieres eliminar '{name}'? [s/N]: ").strip().lower()
    if confirm == "s":
        shutil.rmtree(dest_dir)
        print(f"✅ Add-on '{name}' eliminado.")
    else:
        print("❌ Cancelado.")
