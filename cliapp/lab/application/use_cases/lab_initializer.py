# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/application/use_cases/lab_initializer.py
import sys
import time
from typing import Tuple

from lab.core.entities.lab import Lab
from lab.core.dtos.EventInfo import EventInfo
from lab.core.interfaces.lab_repository import LabRepository
from lab.core.interfaces.lab_port import LabPort
from lab.infrastructure.ui.progress_notifier_adapter import ProgressNotifierAdapter
from lab.infrastructure.adapters.container_adapter import ContainerAdapter
from lab.infrastructure.adapters.registry_adapter import RegistryAdapter
from lab.infrastructure.ui.i18n import get_text

class LabInitializer:

    def _deploy_priv_key(self) -> Tuple[bool, str]:
        """
        Despliega la clave privada id_lab en ~/.ssh/id_lab con permisos seguros.
        Si falla, devuelve failed=True y un mensaje descriptivo.
        """
        from pathlib import Path
        import textwrap
        failed = False
        error_output = ""
        time.sleep(1)
        try:
            private_key = textwrap.dedent("""\
                -----BEGIN OPENSSH PRIVATE KEY-----
                b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
                QyNTUxOQAAACAlNpdpQ1SOR6rkTP5ly3FWO+kRf0vD3kCUWCJXD7xITQAAAJj+Geqk/hnq
                pAAAAAtzc2gtZWQyNTUxOQAAACAlNpdpQ1SOR6rkTP5ly3FWO+kRf0vD3kCUWCJXD7xITQ
                AAAECLneRveOUfilM5jqNF0zPHOFPQYQx35/alCTryk5ntMiU2l2lDVI5HquRM/mXLcVY7
                6RF/S8PeQJRYIlcPvEhNAAAAEHVzZXJAYW5zaWJsZS1sYWIBAgMEBQ==
                -----END OPENSSH PRIVATE KEY-----
            """)
            # --- Crear ~/.ssh ---
            ssh_dir = Path.home() / ".ssh"
            ssh_dir.mkdir(mode=0o700, exist_ok=True)
            # --- Ruta final de la clave ---
            key_path = ssh_dir / "id_lab"
            # --- Escribir la clave privada (idempotente: siempre la reemplaza) ---
            key_path.write_text(private_key + "\n")
            # --- Permisos estrictos requeridos por SSH ---
            key_path.chmod(0o600)
            return False, ""   # Éxito
        except Exception as e:
            failed = True
            error_output = f"Error desplegando clave privada id_lab: {e}"
            return failed, error_output


    # def execute(self, service: LabPort, repo_adapter: LabRepository, engine: str, force: bool) -> None:
    def execute(self, service: LabPort, repo_adapter: LabRepository, lab: Lab) -> None:
        notifier = ProgressNotifierAdapter()

        event_info = EventInfo(name=get_text(lab.language,'definiendo_fichero'))
        spinner_handle, finished_event = notifier.start(event_info)
        repo_adapter.save(lab)
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name=get_text(lab.language,'verificando_ansible'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = service.verify_context()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name=get_text(lab.language,'inicializando_lab'))
        spinner_handle, finished_event = notifier.start(event_info)
        LAB_IMAGES = RegistryAdapter().auto_discover_images()
        failed, error_output = service.init(ContainerAdapter(engine=lab.engine), LAB_IMAGES)
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name=get_text(lab.language,'desplegando_clave'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._deploy_priv_key()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None
