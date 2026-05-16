# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/infrastructure/adapters/container_adapter.py
from typing import Dict, Tuple, Optional, Any
import logging

logger = logging.getLogger("lab")

class ContainerAdapter:
    def __init__(self, engine="podman"):
        self.engine = engine
        self.client = None

    def init_client(self) -> Tuple[bool, str]:
        import shutil
        import subprocess
        failed = False
        error_output = ''
        if not shutil.which(self.engine):
            failed = True
            error_output = f"El cliente '{self.engine}' no se cuentra instalado"
            return failed, error_output
        try:
            result = subprocess.run(
                [self.engine, "info"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                failed = True
                error_output = f"No se puede contactar con la API del cliente '{self.engine}'. Revise que este inicializado con el comando `{self.engine} ps`"
                return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"No se puede contactar con la API del cliente '{self.engine}'. Revise que este inicializado con el comando `{self.engine} ps`"
            return failed, error_output

        if self.engine == "podman":
            import podman
            self.client = podman.from_env()
        # elif self.engine == "docker":
        #     import docker
        #     self.client = docker.from_env()
        return failed, error_output

    def build_image(
        self,
        image: Tuple[str, Dict[str, str]]
    ) -> Tuple[bool, str]:
        name, info = image
        failed = False
        error_output = ''

        try:
            import tempfile
            from pathlib import Path
            assert self.client is not None
            # Creamos un directorio limpio en /tmp
            with tempfile.TemporaryDirectory() as ctx_dir:
                ctx = Path(ctx_dir)
                # Creamos el Containerfile dentro del contexto limpio
                dockerfile_path = ctx / "Containerfile"
                dockerfile_path.write_text(info["content"])
                # Construir la imagen usando el Containerfile temporal
                self.client.images.build(
                    path=str(ctx),
                    dockerfile="Containerfile",
                    tag=info["tag"],
                    rm=True
                )
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"

        return failed, error_output

    def run_container(
        self,
        image: str,
        name: str,
        ports: Optional[dict] = None,
    ) -> Tuple[Any, bool, str]:
        failed = False
        error_output = ''
        container = None
        try:
            assert self.client is not None
            try:
                old = self.client.containers.get(name)
                old.remove(force=True)
            except Exception as e:
                pass

            container = self.client.containers.run(
                image=image,
                detach=True,
                name=name,
                hostname=name,
                ports=ports
            )
            return container, failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return container, failed, error_output

    def remove_container(
        self,
        name: str,
    ) -> Tuple[bool, str]:
        failed = False
        error_output = ''
        try:
            assert self.client is not None
            container = self.client.containers.get(name)
            container.remove(force=True)
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output
