import os
import sys
import json
import time
import queue
import threading
# import subprocess
from pathlib import Path
import sounddevice as sd

try:
    import vosk_termux as vosk
except ImportError:
    try:
        import vosk
    except ImportError:
        print("⚠️ Instala vosk-termux (Termux) o vosk (otros)")
        sys.exit(1)

from ..core.config import load_config, get_lan_ip
from ..core.i18n import translate
from ..core.commands import CommandRegistry
from ..addons.ppsspp.paths import get_games_directory
from .assistant import setup_voice_model

# Segundos que el asistente permanece "despierto" tras la activación
WAKE_TIMEOUT = 6.0

# Frecuencia de muestreo requerida por Vosk
SAMPLE_RATE = 16000.0


class VoiceAssistant:
    def __init__(self):
        self.config = load_config()
        self.wake_word = "catarsis"
        # Wake word fija + aliases opcionales del config
        self.wake_words = [self.wake_word] + list(self.config.get("aliases", []))
        self.is_listening = True
        self.stream = None
        self.awake_until = 0.0
        self._wake_timer = None

        # Cola para transferir datos de audio desde el hilo de captura al de reconocimiento
        self.audio_queue = queue.Queue()

        # Cargar el modelo de Vosk
        model_path = str(Path(
            self.config.get("models_dir"),
            self.config.get("lang_model_name")))
        #
        print("\n", translate(
            "loading_lang_model", lang=self.config.get("lang"),
            name=self.config.get("lang_model_name")))
        self.model = vosk.Model(model_path)

        self.registry = CommandRegistry()
        self.registry.register_core()
        # Cuando haya add-ons con comandos:
        # for addon in discover_addons():
        #     self.registry.register_addon(addon.manifest)

        grammar = self.registry.build_grammar(self.config.get("lang", "es"), self.wake_words)
        #
        # Configuración estándar de audio a 16000Hz monocanal
        self.recognizer = vosk.KaldiRecognizer(self.model, SAMPLE_RATE, grammar)

    def _detect_wake_word(self, text: str) -> bool:
        """Devuelve True si el texto contiene la wake word o algún alias."""
        return any(w in text for w in self.wake_words)

    # --- Captura de audio -----------
    def _audio_callback(self):
        """Captura audio con sounddevice (compatible con Termux)."""
        def callback(indata, frames, time_info, status):
            if status:
                print(f"⚠️ {status}", file=sys.stderr)
            self.audio_queue.put(bytes(indata))

        try:
            self.stream = sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=callback,
            )
            self.stream.start()
            while self.is_listening:
                sd.sleep(100)  # bloquear el hilo sin CPU
        except Exception as e:
            print(f"❌ Error con el micrófono: {e}")
            self.is_listening = False

        finally:
            # Si ya estamos saliendo, no intentar cerrar
            # (evita deadlock con os._exit del hilo principal)
            # if self.is_listening is False:
            #    return

            # Cerrar el stream de audio explícitamente
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                print("Error al cerrar stream (interno):", e)

    # --- Control de tiempo de ventana -----------
    def _on_wake(self):
        """Activa la ventana de escucha y programa su cierre."""
        # Cancelar el timer anterior si existe
        if self._wake_timer is not None:
            self._wake_timer.cancel()

        was_asleep = time.time() >= self.awake_until
        self.awake_until = time.time() + WAKE_TIMEOUT

        # Mostrar mensaje solo si la ventana estaba cerrada
        # SONIDO
        if was_asleep:
            lang = self.config.get("lang", "es")
            print(translate("voice_activated", lang=lang, seconds=int(WAKE_TIMEOUT)))

        # Programar el cierre de la ventana
        self._wake_timer = threading.Timer(WAKE_TIMEOUT, self._on_wake_expire)
        self._wake_timer.daemon = True
        self._wake_timer.start()

    def _on_wake_expire(self):
        """Se ejecuta cuando la ventana de escucha se cierra."""
        print("🔐")
        # Futuro: reproducir un tono de audio aquí
        # Ejemplo: self._play_tone("lock.wav")

    # --- Bucle principal -----------
    def start_listening(self):
        lang = self.config.get("lang", "es")
        # games_dir = get_games_directory()  # self.config["games_dir"]
        # Wake word fija — no se puede desactivar
        WAKE_WORD = self.wake_word

        print(translate("voice_init", lang=lang))
        # print(translate("voice_games_dir", lang=lang, path=games_dir))
        print(translate("voice_say_wake", lang=lang, wake=WAKE_WORD.capitalize()))

        # Iniciar captura de micrófono en un hilo separado
        capture_thread = threading.Thread(target=self._audio_callback, daemon=True)
        capture_thread.start()

        # Bucle principal de reconocimiento
        while self.is_listening:
            data = self.audio_queue.get()
            if not self.recognizer.AcceptWaveform(data):
                continue

            result = json.loads(self.recognizer.Result())
            text = result.get("text", "").strip().lower()
            if not text:
                continue

            # 1. ¿Es la wake word o un alias?
            if self._detect_wake_word(text):
                print(translate("voice_heard", lang=lang, text=text.capitalize()))
                self._on_wake()
                continue

            # 2. ¿Estamos dentro de la ventana?
            if time.time() >= self.awake_until:
                continue

            # 3. Procesar comando y renovar la ventana
            self.handle_command(text)
            self._on_wake()

    # --- Manejo de comandos -----------
    def handle_command(self, text):
        lang = self.config.get("lang", "es")

        print(translate("voice_analyzing", lang=lang))

        # Quitar la wake word o alias y limpiar espacios
        for w in self.wake_words:
            text = text.replace(w, "")
        command = text.strip()

        if not command:
            print(translate("voice_ask", lang=lang))
            return

        # TRADUCIR COMANDOS (en cada add-on)
        '''

        # Comandos por orden de especificidad
        if command.startswith(("desactivar", "detener", "parar", "apagar")):
            pass  # uso futuro

        elif command.startswith(("activar", "iniciar", "arrancar", "encender")):
            pass  # uso futuro
        '''

        intent = self.registry.find_intent(command, lang)

        if intent == "status":
            self.check_status()
        elif intent == "help":
            self.show_help()  # CommandRegistry.list_commands(lang)
        elif intent is None:
            print(translate("voice_unknown", lang=lang))
        else:
            # Comando de add-on (futuro): dispatch al add-on correspondiente
            print(f"🔧 Comando de add-on: {intent}")

    def check_status(self):
        """Muestra el estado actual de Hiapp y sus add-ons."""
        lang = self.config.get("lang", "es")
        games_dir = get_games_directory()
        model = self.config.get("lang_model_name")
        # host = self.config.get("host", "0.0.0.0")
        host = get_lan_ip()
        port = self.config.get("port", 5000)

        print(translate("status_title", lang=lang))
        print(translate("status_server", lang=lang, url=f"http://{host}:{port}/"))
        print(translate("status_games", lang=lang, url=f"http://{host}:{port}/game/"))
        print(translate("status_dir", lang=lang, path=games_dir))
        print(translate("status_model", lang=lang, model=model))

    def show_help(self):
        """Muestra los comandos de voz disponibles."""
        lang = self.config.get("lang", "es")
        print("\n", translate("voice_help_title", lang=lang))
        print(translate("voice_help_prefix", lang=lang))
        print(translate("voice_help_status", lang=lang))
        print(translate("voice_help_help", lang=lang), "\n")

    def stop(self):
        """Señaliza detener el bucle de escucha."""
        self.is_listening = False


def main():
    # 1. Obtener configuración
    config = load_config()

    # 2. Si no hay modelo configurado, lanzar asistente
    if not config.get("lang_model_name"):
        config = setup_voice_model(config)  # También guarda cambios
        if not config:
            print("👋 Regresa pronto")
            sys.exit(1)

    # 3. Validar y cargar el modelo
    model_path = Path(config["models_dir"], config["lang_model_name"])
    if not model_path.exists():
        print(f"❌ No se encontró el modelo en: {model_path}")
        sys.exit(1)

    # 4. Exportar la ruta del modelo para Vosk
    os.environ["VOSK_MODEL_PATH"] = str(model_path)

    # ... iniciar bucle de escucha ...
    v_assistant = VoiceAssistant()
    try:
        v_assistant.start_listening()
    except KeyboardInterrupt:
        print("\n👋 Cerrando Hiapp de forma limpia...")
        v_assistant.is_listening = False
        v_assistant.stop()

        # Cerrar el stream de audio explícitamente
        if v_assistant.stream is not None:
            try:
                v_assistant.stream.stop()
                v_assistant.stream.close()
            except Exception as e:
                print("Error al cerrar stream (externo):", e)
        print("👋 ¡Hasta pronto!")
        os._exit(0)


if __name__ == "__main__":
    main()
