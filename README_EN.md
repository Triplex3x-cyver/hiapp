[![PyPI version](https://img.shields.io/pypi/v/hiapp.svg)](https://pypi.org/project/hiapp)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/hiapp?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=Downloads)](https://pepy.tech/projects/hiapp)

**🌐 Languages:** [Español](README.md) | **English**

---

# Hiapp

> **H.I.A.P.P.** = **H**ome with **I**ntelligent **A**rtificial **P**rivate **P**ersonal Assistant.

**Self-hosted voice assistant for the home, with a game server for PPSSPP.**

Hiapp runs locally and is designed to work **without internet**.
Voice, data, and logic are processed on the device itself.

---

## :sparkles: Features

- 🎤 **Local Wake Word**: responds to the activation word `"Catarsis"`.
- 🎮 **Game server**: supports range requests (`Range Requests`) for **PPSSPP** and others.
- 🔒 **Total privacy**: nothing leaves your local network.
- ⚙️ **Simple configuration**: a single command to adjust everything (`hiapp-config`).

---

## :construction: Project status

Currently in **Alpha** phase. Version `0.0.1` includes:

- ✅ HTTP server for games, with range support.
- ✅ Voice control with wake word `"Catarsis"`.
- ✅ Configuration command `hiapp-config`.
- 🚧 In development: support for IP cameras, alarms, Telegram bot for game groups, and more.
- 🚧 Initial target is Termux; Windows will be included later.

---

## :inbox_tray: Installation

### Requirements

- **Termux** (Android) or **Linux**.
- **Python 3.10 or higher**.

### Command

```bash
pip install hiapp
```

---

## :rocket: Getting started

### 1. Start the voice assistant

```bash
hiapp-voice
```

The first time, the assistant will:

1. Ask for **your language** (e.g., `es` for Spanish, `en` for English).
2. Start downloading the corresponding voice model.
3. Show the download progress.

It allows **resuming** if interrupted:
if you run the command again, it will continue from where it left off,
so you don't lose progress or waste your mobile data.

All data is saved in `~/.hiapp/`:

- `~/.hiapp/config.json` → User configuration.
- `~/.hiapp/models/`     → Downloaded voice models.

### 2. Start only the server (without voice control)

```bash
hiapp-server
```

By default, the server listens on `0.0.0.0:5000`, meaning all available IPs on the device.

To stop it, press `Ctrl+C`.

### 3. Configure PPSSPP (if you want to play)

#### On the server

Find your local IP (in Termux):

```bash
termux-wifi-connectioninfo | grep ip
```

Example output: `"ip": "192.168.10.1",`

#### In PPSSPP

1. Go to **Settings → Tools → Network / Ad-hoc**.
2. Enable the **network server** and add the URL:

   ```
   http://<your-server-IP>:5000/
   ```

   With the example above, you would enter `http://192.168.10.1:5000/`.
3. Browse the available games. PPSSPP will request the fragments it needs.

---

## :gear: Configuration

Hiapp uses a configuration file at `~/.hiapp/config.json`. You can edit it with the `hiapp-config` command.

### View current configuration

```bash
hiapp-config list
```

### View a specific value

```bash
hiapp-config get port
```

### Set a value

```bash
hiapp-config set games-dir /storage/XXXX-XXXX/PSP
hiapp-config set port 8080
```

### Reset a value

```bash
hiapp-config reset port
hiapp-config reset --all
```

### Available options

| Key           | Default value      | Description                  |
|---------------|--------------------|------------------------------|
| `models-dir`  | `~/.hiapp/models`  | Voice models directory       |
| `games-dir`   | `~/PSP`            | PSP ISO directory            |
| `port`        | `5000`             | HTTP server port             |
| `host`        | `0.0.0.0`          | Network interface            |
| `lang`        | `es`               | Model language               |

> [!TIP]
> **Advanced users**: you can override any value with environment variables
> (`HIAPP_PORT`, `HIAPP_GAMES_DIR`, etc.).
> Environment variables take priority over the configuration file.

> [!NOTE]
> The activation word **`"Catarsis"`** is fixed and cannot be disabled.
> Additional *aliases* for other languages may be added in the future.

---

## :microphone: Voice control

Once `hiapp-voice` is running, say the activation word and then the command:

| Command                 | Action                               |
|-------------------------|--------------------------------------|
| `"Catarsis"`            | Activates the assistant (wake word)  |
| `"Activar servidor"`    | Starts the HTTP server               |
| `"Desactivar servidor"` | Stops the HTTP server                |
| `"Estado"`              | Reports whether the server is active |
| `"Ayuda"`               | Lists available commands             |

> [!WARNING]
> Voice control is only available on Termux/Linux.
> On Windows, the HTTP server works, but the voice module does not yet.

---

## :brain: Voice model

Hiapp does not include voice models by default (they take up a lot of space).
Hiapp **automatically downloads** the voice model the first time you run the assistant.

```bash
hiapp-voice
```

> [!TIP]
> If you prefer to use a model already downloaded elsewhere,
> or want them downloaded there, use the command:
>
> ```bash
> hiapp-config set models-dir "path/to/model"
> ```
>
> The assistant will use that path to search for or download models.

---

## :hammer_and_wrench: Troubleshooting

### The server is not accessible from PPSSPP

1. Verify both devices are on the **same WiFi network**.
2. Check the IP of the device running Hiapp: `termux-wifi-connectioninfo`.
3. Make sure the port is not blocked by the firewall.
4. Test from the client device's browser: `http://<IP>:5000/`.

### The model download is interrupted

Run `hiapp-voice` again. The download will automatically resume from where it left off.

### The microphone does not work

1. Grant microphone permissions on Android.
2. Test with: `termux-microphone-record -d 3`.
3. Verify that `sounddevice` is installed: `pip show sounddevice`.

---

## :handshake: Contributing

See the [contributing guide](docs/CONTRIBUTING.md) for more details.

## :scroll: License

This project is distributed under the *Apache-2.0* license.
See the `LICENSE` file in the source, or `licenses/LICENSE` in the wheel, for more details.
[View License](LICENSE).

Unofficial Spanish translation: [LICENSE_ES](LICENSE_ES).

---

## :pray: Acknowledgements

To the creators of [Termux](https://termux.dev/), for making possible the dream of thousands of developers and enthusiasts, like me, of having even an _AI_ at home.


To the developers of [Vosk](https://github.com/alphacep/vosk-api) —**Alpha Cephei Inc**— for contributing to offline speech recognition.


To the [PPSSPP](https://www.ppsspp.org/) team, for an extraordinary emulator I have enjoyed so much, and its network server support.


To my wife Lili, for so much.


And to [DeepSeek](https://chat.deepseek.com/), which will be integrated as online support for my **PRO** users.


Others will be added...

---

Last updated: September 19, 2026

[Go to top](#hiapp)
