# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

TEXTS = {
    "es": {
        "app_help": "Un app para tus herramientas de laboratorio.",
        "engine_help": "Container engine a usar",
        "debug_help": "Activa el modo debug",
        "init_help": "Inicia el laboratorio y sus dependencias",
        "start_exercise_help": "Nombre del ejercicio a iniciar",
        "start_help": "Inicia las dependencias del ejercicio correspondiente",
        "error_exercise_not_found": "\n❌ Error: Ejercicio '{exercisename}' no existe.\n",
        "grade_exercise_help": "Nombre del ejercicio a evaluar",
        "grade_help": "Evalua el ejercicio correspondiente",
        "finish_exercise_help": "Nombre del ejercicio a finalizar.",
        "finish_help": "Libera las dependencias del ejercicio correspondiente",
        "version_help": "Muestra la version",
        "prompt_language": "Selecciona el idioma / Select language (es/en)",
        "prompt_language_invalid": "Idioma inválido. Usa 'es' o 'en'.",
        "verificando_ansible": "Verificando si Ansible esta instalado",
        "ansible_no_disponible": "Ansible no esta disponible en el entorno actual",
        "error_ansible_version": "No se pudo ejecutar `ansible --version`. Verifica la instalacion",
        "error_ansible_path": "No se encontro el ejecutable de Ansible en el PATH",
        "definiendo_fichero": "Definiendo fichero de configuracion",
        "inicializando_lab": "Inicializando laboratorio",
        "desplegando_clave": "Desplegando la clave privada del laboratorio"
    },
    "en": {
        "app_help": "An app for your lab tools.",
        "engine_help": "Container engine to use",
        "debug_help": "Enable debug mode",
        "init_help": "Initialize the lab and its dependencies",
        "start_exercise_help": "Name of the exercise to start",
        "start_help": "Starts the dependencies for the corresponding exercise",
        "error_exercise_not_found": "\n❌ Error: Exercise '{exercisename}' does not exist.\n",
        "grade_exercise_help": "Name of the exercise to grade",
        "grade_help": "Grades the corresponding exercise",
        "finish_exercise_help": "Name of the exercise to finish.",
        "finish_help": "Releases the dependencies for the corresponding exercise",
        "version_help": "Shows the version",
        "prompt_language": "Select language (es/en)",
        "prompt_language_invalid": "Invalid language. Use 'es' or 'en'.",
        "verificando_ansible": "Verifying if Ansible is installed",
        "ansible_no_disponible": "Ansible is not available in the current environment",
        "error_ansible_version": "Could not execute `ansible --version`. Check installation",
        "error_ansible_path": "Ansible executable not found in PATH",
        "definiendo_fichero": "Defining configuration file",
        "inicializando_lab": "Initializing lab",
        "desplegando_clave": "Deploying lab private key"
    }
}

import json
from pathlib import Path

def get_current_language():
    config_path = Path.cwd() / ".lab_config.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text())
            return data.get("language", "es")
        except:
            pass
    return "es"

def get_text(lang: str = None, key: str = None, **kwargs) -> str:
    """Devuelve el texto traducido. Si no existe la clave, devuelve la clave."""
    if not lang:
        lang = get_current_language()
    # Si se nos olvida la clave pero la pasamos como primer argumento:
    if key is None:
        key = lang
        lang = get_current_language()
        
    lang_dict = TEXTS.get(lang, TEXTS["es"])
    text = lang_dict.get(key, TEXTS["es"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text
