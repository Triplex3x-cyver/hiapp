"""
Registro de comandos de voz de Hiapp.

Los comandos se recogen de dos fuentes:
    - El núcleo: estado, ayuda.
    - Los add-ons: cada uno declara los suyos en su addon.json.

Con todos los comandos + la wake word, se construye una gramática JSON
que se pasa a Vosk para restringir el reconocimiento.

Beneficios de la gramática:
    - Menos falsos positivos (de ~50% a ~100% de precisión).
    - Menos uso de CPU (espacio de búsqueda reducido).
    - Misma velocidad que un modelo "small".
"""

import json


# Comandos del núcleo por idioma
CORE_COMMANDS = {
    "es": {
        "status": ("estado", "estatus"),
        "help":   ("ayuda", "aiuda", "ayúa"),
    },
    "en": {
        "status": ("status", "state"),
        "help":   ("help",),
    },
}


class CommandRegistry:
    """
    Recoge comandos del núcleo y de los add-ons, y construye la gramática
    de Vosk para el idioma activo.

    Mapea frases exactas a intenciones para que el controlador sepa
    qué hacer cuando Vosk devuelve una transcripción.
    """

    def __init__(self):
        # {lang: {intent: [frases]}}
        self._by_intent = {}
        # {lang: {frase: intent}}
        self._phrase_to_intent = {}

    # --- Registro -----------

    def register_core(self):
        """Registra los comandos del núcleo (estado, ayuda)."""
        for lang, intents in CORE_COMMANDS.items():
            for intent, phrases in intents.items():
                self._register(lang, intent, phrases)

    def register_addon(self, manifest: dict):
        """
        Registra los comandos de un add-on a partir de su manifest
        (el diccionario cargado desde addon.json).

        El manifest debe exponer los comandos con esta estructura:
            "commands": {
                "es": {
                    "start": ["activar servidor de juegos"],
                    "stop":  ["desactivar servidor de juegos"]
                }
            }

        Las intenciones se registran con el prefijo del add-on:
            "ppsspp:start", "ppsspp:stop"
        """
        name = manifest.get("name", "addon")
        commands = manifest.get("commands", {})

        for lang, intents in commands.items():
            for intent, phrases in intents.items():
                full_intent = f"{name}:{intent}"
                self._register(lang, full_intent, phrases)

    def _register(self, lang: str, intent: str, phrases):
        """Añade frases a una intención en un idioma, evitando duplicados."""
        self._by_intent.setdefault(lang, {})
        self._by_intent[lang].setdefault(intent, [])

        self._phrase_to_intent.setdefault(lang, {})

        for phrase in phrases:
            # Evitar duplicados
            if phrase not in self._by_intent[lang][intent]:
                self._by_intent[lang][intent].append(phrase)
            # Mapear frase → intención (el último gana si hay colisión)
            self._phrase_to_intent[lang][phrase] = intent

    # --- Gramática -----------

    def build_grammar(self, lang: str, wake_words: list) -> str:
        """
        Construye la gramática JSON para Vosk.
        Incluye la wake word, los comandos del idioma, y el token [unk].
        """
        phrases = set(wake_words)

        for phrases_list in self._by_intent.get(lang, {}).values():
            phrases.update(phrases_list)

        phrases.add("[unk]")
        return json.dumps(sorted(phrases))

    # --- Búsqueda de intención -----------

    def find_intent(self, text: str, lang: str) -> str | None:
        """
        Devuelve la intención cuyo comando aparece en el texto, o None.

        Con gramática activa, Vosk devuelve frases exactas. El fallback
        por substring está por si el modelo devuelve algo inesperado.
        """
        mapping = self._phrase_to_intent.get(lang, {})

        # 1. Coincidencia exacta
        if text in mapping:
            return mapping[text]

        # 2. Fallback: substring
        for phrase, intent in mapping.items():
            if phrase in text:
                return intent

        return None

    # --- Utilidades -----------

    def list_commands(self, lang: str) -> list:
        """Devuelve las frases registradas para un idioma."""
        phrases = []
        for phrases_list in self._by_intent.get(lang, {}).values():
            phrases.extend(phrases_list)
        return sorted(phrases)
