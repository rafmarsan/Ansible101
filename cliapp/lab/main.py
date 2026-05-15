# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

import typer
from typing_extensions import Annotated
from rich.logging import RichHandler
import logging
import sys
import json
from pathlib import Path

from lab.infrastructure.ui.progress_notifier_adapter import ProgressNotifierAdapter
from lab.infrastructure.adapters.registry_adapter import RegistryAdapter
from lab.infrastructure.ui.i18n import get_text

def get_current_language():
    config_path = Path.cwd() / ".lab_config.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text())
            return data.get("language", "es")
        except:
            pass
    return "es"

LANG = get_current_language()

IS_PACKAGED = getattr(sys, "frozen", False) or "__compiled__" in globals()

# Configuracion global del logger
logger = logging.getLogger("lab")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
handler = RichHandler(rich_tracebacks=True, show_path=not IS_PACKAGED)
handler.setFormatter(formatter)
handler.setLevel(logging.NOTSET)
logger.addHandler(handler)

# descripcion general
app = typer.Typer(
    help=get_text(LANG, "app_help"),
    context_settings={"help_option_names": ["-h", "--help"]}
) 

# Funciones de autocompletado dinamico
def exercises_autocomplete(ctx: typer.Context, args: list, incomplete: str):
    registry = RegistryAdapter()
    exercises_map = registry.auto_discover_exercises()
    return [name for name in exercises_map.keys() if name.startswith(incomplete)]

def graders_autocomplete(ctx: typer.Context, args: list, incomplete: str):
    registry = RegistryAdapter()
    graders_map = registry.auto_discover_graders()
    return [name for name in graders_map.keys() if name.startswith(incomplete)]

@app.command(help=get_text(LANG, "init_help"))
def init(
    # Un argumento posicional se define simplemente con el tipo
    # y typer.Argument() si quieres añadir metadatos (como la ayuda)
    engine: Annotated[str, typer.Argument(help=get_text(LANG, "engine_help"))] = "podman",
    debug: bool = typer.Option(False, "--debug", "-d", help=get_text(LANG, "debug_help")),
    # force: bool = typer.Option(False, "--force", "-f", help="Fuerza la inicializacion de un nuevo lab")
):
    from lab.infrastructure.adapters.lab_repository_adapter import LabRepositoryAdapter
    from lab.infrastructure.adapters.lab_adapter import LabAdapter
    from lab.application.use_cases.lab_initializer import LabInitializer
    from lab.core.entities.lab import Lab
    if debug:
        logger.setLevel(logging.DEBUG)

    language = typer.prompt(get_text(LANG, "prompt_language"), default="es")
    if language.lower() not in ["es", "en"]:
        typer.secho(get_text(LANG, "prompt_language_invalid"), fg=typer.colors.RED)
        raise typer.Exit(code=1)

    LabInitializer().execute(
        service=LabAdapter(),
        repo_adapter=LabRepositoryAdapter(),
        lab=Lab(engine=engine, language=language.lower()),
        # force=force
    )


@app.command(help=get_text(LANG, "start_help"))
def start(
    # Un argumento posicional se define simplemente con el tipo
    # y typer.Argument() si quieres añadir metadatos (como la ayuda)
    exercisename: Annotated[str, typer.Argument(
        help=get_text(LANG, "start_exercise_help"),
        autocompletion=exercises_autocomplete
        )],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    if debug:
        logger.setLevel(logging.DEBUG)

    registry = RegistryAdapter()
    exercises_map = registry.auto_discover_exercises()
    cls = exercises_map.get(exercisename.lower())
    if not cls:
        typer.secho(
            get_text(LANG, "error_exercise_not_found", exercisename=exercisename),
            fg=typer.colors.RED,
            bold=False
        )
        raise typer.Exit(code=1)
    # Creamos instancia de Exercise con el nombre pasado
    exercise = cls(exercisename)
    notifier = ProgressNotifierAdapter()
    exercise.start(notifier)


@app.command(help=get_text(LANG, "grade_help"))
def grade(
    exercisename: Annotated[str, typer.Argument(
        help=get_text(LANG, "grade_exercise_help"),
        autocompletion=graders_autocomplete
        )],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    from lab.infrastructure.ui.progress_notifier_adapter import ProgressNotifierAdapter
    if debug:
        logger.setLevel(logging.DEBUG)

    registry = RegistryAdapter()
    graders_map = registry.auto_discover_graders()
    cls = graders_map.get(exercisename.lower())
    if not cls:
        typer.secho(
            get_text(LANG, "error_exercise_not_found", exercisename=exercisename),
            fg=typer.colors.RED,
            bold=False
        )
        raise typer.Exit(code=1)
    # Creamos instancia de Grader con el nombre pasado
    grader = cls(exercisename)
    notifier = ProgressNotifierAdapter()
    grader.grade(notifier)


@app.command(help=get_text(LANG, "finish_help"))
def finish(
    exercisename: Annotated[str, typer.Argument(help=get_text(LANG, "finish_exercise_help"))],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    if debug:
        logger.setLevel(logging.DEBUG)

    registry = RegistryAdapter()
    exercises_map = registry.auto_discover_exercises()
    cls = exercises_map.get(exercisename.lower())
    if not cls:
        typer.secho(
            get_text(LANG, "error_exercise_not_found", exercisename=exercisename),
            fg=typer.colors.RED,
            bold=False
        )
        raise typer.Exit(code=1)
    # Creamos instancia de Exercise con el nombre pasado
    exercise = cls(exercisename)
    notifier = ProgressNotifierAdapter()
    exercise.finish(notifier)

def version_callback(value: bool):
    if value:
        __version__ = "0.8.7-final"
        print('Ansible101 Lab')
        print('version :',__version__)
        raise typer.Exit()

@app.callback()
def root(
    version: bool = typer.Option(
        None,
        "--version","-version",
        callback=version_callback,
        is_eager=True,
        help=get_text(LANG, "version_help"),
    )
):
    pass



if __name__ == '__main__':
    app()