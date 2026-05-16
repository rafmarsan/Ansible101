# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/core/dtos/EventInfo.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class EventInfo:
    """
    Data Transfer Object (DTO) para la informacion de un evento.
    Se utiliza para transferir datos de estado entre capas
    """
    name: str
    failed: bool = False
    error_msg: Optional[str] = None
