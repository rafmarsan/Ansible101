# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/core/interfaces/lab_port.py
from typing import Protocol, Tuple, runtime_checkable, Dict

from lab.core.interfaces.container_port import ContainerPort

@runtime_checkable
class LabPort(Protocol):
    """
    Define el contrato para verificar si estamos en una carpeta de trabajo valida
    """
    def verify_context(self) -> Tuple[bool, str]:
        """
        Ejecuta las dependencias de verificacion
        """
        ...

    """
    Define el contrato para la inicializacion tecnica 
    de la infraestructura del Lab (Ej: inicializar el lab, construir imagenes, etc).
    """
    def init(self, container_service: ContainerPort, LAB_IMAGES: Dict[str, Dict[str, str]]) -> Tuple[bool, str]:
        """
        Ejecuta las dependencias de inicializacion
        """
        ...