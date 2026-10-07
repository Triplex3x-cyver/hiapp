[![PyPI version](https://img.shields.io/pypi/v/hiapp.svg)](https://pypi.org/project/hiapp)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/hiapp?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=Downloads)](https://pepy.tech/projects/hiapp)

**🌐 Idiomas / Languages:** Español | [English](https://github.com/Triplex3x-cyver/hiapp/blob/main/README_EN.md)

---

# Hiapp

## Descripción

**Asistente de voz con servidor de juegos para PPSSPP.**

### Características
- **Wake Word local:** Controlado mediante la palabra de activación `"Catarsis"` y un alias para tu idioma.
- **Streaming directo:** Servidor HTTP/1.1 con soporte nativo de peticiones de rango (`Range Requests`).
- **Sin configuración compleja:** PPSSPP lee los fragmentos de las ISOs a medida que los necesita, sin selección manual de juegos.
- **Autogestionado:** Funciona sin internet. Los datos y la voz se procesan localmente.

### Problemas que resuelve
- ✅ Evita duplicar ISOs pesadas de PSP en múltiples dispositivos Android.
- ✅ Monta un servidor de contenidos compatible con el protocolo de red de PPSSPP.
- ✅ Integración fluida en entornos de consola Termux.
- ✅ Se añadirán más funciones, y otras plataformas.

---

## 🧠 Palabra de activación
El motor de voz interno responde por defecto a **"Catarsis"**.
Esta elección reduce los falsos positivos en conversaciones diarias<br/>
y evita colisiones con otros asistentes virtuales del hogar.

> 💡Consejo  
> Puedes utilizar la variable de entorno `HIAPP_GAMES_DIR`  
> para definir una ruta _personalizada_ al directorio donde guardas tus ISOs de PSP 👍.

---

## 📥 Instalación
```bash
pip install hiapp
```

---

### 🚀 Configuración rápida
1. Coloca tus ISOs en un directorio, por ejemplo `~/PSP/`.
2. Crea un punto WI-FI o conecta el servidor a uno.
3. Copia la ip del servidor, se ve en sus ajustes.
4. Inicia el servidor manualmente solo esta vez:
   ```bash
   hiapp-server
   ```
5. En PPSSPP, añade el servidor de red con la URL:
   ```textplain
   http://<IP-del-dispositivo-servidor>:PUERTO/
   ```
   El **PUERTO** es configurable mediante la variable de entorno `HIAPP_PORT`.  
   Por defecto es el 5000. Puedes detener el servidor con Ctrl+C.

---

## 😕 Uso
Iniciar el asistente de voz, lo controla todo:
```bash
hiapp-voice
```

Iniciar solo el servidor de streaming para el emulador:
```bash
hiapp-server
```

Y para mostrar ayuda y los comandos de los modulos nativos  
y PRO instalados (no está incluido, próximamente):
```bash
hiapp-help
```

---

### 🤝 Contribución
Consulta la [hoja de contribución](https://github.com/Triplex3x-cyver/hiapp/blob/main/docs/CONTRIBUTING.md) para más detalles.

### 📄 Licencia
Este proyecto se distribuye bajo la licencia *Apache-2.0*.<br/>
Consulta el archivo _LICENSE_ en fuente, o _licenses/LICENSE_ en rueda, para más detalles.<br/>
[Ver en GitHub](https://github.com/Triplex3x-cyver/hiapp/blob/main/LICENSE).

---

### 🙏 Agradecimientos
A la comunidad de **Termux**, por expandir las capacidades de hardware de nuestros teléfonos  
y permitirnos levantar ecosistemas de asistencia local en la palma de la mano.

---

Última actualización: 16 de Septiembre 2026

[Ir al inicio](#hiapp)
