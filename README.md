[![PyPI version](https://img.shields.io/pypi/v/hiapp.svg)](https://pypi.org/project/hiapp)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/hiapp?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=Downloads)](https://pepy.tech/projects/hiapp)

**🌐 Idiomas:** **Español** | [English](README_EN.md)

---

# Hiapp

> **H.I.A.P.P.** = **H**ogar con **I**nteligencia **A**rtificial **P**rivada **P**ersonal.

**Asistente de voz autogestionado para el hogar, con servidor de juegos para PPSSPP.**

Hiapp corre localmente y está diseñado para funcionar **sin internet**.
La voz, los datos y la lógica se procesan en el propio dispositivo.

---

## :sparkles: Características

- 🎤 **Wake Word local**: responde a la palabra de activación `"Catarsis"`.
- 🎮 **Servidor de videojuegos**: soporta peticiones de rangos (`Range Requests`), para **PPSSPP** y otros.
- 🔒 **Privacidad total**: nada sale de tu red local.
- ⚙️ **Configuración sencilla**: un solo comando para ajustar todo (`hiapp-config`).

---

## :construction: Estado del proyecto

Actualmente en fase **Alpha**. La versión `0.0.1` incluye:

- ✅ Servidor HTTP para videojuegos, con soporte de rangos.
- ✅ Control por voz con wake word `"Catarsis"`.
- ✅ Comando de configuración `hiapp-config`.
- 🚧 En desarrollo: soporte para cámaras IP, alarmas, bot de Telegram para grupos de juego, y más.
- 🚧 El objetivo inicial es Termux; se incluirá Windows más adelante.

---

## :inbox_tray: Instalación

### Requisitos

- **Termux** (Android) o **Linux**.
- **Python 3.10 o superior**.

### Comando

Termux
```bash
pip install hiapp[termux]
```

---

## :rocket: Primeros pasos

### 1. Iniciar Hiapp

```bash
hiapp
```

La primera vez, el asistente:

1. Pedirá **tu idioma** (ej. `es` para español, `en` para inglés).
2. Iniciará la descarga del modelo de voz correspondiente.
3. Mostrará el progreso de la descarga.

Permite **reanudarla** si se interrumpe: si vuelves a ejecutar el comando, continuará desde donde se quedó, así que no pierdes el progreso ni malgastas tu tarifa móvil.

Todos los datos se guardan en `~/.hiapp/`:

- `~/.hiapp/config.json` → Configuración del usuario.
- `~/.hiapp/models/`     → Modelos de voz descargados.

### 2. Iniciar solo el servidor (sin control por voz)

Útil para probar el servidor HTTP sin el asistente de voz:
```bash
hiapp-server
```

Por defecto, el servidor escucha en `0.0.0.0:5000`, es decir, todas las IP disponibles del dispositivo.

Para detenerlo, presiona `Ctrl+C`.

### 3. Configurar PPSSPP (si quieres jugar)

#### En el servidor

Averigua la IP local (en Termux):

```bash
termux-wifi-connectioninfo | grep ip
```

Ejemplo de salida: `"ip": "192.168.10.1",`

#### En PPSSPP

1. Ve a **Ajustes → Herramientas → Red / Ad-hoc**.
2. Activa el **servidor de red** y añade la URL:
   ```
   http://<IP-de-tu-servidor>:5000/game/
   ```
   Con el ejemplo anterior sería `http://192.168.10.1:5000/game/`.
3. Navega por los juegos disponibles. PPSSPP solicitará los fragmentos que necesite.

---

## :gear: Configuración

Hiapp usa un archivo de configuración en `~/.hiapp/config.json`.  
Puedes editarlo con el comando `hiapp-config set <clave> <valor>`.

### Ver la configuración actual

```bash
hiapp-config list
```

### Ver un valor específico

```bash
hiapp-config get port
```

### Establecer un valor

```bash
hiapp-config set games_dir /storage/XXXX-XXXX/PSP
hiapp-config set port 8080
```

### Restablecer un valor

```bash
hiapp-config reset port
hiapp-config reset --all
```

### Opciones disponibles

| Clave         | Valor por defecto  | Descripción                     |
|---------------|--------------------|---------------------------------|
| `models_dir`  | `~/.hiapp/models`  | Directorio de modelos de voz    |
| `games_dir`   | `~/PSP`            | Directorio de ISOs de PSP       |
| `port`        | `5000`             | Puerto del servidor HTTP        |
| `host`        | `0.0.0.0`          | Interfaz de red                 |
| `aliases`     | `[]`               | Aliases adicionales para activar Hiapp |

> [!NOTE]
> La palabra de activación **`"Catarsis"`** es fija y no se puede desactivar.
> Puedes añadir **aliases** adicionales con:
>
> `hiapp-config set aliases "oye hiapp"`

---

## :microphone: Control por voz

Una vez iniciado `hiapp`, di la palabra de activación y luego el comando:

| Comando           | Acción                              |
|-------------------|-------------------------------------|
| `"Catarsis"`      | Activa el asistente (wake word)     |
| `"Catarsis estado"` | Muestra el estado de Hiapp        |
| `"Catarsis ayuda"`  | Lista los comandos disponibles    |


> [!WARNING]
> El control por voz solo está disponible en Termux/Linux.
> En Windows, el servidor HTTP funciona, pero el módulo de voz aún no.

---

## :brain: Modelo de voz

Hiapp no incluye modelos de voz por defecto (ocupan mucho espacio).
Hiapp **descarga automáticamente** el modelo de voz la primera vez que ejecutes el asistente.

```bash
hiapp
```

> [!TIP]
> Si prefieres usar un modelo ya descargado en otra ubicación,
> o quieres que se descarguen ahí, usa el comando:
>
> ```bash
> hiapp-config set models_dir "ruta/al/modelo"
> ```
>
> El asistente usará esa ruta para buscar los modelos o descargarlos.

---

## :hammer_and_wrench: Solución de problemas

### El servidor no es accesible desde PPSSPP

1. Verifica que ambos dispositivos estén en la **misma red WiFi**.
2. Comprueba la IP del dispositivo que corre Hiapp: `termux-wifi-connectioninfo`.
3. Asegúrate de que el puerto no esté bloqueado por el firewall.
4. Prueba desde el navegador del dispositivo cliente: `http://<IP>:5000/game/`.

### La descarga del modelo se interrumpe

Vuelve a ejecutar `hiapp`. La descarga se reanudará automáticamente desde donde quedó.

### El micrófono no funciona

1. Otorga permisos al micrófono en Android.
2. Prueba con: `termux-microphone-record -d 3`.
3. Verifica que `sounddevice` esté instalado: `pip show sounddevice`.

---

## :handshake: Contribución

Consulta la [hoja de contribución](docs/CONTRIBUTING.md) para más detalles.

## :scroll: Licencia

Este proyecto se distribuye bajo la licencia *Apache-2.0*.
Consulta el archivo _LICENSE_ en fuente, o _licenses/LICENSE_ en rueda, para más detalles.
[Ver Licencia](LICENSE).

Traducción no oficial al español: [LICENSE_ES](LICENSE_ES).

---

## :pray: Agradecimientos

A los creadores de [Termux](https://termux.dev/), por hacer posible el sueño de miles de desarrolladores y entusiastas, como yo, de poder tener incluso una _IA_ en la casa.


A los desarrolladores de [Vosk](https://github.com/alphacep/vosk-api) —**Alpha Cephei Inc**— por contribuir al reconocimiento de voz sin conexión.


Al equipo de [PPSSPP](https://www.ppsspp.org/), por un emulador extraordinario que tanto he disfrutado, y su soporte de servidores de red.


A mi esposa Lili, por mucho.


Y a [DeepSeek](https://chat.deepseek.com/), que se integrará como soporte en línea para mis usuarios **PRO**.


Otros más serán añadidos...

---

Última actualización: 8 de Octubre de 2026

[Ir al inicio](#hiapp)
