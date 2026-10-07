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

from .core.config import get_lan_ip, load_config, save_config
from .core.i18n import translate


def _start_server_thread(config):
    """
    Levanta el servidor Flask en un hilo daemon
    y devuelve el hilo.
    """
    from .server.app import create_app, _silence_flask_banner

    # Silenciar el banner antes de crear la app
    _silence_flask_banner()

    app = create_app()
    host = config.get("host", "0.0.0.0")
    port = config.get("port", 5000)

    def run():
        app.run(host=host, port=port, threaded=True, use_reloader=False)

    thread = threading.Thread(target=run, name="hiapp-server", daemon=True)
    thread.start()
    return thread


def _print_server_urls(lan_ip, port, lang):
    if lan_ip == "127.0.0.1":
        # Modo solo-local
        print(translate("server_local_only", lang=lang, port=port))
        print(translate("server_local_hint", lang=lang))
    else:
        print(translate("server_running", lang=lang, ip=lan_ip, port=port))
        print(translate("game_running", lang=lang, ip=lan_ip, port=port))
    print()


def main():
    # --- 1. Configuración -----------
    config = load_config()
    lang = config.get("lang")

    # --- 2. Asistente de primer inicio -----------
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

    # --- 3. Datos de red para el usuario -----------
    lan_ip = get_lan_ip()
    port = config.get("port", 5000)
    _print_server_urls(lan_ip, port, lang)  # No afecta a check_status en voice/controller.py

    # --- 4. Levantar servidor Flask (hilo daemon) -----------
    _start_server_thread(config)

    print("\n", translate("server_running", lang=lang, ip=lan_ip, port=port))
    print(translate("game_running", lang=lang, ip=lan_ip, port=port))
    print()

    # --- 5. Levantar asistente de voz (hilo principal) -----------
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
