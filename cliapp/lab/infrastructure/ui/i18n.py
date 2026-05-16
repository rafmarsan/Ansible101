# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

TEXTS = {
    "es": {
        "error_nginx_health": "El endpoint de NGINX /health no devuelve 200 OK. Revise el template 'reverse-proxy.conf.j2' y la tarea de despliegue del template",
        "verificamos_endpoint_health": "Verificamos el endpoint /health",
        "error_apache_pagina": "El servidor Apache no esta devolviendo la pagina esperada. Revise el template 'index.html.j2' y la tarea de despliegue del template",
        "error_http_status": "HTTP {status}: la pagina no responde correctamente",
        "verificamos_despliegue_custom": "Verificamos el despliegue de la pagina custom",
        "error_apache_puerto": "Apache no tiene configurado el puerto 9090. Revise roles/apache/defaults/main.yml",
        "verificamos_config_apache": "Verificamos la configuracion de Apache",
        "error_vars_no_definidas": "No se han definido las variables {vars}",
        "verificamos_fichero_index": "Verificamos el fichero /tmp/demo/index.html",
        "verificamos_dir_tmp_demo": "Verificamos el directorio /tmp/demo",
        "error_contenido_index": "El contenido de index.html NO es el solicitado",
        "verificamos_contenido_fichero": "Verificamos el contenido del fichero /tmp/demo/index.html",
        "error_fichero_no_existe": "El fichero {file} NO existe",
        "verificamos_existe_fichero": "Verificamos SI EXISTE el fichero /tmp/demo/index.html",
        "error_dir_no_existe": "El directorio {dir} NO existe",
        "verificamos_existe_dir": "Verificamos SI EXISTE el directorio /tmp/demo",
        "error_no_include_tasks": "No se usado 'include_tasks' en el punto de entrada del rol",
        "verificamos_def_role": "Verificamos la definicion del role",
        "error_no_rol_definido": "No se han definido el rol",
        "verificamos_def_playbook": "Verificamos la definicion del playbook",
        "error_no_usuarios": "No se han creados los usuarios en la tabla 'empleados' en PostgreSQL . Repase 'Ejercicio 3 y 4'",
        "verificamos_usuarios_creados": "Verificamos si se han creados los usuarios",
        "error_no_tabla_empleados": "No existe la tabla 'empleados' en PostgreSQL . Repase 'Ejercicio 2 — Añadir una tabla'",
        "verificamos_tabla_empleados": "Verificamos si existe la tabla empleados",
        "error_pg_port": "PostgreSQL no tiene configurado el puerto 5433. Revise roles/postgresql/defaults/main.yml",
        "error_exec_db1": "Error ejecutando el comando en db1: {error}",
        "verificamos_config_listener": "Verificamos la configuracion del listener",
        "eliminando_containers_web1_db1": "Eliminando containers: web1, db1",
        "eliminando_container_web1": "Eliminando container web1",
        "eliminando_container_db1": "Eliminando container db1",
        "creacion_playbook_site": "Creacion del playbook principal: site.yml",
        "creacion_playbook_webservers": "Creacion del playbook principal: webservers.yml",
        "creacion_playbook_databases": "Creacion del playbook principal: databases.yml",
        "limpiando_carpetas_dynamic": "Limpiando carpetas NO necesarias del rol {role_name}",
        "limpiando_carpetas_nginx": "Limpiando carpetas NO necesarias del rol Nginx",
        "limpiando_carpetas_apache": "Limpiando carpetas NO necesarias del rol Apache",
        "limpiando_carpetas_postgresql": "Limpiando carpetas NO necesarias del rol PostgreSQL",
        "creando_role_dynamic": "Creando ansible role: {role_name}",
        "creando_role_nginx": "Creando ansible role: Nginx",
        "creando_role_apache": "Creando ansible role: Apache",
        "creando_role_postgresql": "Creando ansible role: PostgreSQL",
        "preparando_entorno_ansible": "Preprando el entorno de Ansible",
        "configurando_ssh_contenedor": "Configurando ~/.ssh para acceder al contenedor",
        "creando_containers_web1_db1": "Creando containers: web1, db1",
        "creando_container_web1": "Creando container: web1",
        "creando_container_db1": "Creando container: db1",
        "error_create_site_yml": "Fallo en la creacion del fichero: site.yml",
        "error_create_webservers_yml": "Fallo en la creacion del fichero: webservers.yml",
        "error_create_databases_yml": "Fallo en la creacion del fichero: databases.yml",
        "error_env_config": "Fallo en la configuracion del entorno",
        "error_ssh_config": "Error configurando ~/.ssh/config: {e}",
        "error_delete_role": "Error eliminando el role '{role_name}': {e}",
        "error_remove_role_site": "Fallo al eliminar el role y el fichero 'site.yml'. Situese en el directorio correcto",
        "eliminando_containers_ejercicio": "Eliminando containers del ejercicio",
        "limpiando_carpetas_rol": "Limpiando carpetas NO necesarias del rol",
        "creando_ansible_role": "Creando Ansible role",
        "error_remove_vars_lab": "Fallo al eliminar el fichero: vars_lab.yml. Situese en el directorio del fichero",
        "error_create_vars_lab": "Fallo en la creacion del fichero: vars_lab.yml",
        "eliminando_ficheros_ejercicio": "Eliminando ficheros del ejercicio",
        "creando_fichero_base": "Creando fichero base",
        "app_help": "Un app para tus herramientas de laboratorio.",
        "engine_help": "Container engine a usar",
        "debug_help": "Activa el modo debug",
        "init_help": "Inicia el laboratorio y sus dependencias",
        "start_exercise_help": "Nombre del ejercicio a iniciar",
        "start_help": "Inicia las dependencias del ejercicio correspondiente",
        "error_exercise_not_found": "\n❌ Error: Ejercicio '{exercisename}' no existe.\n",
        "grade_exercise_help": "Nombre del ejercicio a evaluar",
        "grade_help": "Evalua el ejercicio correspondiente",
        "finish_exercise_help": "Nombre del ejercicio a finalizar.",
        "finish_help": "Libera las dependencias del ejercicio correspondiente",
        "version_help": "Muestra la version",
        "prompt_language": "Selecciona el idioma / Select language (es/en)",
        "prompt_language_invalid": "Idioma inválido. Usa 'es' o 'en'.",
        "verificando_ansible": "Verificando si Ansible esta instalado",
        "ansible_no_disponible": "Ansible no esta disponible en el entorno actual",
        "error_ansible_version": "No se pudo ejecutar `ansible --version`. Verifica la instalacion",
        "error_ansible_path": "No se encontro el ejecutable de Ansible en el PATH",
        "definiendo_fichero": "Definiendo fichero de configuracion",
        "inicializando_lab": "Inicializando laboratorio",
        "desplegando_clave": "Desplegando la clave privada del laboratorio",
        "grade_role_file_content": "Servidor escuchando en el puerto 8080",
        "expected_snippet": "¡Apache funcionando!",
        "table_name": "empleados"
    },
    "en": {
        "error_nginx_health": "The NGINX /health endpoint does not return 200 OK. Check the 'reverse-proxy.conf.j2' template and the deployment task",
        "verificamos_endpoint_health": "Verifying /health endpoint",
        "error_apache_pagina": "The Apache server is not returning the expected page. Check the 'index.html.j2' template and the deployment task",
        "error_http_status": "HTTP {status}: the page is not responding correctly",
        "verificamos_despliegue_custom": "Verifying custom page deployment",
        "error_apache_puerto": "Apache is not configured on port 9090. Check roles/apache/defaults/main.yml",
        "verificamos_config_apache": "Verifying Apache configuration",
        "error_vars_no_definidas": "Variables {vars} have not been defined",
        "verificamos_fichero_index": "Verifying file /tmp/demo/index.html",
        "verificamos_dir_tmp_demo": "Verifying directory /tmp/demo",
        "error_contenido_index": "The content of index.html is NOT as requested",
        "verificamos_contenido_fichero": "Verifying content of file /tmp/demo/index.html",
        "error_fichero_no_existe": "File {file} DOES NOT exist",
        "verificamos_existe_fichero": "Verifying IF FILE /tmp/demo/index.html EXISTS",
        "error_dir_no_existe": "Directory {dir} DOES NOT exist",
        "verificamos_existe_dir": "Verifying IF DIRECTORY /tmp/demo EXISTS",
        "error_no_include_tasks": "'include_tasks' was not used in the role entry point",
        "verificamos_def_role": "Verifying role definition",
        "error_no_rol_definido": "Role has not been defined",
        "verificamos_def_playbook": "Verifying playbook definition",
        "error_no_usuarios": "Users were not created in the 'employees' table in PostgreSQL. Review 'Exercise 3 and 4'",
        "verificamos_usuarios_creados": "Verifying if users were created",
        "error_no_tabla_empleados": "Table 'employees' does not exist in PostgreSQL. Review 'Exercise 2 — Add a table'",
        "verificamos_tabla_empleados": "Verifying if 'employees' table exists",
        "error_pg_port": "PostgreSQL is not configured on port 5433. Check roles/postgresql/defaults/main.yml",
        "error_exec_db1": "Error executing command in db1: {error}",
        "verificamos_config_listener": "Verifying listener configuration",
        "eliminando_containers_web1_db1": "Removing containers: web1, db1",
        "eliminando_container_web1": "Removing container web1",
        "eliminando_container_db1": "Removing container db1",
        "creacion_playbook_site": "Creating main playbook: site.yml",
        "creacion_playbook_webservers": "Creating main playbook: webservers.yml",
        "creacion_playbook_databases": "Creating main playbook: databases.yml",
        "limpiando_carpetas_dynamic": "Cleaning unnecessary folders from {role_name} role",
        "limpiando_carpetas_nginx": "Cleaning unnecessary folders from Nginx role",
        "limpiando_carpetas_apache": "Cleaning unnecessary folders from Apache role",
        "limpiando_carpetas_postgresql": "Cleaning unnecessary folders from PostgreSQL role",
        "creando_role_dynamic": "Creating ansible role: {role_name}",
        "creando_role_nginx": "Creating ansible role: Nginx",
        "creando_role_apache": "Creating ansible role: Apache",
        "creando_role_postgresql": "Creating ansible role: PostgreSQL",
        "preparando_entorno_ansible": "Preparing Ansible environment",
        "configurando_ssh_contenedor": "Configuring ~/.ssh to access container",
        "creando_containers_web1_db1": "Creating containers: web1, db1",
        "creando_container_web1": "Creating container: web1",
        "creando_container_db1": "Creating container: db1",
        "error_create_site_yml": "Failed to create file: site.yml",
        "error_create_webservers_yml": "Failed to create file: webservers.yml",
        "error_create_databases_yml": "Failed to create file: databases.yml",
        "error_env_config": "Failed to configure environment",
        "error_ssh_config": "Error configuring ~/.ssh/config: {e}",
        "error_delete_role": "Error deleting role '{role_name}': {e}",
        "error_remove_role_site": "Failed to remove role and 'site.yml' file. Ensure you are in the correct directory",
        "eliminando_containers_ejercicio": "Removing exercise containers",
        "limpiando_carpetas_rol": "Cleaning unnecessary role folders",
        "creando_ansible_role": "Creating Ansible role",
        "error_remove_vars_lab": "Failed to remove file: vars_lab.yml. Ensure you are in the correct directory",
        "error_create_vars_lab": "Failed to create file: vars_lab.yml",
        "eliminando_ficheros_ejercicio": "Removing exercise files",
        "creando_fichero_base": "Creating base file",
        "app_help": "An app for your lab tools.",
        "engine_help": "Container engine to use",
        "debug_help": "Enable debug mode",
        "init_help": "Initialize the lab and its dependencies",
        "start_exercise_help": "Name of the exercise to start",
        "start_help": "Starts the dependencies for the corresponding exercise",
        "error_exercise_not_found": "\n❌ Error: Exercise '{exercisename}' does not exist.\n",
        "grade_exercise_help": "Name of the exercise to grade",
        "grade_help": "Grades the corresponding exercise",
        "finish_exercise_help": "Name of the exercise to finish.",
        "finish_help": "Releases the dependencies for the corresponding exercise",
        "version_help": "Shows the version",
        "prompt_language": "Select language (es/en)",
        "prompt_language_invalid": "Invalid language. Use 'es' or 'en'.",
        "verificando_ansible": "Verifying if Ansible is installed",
        "ansible_no_disponible": "Ansible is not available in the current environment",
        "error_ansible_version": "Could not execute `ansible --version`. Check installation",
        "error_ansible_path": "Ansible executable not found in PATH",
        "definiendo_fichero": "Defining configuration file",
        "inicializando_lab": "Initializing lab",
        "desplegando_clave": "Deploying lab private key",
        "grade_role_file_content": "Server listening on port 8080",
        "expected_snippet": "Apache is working!",
        "table_name": "employees"
    }
}

import json
from pathlib import Path

def get_current_language():
    config_path = Path.cwd() / ".lab_config.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text())
            return data.get("language", "es")
        except:
            pass
    return "es"

def get_text(lang: str = None, key: str = None, **kwargs) -> str:
    """Devuelve el texto traducido. Si no existe la clave, devuelve la clave."""
    if not lang:
        lang = get_current_language()
    # Si se nos olvida la clave pero la pasamos como primer argumento:
    if key is None:
        key = lang
        lang = get_current_language()
        
    # Busca el diccionario del idioma solicitado (por ejemplo: TEXTS["en"])
    # Si ese idioma no existe en TEXTS, usa por defecto el diccionario de español (TEXTS["es"])
    lang_dict = TEXTS.get(lang, TEXTS["es"])

    # Busca la clave en el idioma elegido. Si no la encuentra, activa el plan de rescate:
    # - Primero intenta buscar la clave en el diccionario de español (TEXTS["es"])
    # - Si tampoco está en español, devuelve el texto de la propia 'key' literal.
    text = lang_dict.get(key, TEXTS["es"].get(key, key))

    if kwargs:
        return text.format(**kwargs)
    return text
