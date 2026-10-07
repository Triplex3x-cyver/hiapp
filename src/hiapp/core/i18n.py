"""
Sistema de internacionalización (i18n) de Hiapp.

Uso:
    from .core.i18n import translate
    print(translate("welcome", lang="es"))
"""

MESSAGES = {
    "es": {
        # Inicio
        "welcome":                "Bienvenido a Hiapp",
        "choose_lang":            "Elige tu idioma",
        "downloading":            "📥 Descargando modelo '{name}'...",
        "resuming":               "⏩ Reanudando descarga desde el byte {n}",
        "extracting":             "📦 Descomprimiendo...",
        "ready":                  "✅ Modelo listo en {path}",
        "server_local_only":   "⚠️  Servidor en http://127.0.0.1:{port}/ (solo este dispositivo)",
        "server_local_hint":   "   Para acceder desde otro dispositivo, conéctate a una red WiFi.",
        "game_local_only":     "🎮 Juegos en http://127.0.0.1:{port}/game/ (solo este dispositivo)",
        "server_running":         "🌐 Servidor en http://{ip}:{port}/",
        "game_running":           "🎮 Juegos en http://{ip}:{port}/game/",
        "loading_lang_model":     "🧠 Cargando modelo Vosk {name}...",
        "goodbye":                "👋 ¡Hasta pronto!",
        # ... más mensajes

        # Voz
        "voice_init":             "🎙️  Asistente inicializado de forma limpia.",
        "voice_games_dir":        "📂 Directorio de juegos activo: {path}",
        "voice_say_wake":         "🎤 Di '{wake}' para activar los comandos de voz...",
        "voice_heard":            "🗣️  Escuchado: {text}",
        "voice_activated":        "🔓 Asistente activado. Di tu comando ({seconds}s).",
        "voice_analyzing":        "✨ Analizando comando...",
        "voice_ask":              "❓ Dime un comando. Di 'Catarsis ayuda' para ver las opciones.",
        "voice_unknown":          "❓ Comando no reconocido. Di 'Catarsis ayuda' para ver las opciones.",
        "voice_help_title":       "📋 --- Comandos Disponibles ---",
        "voice_help_prefix":      "Prefijo: Catarsis, o un alias",
        "voice_help_status":      "  -> 'Catarsis estado'",
        "voice_help_help":        "  -> 'Catarsis ayuda'",

        # Estado
        "status_title":           "📊 [Estado de Hiapp]",
        "status_server":          "   Servidor:   {url}",
        "status_games":           "   Juegos:     {url}",
        "status_dir":             "   Directorio: {path}",
        "status_model":           "   Modelo:     {model}",

        # Configuración
        "config_title":           "🔧 Configuración actual de Hiapp",
        "config_unknown_key":     "❌ Clave desconocida: {text}",
        "config_valid_keys":      "   Claves válidas: {valid}",
        "config_applang_warn":    "⚠️  '{text}' es una clave gestionada por la app."+"\n"
            + "    Reconfigura el modelo de voz para cambiarla, ejecuta:"+"\n"
            + "      hiapp-config reset lang-model-name"+"\n"
            + "    Luego reinicia Hiapp.",
        "config_appstat_warn":    "⚠️  '{text}' es una clave de estado de la app."+"\n"
            + "   Si la reseteas, Hiapp volverá a pedir la descarga del modelo.",
        "config_nan_err":         "❌ '{value}' no es un número válido para '{text}'",
        "config_reset_ok":        "✅ Configuración de usuario restablecida.",
        "config_nokey_err":       "❌ Especifica una clave o usa --all",
        # CMD
        "cmd_parser_desc":        "Gestiona la configuración de Hiapp.",
        "cmd_list_help":          "Muestra toda la configuración",
        "cmd_get_help":           "Muestra un valor",
        "cmd_set_help":           "Establece un valor",
        "cmd_setvalue_help":      "Valor (varios para listas)",
        "cmd_reset_help":         "Restablece un valor",
        "cmd_resetkey_help":      "Clave a restablecer",
        "cmd_resetall_help":          "Restablecer toda la configuración de usuario",

        # Otros
        "canceled":               "❌ Cancelado",
    },

    "en": {
        # Start
        "welcome":                "Welcome to Hiapp",
        "choose_lang":            "Choose your language",
        "downloading":            "📥 Downloading model '{name}'...",
        "resuming":               "⏩ Resuming download from byte {n}",
        "extracting":             "📦 Extracting...",
        "ready":                  "✅ Model ready at {path}",
        "server_local_only":   "⚠️  Server at http://127.0.0.1:{port}/ (this device only)",
        "server_local_hint":   "   To access from another device, connect to a WiFi network.",
        "game_local_only":     "🎮 Games at http://127.0.0.1:{port}/game/ (this device only)",
        "server_running":         "🌐 Server at http://{ip}:{port}/",
        "game_running":           "🎮 Games at http://{ip}:{port}/game/",
        "loading_lang_model":     "🧠 Loading Vosk model {name}...",
        "goodbye":                "👋 Goodbye!",
        # ... more messages

        # Voice
        "voice_init":             "🎙️  Assistant initialized cleanly.",
        "voice_games_dir":        "📂 Active games directory: {path}",
        "voice_say_wake":         "🎤 Say '{wake}' to activate voice commands...",
        "voice_heard":            "🗣️  Heard: {text}",
        "voice_activated":        "🔓 Assistant activated. Say your command ({seconds}s).",
        "voice_analyzing":        "✨ Analyzing command...",
        "voice_ask":              "❓ Say a command. Say 'Catarsis help' to see options.",
        "voice_unknown":          "❓ Command not recognized. Say 'Catarsis help' to see options.",
        "voice_help_title":       "📋 --- Available Commands ---",
        "voice_help_prefix":      "Prefix: Catarsis, or an alias",
        "voice_help_status":      "  -> 'Catarsis status'",
        "voice_help_help":        "  -> 'Catarsis help'",

        # Status
        "status_title":           "📊 [Hiapp Status]",
        "status_server":          "   Server:     {url}",
        "status_games":           "   Games:      {url}",
        "status_dir":             "   Directory:  {path}",
        "status_model":           "   Model:      {model}",

        # Configuration
        "config_title":           "🔧 Current Hiapp configuration",
        "config_unknown_key":     "❌ Unknown key: {text}",
        "config_valid_keys":      "   Valid keys: {valid}",
        "config_applang_warn":    "⚠️  '{text}' is an app-managed key.\n"
            + "    To change it, reconfigure the voice model:\n"
            + "      hiapp-config reset lang-model-name\n"
            + "    Then restart Hiapp.",
        "config_appstat_warn":    "⚠️  '{text}' is an app-state key.\n"
            + "   Resetting it will make Hiapp ask to download the model again.",
        "config_nan_err":         "❌ '{value}' is not a valid number for '{text}'",
        "config_reset_ok":        "✅ User configuration reset.",
        "config_nokey_err":       "❌ Specify a key or use --all",

        # CMD
        "cmd_parser_desc":        "Manage Hiapp configuration.",
        "cmd_list_help":          "Show full configuration",
        "cmd_get_help":           "Show a value",
        "cmd_set_help":           "Set a value",
        "cmd_setvalue_help":      "Value (several for lists)",
        "cmd_reset_help":         "Reset a value",
        "cmd_resetkey_help":      "Key to reset",
        "cmd_resetall_help":      "Reset all user configuration",

        # Others
        "canceled":               "❌ Canceled",
        
    },
}


def translate(key: str, lang: str = "es", **kwargs) -> str:
    """Traduce una clave al idioma indicado.
    Args:
        key: clave de mensaje o comando.
        lang: código de idioma de dos letras.
        kwargs: otras claves útiles.
    Si la clave no existe, devuelve un aviso visible.
    """
    translations = MESSAGES.get(lang, MESSAGES["es"])

    if key not in translations:
        return f"[{key}] Sin traducción disponible. No translation available."  # marcador visible: traducción faltante

    text = translations[key]
    try:
        return text.format(**kwargs)
    except (KeyError, IndexError):
        # La clave existe pero falta alguna variable en kwargs
        return text
