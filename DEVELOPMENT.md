## Pruebas locales

```shell
python -m venv venv
source venv/bin/activate
cd cliapp/
pip install -e .
```

Durante `lab init` se despliega localmente una **clave privada** `id_lab` la cual permite que Ansible se conecte sin password a los contenedores de desarrollo. Durante el build de la imagen se inyecta en la **clave pública** asociada a esta clave privada para permitir el acceso.

- [lab_initializer.py](cliapp/lab/application/use_cases/lab_initializer.py)
- [podman-ssh-ol8.Containerfile](cliapp/lab/infrastructure/containerfiles/podman-ssh-ol8.Containerfile)

## Compilación

Dependencias para Linux:
```shell
sudo apt install python3-dev build-essential patchelf ccache
cd cliapp/
pip install -r build_requirements.txt
```

Fichero único:
```shell
python -m nuitka \
  --standalone \
  --onefile \
  --static-libpython=no \
  --include-data-dir=lab/infrastructure/containerfiles=lab/infrastructure/containerfiles \
  lab/main.py \
  --output-filename=lab-cli
```

### Compilación en contendor

Para dar soporte a distro de linux antiguas con glibc >= 2.28, se compilará en una imagen de Oracle Linux 8.10
```Dockerfile
FROM oraclelinux:8.10

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 1. Habilitar EPEL (necesario para patchelf) y dependencias de compilación
RUN dnf -y install oracle-epel-release-el8 && \
    dnf -y install \
    gcc \
    gcc-c++ \
    make \
    patchelf \
    libffi-devel \
    zlib-devel \
    openssl-devel \
    bzip2-devel \
    xz-devel \
    readline-devel \
    sqlite-devel \
    findutils \
    which && \
    dnf clean all

# 2. Instalar Python 3.11 directamente (usando los nombres de tu búsqueda)
RUN dnf install -y \
    python3.11 \
    python3.11-devel \
    python3.11-pip \
    python3.11-setuptools \
    python3.11-wheel && \
    dnf clean all

# 3. Usuario builder
RUN useradd -m builder
USER builder
WORKDIR /home/builder

# 4. Virtualenv usando Python 3.11
RUN python3.11 -m venv venv
ENV PATH="/home/builder/venv/bin:$PATH"

# 5. Instalación controlada de dependencias
# Instalamos primero las herramientas base en el orden correcto
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir setuptools==80.1.0 wheel toml

# Instalamos Nuitka y tus librerías de aplicación
RUN pip install --no-cache-dir \
    nuitka==2.7.14 \
    typer==0.17.4 \
    typing_extensions==4.15.0 \
    rich==14.1.0 \
    podman==5.6.0 \
    paramiko==4.0.0
```

<!-- ```shell
podman run --name lab-build -it \
  -v "$PWD:/src:Z" \
  -w /src \
  lab-build-ol8 \
  bash -c "
    python -m nuitka \
    --standalone \
    --onefile \
    --static-libpython=no \
    --include-distribution-metadata=lab \
    --include-data-dir=lab/infrastructure/containerfiles=lab/infrastructure/containerfiles \
    --output-dir=/home/builder/build_output \
    --output-filename=lab-cli \
    lab/main.py
"
``` -->
```shell
podman rm -f lab-build
podman run --name lab-build -it \
  -v "$PWD:/src:Z" \
  lab-build-ol8 \
  bash -c "
    cp -r /src /tmp/build_dir && \
    cd /tmp/build_dir && \
    pip install -r build_requirements.txt && \
    pip install . && \
    python -m nuitka \
      --standalone \
      --onefile \
      --static-libpython=no \
      --include-distribution-metadata=lab \
      --include-data-dir=lab/infrastructure/containerfiles=lab/infrastructure/containerfiles \
      --include-package=lab \
      --include-module=yaml \
      --output-dir=/home/builder/build_output \
      --output-filename=lab-cli \
      lab/main.py
"
```

```shell
podman cp lab-build:/home/builder/build_output/lab-cli lab && \
podman rm -f lab-build
```

<!-- Carpeta con binario y dependencias:
```shell
python -m nuitka \
  --standalone \
  --assume-yes-for-downloads \
  --no-onefile \
  --static-libpython=no \
  --include-data-dir=lab/infrastructure/containerfiles=lab/infrastructure/containerfiles \
  --lto=yes \
  --pgo-python=lab/main.py \
  lab/main.py \
  --output-filename=lab-cli
``` -->


<!-- <details>
<summary><h2>Laboratorio - CLI</h2></summary> -->

### Estructura de carpeta
```
.
├── lab
│   ├── __init__.py
│   ├── grade
│   │   ├── __init__.py
│   │   ├── grade_functions.py
│   │   ├── grade.py
│   │   └── scripts
│   │       ├── __init__.py
│   │       ├── grade_error.py
│   │       ├── grade_ok.py
│   │       └── grade_rich.py
│   └── main.py
└── pyproject.toml
```

## Apuntes

### Live

Lo usas como un gestor de contexto (`with` Live(...) as live:):
- Cuando entras al bloque `with`: Rich "captura" la línea actual de la terminal. Cualquier cosa que live.console.print() (o console.print() si no estás usando live.console explícitamente dentro del Live para ese contenido específico) imprima dentro de ese bloque, se mostrará en el área "en vivo" y se actualizará.
- Dentro del bloque `with`: Puedes cambiar el contenido que se muestra en el área de Live simplemente volviendo a llamar a live.update() (aunque a menudo no es necesario, ya que console.print dentro del contexto de Live ya actualiza el contenido).
- Cuando sales del bloque `with`:
  + Si `transient=True` (como lo tenemos), el contenido de Live desaparece, dejando la terminal limpia como estaba antes de que Live se activara. Esto es ideal para barras de progreso o spinners que solo quieres ver mientras la tarea se ejecuta.
  + Si `transient=False` (por defecto), el contenido final de Live permanece en la terminal.



### Enlaces de interés
- [Libreria click](https://click.palletsprojects.com/en/8.1.x/)
- [click-completion](https://github.com/click-contrib/click-completion?tab=readme-ov-file)
- [Packaging Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)