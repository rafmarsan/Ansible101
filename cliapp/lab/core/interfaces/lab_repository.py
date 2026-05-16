# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/core/interfaces/lab_repository.py
from typing import Protocol, Tuple, runtime_checkable
from lab.core.entities.lab import Lab

@runtime_checkable
class LabRepository(Protocol):
    """
    Define el contrato para la persistencia de la entidad Lab
    """
    # def load(self, force: bool) -> Tuple[bool, Lab, str]:
    def load(self) -> Tuple[bool, Lab, str]:
        """
        Carga la instancia de Lab persistida.
        Si `force=True` o no existe la configuracion previa, retorna (False, nuevo_lab)
        Retorna (exists: bool, lab: Lab)
        """
        ...

    def save(self, lab: Lab) -> Tuple[bool, str]:
        """
        Persiste el estado actual de la entidad Lab
        """
        ...