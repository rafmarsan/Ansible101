# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/core/interfaces/container_port.py
from typing import Dict, Protocol, Tuple, Optional, Any, runtime_checkable

@runtime_checkable
class ContainerPort(Protocol):
    """
    Define el contrato para la gestion de contenedores.
    """
    engine: str
    client: Any
    def init_client(self) -> Tuple[bool, str]:
        """
        Inicializa el cliente del container runtime
        """
        ...

    def build_image(
        self,
        image: Tuple[str, Dict[str, str]]
    ) -> Tuple[bool, str]:
        """
        Construye la imagen Docker con el tag `name` usando el Dockerfile especificado
        Devuelve: (failed: bool, error_output: str)
        """
        ...

    def run_container(
        self,
        image: str,
        name: str,
        ports: Optional[dict] = None,
    ) -> Tuple[Any, bool, str]:
        """
        Lanza un contenedor y devuelve (container_object, failed: bool, error_output: str).
        """
        ...

    def remove_container(
        self,
        name: str,
    ) -> Tuple[bool, str]:
        """
        Elimina un contenedor y devuelve (failed: bool, error_output: str).
        """
        ...