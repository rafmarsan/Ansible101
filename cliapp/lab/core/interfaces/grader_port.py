# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

from typing import Protocol, runtime_checkable

from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort

@runtime_checkable
class Grader(Protocol):
    """
    Define el contrato para la inicializacion tecnica 
    de la infraestructura del Lab (Ej: inicializar el lab, construir imagenes, etc).
    """
    exercisename: str
    def grade(self, notifier: ProgressNotifierPort) -> None:
        """
        Ejecuta la logica de evaluacion del ejercicio
        """
        ...
