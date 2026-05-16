# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/infrastructure/ui/progress_notifier_adapter.py
from rich.text import Text
from rich.console import Console, Group
from rich.spinner import Spinner
from rich.text import Text
from rich.live import Live
from typing import Tuple
from threading import Thread, Event, Lock

from lab.core.dtos.EventInfo import EventInfo

class ProgressNotifierAdapter:

    def __init__(self):
        self.console = Console()
        self.render_lock = Lock()  

    def _spinner_task(self, stop_event: Event, finished_event: Event, event_info: EventInfo) -> None:
        """Spinner que corre hasta que stop_event este activado"""
        import time
        spinner_line = Group(
            Spinner("dots", text=Text(event_info.name, style="default not bold"))
        )
        with self.render_lock:
            with Live(console=self.console, refresh_per_second=10) as live:
                live.update(spinner_line)
                while not stop_event.is_set():
                    time.sleep(0.05)
                if event_info.failed:
                    final_text = (
                        Text("FAILED\t", style="red")
                        + Text(event_info.name, style="default bold")
                    )
                    final_text.append(Text(f"\n{event_info.error_msg}", style="italic yellow"))
                else:
                    final_text = (
                        Text("SUCCESS\t", style="green")
                        + Text(event_info.name, style="default bold")
                    )
                live.update(final_text)
                finished_event.set()

    def start(self, event_info: EventInfo) -> Tuple[Event, Event]:
        """
        Inicia un spinner con el texto dado.
        Devuelve un Event que debe ser activado cuando la tarea termine.
        """
        stop_event = Event()
        finished_event = Event()
        # Si daemon=True → el hilo no bloquea que el programa termine.
        #   Cuando el hilo principal termina, todos los threads daemon se cierran automáticamente, aunque estén en bucle.
        # Si daemon=False (por defecto) → el hilo obliga al programa a esperar hasta que termine, aunque el hilo principal haya acabado.
        thread = Thread(target=self._spinner_task, args=(stop_event, finished_event, event_info), daemon=False)
        thread.start()
        return stop_event,finished_event

    def finish(self, spinner_handle: Event, finished_event: Event) -> None:
        """
        Detiene el spinner y muestra el resultado final
        """
        spinner_handle.set()
        finished_event.wait()
