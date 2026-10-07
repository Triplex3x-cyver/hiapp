# Changelog

Todos los cambios importantes de este proyecto se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto sigue [Versionado Semántico](https://semver.org/lang/es/).

---

## [Sin publicar]

### En desarrollo
- [ ] Compatibilidad con Windows.
- Módulos premium (`hiapp-pro`).
  - [ ] Soporte para cámaras IP.
  - [ ] Integración con alarmas y sensores.
  - [ ] Bot de Telegram para grupos de juego (cacerías, etc.).

---

## [0.0.1] - 2026-09-19

### Añadido
- **Servidor HTTP** con soporte de peticiones de rango (`Range Requests`), compatible con PPSSPP.
- **Control por voz** con wake word fija `"Catarsis"`.
- **Comando `hiapp-voice`** para iniciar el asistente de voz.
- **Comando `hiapp-server`** para iniciar solo el servidor de juegos.
- **Comando `hiapp-config`** para gestionar la configuración:
  - `list`: muestra toda la configuración actual.
  - `get <clave>`: muestra un valor específico.
  - `set <clave> <valor>`: establece un valor.
  - `reset <clave>`: restablece un valor a su valor por defecto.
  - `reset --all`: restablece toda la configuración.
- **Descarga automática de modelos de voz** desde Vosk Models.
- **Descarga reanudable** con soporte de `Range` para conexiones inestables.
- **Configuración persistente** en `~/.hiapp/config.json`.
- **Modelos guardados** en `~/.hiapp/models/` por defecto.
- **Variables de entorno** para usuarios avanzados:
  - `HIAPP_PORT`
  - `HIAPP_HOST`
  - `HIAPP_GAMES_DIR`
  - `HIAPP_MODELS_DIR`
  - `HIAPP_LANG`
- **Documentación bilingüe** (español e inglés).
- **Soporte inicial** para Termux y Linux (el servidor HTTP funciona en Windows).

### Notas
- La palabra de activación `"Catarsis"` es **fija** y no se puede desactivar. Esto evita falsos positivos y mantiene una identidad clara del asistente.
- En el futuro se podrán añadir **aliases** adicionales para otros idiomas.

---

## Formato de versiones

- **MAJOR**: cambios incompatibles con versiones anteriores.
- **MINOR**: nuevas funcionalidades compatibles.
- **PATCH**: corrección de errores compatible.

Ejemplo: `0.0.1` → `0.0.2` (parche), `0.0.2` → `0.1.0` (nueva funcionalidad), `0.1.0` → `1.0.0` (versión estable).

---

Última actualización: 19 de Septiembre de 2026
