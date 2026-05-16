<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 7: Gestión de Bases de Datos con PostgreSQL

## 🎯 Objetivo general

Al finalizar este módulo, serás capaz de:

1. Instalar y configurar PostgreSQL 16 mediante un **rol dedicado**
2. Inicializar el cluster (bases de datos, usuarios y permisos) usando Ansible
3. Ejecutar consultas SQL desde un playbook

---

## 🛞 Comandos del ejercicio

Para iniciar el ejercicio, ejecuta:
```shell
lab start databases
```

Para evaluar el ejercicio, ejecuta:
```shell
lab grade databases
```

---

## 📘 Instalación y Configuración de PostgreSQL usando roles

### 🏗️ Estructura del rol

```
roles/
  postgresql/
    defaults/
      main.yml
    tasks/
      main.yml
      install.yml
      configure.yml
    templates/
      pg_hba.conf.j2
    handlers/
      main.yml
```

---

**defaults/main.yml**
```yaml
postgresql_version: 16
postgresql_port: 5432
postgresql_listen_address: "0.0.0.0"
postgresql_db_name: appdb
postgresql_db_user: appuser
postgresql_db_password: ansible_123
```

---

**templates/pg_hba.conf.j2**
```
# cualquier usuario del sistema puede conectarse a cualquier base de datos sin contraseña usando el socket Unix
local   all             all                                     trust
# cualquier host puede conectarse via TCP/IP, pero debe usar contraseña
host    all             all             0.0.0.0/0               md5
```

---

**tasks/main.yml**
```yaml
- name: Instalar PostgreSQL
  ansible.builtin.include_tasks: install.yml

- name: Configurar PostgreSQL
  ansible.builtin.include_tasks: configure.yml
```

---

**tasks/install.yml**
```yaml
---
- name: Instalar repositorio oficial de PostgreSQL
  become: true
  ansible.builtin.dnf:
    name: "https://download.postgresql.org/pub/repos/yum/reporpms/EL-{{ ansible_distribution_major_version }}-{{ ansible_architecture }}/pgdg-redhat-repo-latest.noarch.rpm"
    state: present
    disable_gpg_check: true

- name: Deshabilitar PostgreSQL del AppStream
  become: true
  ansible.builtin.shell: dnf -qy module disable postgresql
  ignore_errors: true

- name: Instalar PostgreSQL Server
  become: true
  ansible.builtin.package:
    name:
      - "postgresql{{ postgresql_version }}"
      - "postgresql{{ postgresql_version }}-server"
    state: present
```

---

**tasks/configure.yml**
```yaml
- name: Inicializar el repositorio
  become: true
  ansible.builtin.shell: /usr/pgsql-{{ postgresql_version }}/bin/postgresql-{{ postgresql_version }}-setup initdb
  args:
    creates: "/var/lib/pgsql/{{ postgresql_version }}/data/PG_VERSION"

- name: Configurar el servicio
  become: true
  ansible.builtin.service:
    name: postgresql-{{ postgresql_version }}
    enabled: true
    state: started

- name: Copiar pg_hba.conf
  become: true
  become_user: postgres
  ansible.builtin.template:
    src: pg_hba.conf.j2
    dest: "/var/lib/pgsql/{{ postgresql_version }}/data/pg_hba.conf"
  notify: Reiniciar PostgreSQL

- name: Activamos el listener
  become: true
  become_user: postgres
  ansible.builtin.replace:
    path: /var/lib/pgsql/{{ postgresql_version }}/data/postgresql.conf
    regexp: "^#listen_addresses = 'localhost'"
    replace: "listen_addresses = '{{ postgresql_listen_address }}'"
  notify: Reiniciar PostgreSQL

- name: Activamos el puerto
  become: true
  become_user: postgres
  ansible.builtin.replace:
    path: /var/lib/pgsql/{{ postgresql_version }}/data/postgresql.conf
    regexp: '^\s*#?\s*port\s*=.*$'
    replace: 'port = {{ postgresql_port }}'
  notify: Reiniciar PostgreSQL

- ansible.builtin.meta: flush_handlers

- name: Esperar a que {{ postgresql_port }} este activo
  become: true
  ansible.builtin.wait_for:
    host: localhost
    port: "{{ postgresql_port }}"
    delay: 5
    timeout: 60
    state: started

- name: Testar conexion a la instancia
  become: true
  become_user: postgres
  become_flags: -i
  ansible.builtin.shell:
    cmd: psql -p {{ postgresql_port }} -t -c "select version();"
  register: version_output

- name: Seteamos password al usuario 'postgres'
  become: true
  become_user: postgres
  become_flags: -i
  ansible.builtin.shell:
    cmd: psql -p {{ postgresql_port }} -c "ALTER USER postgres WITH PASSWORD '{{ postgresql_db_password }}';"

- name: Mostramos la version instalada
  ansible.builtin.debug:
    msg: 
      - "Instalada la version:"
      - "{{ version_output.stdout | trim }}"
```

---

**handlers/main.yml**
```yaml
- name: Reiniciar PostgreSQL
  become: true
  ansible.builtin.service:
    name: "postgresql-{{ postgresql_version }}"
    state: restarted
```

---

## 📘 Playbook principal

**databases.yml**
```yaml
---
- hosts: dbservers
  gather_facts: true
  roles:
    - role: postgresql
```

!!! info "Ejecución del playbook"
    Tras ejecutar **sin errores** el playbook 
    ```shell
    ansible-playbook databases.yml
    ```
    deberias poder logar en la máquina con 
    ```shell
    ssh db1
    ```
    cambiar al usuario `postgres` con 
    ```shell
    sudo su - postgres
    ```
    y logar en la instancia con el comando 
    ```shell
    psql
    ```

---

## 📚 Ejercicio 1 — Cambiar el puerto de PostgreSQL

Modificar:
```yaml
postgresql_port: 5433
```

Y probar conexión, usando como password `ansible_123`:
```bash
psql -h localhost -p 5433
```

??? tip "Solucion"
    En **postgresql/defaults/main.yml** modificar `postgresql_port: 5433` PostgreSQL se reiniciará automaticamente por handler.
---

## 📚 Ejercicio 2 — Añadir una tabla

!!! danger
    Para el laboratorio vamos a usar la base de datos **postgres**, pero NO es una buena práctica

Crear el fichero **postgresql/tasks/database.yml**:
```yaml
- name: Crear tabla empleados
  become: true
  become_user: postgres
  become_flags: -i
  ansible.builtin.shell: |
    psql -p {{ postgresql_port }} -d "postgres" -c "
      CREATE TABLE IF NOT EXISTS empleados (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
      );
    "
```

!!! note
    RECUERDA añadir el nuevo fichero **database.yml** en **postgresql/tasks/main.yml**
    ??? tip "Solucion"
        ```yaml
        - name: Creacion de tablas y usuarios
          ansible.builtin.include_tasks: database.yml
        ```

---

## 📚 Ejercicio 3 — Insertar datos desde Ansible

Añadir una tarea en **postgresql/tasks/database.yml**:
```yaml
- name: Insertar usuario admin
  become: true
  become_user: postgres
  become_flags: -i
  ansible.builtin.shell: |
    psql -p {{ postgresql_port }} -d "postgres" -c "INSERT INTO empleados (username) VALUES ('admin');"
```

---

## 📚 Ejercicio 4 — Crear varios usuarios dinámicamente

Añadir lista en **defaults/main.yml**:
```yaml
postgresql_initial_users:
  - alice
  - bob
  - charlie
```

Añadir una tarea en **postgresql/tasks/database.yml**:
```yaml
- name: Insertar usuarios iniciales
  become: true
  become_user: postgres
  become_flags: -i
  ansible.builtin.shell:
    cmd: psql -p {{ postgresql_port }} -d "postgres" -c "INSERT INTO empleados (username) VALUES ('{{ nombre_empleado }}');"
  loop: "{{ postgresql_initial_users }}"
  loop_control:
    loop_var: nombre_empleado
```

!!! info "Validar"
    Tras ejecutar **sin errores** el playbook 
    ```shell
    ansible-playbook databases.yml
    ```
    deberias poder logar en la máquina con 
    ```shell
    ssh db1
    ```
    cambiar al usuario `postgres` con 
    ```shell
    sudo su - postgres
    ```
    y logar en la instancia con el comando 
    ```shell
    export PGPORT=5433
    psql
    ```
    ```sql
    select * from empleados;
    ```
    y ver algo como:
    ```
    postgres=# select * from empleados;
    id | username |         created_at
    ----+----------+----------------------------
      1 | admin    | 2025-11-27 20:55:37.380092
      2 | alice    | 2025-11-27 20:55:37.802237
      3 | bob      | 2025-11-27 20:55:38.21942
      4 | charlie  | 2025-11-27 20:55:38.629579
    ```