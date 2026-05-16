# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/application/use_cases/exercise/exercise_vars.py
from typing import Tuple, Union, List
from rich.text import Text
from lab.infrastructure.ui.i18n import get_text, get_current_language
import logging
import sys
import time

from lab.core.dtos.EventInfo import EventInfo
from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort

logger = logging.getLogger("lab")
LANG = get_current_language()

class ExerciseVars:
    """
    Logica para inicializacion del ejercicio "Role - Practica"
    """
    def __init__(self, name: str, debug_msg: List[Union[str, Text]] = []):
        self.name = name
        self.debug_msg = debug_msg

    def _create_file_in_cwd(self) -> Tuple[bool, str]:
        import os
        failed = False
        error_output = ""
        try:
            cwd = os.getcwd()
            file_path = os.path.join(cwd, 'vars_lab.yml')
            open(file_path, "a").close()
            time.sleep(1)
        except:
            failed = True
            error_output = get_text(LANG,'error_create_vars_lab')
        return failed, error_output

    def _remove_file_in_cwd(self) -> Tuple[bool, str]:
        from pathlib import Path
        import time
        failed = False
        error_output = ""
        try:
            file_path = Path.cwd() / "vars_lab.yml"
            file_path.unlink() # borra el fichero
            time.sleep(1)
        except:
            failed = True
            error_output = get_text(LANG,'error_remove_vars_lab')
        return failed, error_output

    def start(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        event_info = EventInfo(name=get_text(LANG,'creando_fichero_base'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._create_file_in_cwd()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

    def finish(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion de finalizacion: Define la secuencia de eventos.
        """
        event_info = EventInfo(name=get_text(LANG,'eliminando_ficheros_ejercicio'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._remove_file_in_cwd()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None
