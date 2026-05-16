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

## Compilación (Wheel)

Para compilar el proyecto y generar un archivo `.whl` distribuible:

```shell
cd cliapp/
pip install -r build_requirements.txt
python -m build
```

Esto genera `dist/lab-X.Y.Z-py3-none-any.whl`, que se puede publicar en GitHub Releases e instalar directamente con:

```shell
pip install https://github.com/rafmarsan/Ansible101/releases/download/vX.Y.Z/lab-X.Y.Z-py3-none-any.whl
```

<!-- <details>
<summary><h2>Laboratorio - CLI</h2></summary> -->

### Estructura de carpeta
```
.
├── LICENSE
├── README.md
├── build_requirements.txt
├── lab
│   ├── __init__.py
│   ├── application
│   │   └── use_cases
│   │       ├── exercise
│   │       │   ├── __init__.py
│   │       │   ├── exercise_databases.py
│   │       │   ├── exercise_final.py
│   │       │   ├── exercise_role.py
│   │       │   ├── exercise_vars.py
│   │       │   ├── exercise_webservers.py
│   │       │   ├── exercise_final.py
│   │       │   ├── exercise_role.py
│   │       │   ├── exercise_vars.py
│   │       │   ├── exercise_webservers.py
│   │       │   ├── solutions
│   │       │   │   └── vars.yml
│   │       │   └── template.py
│   │       ├── grader
│   │       │   ├── __init__.py
│   │       │   ├── grader_databases.py
│   │       │   ├── grader_role.py
│   │       │   ├── grader_vars.py
│   │       │   └── grader_webservers.py
│   │       └── lab_initializer.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── __init__.cpython-313.pyc
│   │   ├── dtos
│   │   │   ├── EventInfo.py
│   │   │   └── __pycache__
│   │   │       └── EventInfo.cpython-313.pyc
│   │   ├── entities
│   │   │   ├── __init__.py
│   │   │   └── lab.py
│   │   └── interfaces
│   │       ├── container_port.py
│   │       ├── exercise_port.py
│   │       ├── grader_port.py
│   │       ├── lab_port.py
│   │       ├── lab_repository.py
│   │       ├── progress_notifier_port.py
│   │       └── registry_port.py
│   ├── infrastructure
│   │   ├── __init__.py
│   │   ├── adapters
│   │   │   ├── container_adapter.py
│   │   │   ├── lab_adapter.py
│   │   │   ├── lab_repository_adapter.py
│   │   │   └── registry_adapter.py
│   │   ├── containerfiles
│   │   │   ├── docker-ssh-ol8.Containerfile.old
│   │   │   └── podman-ssh-ol8.Containerfile
│   │   └── ui
│   │       ├── __init__.py
│   │       ├── console_utils.py
│   │       ├── i18n.py
│   │       └── progress_notifier_adapter.py
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