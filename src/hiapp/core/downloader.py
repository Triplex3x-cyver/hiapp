import json
from pathlib import Path

import requests
from tqdm import tqdm


def download_file(url: str, dest_path: Path, add_meta: dict = {}, get_meta_only: bool = False):
    """
    Descarga un archivo con soporte de reanudación.

    Primero genera la ruta del archivo a guardar.
    Luego busca el archivo de metadatos correspondiente,
    si lo encuentra, carga el contenido y ejecuta los valores:
    {
      "accept_ranges": bool,
      "total_size": int,
      "md5": str
    }
    Intenta continuar una descarga previa.
    Si no, obtiene los metadatos con una solicitud HEAD,
    guarda el archivo de metadatos, por si se interrumpe la descarga.
    Al terminar elimina el archivo de metadatos.

    Args:
        url: URL del archivo a descargar.
        dest_path: Ruta donde guardar el archivo, sin nombre de archivo.
        add_meta: Al crear el archivo, inserta metadatos del llamador.
        get_meta_only: (False) Si True, solo retorna los metadatos o un dict vacío.
    """
    dest_path = Path(dest_path)
    dest_path.mkdir(parents=True, exist_ok=True)
    file_path = Path(dest_path, url.split("/")[-1])

    # Verificar si ya existe y está completo
    if file_path.exists():
        print(f"✅ El archivo ya existe: {file_path}")
        return file_path

    temp_path = file_path.with_suffix(file_path.suffix + ".part")

    # Intentar cargar metadatos desde la ruta
    meta_data = {}
    meta_data_file = Path(str(temp_path) + ".meta")
    if meta_data_file.exists():
        with open(meta_data_file, "r", encoding="utf-8") as f:
            meta_data = json.load(f)

    if get_meta_only:
        return meta_data

    if not meta_data_file.exists():
        # Verificar si el servidor soporta Range
        try:
            test = requests.get(
                url, headers={"Range": "bytes=0-0"},
                stream=True, allow_redirects=True,
                timeout=10
            )
            # Según el código de estado,
            # obtener el tamaño del archivo remoto
            if test.status_code == 206:
                meta_data["accept_ranges"] = True
                # Content-Range: bytes 0-0/<total_size>
                content_range = test.headers.get("Content-Range", "")
                if "/" in content_range:
                    meta_data["total_size"] = int(content_range.split("/")[-1])
            elif test.status_code == 200:
                meta_data["accept_ranges"] = False
                meta_data["total_size"] = int(test.headers.get("Content-Length", 0))

            else:
                # 403, 404, 500... no es un archivo válido
                test.raise_for_status()
            test.close()

            # Añadir metadatos del llamador
            if add_meta:
                meta_data.update(add_meta)

            if meta_data.get("accept_ranges"):
                # Crear archivo de metadatos para reanudación
                with open(meta_data_file, "w", encoding="utf-8") as f:
                    json.dump(meta_data, f, indent=2, ensure_ascii=False)

            else:
                print("⚠️  El servidor no soporta reanudación. Reiniciando descarga.")
        except requests.RequestException as e:
            print(f"⚠️  No se pudo verificar el archivo remoto: {e}")
            raise  # el llamador decide si reintentar

    # Si no hay metadatos, no recomiendo seguir

    accept_ranges = meta_data.get("accept_ranges")
    total_size = meta_data.get("total_size", 0)
    mode = "wb"
    headers = {}
    downloaded = 0
    if accept_ranges:
        # Si existe el archivo parcial, obtener el progreso.
        if temp_path.exists():
            downloaded = temp_path.stat().st_size
        mode = "ab"  # Añadir al final para continuar
        headers["Range"] = f"bytes={downloaded}-"
        print(f"⏩ Reanudando descarga desde el byte {downloaded}")
    else:
        print("⏩ Iniciando descarga desde cero")

    # Descargar
    try:
        with requests.get(url, headers=headers, stream=True, timeout=30) as r:
            r.raise_for_status()

            # Si hay Range: tamaño del rango solicitado
            # Si no hay: tamaño del archivo solicitado
            content_length = int(r.headers.get("Content-Length", 0))

            if total_size == 0:
                # Si hay <accept_ranges>:
                # - <Content-Length> es la longitud restante de <downloaded>.
                # Si no, es la longitud total del archivo.
                total_size = content_length + downloaded if accept_ranges else content_length

            with open(temp_path, mode) as f:
                # <desc> por sobre la barra, para pantalla estrecha
                print("\n", file_path.name, "_" * 30)
                with tqdm(
                    total=total_size,
                    initial=downloaded,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    miniters=1,
                ) as pbar:
                    # Aquí no se manejan los reintentos, solo el bucle de trozos
                    for chunk in r.iter_content(chunk_size=8192):  # 8Kb
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

    except KeyboardInterrupt:
        if accept_ranges:
            print("\n⏸️  Descarga interrumpida. Se reanudará la próxima vez.")
            print(f"   Progreso conservado en: {temp_path}")
        else:
            print("\n⏸️  Descarga interrumpida. No se podrá recuperar el progreso.")
        raise  # re-lanzar para que el llamador decida

    except Exception as e:
        print(f"❌ Error durante la descarga: {e}")
        print(f"   Progreso conservado en {temp_path}")
        print("   Vuelve a intentarlo y se reanudará desde donde quedó.")
        raise

    temp_path.rename(file_path)
    meta_data_file.unlink(missing_ok=True)
    print(f"✅ Descarga completada: {file_path}")
    return file_path
