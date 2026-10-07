[![PyPI version](https://img.shields.io/pypi/v/hiapp.svg)](https://pypi.org/project/hiapp)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/hiapp?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=Downloads)](https://pepy.tech/projects/hiapp)

**🌐 Idiomas / Languages:** Español | [English](https://github.com/Triplex3x-cyver/hiapp/blob/main/README_EN.md)

---

# Hiapp

## Descripción

**Asistente de voz autogestionado para el hogar, con servidor HTTP para PPSSPP.**

Hiapp es la base de un sistema de seguridad doméstica que crecerá con el tiempo.
Esta primera versión incluye el núcleo del servidor y el control por voz.

### Características
- **Wake Word local:** Controlado mediante la palabra de activación `"Catarsis"` y un alias para tu idioma.
- **Streaming directo:** Servidor HTTP/1.1 con soporte nativo de peticiones de rango (`Range Requests`).
- **Sin configuración compleja:** PPSSPP lee los fragmentos de las ISOs a medida que los necesita, sin selección manual de juegos.
- **Autogestionado:** Funciona sin internet. Los datos y la voz se procesan localmente.

### Problemas que resuelve
- ✅ Evita duplicar ISOs pesadas de PSP en múltiples dispositivos Android.
- ✅ Monta un servidor de contenidos compatible con el protocolo de red de PPSSPP.
- ✅ Integración fluida en entornos de consola Termux.

### Road map

- 🔜 Próximamente: podrás instalar módulos gratuitos y PRO, para un asistente más útil.
  - Al instalar modulos, tienes solo lo que necesitas, nada de contenidos inútiles para ti.
- 🔜 Próximamente: tus módulos se conservan en un directorio tuyo.
  - No los pierdes al actualizar o desinstalar.
- 🔜 Próximamente: se añadirán más funciones, y otras plataformas.

---

## 🧠 Palabra de activación

El motor de voz interno responde por defecto a **"Catarsis"**.

Esta elección reduce los falsos positivos en conversaciones diarias  
y evita colisiones con otros asistentes virtuales del hogar.

> 💡 **Consejo**
>
> Puedes añadir un alias (por ejemplo "oye hiapp") con:
> `hiapp-config set aliases "oye hiapp"`
> Cuidado con la pronunciación, tu alias puede no funcionar al hablarlo.
>
> También puedes cambiar el directorio de ISOs de PSP con:
> `hiapp-config set games_dir /ruta/a/tus/ISOs`

---

## 📥 Instalación

Termux
```bash
pip install hiapp[termux]
```

---

### 🚀 Configuración rápida

1. Coloca tus ISOs en un directorio, por ejemplo `~/PSP/`.
2. Conecta el dispositivo a tu red Wi-Fi (o crea un hotspot).
3. Inicia Hiapp con el comando principal:

   ```bash
   hiapp
   ```
   Al arrancar verás las URLs exactas con la IP LAN:
   ```
   🌐 Servidor en http://192.168.1.5:5000/
   🎮 Juegos en http://192.168.1.5:5000/game/
   ```
4. En PPSSPP, añade el servidor de red con la URL de juegos:
   ```
   http://<IP-del-servidor>:5000/game/
   ```
   Nota: la ip y el puerto los tomas del mensaje de Hiapp al iniciar.
5. Detén Hiapp con Ctrl+C (mientras no gestione la seguridad del hogar).

---

## 😕 Uso

Iniciar Hiapp (servidor + voz):

```bash
hiapp
```

Comandos de voz disponibles (dependen del idioma del modelo):
| Modelo español    | Modelo inglés     |
|-------------------|-------------------|
| "Catarsis estado" | "Catarsis status" |
| "Catarsis ayuda"  | "Catarsis help"   |

### Comandos de desarrollo

Útiles para pruebas y depuración:

```bash
hiapp-server   # Solo el servidor HTTP
hiapp-voice    # Solo el asistente de voz
hiapp-config   # Gestionar la configuración
```
*hiapp-server:* Útil para probar el servidor HTTP sin el asistente de voz.

### Configuración

Ver la configuración actual:

```bash
hiapp-config list
```

Cambiar cualquier valor:

```bash
hiapp-config set port 8080
hiapp-config set games_dir /storage/XXXX-XXXX/PSP
hiapp-config set aliases "oye hiapp"
```

---

## 🤝 Contribución
Consulta la [hoja de contribución](https://github.com/Triplex3x-cyver/hiapp/blob/main/docs/CONTRIBUTING.md) para más detalles.

## 📄 Licencia
Este proyecto se distribuye bajo la licencia *Apache-2.0*.<br/>
Consulta el archivo _LICENSE_ en fuente, o _licenses/LICENSE_ en rueda, para más detalles.<br/>
[Ver en GitHub](https://github.com/Triplex3x-cyver/hiapp/blob/main/LICENSE).

---

## 🙏 Agradecimientos
A la comunidad de **Termux**, por expandir las capacidades de hardware de nuestros teléfonos  
y permitirnos levantar ecosistemas de asistencia local en la palma de la mano.

---

Última actualización: 7 de Octubre de 2026

[Ir al inicio](#hiapp)
