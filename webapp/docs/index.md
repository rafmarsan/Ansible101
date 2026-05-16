<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# Bienvenido a Ansible101 Lab

## Requisitos

!!! info
    **SOLO** sorpotado en Linux y en [Windows con WSL](./wsl.md)

Es necesario instalar Podman: [https://podman.io/docs/installation#installing-on-linux](https://podman.io/docs/installation#installing-on-linux)


## Habilitar el socket API de Podman

Verificar que el socket existe:
```bash
ls -l /run/user/$UID/podman/podman.sock
```

Si aparece, la API está habilitada.

Si no existe ([Errores comunes en WSL](./wsl.md)), ejecuta:
```bash
systemctl --user enable --now podman.socket
```

Esto crea el socket:
```
/run/user/$UID/podman/podman.sock
```

Comprueba que está activo:
```bash
systemctl --user status podman.socket
```

Debes ver algo como:
```
Active: active (listening)
```

Verificar que el socket existe:
```bash
ls -l /run/user/$UID/podman/podman.sock
```

Si aparece, la API está habilitada.

## Instalación
> Python >= 3.10

1. Crear directorio de trabajo y crear un **virtual enviroment** de trabajo:

    !!! warning
        En sistemas Debian/Ubuntu con Python3.1X (donde X es la version minor de python)
        ```
        sudo apt install python3.1X-venv
        ```
    
```shell
mkdir -p ansible101
cd ansible101
python -m venv venv
source venv/bin/activate
```

2. Instalar el cli del labaratorio
```shell
pip install https://github.com/rafmarsan/Ansible101/releases/download/v1.0.0/lab-1.0.0-py3-none-any.whl
```

    !!! nota
        Ya que los comando **crean ficheros en la ruta donde se lanzan**, se recomienda crear una **carpeta nueva** donde trabajar

3. Instalar Ansible

    Instalar **ansible-core**:
    ```
    pip install ansible-core==2.16.14
    ```

    Verifica la versión instalada:
    ```bash
    ansible --version
    ```

## Comandos

- `lab [OPTIONS] COMMAND [ARGS]...` - Comando para interactuar con el laboratorio
```
Options
--install-completion     Install completion for the current shell
--show-completion        Show completion for the current shell, to copy it or customize the installation
--help               -h  Show this message and exit

Command
init        Inicia el laboratorio y sus dependencias
start       Inicia las dependencias del ejercicio correspondiente
grade       Evalua el ejercicio correspondiente
finish      Libera las dependencias del ejercicio correspondiente
```

## Inicializar el laboratorio

Lanzar el comando:
```shell
lab init
```

esto comenzará realizar varias comprobaciones, buildear la imagen necesaria, generará un fichero de configuración `.lab_config.json`

!!! nota
    La inicialización del labarotario puede tardar **VARIOS MINUTOS** ya que tiene que:
    
    - Generar claves SSH
    - Hacer build de la imagen que usamos durante el laboratorio
    