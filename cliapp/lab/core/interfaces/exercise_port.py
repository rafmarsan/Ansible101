# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/core/interfaces/exercise_port.py
from typing import TYPE_CHECKING, Protocol, Union, List, runtime_checkable
from rich.text import Text

if TYPE_CHECKING:
    from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort

@runtime_checkable
class Exercise(Protocol):
    name: str
    debug_msg: List[Union[str, Text]]
    def start(self, notifier: ProgressNotifierPort) -> None:
        """
        Inicializa dependencias y recursos especificos del ejercicio
        """
        ...

    def finish(self, notifier: ProgressNotifierPort) -> None:
        """
        Libera recursos y hace limpieza especifica del ejercicio
        """
        pass