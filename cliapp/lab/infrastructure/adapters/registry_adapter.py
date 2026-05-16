# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/infrastructure/adapters/registry_adapter.py
from lab.application.use_cases.exercise import EXERCISES
from lab.application.use_cases.grader import GRADERS
import importlib.resources as resources
from tempfile import NamedTemporaryFile

class RegistryAdapter:

    def auto_discover_exercises(self):
        return EXERCISES

    def auto_discover_graders(self):
        return GRADERS

    def auto_discover_images(self):
        """
        Recorre todos los Containerfile en lab/infrastructure/containerfiles/
        y registra los tags e info necesaria en LAB_IMAGES

        Clave: nombre simplificado del containerfile sin extension
        Valor: contenido del containerfile y tag de la imagen
        """
        LAB_IMAGES = {}
        package = "lab.infrastructure.containerfiles"

        for containerfile in resources.files(package).iterdir():
            if containerfile.name.endswith(".Containerfile"):
                # Leer contenido del archivo usando el propio objeto
                content = containerfile.read_text()
                name = containerfile.name.replace(".Containerfile", "")
                name = name.replace("docker-","lab-").replace("podman-","lab-")
                tag = f"{name}:latest"
                LAB_IMAGES[name] = {
                    "content": content,
                    "tag": tag
                }
        return LAB_IMAGES

    def write_containerfile_to_temp(self, name, lab_images):
        """
        Crea un archivo temporal con el contenido del containerfile
        y devuelve la ruta del archivo
        """
        content = lab_images[name]["content"]
        with NamedTemporaryFile("w+", delete=False) as tmp:
            tmp.write(content)
            return tmp.name
