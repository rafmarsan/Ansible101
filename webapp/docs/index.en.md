<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# Welcome to Ansible101 Lab

## Requirements

!!! info
    **ONLY** supported on Linux and on [Windows with WSL](./wsl.md)

It is necessary to install Podman: [https://podman.io/docs/installation#installing-on-linux](https://podman.io/docs/installation#installing-on-linux)


## Enable Podman API socket

Verify that the socket exists:
```bash
ls -l /run/user/$UID/podman/podman.sock
```

If it appears, the API is enabled.

If it does not exist ([Common WSL errors](./wsl.md)), run:
```bash
systemctl --user enable --now podman.socket
```

This creates the socket:
```
/run/user/$UID/podman/podman.sock
```

Check that it is active:
```bash
systemctl --user status podman.socket
```

You should see something like:
```
Active: active (listening)
```

## Installation
> Python >= 3.10

1. Create a working directory and create a working **virtual environment**: 

    !!! warning
        On Debian/Ubuntu systems using Python3.1X (where X is the minor version)
        ```
        sudo apt install python3.1X-venv
        ```

```shell
mkdir -p ansible101
cd ansible101
python -m venv venv
source venv/bin/activate
```

2. Install labaratory cli
```shell
pip install https://github.com/rafmarsan/Ansible101/releases/download/v1.0.0/lab-1.0.0-py3-none-any.whl
```

    !!! note
        Since the commands **create files in the path where they are launched**, it is recommended to create a **new folder** to work in

3. Install Ansible

    Install **ansible-core**:
    ```
    pip install ansible-core==2.16.14
    ```

    Verify the installed version:
    ```bash
    ansible --version
    ```

## Commands

- `lab [OPTIONS] COMMAND [ARGS]...` - Command to interact with the lab
```
Options
--install-completion     Install completion for the current shell
--show-completion        Show completion for the current shell, to copy it or customize the installation
--help               -h  Show this message and exit

Command
init        Initialize the lab and its dependencies
start       Starts the dependencies for the corresponding exercise
grade       Grades the corresponding exercise
finish      Releases the dependencies for the corresponding exercise
```

## Initialize the lab

Run the command:
```shell
lab init
```

This will begin to perform various checks, build the necessary image, and generate a `.lab_config.json` configuration file.

!!! note
    The lab initialization can take **SEVERAL MINUTES** because it has to:
    
    - Generate SSH keys
    - Build the image used during the lab
