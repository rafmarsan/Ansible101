# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

from rich.text import Text
from rich.console import Console, Group
from rich.spinner import Spinner
from rich.text import Text
from rich.live import Live
from datetime import datetime

def append_msg_with_datatime(instance, msg, last=False):
    instance.debug_msg.append(
        Text.assemble(
            (f"[{datetime.now().strftime('%m/%d/%y %H:%M:%S')}]", "dim cyan"),
            (" DEBUG    ", "green"),
            (msg, "default"),
        )
    )
    if last:
        instance.debug_msg.append('')

def check_status(failed, error_output, check_text):
    # Mostrar el spinner durante la "validacion"
    import time
    time.sleep(2)

    # Al terminar, mostrar texto plano con el resultado
    if failed:
        final_text = (
            Text("FAILED\t", style="red")
            + Text(check_text, style="default bold")
        )
        final_text.append(Text(f"\n{error_output}", style="italic yellow"))
    else:
        final_text = (
            Text("SUCCESS\t", style="green")
            + Text(check_text, style="default bold")
        )

    return final_text


def run_with_spinner(action, checks, instance):
    console = Console()
    failed = False

    for check_text, check_fn in checks:
        spinner_line = Group(
            Spinner("dots", text=Text(check_text, style="default not bold"))
        )
        with Live(console=console, refresh_per_second=10) as live:
            live.update(spinner_line)
            failed,error_output = check_fn()
            final_text = check_status(failed,error_output, check_text)
            if instance.debug_msg:
                group = Group(
                        final_text,
                        *[line for line in instance.debug_msg],
                    )
                instance.debug_msg.clear()
                live.update(group)
            else:
                live.update(final_text)
            
            if failed:
                break

    if action == 'grader' and not failed:
        console.print("\nValidacion completada", highlight=False)

    print("\n")