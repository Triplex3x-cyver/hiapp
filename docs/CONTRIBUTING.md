# Guía de contribución / Contributing Guide

**🌐 Idiomas:** **Español** | [English](#english)

---

## Español

¡Gracias por tu interés en contribuir a **Hiapp**!  
Este proyecto nace con la idea de ser **abierto, útil y respetuoso** con la privacidad de sus usuarios. Toda ayuda es bienvenida.

### :dart: Formas de contribuir

No hace falta ser programador para aportar. Algunas ideas:

- **Reportar errores** abriendo un [Issue](https://github.com/Triplex3x-cyver/hiapp/issues).
- **Sugerir funcionalidades** o mejoras.
- **Mejorar la documentación** (README, traducciones, ejemplos).
- **Traducir** el proyecto a otros idiomas.
- **Probar** la aplicación en distintos dispositivos y reportar resultados.
- **Compartir** el proyecto en redes, foros o con quien pueda necesitarlo.

### :bug: Reportar un error

Antes de abrir un Issue, verifica:

1. Que no exista ya un Issue similar.
2. Que estás usando la **última versión** (`pip install --upgrade hiapp`).

Al abrir el Issue, incluye:

- **Descripción clara** del problema.
- **Pasos para reproducirlo**.
- **Comportamiento esperado** vs. **comportamiento real**.
- **Sistema operativo** y versión (Termux, Linux, Windows...).
- **Versión de Python** (`python --version`).
- **Versión de Hiapp** (`pip show hiapp`).
- **Logs o capturas** si es posible.

### :bulb: Sugerir una funcionalidad

Abre un Issue con la etiqueta `enhancement` y describe:

- **Qué problema resuelve**.
- **Cómo imaginas la solución**.
- **Alternativas** que hayas considerado.

### :wrench: Enviar código (Pull Request)

1. Haz un **fork** del repositorio.
2. Crea una rama descriptiva:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Sigue el **estilo del código existente** (PEP 8, nombres claros).
4. Añade **comentarios** donde sea necesario.
5. **Prueba** tu cambio en al menos un dispositivo.
6. Actualiza el `CHANGELOG.md` si aplica.
7. Envía el Pull Request con una **descripción clara**.

### :triangular_ruler: Estilo de código

- **Python**: PEP 8, 4 espacios, líneas ≤ 100 caracteres.
- **Idioma del código**: inglés (variables, funciones, clases).
- **Comentarios y docstrings**: pueden estar en español o inglés.
- **Mensajes de commit**: en inglés, imperativo ("Add feature X", "Fix bug Y").

### :test_tube: Probar antes de enviar

Antes de enviar un Pull Request, ejecuta:

```bash
rm -rf build/ dist/ src/*.egg-info
python -m build
python -m twine check dist/*
```

Si todo pasa, tu paquete está listo.

> [!NOTE]
> Nota sobre codificación:
> Asegúrate de que tus archivos de texto estén guardados en UTF-8 sin BOM.
> Algunos editores (como Total Commander de Android) añaden un BOM al inicio del archivo,
> lo que impide que PyPI renderice correctamente el README. Verifica con:

```bash
file README.md
```

Si ves with BOM, guarda el archivo de nuevo sin BOM.

### :scroll: Licencia

Al contribuir, aceptas que tu aporte se distribuya bajo la misma licencia del proyecto: **Apache 2.0**.

### :pray: Gracias

Cada contribución, por pequeña que sea, hace que Hiapp sea mejor para todos. ¡Gracias por ser parte!

---

## English

Thank you for your interest in contributing to **Hiapp**!  
This project was born with the idea of being **open, useful, and respectful** of its users' privacy. All help is welcome.

### :dart: Ways to contribute

You don't need to be a programmer to contribute. Some ideas:

- **Report bugs** by opening an [Issue](https://github.com/Triplex3x-cyver/hiapp/issues).
- **Suggest features** or improvements.
- **Improve documentation** (README, translations, examples).
- **Translate** the project into other languages.
- **Test** the application on different devices and report results.
- **Share** the project on social media, forums, or with anyone who might need it.

### :bug: Reporting a bug

Before opening an Issue, check:

1. That a similar Issue doesn't already exist.
2. That you're using the **latest version** (`pip install --upgrade hiapp`).

When opening the Issue, include:

- **Clear description** of the problem.
- **Steps to reproduce** it.
- **Expected behavior** vs. **actual behavior**.
- **Operating system** and version (Termux, Linux, Windows...).
- **Python version** (`python --version`).
- **Hiapp version** (`pip show hiapp`).
- **Logs or screenshots** if possible.

### :bulb: Suggesting a feature

Open an Issue with the `enhancement` label and describe:

- **What problem it solves**.
- **How you imagine the solution**.
- **Alternatives** you've considered.

### :wrench: Submitting code (Pull Request)

1. **Fork** the repository.
2. Create a descriptive branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Follow the **existing code style** (PEP 8, clear names).
4. Add **comments** where necessary.
5. **Test** your change on at least one device.
6. Update `CHANGELOG.md` if applicable.
7. Submit the Pull Request with a **clear description**.

### :triangular_ruler: Code style

- **Python**: PEP 8, 4 spaces, lines ≤ 100 characters.
- **Code language**: English (variables, functions, classes).
- **Comments and docstrings**: Spanish or English are both fine.
- **Commit messages**: in English, imperative ("Add feature X", "Fix bug Y").

### :test_tube: Test before submitting

Before submitting a Pull Request, run:

```bash
rm -rf build/ dist/ src/*.egg-info
python -m build
python -m twine check dist/*
```

If everything passes, your package is ready.

> [!NOTE]
> Encoding note:
> Make sure your text files are saved as UTF-8 without BOM.
> Some editors (like Android Total Commander) add a BOM at the beginning of the file,
> which prevents PyPI from rendering the README correctly. Check with:

```bash
file README.md
```

If you see with BOM, save the file again without BOM.

### :scroll: License

By contributing, you agree that your contribution will be distributed under the same license as the project: **Apache 2.0**.

### :pray: Thank you

Every contribution, no matter how small, makes Hiapp better for everyone. Thanks for being part of it!
