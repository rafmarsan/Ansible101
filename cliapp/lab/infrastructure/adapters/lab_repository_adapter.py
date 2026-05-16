# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/infrastructure/adapters/lab_repository_adapter.py
import json
from pathlib import Path
from typing import Tuple
import logging

from lab.core.entities.lab import Lab

LAB_CONFIG_PATH = Path.cwd() / ".lab_config.json"
logger = logging.getLogger("lab")

class LabRepositoryAdapter:
    
    # def load(self, force: bool = False) -> Tuple[bool, Lab, str]:
    def load(self) -> Tuple[bool, Lab, str]:
        import time
        time.sleep(1)
        failed = False
        error_output = ''
        if not LAB_CONFIG_PATH.exists():
            failed = True
            error_output = f"No existe ninguna instancia de Lab. Para crear una nueva instancia, usar 'lab init <engine>'"
            return failed, Lab(), error_output
        try:
            data = json.loads(LAB_CONFIG_PATH.read_text())
        except json.JSONDecodeError as e:
            error_output = f"{type(e).__name__}: {e}"
            return False, Lab(), error_output
        engine = data.get('engine')
        language = data.get('language', 'es')
        lab = Lab(engine=engine, language=language) 
        # if LAB_CONFIG_PATH.exists() and not force:
        #     failed = True
        #     error_output = f"Ya existe una instancia de Lab [engine={lab.engine}]. Para crear una nueva instancia, usar 'lab init <engine> -f' o borrar el fichero '~/.lab_config.json'"
        #     return failed, lab, error_output
        return failed, lab, error_output

    def save(self, lab: Lab) -> Tuple[bool, str]:
        """
        Persiste el estado actual de la entidad Lab recorriendo sus atributos.
        """
        import inspect
        failed = False
        error_output = ''
        data = {}
        # for key, value in vars(lab).items():
        #     data[key.replace('_','')] = value
        for name, _ in inspect.getmembers(lab.__class__, lambda x: isinstance(x, property)):
            data[name] = getattr(lab, name)
        LAB_CONFIG_PATH.write_text(json.dumps(data))
        return failed, error_output
