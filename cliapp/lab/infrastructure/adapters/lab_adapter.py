# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/infrastructure/adapters/lab_adapter.py
from typing import Tuple, Dict
import logging

from lab.core.interfaces.container_port import ContainerPort
from lab.infrastructure.ui.i18n import get_text, get_current_language

logger = logging.getLogger("lab")
LANG = get_current_language()

class LabAdapter:

    def verify_context(self) -> Tuple[bool, str]:
        import subprocess
        import shutil
        failed: bool = False
        error_output: str = ''
        # comprobamos si el ejecutable `ansible` existe en PATH
        ansible_path = shutil.which("ansible")
        # if ansible_path is None:
        if ansible_path is None:
            failed = True
            error_output = get_text(LANG,'ansible_no_disponible')
            return failed, error_output 
        try:
            result = subprocess.run(
                ["ansible", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            version_line = result.stdout.splitlines()[0]
            return failed, error_output
        except subprocess.CalledProcessError as e:
            failed = True
            error_output = get_text(LANG,'error_ansible_version')
            return failed, error_output 
        except FileNotFoundError:
            failed = True
            error_output = get_text(LANG,'error_ansible_path')
            return failed, error_output 

    
    def init(self, container_service: ContainerPort, LAB_IMAGES: Dict[str, Dict[str, str]]) -> Tuple[bool, str]:
        failed = False
        error_output = ''
        failed, error_output = container_service.init_client()
        if failed:
            return failed, error_output
        for image in LAB_IMAGES.items():
            failed, error_output = container_service.build_image(image)
            if failed:
                break
        return failed, error_output


