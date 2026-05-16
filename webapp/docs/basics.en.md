<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 2: Ansible Basics

## 🎯 Objectives

By the end of this module, you will be able to:

1. Understand what **inventories** are and how they are used
2. Run **ad-hoc commands** to perform quick actions
3. Understand the **structure and syntax** of a playbook in YAML
4. Create and run **simple and compound tasks** within a playbook
5. Use **common Ansible modules**
6. Differentiate between **one-off execution (ad-hoc)** and **persistent automation (playbooks)**

---

## 🧠 Theory

### Inventories

In **Ansible**, an **inventory** is a file where you define **which machines we are going to manage** and how to connect to them. It allows you to organize your servers into **groups** and assign them specific variables.

Inventories can be in several formats:

- **INI** (the most classic)
- **YAML**
- **JSON**

#### INI format inventory example

```ini
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[dbservers]
db1 ansible_host=192.168.1.20

[app:children]
webservers
dbservers
```

- `webservers` and `dbservers` are **host groups**.
- `app` is a **group that groups other groups** (children).
- `ansible_host` indicates the IP or DNS to connect to.
- We can define group or host variables inside the inventory, for example:

```ini
[webservers:vars]
ansible_user=ubuntu
apache_port=8080
```

#### YAML format inventory example

```yaml
all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: 192.168.1.10
        web2:
          ansible_host: 192.168.1.11
      vars:
        ansible_user: ubuntu
        apache_port: 8080
    dbservers:
      hosts:
        db1:
          ansible_host: 192.168.1.20
    app:
      children:
        webservers: {}
        dbservers: {}
```
!!! info "Summary"
    The inventory **defines the physical and logical inventory of your hosts**, allows you to **group them**, and assign **variables per host or per group**. It is **the foundation for running any playbook or ad-hoc command**.


### *Ad-hoc* Commands

**Ad-hoc commands** are a quick way to run simple tasks on one or multiple machines **without writing a playbook**.

General syntax:

```bash
ansible -i <inventory_file> <group_or_host> -m <module> -a "<arguments>"
```
!!! info
    To avoid having to use `-i <inventory_file>` all the time, it is recommended to define the line `inventory = ./inventory` in the **ansible.cfg** file.
    When using both `ansible` and `ansible-playbook` in the directory where we have the file, there will be no need to use `-i`.

Examples:

| Objective              | Command                                                               |
| ---------------------- | --------------------------------------------------------------------- |
| Check connectivity     | `ansible -i inventory all -m ping`                                                 |
| View kernel version    | `ansible -i inventory all -m command -a "uname -r"`                                |
| Create a directory     | `ansible -i inventory all -m file -a "path=/tmp/demo state=directory"`             |
| Install a package      | `ansible -i inventory webservers -m apt -a "name=nginx state=present become=true"` |

!!! note
    **Ad-hoc commands** are useful for testing or simple tasks, but they are neither **repeatable nor versionable**.
    For full automation, a **playbook** is always recommended.

---

### Playbook Syntax

A **playbook** is a YAML file that describes one or more [*plays*](./introduction.en.md#plays).
Each *play* defines:

1. **Which hosts** it will apply to (`hosts:`)
2. **What tasks** will be executed (`tasks:`)
3. **With what permissions** (`become:`)
4. Optionally, **roles**, **variables**, or **handlers**

Example:

```yaml
---
- name: Install and enable Nginx
  hosts: webservers
  become: true
  tasks:
    - name: Install Nginx
      ansible.builtin.package:
        name: nginx
        state: present

    - name: Start and enable the service
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true
```

!!! tip
    YAML is **indentation-sensitive** and Ansible, by default, requires the use of **spaces** (not tabs).

    **Recommendation:** Configure your code editor so that **`TAB`** inserts **two spaces** instead of a tab character. This prevents most syntax errors.

---

Each *playbook* is composed of **logical blocks**:

| Element     | Description                                               | Example                     |
| ----------- | --------------------------------------------------------- | --------------------------- |
| `hosts:`    | Defines on which group of servers the play will run       | `hosts: webservers`         |
| `become:`   | Allows running tasks as superuser (sudo)                  | `become: true`              |
| `gather_facts:`| Automatically gathers system information                 | `gather_facts: true`        |
| `tasks:`    | List of actions to execute                                | See example above           |
| `vars:`     | Defines internal variables for the playbook               | `vars: { pkg_name: nginx }` |
| `handlers:` | Tasks that are executed only when notified                | `notify: Restart Nginx`   |

---
**`gather_facts`**

By default, when you run a playbook, Ansible **automatically gathers system information** from each host before executing the tasks. This information is called **facts** and contains details like:

- Operating system name (`ansible_distribution`)
- Version (`ansible_distribution_version`)
- Architecture (`ansible_architecture`)
- IPs, network interfaces, CPU, memory, etc.

This gathering is performed with the [`setup`](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_vars_facts.html#ansible-facts) module and is activated automatically **because `gather_facts: true` by default**.

**Common facts example:**

```yaml
ansible_distribution: Ubuntu
ansible_distribution_version: "22.04"
ansible_architecture: x86_64
ansible_default_ipv4:
  address: 192.168.1.10
```

**When to use `gather_facts: false`**

- If your playbook does not need system information (e.g., copying static files or installing known packages)
- To **save time**, especially if you manage many hosts
- To **avoid errors** in environments where the connection does not allow gathering facts

!!! info "Summary"
    - `gather_facts` is useful when you need dynamic host data, but **setting it to `false` improves execution performance**.
    - It is enabled by default if you do not explicitly set `gather_facts: false`.

---

### Common Modules

The most used modules in **ad-hoc commands** would be:

| Module    | Description                             | Example                                                      |
| --------- | --------------------------------------- | ------------------------------------------------------------ |
| `ping`    | Check connection and authentication     | `ansible all -m ping`                                        |
| `command` | Execute a command without a shell       | `ansible all -m command -a "uptime"`                         |
| `shell`   | Execute commands inside a shell         | `ansible all -m shell -a "cat /etc/os-release"`              |
| `file`    | Manage files and permissions            | `ansible all -m file -a "path=/tmp/demo state=directory"`    |
| `copy`    | Copy local files to remote hosts        | `ansible all -m copy -a "src=./test.txt dest=/tmp/test.txt"` |
| `service` | Control system services                 | `ansible all -m service -a "name=nginx state=restarted"`     |

!!! warning
    Use the `shell` module **only when necessary**.

    Try to use specific modules (`user`, `package`, `service`, `copy`, etc.) to ensure **idempotency** (getting the same result even if applied multiple times).

---

## ⚙️ Practical Example

Let's practice the complete flow:

- Run an ad-hoc command
- Create a playbook with equivalent tasks

### 1. Ad-hoc command

Let's create a directory `/tmp/webdemo` on `localhost`:

```bash
ansible localhost -m file -a "path=/tmp/webdemo state=directory"
```

Expected output:

```shell
localhost | CHANGED => {
    "path": "/tmp/webdemo",
    "state": "directory",
    "changed": true
}
```

---

### 2. Create Playbook with extra tasks

> A **playbook** allows us to run multiple tasks sequentially.

File `webdemo.yml`:

```yaml
---
- name: Create web demo structure
  hosts: localhost
  tasks:
    - name: Create working directory
      ansible.builtin.file:
        path: /tmp/webdemo
        state: directory

    - name: Create a basic index.html
      ansible.builtin.copy:
        dest: /tmp/webdemo/index.html
        content: "<h1>Server managed with Ansible</h1>"

    - name: Show final message
      ansible.builtin.debug:
        msg: "The web structure has been successfully created in /tmp/webdemo"
```

Run:

```shell
ansible-playbook webdemo.yml
```

Expected output:

```shell
PLAY [Create web demo structure] *******************************************

TASK [Create working directory] ********************************************
changed: [localhost]

TASK [Create a basic index.html] *********************************************
changed: [localhost]

TASK [Show final message] **************************************************
ok: [localhost] => {
    "msg": "The web structure has been successfully created in /tmp/webdemo"
}

PLAY RECAP ********************************************************************
localhost : ok=3  changed=2  failed=0
```

---

## 🚨 Common Errors and Best Practices

### Common Errors

1. **Incorrect indentation (YAML)**

    ```
    Syntax Error while loading YAML.
        mapping values are not allowed in this context
    ```

2. **Connection error**

    ```
    UNREACHABLE! => Failed to connect via ssh
    ```

    → Verify the `inventory` and access permissions.

3. **Improper use of `shell`**
   → If you can achieve it with a module, **do not use `shell` or `command`**.

---

### Best Practices

!!! tip
    - **Ad-hoc commands** are for **quick actions**, not permanent automations.
    - Playbooks should be **clear and repeatable**, and versioned in Git.
    - Use descriptive names in tasks (`name:`).
    - Maintain a consistent format in YAML and group related tasks.
    - Add comments and use variables to avoid hardcoded values.

---

## 📚 Proposed Exercise

Create a **playbook named `system_info.yml`** that:

1. Runs on `localhost` (local connection).
2. Retrieves and displays the following information:
    * Operating system name (`ansible_distribution`)
    * Version (`ansible_distribution_version`)
    * Main IP address (`ansible_default_ipv4.address`)
3. Saves the information in a file `/tmp/system_info.txt` in plain text format.
4. Shows a final message with `debug:` confirming the file creation.


!!! tip
    - Use the `copy` module with the `content:` option to write text directly to a file
    - You can get system information using the `setup` module or by adding `gather_facts: true` in the **play**
        - That information is defined in special variables starting with `ansible_` ➜ [docs link](https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html)

!!! note
    This exercise teaches you how to combine **modules**, **facts**, and **variables**, the three pillars of daily work with Ansible.
