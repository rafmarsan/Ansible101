# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/application/use_cases/grader/grader_webservers.py
from typing import Tuple, Union, List
from rich.text import Text
from lab.infrastructure.ui.i18n import get_text, get_current_language
import logging
import sys
import time

from lab.core.dtos.EventInfo import EventInfo
from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort

logger = logging.getLogger("lab")
LANG = get_current_language()

class GraderWebservers:
    """
    Logica para evaluar del ejercicio "WebServers - Practica"
    """
    def __init__(self, name: str, debug_msg: List[Union[str, Text]] = []):
        self.name = name
        self.debug_msg = debug_msg

    def _verify_apache_config(self) -> Tuple[bool, str]:
        import paramiko
        from pathlib import Path
        config_path = "/etc/httpd/conf.d/main.conf"
        line_to_search = "Listen 9090"
        time.sleep(0.5)
        failed = False
        error_output = ""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ---- Cargar ~/.ssh/config ----
            config = paramiko.SSHConfig()
            with open(Path.home() / ".ssh/config") as f:
                config.parse(f)
            host_config = config.lookup("web1")
            key_path = Path(host_config["identityfile"][0]).expanduser()
            ssh.connect(
                hostname='localhost',
                port=2232,
                username='ansible',
                key_filename=str(key_path) if key_path else None,
                allow_agent=True,
                look_for_keys=True
            )
            sftp = ssh.open_sftp()
            with sftp.open(config_path, "r") as f:
                content = f.read().decode('utf-8')
            if not line_to_search in content:
                failed = True
                error_output = get_text(LANG,'error_apache_puerto')
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output

    def _verify_custom_index(self) -> Tuple[bool, str]:
        """
        Verifica que http://localhost:8080 devuelve la pagina
        personalizada usando la libreria requests
        """
        import requests
        failed = False
        error_output = ""
        time.sleep(0.5)
        url = "http://localhost:8080"
        expected_snippet = get_text(LANG,'expected_snippet')
        try:
            response = requests.get(url, timeout=2)
            if response.status_code != 200:
                failed = True
                error_output = get_text(LANG,'error_http_status', status=response.status_code)
            content = response.text
            if not expected_snippet in content:
                failed = True
                error_output = get_text(LANG,'error_apache_pagina')
            return failed, error_output
        except Exception as e:
            return True, f"{type(e).__name__}: {e}"

    def _verify_endpoint(self) -> Tuple[bool, str]:
        """
        Verifica que http://localhost:8080/health devuelve 200 OK
        """
        import requests
        failed = False
        error_output = ""
        time.sleep(0.5)
        url = "http://localhost:8080/health"
        try:
            response = requests.get(url, timeout=2)
            if response.status_code != 200:
                failed = True
                error_output = get_text(LANG,'error_http_status', status=response.status_code)
            content = response.text
            if not 'OK' in content:
                failed = True
                error_output = get_text(LANG,'error_nginx_health')
            return failed, error_output
        except Exception as e:
            return True, f"{type(e).__name__}: {e}"

    def grade(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        event_info = EventInfo(name=get_text(LANG,'verificamos_config_apache'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_apache_config()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name=get_text(LANG,'verificamos_despliegue_custom'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_custom_index()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name=get_text(LANG,'verificamos_endpoint_health'))
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_endpoint()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

