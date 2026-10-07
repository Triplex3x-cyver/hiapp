
"""
Comando `hiapp-config`: gestiona la configuración de Hiapp.

Reglas:
    - USER_DEFAULTS se pueden leer, escribir y resetear.
    - APP_DEFAULTS solo se leen. Para cambiar lang/lang_model_name,
      se usa el flujo de reconfiguración (reset lang_model_name + reinicio).
    - `reset --all` solo afecta a USER_DEFAULTS.

Modo interactivo:
hiapp-config list
hiapp-config get port
hiapp-config set port 8080
hiapp-config get port
hiapp-config reset port
hiapp-config get port

hiapp-config get models-dir
hiapp-config set models-dir /storage/XXXX-XXXX/models
hiapp-config get models-dir
hiapp-config reset models-dir
hiapp-config get models-dir
hiapp-config list
"""

# 🔧 Configuración de Hiapp
# ------------------------------
import sys
import argparse

from .core.config import (
    ALL_DEFAULTS,
    APP_DEFAULTS,
    USER_DEFAULTS,
    load_config,
    save_config,
)
from .core.i18n import translate

# Traducir guiones (CLI) a guiones bajos (interno)
CLI_TO_INTERNAL = {k.replace("_", "-"): k for k in ALL_DEFAULTS}
config = load_config()


def _resolve_key(key: str) -> str:
    """Convierte 'models-dir' → 'models_dir'. Deja pasar claves ya válidas."""
    return CLI_TO_INTERNAL.get(key, key)


def _is_app_key(key: str) -> bool:
    """¿Es una clave gestionada por la app (no libremente editable)?"""
    return key in APP_DEFAULTS


# --- Comandos -----------
def cmd_list(args):
    print(translate("config_title", config.get("lang")))
    print("=" * 40)
    for key, value in config.items():
        marca = "  [app]" if _is_app_key(key) else ""
        print(f"  {key:18} = {value}{marca}")


def cmd_get(args):
    key = _resolve_key(args.key)
    if key not in ALL_DEFAULTS:
        print(translate("config_unknown_key", config.get("lang"), text=key))
        print(translate(
            "config_valid_keys", config.get("lang"), valid=", ".join(CLI_TO_INTERNAL.keys())))
        sys.exit(1)

    print(config.get(key))


def cmd_set(args):
    global config
    key = _resolve_key(args.key)

    if key not in USER_DEFAULTS:
        if _is_app_key(key):
            print(translate("config_applang_warn", config.get("lang"), text=key))
        else:
            print(translate("config_unknown_key", config.get("lang"), text=key))
            print(translate(
                "config_valid_keys", config.get("lang"), valid=", ".join(CLI_TO_INTERNAL.keys())))
        sys.exit(1)

    # Unir todos los argumentos en un solo string
    raw_value = " ".join(args.value)

    # Convertir tipo si el valor por defecto es int
    if isinstance(USER_DEFAULTS[key], int):
        try:
            value = int(raw_value)
        except ValueError:
            print(translate(
                "config_nan_err", config.get("lang"), value=raw_value, text=key))
            sys.exit(1)

    elif isinstance(USER_DEFAULTS[key], list):
        # Para listas (aliases), separar por comas
        value = [v.strip() for v in raw_value.split(",") if v.strip()]
    else:
        value = raw_value

    config[key] = value
    save_config(config)
    print(f"✅ {key} = {value}")


def cmd_reset(args):
    global config

    # Caso especial: reset --all
    if args.all:
        #
        # Solo resetear las configurables
        for key in USER_DEFAULTS:
            config[key] = USER_DEFAULTS[key]
        save_config(config)
        print(translate("config_reset_ok", config.get("lang")))
        return

    if not args.key:
        print(translate("config_nokey_err", config.get("lang")))
        print(translate(
                "config_valid_keys", config.get("lang"), valid=", ".join(CLI_TO_INTERNAL.keys())+", --all"))
        sys.exit(1)

    key = _resolve_key(args.key)

    # RESET LANG
    if key == "lang":
        print(translate("config_applang_warn", config.get("lang"), text=key))
        sys.exit(1)
    #
    # Claves de APP (excepto lang, ya bloqueada arriba)
    if _is_app_key(key):
        print(translate("config_appstat_warn", config.get("lang"), text=key))
        confirm = input("¿Continuar? [s/N]: ").strip().lower()
        if confirm != "s":
            print(translate("canceled", config.get("lang")))
            return

        config[key] = APP_DEFAULTS[key]
        save_config(config)
        print(f"✅ {key} = {config[key]}")
        return

    if key not in ALL_DEFAULTS:
        print(translate("config_unknown_key", config.get("lang"), text=key))
        print(translate(
            "config_valid_keys", config.get("lang"), valid=", ".join(CLI_TO_INTERNAL.keys())+", --all"))
        sys.exit(1)

    # Ejecutar reset en clave de usuario
    config[key] = USER_DEFAULTS[key]
    save_config(config)
    print(f"✅ {key} = {USER_DEFAULTS[key]}")


# --- Punto de entrada -----------
def main():
    parser = argparse.ArgumentParser(
        prog="hiapp-config",
        description=translate("cmd_parser_desc", config.get("lang"))
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help=translate("cmd_list_help", config.get("lang")))

    p_get = subparsers.add_parser("get", help=translate("cmd_get_help", config.get("lang")))
    p_get.add_argument("key")


    p_set = subparsers.add_parser("set", help=translate("cmd_set_help", config.get("lang")))
    p_set.add_argument("key")
    # p_set.add_argument("value", help="Valor (para listas, separar por comas a,b,c)")
    p_set.add_argument(
        "value", nargs="+", help=translate("cmd_setvalue_help", config.get("lang")))

    p_reset = subparsers.add_parser("reset", help=translate("cmd_reset_help", config.get("lang")))
    p_reset.add_argument("key", nargs="?", help=translate("cmd_resetkey_help", config.get("lang")))
    p_reset.add_argument("--all", action="store_true",
                     help=translate("cmd_resetall_help", config.get("lang")))

    args = parser.parse_args()

    # Dispatch
    if args.command == "list":
        cmd_list(args)
    elif args.command == "get":
        cmd_get(args)
    elif args.command == "set":
        cmd_set(args)
    elif args.command == "reset":
        cmd_reset(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
