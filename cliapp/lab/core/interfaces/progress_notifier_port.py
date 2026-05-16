# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

from typing import Protocol, Tuple, runtime_checkable
from threading import Event

from lab.core.dtos.EventInfo import EventInfo

@runtime_checkable
class ProgressNotifierPort(Protocol):
    """
    Contrato para notificar el progreso de la ejecución de un caso de uso.
    """
    def start(self, event_info: EventInfo) -> Tuple[Event, Event]:
        """
        Inicia un spinner con el texto dado.
        Devuelve un objeto que se usará para detener el spinner más tarde.
        """
        ...

    def finish(self, spinner_handle: Event, finished_event: Event) -> None:
        """
        Detiene el spinner e imprime el resultado final.
        """
        ...
