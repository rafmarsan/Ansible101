<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 1: Introduction to Ansible

## 🎯 Objectives

By the end of this module, you will be able to:

1. Understand what Ansible is and what it is used for in system automation
2. Install Ansible in a Linux environment using the corresponding package manager
3. Configure the basic files (`inventory`, `ansible.cfg`) to run tasks
4. Execute a first sample *playbook* in the lab
5. Verify connectivity and authentication between the control node and managed nodes

---

## 🧠 Theory

### What is Ansible?

Ansible is an **IT automation tool** that allows you to manage configurations, deploy applications, and orchestrate complex infrastructure tasks in a **declarative** and **agentless** way.

* **Agentless:** Does not require installing software on managed servers.
* **Uses SSH:** Communication is done via SSH (or WinRM on Windows).
* **Declarative:** Describes the desired state, not the steps to reach it.

!!! note
    Ansible was created by Michael DeHaan in 2012 and is currently maintained by **Red Hat**.
    It is one of the most used tools in **DevOps** environments, along with Terraform and Puppet.

### Basic Architecture

```
┌────────────────────┐
│ Control Node       │
│ (ansible installed)│
└────────┬───────────┘
         │ SSH
         ▼
┌─────────────────────┐
│ Managed Nodes       │
│ (remote servers)    │
└─────────────────────┘
```

### Fundamental Concepts

Before we start running commands or playbooks, let's review the **basic concepts** of the Ansible ecosystem:

#### 🖥️ Control Node

It is the machine that has the engine installed and from which we execute Ansible commands (`ansible`, `ansible-playbook`, `ansible-vault`, etc.).

- It can be a **local computer**, a **server**, or even a **container** (Execution Environment).
- It is the central point of operation: from here, tasks are orchestrated towards the managed nodes.

!!! tip
    Any machine with Python and SSH access to the managed servers can act as a control node.

---

#### 💻 Managed Nodes

Also called **hosts**, these are the devices or servers that Ansible manages.
They can be Linux servers, Windows, or any network-accessible system where python can be installed (used as a dependency).

!!! note
    **Ansible is not installed on them.** The control node connects via SSH or WinRM and generates the necessary temporary resources.

---

#### 📋 Inventory

It is a **list of managed nodes**, organized by groups.

The inventory can be:

- A static file (`inventory`, `hosts`)
- Or a dynamic source (e.g., AWS EC2, VMware, Docker, etc.)

Basic example of a static inventory:

```ini
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[dbservers]
db1 ansible_host=192.168.1.20
```

!!! note
    The inventory can also define **variables per host or group**, which are then used inside the playbooks.

---

#### 🧱 Tasks

Each **task** defines a **specific action** that is applied to the managed nodes.

Example:

```yaml
- name: Create an empty file
  ansible.builtin.file:
    path: /tmp/test.txt
    state: touch
```

---
#### 🧩 Roles

A **role** is a structured and reusable way of packaging Ansible content:

| Directory | Main Purpose | Brief Explanation |
| :--- | :--- | :--- |
| **`tasks/`** | **Execution Flow** | Contains the YAML files (`main.yml`) that define the **actions** (tasks) Ansible must perform on the *hosts* (e.g., install packages, create users, copy files). |
| **`handlers/`** | **Event Handling** | Contains the *handlers*, which are **tasks that only run when notified** by a task in `tasks/`. They are generally used to restart services, which should only be done if the configuration has changed. |
| **`vars/`** | **Default Variables** | Stores specific variables for this *role* (in `main.yml`). These are variables the *role* needs, but which **can be overridden** from the *playbook* or inventory. |
| **`defaults/`** | **Preset Values** | Contains variables (in `main.yml`) that set the **default values** for the *role*. They have the *lowest* priority, ensuring the *role* always works with safe values if no others are specified. |
| **`templates/`** | **Dynamic Files (Jinja2)** | Contains file templates (usually with `.j2` extension) that are copied to the managed *host*. Before copying, Ansible **replaces the variables** defined in Jinja2 (`{{ variable }}`) with their real values. |
| **`files/`** | **Static Files** | Contains static files that must be copied **as-is** to the managed *hosts*. They are accessed using the `copy` or `template` module, but are not processed as templates. |
| **`meta/`** | **Metadata and Dependencies** | Contains information about the *role* itself, such as its author, license, supported platforms, and most importantly, **the dependencies on other *roles*** that must be executed before this one. |

The main difference between `vars/` and `defaults/` is the **priority** of the variables (we will see this later).

!!! tip
    Roles allow you to **modularize** your automations and **reuse** code across projects.

    To use them, simply include them within a play:

    ```yaml
    roles:
      - common
      - webserver
    ```
---

#### 🛎️ Handlers

These are special tasks that **only run when notified** by other tasks that change something.

Example:

```yaml
tasks:
  - name: Copy configuration file
    ansible.builtin.copy:
      src: nginx.conf
      dest: /etc/nginx/nginx.conf
    notify: Restart Nginx # calls the handler with "name: Restart Nginx"

handlers:
  - name: Restart Nginx # the name must match the "notify" field
    ansible.builtin.service:
      name: nginx
      state: restarted
```

---

#### ▶️ Plays

A **play** encapsulates an ordered list of **actions** against a set of **hosts**.

Each play can include **variables**, **roles**, **handlers**, and **tasks**.

We can think of a play as:

> "Execute these tasks on these servers, in this way."

---
#### 🎮 Playbooks

**Playbooks** are files written in **YAML** that define what tasks to execute and on which hosts.

- They are the **core piece of Ansible**
- Each playbook contains one or more *plays*

Basic playbook example:

```yaml
---
- name: Install Apache on web servers # Name of the play
  hosts: webservers # server group
  become: true # run as 'root'
  tasks:
    - name: Install Apache package
      ansible.builtin.package:
        name: apache2
        state: present
```

---

#### ⚙️ Modules

**Modules** are code packages that Ansible temporarily copies to managed nodes to execute specific actions.

* There are modules to manage packages, users, databases, networks, etc.
* They are grouped into **collections**.

Example:

```yaml
- name: Install Nginx package
  ansible.builtin.package:
    name: nginx
    state: present
```

!!! note
    Modules are **self-contained** and **declarative**: they define what must be achieved, not how.

---

#### 🔌 Plugins

**Plugins** extend the capabilities of the Ansible core.

Common plugin types:

* **Connection plugins:** control how Ansible connects (SSH, WinRM, local, Docker…)
* **Filter plugins:** manipulate data and variables
* **Callback plugins:** control output and result formatting

---

#### 📦 Collections

**Collections** group Ansible content: **roles**, **modules**, **plugins**, and **playbooks**.

They can be easily installed from **Ansible Galaxy**:

```bash
ansible-galaxy collection install ansible.posix
```

!!! tip
    Use official collections (e.g., `ansible.builtin`, `community.general`) to maintain compatibility and security.


### Fundamental Files

1. The aforementioned **Inventory (`inventory`)**
    List of hosts or host groups that Ansible will manage:

    ```ini
    [webservers]
    web1 ansible_host=192.168.1.10
    web2 ansible_host=192.168.1.11

    [dbservers]
    db1 ansible_host=192.168.1.20
    ```

2. And the **configuration file (`ansible.cfg`)**
    Controls the global behavior of Ansible.

    ```ini
    [defaults]
    inventory = ./inventory
    host_key_checking = False
    ```

!!! danger
    In production environments `host_key_checking` should always be `True` to prevent **server spoofing** and **man-in-the-middle** attacks.

!!! tip
    You can set a global configuration in `/etc/ansible/ansible.cfg`
    or local per project (recommended) in the working directory.

---

## ✍️ Practical Example
### 1. Create a Simple Inventory

With your trusted editor, create the `inventory` file:

```toml
[all]
localhost ansible_connection=local
```

and `ansible.cfg`:
```toml
[defaults]
inventory = ./inventory
host_key_checking = False # no
```

### 2. Validate local configuration

Run the following command:

```shell
ansible -m ping localhost
```

Expected output:

```shell
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

!!! note
    The `ping` module **does not do a real network ping**, but rather a connectivity and authentication check with the host over SSH.

---

## 🚨 Common Errors and Best Practices

### Common Errors

1. **SSH authentication error**

    ```shell
    UNREACHABLE! => Failed to connect to the host via ssh
    ```
    → Check SSH keys and permissions

2. **Malformed inventory**
    → Ensure there are no incorrect spaces or tabs in the `inventory` file

3. **Incorrect `ansible.cfg` path**
  → Use `ansible --version` to verify where the configuration is being read from

### Best Practices

!!! tip
    - Use inventories **by environment** (dev, stage, prod) or **technology** (oracle, mongo)
    - Define one `ansible.cfg` per project to keep configurations isolated
