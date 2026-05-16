<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 1: Introducción a Ansible

## 🎯 Objetivos

Al finalizar este módulo, serás capaz de:

1. Comprender qué es Ansible y para qué se utiliza en la automatización de sistemas
2. Instalar Ansible en un entorno Linux utilizando el gestor de paquetes correspondiente
3. Configurar los archivos básicos (`inventory`, `ansible.cfg`) para ejecutar tareas
4. Ejecutar un primer *playbook* de ejemplo en el de laboratorio
5. Verificar la conectividad y autenticación entre el nodo de control y los nodos gestionados

---

## 🧠 Teoría

### ¿Qué es Ansible?

Ansible es una **herramienta de automatización IT** que permite gestionar configuraciones, desplegar aplicaciones y orquestar tareas complejas de infraestructura de forma **declarativa** y **sin agentes**.

* **Sin agentes:** No requiere instalar software en los servidores gestionados.
* **Usa SSH:** La comunicación se realiza mediante SSH (o WinRM en Windows).
* **Declarativo:** Describe el estado deseado, no los pasos para alcanzarlo.

!!! note
    Ansible fue creado por Michael DeHaan en 2012 y actualmente es mantenido por **Red Hat**.
    Es una de las herramientas más usadas en entornos **DevOps**, junto con Terraform y Puppet.

### Arquitectura Básica

```
┌────────────────────┐
│ Nodo de Control    │
│ (ansible instalado)│
└────────┬───────────┘
         │ SSH
         ▼
┌─────────────────────┐
│ Nodos Gestionados   │
│ (servidores remotos)│
└─────────────────────┘
```

### Conceptos Fundamentales

Antes de comenzar a ejecutar comandos o playbooks, vamosa a repasar los **conceptos básicos** del ecosistema de Ansible:

#### 🖥️ Nodo de Control (*Control Node*)

Es la máquina que tiene instalado el motor y desde la que ejecutamos los comandos de Ansible (`ansible`, `ansible-playbook`, `ansible-vault`, etc.).

- Puede ser un **ordenador local**, un **servidor** o incluso un **contenedor** (Execution Environment).
- Es el punto central de operación: desde aquí se orquestan las tareas hacia los nodos gestionados.

!!! tip
    Cualquier máquina con Python y acceso SSH a los servidores gestionados puede actuar como nodo de control.

---

#### 💻 Nodos Gestionados (*Managed Nodes*)

También llamados **hosts**, son los dispositivos o servidores que Ansible administra.
Pueden ser servidores Linux, Windows o cualquier sistema accesible por red, donde se pueda instalar python (se usa como dependencia)


!!! note
    **Ansible no se instala en ellos** El nodo de control se conecta mediante SSH o WinRM y genera los recursos temporales necesarios

---

#### 📋 Inventario (*Inventory*)

Es una **lista de nodos gestionados**, organizada por grupos.

El inventario puede ser:

- Un archivo estático (`inventory`, `hosts`)
- O una fuente dinámica (por ejemplo, AWS EC2, VMware, Docker, etc.)

Ejemplo básico de inventario estático:

```ini
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[dbservers]
db1 ansible_host=192.168.1.20
```

!!! note
    El inventario también puede definir **variables por host o grupo**, que luego se usan dentro de los playbooks.

---

#### 🧱 Tareas (*Tasks*)

Cada **tarea** define una **acción específica** que se aplica sobre los nodos gestionados.

Ejemplo:

```yaml
- name: Crear un archivo vacío
  ansible.builtin.file:
    path: /tmp/test.txt
    state: touch
```

---
#### 🧩 Roles

Un **role** es una forma estructurada y reutilizable de empaquetar contenido de Ansible:

| Directorio | Propósito Principal | Explicación Breve |
| :--- | :--- | :--- |
| **`tasks/`** | **Flujo de Ejecución** | Contiene los archivos YAML (`main.yml`) que definen las **acciones** (tareas) que Ansible debe realizar en los *hosts* (p. ej., instalar paquetes, crear usuarios, copiar archivos). |
| **`handlers/`** | **Manejo de Eventos** | Contiene los *handlers* (manejadores) que son **tareas que solo se ejecutan cuando son notificadas** (o *notified*) por una tarea en `tasks/`. Se usan generalmente para reiniciar servicios, lo cual solo debe hacerse si la configuración ha cambiado. |
| **`vars/`** | **Variables por Defecto** | Almacena variables específicas para este *role* (en `main.yml`). Son variables que el *role* necesita, pero que **pueden ser sobrescritas** desde el *playbook* o el inventario. |
| **`defaults/`** | **Valores Preestablecidos** | Contiene variables (en `main.yml`) que establecen los **valores predeterminados** para el *role*. Tienen la *menor* prioridad, asegurando que el *role* siempre funcione con valores seguros si no se especifican otros. |
| **`templates/`** | **Archivos Dinámicos (Jinja2)** | Contiene plantillas de archivos (usualmente con extensión `.j2`) que se copian al *host* gestionado. Antes de copiarse, Ansible **reemplaza las variables** definidas en Jinja2 (`{{ variable }}`) con sus valores reales. |
| **`files/`** | **Archivos Estáticos** | Contiene archivos estáticos que deben copiarse **tal cual** a los *hosts* gestionados. Se accede a ellos usando el módulo `copy` o `template`, pero no se procesan como plantillas. |
| **`meta/`** | **Metadatos y Dependencias** | Contiene información sobre el *role* mismo, como su autor, licencia, plataformas compatibles, y, lo más importante, **las dependencias de otros *roles*** que deben ejecutarse antes que este. |

La diferencia principal entre `vars/` y `defaults/` es la **prioridad** de las variables (lo veremos más adelante).

!!! tip
    Los roles permiten **modularizar** tus automatizaciones y **reutilizar** código entre proyectos.

    Para usarlos, basta con incluirlos dentro de un play:

    ```yaml
    roles:
      - common
      - webserver
    ```
---

#### 🛎️ Handlers

Son tareas especiales que **solo se ejecutan cuando son notificadas** por otras tareas que cambian algo.

Ejemplo:

```yaml
tasks:
  - name: Copiar archivo de configuración
    ansible.builtin.copy:
      src: nginx.conf
      dest: /etc/nginx/nginx.conf
    notify: Reiniciar Nginx # llamada la handler con "name: Reiniciar Nginx"

handlers:
  - name: Reiniciar Nginx # el nombre tiene que coincidir con el campo "notify"
    ansible.builtin.service:
      name: nginx
      state: restarted
```

---

#### ▶️ Plays

Un **play** encapsula una lista ordenada de **acciones** contra un conjunto de **hosts**.

Cada play puede incluir **variables**, **roles**, **handlers** y **tareas**.

Podemos pensar en un play como:

> “Ejecutar estas tareas sobre estos servidores, de esta forma.”

---
#### 🎮 Playbooks

Los **playbooks** son archivos escritos en **YAML** que definen qué tareas ejecutar y sobre qué hosts.

- Son el **la pieza principal de Ansible**
- Cada playbook contiene uno o varios *plays*

Ejemplo de un playbook básico:

```yaml
---
- name: Instalar Apache en los servidores web # Nombre del play
  hosts: webservers # grupo de servidores
  become: true # se lanza como 'root'
  tasks:
    - name: Instalar paquete Apache
      ansible.builtin.package:
        name: apache2
        state: present
```

---

#### ⚙️ Módulos (*Modules*)

Los **módulos** son paquetes de código que Ansible copia temporalmente a los nodos gestionados para ejecutar acciones específicas.

* Existen módulos para administrar paquetes, usuarios, bases de datos, redes, etc.
* Se agrupan en **colecciones** (collections).

Ejemplo:

```yaml
- name: Instalar paquete Nginx
  ansible.builtin.package:
    name: nginx
    state: present
```

!!! note
    Los módulos son **autocontenidos** y **declarativos**: definen qué debe lograrse, no cómo.

---

#### 🔌 Plugins

Los **plugins** amplían las capacidades del núcleo de Ansible

Tipos de plugins comunes:

* **Connection plugins:** controlan cómo se conecta Ansible (SSH, WinRM, local, Docker…)
* **Filter plugins:** manipulan datos y variables
* **Callback plugins:** controlan la salida y formato del resultado

---

#### 📦 Colecciones (*Collections*)

Las **colecciones** agrupan el contenido de Ansible: **roles**, **módulos**, **plugins** y **playbooks**

Se instalan fácilmente desde **Ansible Galaxy**:

```bash
ansible-galaxy collection install ansible.posix
```

!!! tip
    Usa colecciones oficiales (por ejemplo `ansible.builtin`, `community.general`) para mantener compatibilidad y seguridad.


### Archivos Fundamentales

1. El ya comentado **Inventario (`inventory`)**
    Lista de hosts o grupos de hosts que Ansible gestionará:

    ```ini
    [webservers]
    web1 ansible_host=192.168.1.10
    web2 ansible_host=192.168.1.11

    [dbservers]
    db1 ansible_host=192.168.1.20
    ```

2. Y el **archivo de configuración (`ansible.cfg`)**
    Controla el comportamiento global de Ansible.

    ```ini
    [defaults]
    inventory = ./inventory
    host_key_checking = False
    ```

!!! danger
    En entornos productivos `host_key_checking` debe estar siempre a `True` para evitar **server spoofing** y ataques **man-in-the-middle**

!!! tip
    Puedes establecer una configuración global en `/etc/ansible/ansible.cfg`
    o local por proyecto (recomendado) en el directorio de trabajo.

---

## ✍️ Ejemplo Práctico
### 1. Crear un Inventario Simple

Con tu editor de confianza, crea el archivo `inventory`:

```toml
[all]
localhost ansible_connection=local
```

y `ansible.cfg`:
```toml
[defaults]
inventory = ./inventory
host_key_checking = False # no
```

### 2. Validar configuración local

Lanzamos el siguiente comando:

```shell
ansible -m ping localhost
```

Salida esperada:

```shell
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

!!! note
    El módulo `ping` **no hace un ping de red real**, sino una verificación de conectividad y autenticación con el host sobre SSH

---

## 🚨 Errores Comunes y Buenas Prácticas

### Errores Comunes

1. **Error de autenticación SSH**

    ```shell
    UNREACHABLE! => Failed to connect to the host via ssh
    ```
    → Revisa las claves SSH y permisos

2. **Inventario mal formateado**
    → Asegúrate de que no haya espacios o tabulaciones incorrectas en el archivo `inventory`

3. **Ruta incorrecta del `ansible.cfg`**
  → Usa `ansible --version` para verificar desde dónde se está leyendo la configuración

### Buenas Prácticas

!!! tip
    - Usa inventarios **por entorno** (dev, stage, prod) o **tecnología** (oracle, mongo)
    - Define un `ansible.cfg` por proyecto para mantener configuraciones aisladas
