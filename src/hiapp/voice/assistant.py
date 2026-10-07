# -*- coding: utf-8 -*-

import os
import time
import zipfile
import tarfile
from hashlib import md5
from pathlib import Path

import requests

from ..core.config import save_config
from ..core.downloader import download_file

try:
    from vosk_termux import MODEL_PRE_URL
except ImportError:
    try:
        from vosk import MODEL_PRE_URL
    except ImportError:
        print("⚠️ Instala vosk-termux (Termux) o vosk (otros)")


def setup_voice_model(config: dict) -> dict:
    """Asistente de primer inicio para configurar el modelo de voz."""
    print("Bienvenido a Hiapp, vamos a configurar el modelo de voz.")
    print("=" * 60)
    time.sleep(2)

    MODELS_DIR = Path(config["models_dir"])
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    BASE_URL = MODEL_PRE_URL
    url_list = BASE_URL + "model-list.json"
    model_name = None
    model_hash = None
    model_size = 0

    # 1(a). Buscar si ya hay metadatos de una descarga anterior
    meta_files = [
        f for f in os.listdir(MODELS_DIR) if f.lower().endswith(".meta")
    ]
    if meta_files:

        # Elegir el más reciente por fecha de modificación
        meta_files.sort(
            key=lambda f: os.path.getmtime(MODELS_DIR / f),
            reverse=True,
        )
        chosen = meta_files[0]

        # Limpiar los demás (huérfanos)
        for extra in meta_files[1:]:
            (MODELS_DIR / extra).unlink(missing_ok=True)

        # Declarar model_name
        #
        model_name = chosen.split(".zip")[0]

        # Obtener los metadatos locales (si los hay)
        url = f"{BASE_URL}{model_name}.zip"
        meta_data = download_file(
            url, MODELS_DIR, get_meta_only=True)

        model_hash = meta_data.get("md5")
        model_size = meta_data.get("total_size", 0)

    # 1(b). Obtener metadatos del servidor
    else:

        # Buscar el modelo en la lista de Vosk
        while True:
            try:
                response = requests.get(url_list, timeout=10)
                models = response.json()
                # Filtrar por idiomas de tipo "small"
                langs = {}
                for model in models:
                    if model.get("lang") and model.get("lang") not in langs:
                        langs[model["lang"]] = model
                lang_list = sorted(langs.keys())

                print("\nIdiomas disponibles:\n")
                for i, lang in enumerate(lang_list, 1):
                    print(f"  {i:2}. {lang}")
                break
            except Exception as e:
                print(f"\n⚠️  No se pudo obtener la lista de idiomas: {e}\n")
                lang_list = []
                models = {}
                retry = input(
                    "¿Intentar de nuevo? [s/N] [s]: ").strip().lower() or "s"
                if retry != "s":
                    return None

    # 2. Obtener idioma
    if not model_name:
        while True:
            if lang_list:
                lang = input(
                    "\nElige un idioma (número o código) [es]: ").strip() or "es"

                # Si elige un número, obtener el código
                if lang.isdigit() and 1 <= int(lang) <= len(lang_list):
                    lang_code = lang_list[int(lang) - 1]
                else:
                    lang_code = lang
            else:
                lang_code = input(
                    "Escribe el código de idioma "
                    + "('en' para inglés; 'fr' para francés ...) [es]: "
                ).strip() or "es"

            # Declarar model_name
            #
            # Filtrar por idioma y tipo "small"
            for model in models:
                if model["lang"] == lang_code and model["type"] == "small":
                    if model.get("obsolete") == "false":
                        model_name = model["name"]
                        model_hash = model.get("md5")
                        model_size = model["size"]
                        break

            if not model_name:
                print(f"❌ No se encontró un modelo para el idioma '{lang_code}'.")
                # El usuario vió la lista de idiomas, puede ser un error de teclado.
                retry = input(
                    "Pudo ser un error al escribir. ¿Elegir el idioma nuevamente? [s/N] [n]: ").strip().lower() or "n"
                if retry != "s":
                    return None
                continue
            break

        # Guardar el código de lenguaje para no pedirlo si se retoma una descarga
        config["lang"] = lang_code
        save_config(config)
    else:
        # Ya estaba guardado
        lang_code = config["lang"]

    # 3. Definir rutas
    print(f"\n⏳ Preparando enlace para modelo '{lang_code}'...")
    time.sleep(2)
    model_path = MODELS_DIR / model_name
    zip_path = Path(f"{model_path}.zip")

    while True:
        # 4. Descargar (reanudable en el bucle)
        print(f"\n📥 Descargando modelo '{model_name}'...")
        time.sleep(2)
        try:
            url = f"{BASE_URL}{model_name}.zip"
            if meta_files:
                download_file(url, MODELS_DIR)
            else:
                download_file(
                    url, MODELS_DIR, add_meta={"md5": model_hash})
        except KeyboardInterrupt:
            # El usuario detuvo la descarga
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            retry = input("¿Intentar descarga de nuevo? [s/N]: ").strip().lower() or "s"
            if retry != "s":
                return None
            continue
        break

    # 5. Descomprimir y limpiar
    if zip_path.exists():
        # Integridad
        passed = False
        #
        # Comparar md5
        if model_hash:
            h = md5()
            with open(zip_path, "rb") as fh:
                while chunk := fh.read(8192):  # 8Kb
                    h.update(chunk)
                zip_hash = h.hexdigest()

            if model_hash == zip_hash:
                passed = True
            else:
                err = f"⚠️  Hash inesperado: {zip_hash} vs {model_hash} ✅ "
        #
        # Comparar tamaño
        else:
            downloaded = zip_path.stat().st_size
            if model_size == downloaded:
                passed = True
            else:
                err = f"⚠️  Tamaño inesperado: {downloaded} vs {model_size} ✅ "
        #
        if passed:
                print("✅ Integridad verificada")
        else:
            print("❌ El archivo está corrupto")
            print(err)
            zip_path.unlink()
            return None

        print("📦 Descomprimiendo...")
        time.sleep(2)
        #
        if zip_path.suffix == ".zip":
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(MODELS_DIR)
        #
        elif zip_path.name.endswith(".tar.gz"):
            with tarfile.open(zip_path, "r:gz") as t:
                t.extractall(MODELS_DIR, filter="data")
        #
        zip_path.unlink()
    else:
        print("❌  No se encontró el archivo descargado, es un error raro")
        print(zip_path)
        return None

    # 6. Guardar el nombre del modelo de idioma
    config["lang_model_name"] = model_name
    save_config(config)

    # 7. Informar al usuario
    print(f"\n✅ Modelo listo en {model_path}")
    return config
