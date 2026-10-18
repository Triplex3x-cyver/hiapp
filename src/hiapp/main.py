"""
Orquestador principal de Hiapp.

Este módulo arranca todos los subsistemas y los mantiene corriendo
hasta que el usuario interrumpe con Ctrl+C.

Flujo:
    1. Carga la configuración.
    2. Si no hay modelo de voz configurado, lanza el asistente de primer inicio.
    3. Guarda la configuración (si hubo cambios).
    4. Levanta Flask en un hilo daemon (el servidor siempre está activo).
    5. Levanta el asistente de voz en el hilo principal (bloquea hasta Ctrl+C).
    6. Cierre limpio con os._exit(0).
"""

import os
import sys
import time
import threading

# from .core.config import get_lan_ip
from .core.config import load_config, save_config
from .core.i18n import translate

# Importar las funciones del CLI de addons
from .addons_cli import list_addons, install_addon, remove_addon


def _start_server_thread(config):
    """
    Levanta el servidor Flask en un hilo daemon
    y devuelve el hilo.
    En el futuro se usaría waitress.
    """
    # from .server.app import serve (para el futuro)
    from .server.app import create_app, _configure_logging

    # Silenciar el banner antes de crear la app
    _configure_logging()

    app = create_app()
    host = config.get("host", "0.0.0.0")
    port = config.get("port", 5000)

    def run():
        # serve(app, host=host, port=port, threads=8)
        app.run(host=host, port=port, threaded=True, use_reloader=False)

    thread = threading.Thread(target=run, name="hiapp-server", daemon=True)
    thread.start()
    return thread


def main():
    # --- 1. Manejo de comandos CLI (hiapp install, list, remove) -----------
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            list_addons()
            sys.exit(0)

        elif command == "install":
            if len(sys.argv) < 3:
                print("❌ Falta el nombre del add-on. Uso: hiapp install <nombre>")
                sys.exit(1)
            install_addon(sys.argv[2])
            sys.exit(0)

        elif command == "remove":
            if len(sys.argv) < 3:
                print("❌ Falta el nombre del add-on. Uso: hiapp remove <nombre>")
                sys.exit(1)
            remove_addon(sys.argv[2])
            sys.exit(0)

        else:
            print(f"❌ Comando desconocido: '{command}'")
            print("   Comandos disponibles: install, list, remove")
            sys.exit(1)
    # Si no hay argumentos, arrancar el asistente normal

    # --- 2. Configuración -----------
    config = load_config()
    lang = config.get("lang")

    # --- 3. Asistente de primer inicio -----------
    if not config.get("lang_model_name"):
        # Importación diferida: solo se carga si hace falta
        from .voice.assistant import setup_voice_model

        config = setup_voice_model(config)
        if not config:
            print(translate("goodbye", lang=lang or "es"))
            sys.exit(1)

        # Guardar los cambios (idioma, nombre del modelo)
        save_config(config)
        lang = config.get("lang")

    # --- 4. Datos de red para el usuario -----------
    # lan_ip = get_lan_ip()
    # port = config.get("port", 5000)
    # _print_server_urls(lan_ip, port, lang)  # No afecta a check_status en voice/controller.py

    # --- 5. Levantar servidor Flask (hilo daemon) -----------
    _start_server_thread(config)

    # --- 6. Levantar asistente de voz (hilo principal) -----------
    from .voice.controller import VoiceAssistant

    assistant = VoiceAssistant()
    try:
        assistant.start_listening()  # bloquea hasta Ctrl+C
    except KeyboardInterrupt:
        print()
        print(translate("goodbye", lang=lang))
        assistant.stop()          # marca is_listening=False
        time.sleep(0.5)           # deja al hilo de audio cerrar su stream

        # os._exit(0) evita que portaudio/atexit cuelguen el proceso
        os._exit(0)


if __name__ == "__main__":
    # Punto de entrada para el comando 'hiapp' de la consola
    main()
