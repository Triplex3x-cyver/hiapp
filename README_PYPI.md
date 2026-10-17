[![PyPI version](https://img.shields.io/pypi/v/hiapp.svg)](https://pypi.org/project/hiapp)
[![PyPI Total Downloads](https://static.pepy.tech/personalized-badge/hiapp?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=Downloads)](https://pepy.tech/projects/hiapp)

**🌐 Idiomas / Languages:** Español | [English](https://github.com/Triplex3x-cyver/hiapp/blob/main/README_EN.md)

---

# Hiapp

> **H.I.A.P.P.** = **H**ogar con **I**nteligencia **A**rtificial **P**rivada **P**ersonal.

**Asistente de voz autogestionado para el hogar, con servidor HTTP extensible mediante add-ons.**

Hiapp es la base de un sistema de seguridad doméstica que crecerá con el tiempo.
Esta versión incluye el núcleo del servidor, el control por voz y el sistema de add-ons.

### Características
- **Wake Word local:** Controlado mediante la palabra de activación `"Catarsis"` (y aliases).
- **Autogestionado:** Funciona sin internet. Los datos y la voz se procesan localmente.
- **Modular:** Instala solo los add-ons que necesites (juegos, cámaras, etc.).

### Roadmap

- 🔜 Próximamente: podrás instalar módulos gratuitos y PRO, para un asistente más útil.
- 🔜 Próximamente: tus módulos se conservan en un directorio tuyo (no los pierdes al actualizar).
- 🔜 Próximamente: se añadirán más funciones, y otras plataformas.

---

## 🧠 Palabra de activación

El motor de voz interno responde por defecto a **"Catarsis"**.

> 💡 **Consejo**
>
> Puedes añadir un alias (por ejemplo "oye hiapp") con:
> `hiapp-config set aliases "oye hiapp"`.
>
> También puedes cambiar el directorio de ISOs de PSP con:
> `hiapp-config set games_dir /ruta/a/tus/ISOs`.

---

## 📥 Instalación

```bash
pip install hiapp[termux]
```

---

### 🚀 Configuración rápida

1. Conecta el dispositivo a tu red Wi-Fi (o crea un hotspot).
2. Inicia Hiapp con el comando principal:

   ```bash
   hiapp
   ```
   Al arrancar verás las URLs exactas con la IP LAN.
   Detén Hiapp con `Ctrl+C`.

---

## 🧩 Add-ons

Hiapp crece mediante **add-ons**. El servidor de streaming para **PPSSPP** está disponible como un add-on independiente.

Consulta la documentación completa, la lista de add-ons y las instrucciones en:
👉 **https://github.com/Triplex3x-cyver/hiapp-addons**

---

## 😕 Uso

Iniciar Hiapp (servidor + voz):

```bash
hiapp
```

Comandos de voz (según el idioma del modelo):
| Modelo español    | Modelo inglés     |
|-------------------|-------------------|
| "Catarsis estado" | "Catarsis status" |
| "Catarsis ayuda"  | "Catarsis help"   |

### Configuración

```bash
hiapp-config list
hiapp-config set port 8080
hiapp-config set games_dir /storage/XXXX-XXXX/PSP
```

---

## 💬 Comunidad

- 🌐 **Sitio web**: http://hiapp.mywebcommunity.org/
- **Telegram**: https://t.me/hiapp_chat
- **WhatsApp**: https://whatsapp.com/channel/0029VbEIkYy1Hsq3oyhkth2Y

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia *Apache-2.0*. Consulta el archivo `LICENSE` para más detalles.

---

## 🙏 Agradecimientos

A los creadores de [Termux](https://termux.dev/), por hacer posible el sueño de miles de desarrolladores y entusiastas, como yo, de poder tener incluso una _IA_ en la casa.


A los desarrolladores de [Vosk](https://github.com/alphacep/vosk-api) —**Alpha Cephei Inc**— por contribuir al reconocimiento de voz sin conexión.


A mi esposa Lili, por mucho.


Y a [DeepSeek](https://chat.deepseek.com/), que se integrará como soporte en línea para mis usuarios **PRO**.


Otros más serán añadidos...

---
---

*Última actualización: 17 de Octubre de 2026*

[Ir al inicio](#hiapp)