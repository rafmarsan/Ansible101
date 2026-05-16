# Contributing to Ansible101

¡Gracias por tu interés en contribuir! / Thank you for your interest in contributing!

🌐 Este fichero está en castellano — [English version below](#english-version)

---

## Español

### ¿Cómo puedo contribuir?

#### 🐛 Reportar un bug

1. Asegúrate de que el bug no ha sido ya reportado buscando en [Issues](https://github.com/rafmarsan/Ansible101/issues).
2. Abre un nuevo Issue usando la plantilla **Bug Report**.
3. Incluye:
   - Versión del CLI (`lab --version`)
   - Sistema operativo y versión de Python
   - Pasos exactos para reproducir el fallo
   - Comportamiento esperado vs. comportamiento real
   - Output completo del error (con `--debug` si es posible)

#### 💡 Proponer una mejora o nuevo ejercicio

1. Abre un Issue con la etiqueta `enhancement` describiendo tu propuesta.
2. Explica el caso de uso: ¿qué aprende el estudiante con este ejercicio?
3. Si tienes una implementación en mente, descríbela brevemente antes de abrir una PR.

#### 🔧 Enviar un Pull Request

1. Haz un fork del repositorio y trabaja en una rama descriptiva:
   ```shell
   git checkout -b feat/nuevo-ejercicio-mariadb
   ```
2. Lee la [documentación técnica del CLI](cliapp/README.md) para entender la arquitectura antes de escribir código.
3. Sigue el patrón existente:
   - Nuevos ejercicios en `cliapp/lab/application/use_cases/exercise/`
   - Nuevos graders en `cliapp/lab/application/use_cases/grader/`
   - Todas las cadenas de texto en `cliapp/lab/infrastructure/ui/i18n.py` (en `es` y `en`)
4. Prueba tu cambio localmente:
   ```shell
   cd cliapp/
   pip install -e .
   lab start <tu_ejercicio>
   lab grade <tu_ejercicio>
   ```
5. Abre la PR contra la rama `main` con una descripción clara de qué hace y por qué.

### Estilo de código

- **Python:** sin ningún linter obligatorio por ahora, pero se siguen las convenciones de PEP 8.
- **Commits:** mensajes en inglés, formato `tipo: descripción` (ej: `feat: add mariadb exercise`, `fix: lab init ssh key permissions`).
- **Docstrings:** en castellano (el proyecto tiene audiencia hispanohablante).

### Entorno de desarrollo

```shell
python -m venv venv
source venv/bin/activate
cd cliapp/
pip install -e .
```

---

## English version

### How can I contribute?

#### 🐛 Reporting a Bug

1. Make sure the bug hasn't already been reported by searching [Issues](https://github.com/rafmarsan/Ansible101/issues).
2. Open a new Issue using the **Bug Report** template.
3. Include:
   - CLI version (`lab --version`)
   - OS and Python version
   - Exact steps to reproduce
   - Expected vs. actual behavior
   - Full error output (with `--debug` if possible)

#### 💡 Proposing an Improvement or New Exercise

1. Open an Issue labeled `enhancement` describing your proposal.
2. Explain the use case: what does the student learn from this exercise?
3. If you have an implementation in mind, describe it briefly before opening a PR.

#### 🔧 Submitting a Pull Request

1. Fork the repository and work on a descriptive branch:
   ```shell
   git checkout -b feat/new-mariadb-exercise
   ```
2. Read the [CLI technical documentation](cliapp/README.en.md) to understand the architecture before writing code.
3. Follow the existing patterns:
   - New exercises in `cliapp/lab/application/use_cases/exercise/`
   - New graders in `cliapp/lab/application/use_cases/grader/`
   - All text strings in `cliapp/lab/infrastructure/ui/i18n.py` (both `es` and `en`)
4. Test your change locally:
   ```shell
   cd cliapp/
   pip install -e .
   lab start <your_exercise>
   lab grade <your_exercise>
   ```
5. Open a PR against `main` with a clear description of what it does and why.

### Code Style

- **Python:** no mandatory linter for now, but PEP 8 conventions are followed.
- **Commits:** messages in English, format `type: description` (e.g. `feat: add mariadb exercise`, `fix: lab init ssh key permissions`).
- **Docstrings:** in Spanish (the project's primary audience is Spanish-speaking).

### Development Environment

```shell
python -m venv venv
source venv/bin/activate
cd cliapp/
pip install -e .
```

---

## 📝 License

By contributing to this project, you agree that your contributions will be licensed under the [GNU General Public License v3.0](LICENSE).
