# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/core/interfaces/registry_port.py
from typing import Protocol, Dict, Type, runtime_checkable
from lab.core.interfaces.exercise_port import Exercise
from lab.core.interfaces.grader_port import Grader

@runtime_checkable
class RegistryPort(Protocol):
    def auto_discover_exercises(self) -> Dict[str, Type[Exercise]]:
        """
        Descubre y retorna un diccionario de clases Exercise (Clave: nombre, Valor: Clase).
        """
        ...

    def auto_discover_graders(self) -> Dict[str, Type[Grader]]:
        """
        Descubre y retorna un diccionario de clases Grader (Clave: nombre, Valor: Clase).
        """
        ...

    def auto_discover_images(self) -> Dict[str, Dict[str, str]]:
        """
        Descubre y retorna la informacion de las imagenes del Lab (rutas, tags).
        """
        ...