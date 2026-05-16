# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/application/use_cases/exercise/template.py
from typing import Tuple, Union, List
from rich.text import Text
from lab.infrastructure.ui.i18n import get_text, get_current_language
import logging
import sys
import time

from lab.core.dtos.EventInfo import EventInfo
from lab.core.interfaces.container_port import ContainerPort
from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort
from lab.infrastructure.adapters.container_adapter import ContainerAdapter

logger = logging.getLogger("lab")
LANG = get_current_language()

class ExerciseA:
    """
    Logica para inicializacion del ejercicio "Variables - Practica"
    """
    def __init__(self, name: str, debug_msg: List[Union[str, Text]] = []):
        self.name = name
        self.debug_msg = debug_msg

    def _create_containers(self, container_provider: ContainerPort) -> Tuple[bool, str]:
        """
        Implementa una de las tareas (checks) de la secuencia
        """
        container, failed, error_output = container_provider.run_container(
            image="lab-ssh-ol8",
            name="web1",
            ports={"22/tcp": 2232, "80/tcp": 8080},
        )
        return failed, error_output
    
    def _delete_containers(self, container_provider: ContainerPort):
        failed = False
        error_output = ''
        failed, error_output = container_provider.remove_container('web1')
        # if logger.isEnabledFor(logging.DEBUG):
        #     append_msg_with_datatime(instance=self,msg=f"Output: {error_output}",last=True)
        return failed, error_output

    def _install_packages(self) -> Tuple[bool, str]:
        """ Implementa otra tarea de la secuencia. """
        failed = False
        error_output = ""
        time.sleep(5)
        return failed, error_output


    def start(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        # event_info = EventInfo(name='Cargando fichero de contexto')
        # spinner_handle, finished_event = notifier.start(event_info)
        # failed, lab, error_output = repo_adapter.load()
        # event_info.failed = failed; event_info.error_msg = error_output
        # notifier.finish(spinner_handle, finished_event)
        # sys.exit(1) if event_info.failed else None

        container_service = ContainerAdapter()
        container_service.init_client()
        event_info = EventInfo(name='Creando container para el ejercicio')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._create_containers(container_service)
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

    
    def finish(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion de finalizacion: Define la secuencia de eventos.
        """
        container_service = ContainerAdapter()
        container_service.init_client()
        event_info = EventInfo(name=get_text(LANG,'eliminando_containers_ejercicio'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._delete_containers(container_service)
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None
