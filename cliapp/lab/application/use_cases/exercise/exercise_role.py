# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/application/use_cases/exercise/exercise_role.py
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

class ExerciseRole:
    """
    Logica para inicializacion del ejercicio "Variables - Practica"
    """
    def __init__(self, name: str, debug_msg: List[Union[str, Text]] = []):
        self.name = name
        self.debug_msg = debug_msg

    def _role_creation(self) -> Tuple[bool, str]:
        """Crea un role de Ansible usando ansible-galaxy init."""
        import subprocess
        failed = False
        error_output = ""
        role_name = "webdemo"
        time.sleep(0.5)
        res = subprocess.run(
            ["ansible-galaxy", "init", role_name, "--force"],
            capture_output=True,
            text=True,
            check=False  # No lanza excepcion si falla
        )
        if res.returncode != 0:
            failed = True
            error_output = (
                f"{res.stderr.strip()}"
            )
        return failed, error_output

    def _role_cleanup(self) -> Tuple[bool, str]:
        """Crea un role de Ansible usando ansible-galaxy init."""
        import shutil
        from pathlib import Path
        time.sleep(0.5)
        failed = False
        error_output = ""
        role_name = "webdemo"
        try:
            role_path = Path.cwd() / role_name
            subdirs = ["files", "handlers", "meta", "tests", "vars"]
            for sub in subdirs:
                shutil.rmtree(role_path / sub)
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = get_text(LANG,'error_delete_role', role_name=role_name, e=e)
            return failed, error_output
    
    def _remove_role_in_cwd(self) -> Tuple[bool, str]:
        import shutil
        from pathlib import Path
        failed = False
        error_output = ""
        time.sleep(1)
        try:
            role_path = Path.cwd() / "webdemo"
            shutil.rmtree(role_path)
            playbook_path = Path.cwd() / "site.yml"
            playbook_path.unlink() # borra el fichero
        except:
            failed = True
            error_output = get_text(LANG,'error_remove_role_site')
        return failed, error_output

    def start(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        event_info = EventInfo(name=get_text(LANG,'creando_ansible_role'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._role_creation()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name=get_text(LANG,'limpiando_carpetas_rol'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._role_cleanup()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

    
    def finish(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion de finalizacion: Define la secuencia de eventos.
        """
        event_info = EventInfo(name=get_text(LANG,'eliminando_containers_ejercicio'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._remove_role_in_cwd()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None
