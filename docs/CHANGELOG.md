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
  - [ ] Bot de Telegram para grupos de juego (cacerías en grupo, etc.).

---

## [0.0.3] - 2026-10-17

### Corregido
- **PPSSPP (Streaming)**: Solucionados errores de compatibilidad con PPSSPP al solicitar archivos.
  - El problema base era que se solicitaba la ruta equivocada (sin el prefijo correcto) y con espacios sin codificar, lo que provocaba errores `400 Bad Request` y `308` (doble barra).
  - Ahora los nombres con espacios se codifican correctamente como `%20` en el catálogo.
- **PPSSPP (Rutas)**: Protección contra *path traversal* mejorada en el endpoint de streaming.

### Añadido
- Sección de **Comunidad** en los tres READMEs (Telegram, WhatsApp, GitHub Discussions).
- URL del sitio web oficial (`http://hiapp.mywebcommunity.org/`) en el `pyproject.toml` y los READMEs.
- El add-on de PPSSPP ahora es un paquete independiente (ver repo `hiapp-addons`).

## [0.0.2] - 2026-10-08

### Corregido
- **Empaquetado**: Incluidas las carpetas `templates/` y `static/` en las distribuciones. Antes, Flask lanzaba `TemplateNotFound: index.html` al acceder a la raíz (`/`).
- **Clasificadores**: Corregido el clasificador de Android (`Operating System :: Android` en lugar de `POSIX :: Android`, que no es válido).

### Añadido
- Comando `hiapp-config` con soporte para `list`, `get`, `set`, `reset` y `reset --all`.
- Soporte para alias de la palabra de activación (`hiapp-config set aliases "..."`).
- Carga del modelo de voz con verificación de integridad (MD5).

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
