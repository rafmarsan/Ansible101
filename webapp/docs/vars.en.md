<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 3: Ansible Variable Precedence

## 🎯 Objectives

By the end of this module, you will be able to:

1. Define variables at different levels of Ansible (inventory, playbook, roles, etc.)
2. Understand the **precedence and priorities** among them
3. Use **environment variables, facts, and prompts** within playbooks
4. Apply best practices when using variables

---

## 🧠 Theory

### What are Ansible Variables?

**Variables** allow you to **parameterize** playbooks and tasks so they are **reusable** and **flexible**.
They can store values like paths, package names, users, IP addresses, passwords, etc.

Example:

```yaml
- name: Install configurable package
  hosts: localhost
  vars:
    pkg_name: nginx
  tasks:
    - name: Install package
      ansible.builtin.package:
        name: "{{ pkg_name }}"
        state: present
```

!!! note
    Variables are expanded with double curly braces `{{ variable }}`

    They must be quoted when used at the beginning of a value:
    `app_path: {{ base_path }}/22` ➜ `app_path: "{{ base_path }}/22"`

    They can be used anywhere in a playbook: paths, names, commands, etc.

---

## 📜 Where to Define Variables

Ansible allows defining variables in **many places**, depending on the context:

| Level                    | Location                                           | Example or file                                 | Comment                                   |
| :----------------------- | :------------------------------------------------- | :---------------------------------------------- | :---------------------------------------- |
| **Inventory**            | `inventory` file or `group_vars/` / `host_vars/`   | Defines variables per host or group             | Ideal for infrastructure information      |
| **Playbook**             | Inside `vars:` or `vars_files:`                    | `vars: { pkg_name: nginx }`                     | Variables local to the playbook           |
| **Role**                 | In `defaults/` or `vars/` of the role              | `roles/webserver/defaults/main.yml`             | Different priority based on folder        |
| **Environment variables**| Exported from the system                           | `export ANSIBLE_VAR=value`                      | Used with `lookup('env', 'ANSIBLE_VAR')`  |
| **Command line**         | Using `-e` or `--extra-vars`                       | `ansible-playbook play.yml -e "pkg_name=nginx"` | Highest priority                          |
| **System facts**         | Gathered automatically with `gather_facts`         | `ansible_hostname`, `ansible_distribution`      | Special variables from the remote system  |

!!! abstract
    [Link](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) to the official documentation

---

### Practical Example — Variables by Levels

Suppose we have this inventory:

```ini
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11
[webservers:vars]
app_port=80
```

And this playbook `vars_demo.yml`:

```yaml
---
- name: Variable demonstration
  hosts: webservers
  gather_facts: false

  vars:
    app_port: 8080

  tasks:
    - name: Show the value of app_port
      ansible.builtin.debug:
        msg: "The defined port is {{ app_port }}"
```

Run the playbook:

```bash
ansible-playbook -i inventory vars_demo.yml
```

**Expected output:**

```shell
TASK [Show the value of app_port] ********************************************
ok: [web1] => {
    "msg": "The defined port is 8080"
}
```

👉 Although we defined `app_port=80` in the *inventory*, the value inside the **playbook (`vars`) takes precedence** and overrides the inventory's value.

---

## 🧮 Variable Precedence (lowest to highest)

Precedence determines **which value “wins”** when a variable is defined in multiple places. 

A higher priority number overwrites the rest.

| Priority | Level                                                        | Example                                           |
| :-------: | :------------------------------------------------------------| :------------------------------------------------ |
|    1      | `defaults/` inside a role                                    | Default values, safe but overridable              |
|    2      | Inventory variables (`group_vars`, `host_vars`)              | Infrastructure-specific values                    |
|    3      | Variables defined in the playbook (`vars:` or `vars_files:`)| Local definitions                                 |
|    4      | Registered variables (`set_fact`)                            | Dynamic variables inside tasks                    |
|    5      | Environment variables (`lookup('env')`)                      | System environment values                         |
|    6      | Variables passed via command line (`-e`)                     | Have **highest priority**                         |

!!! note
    When two variables with the same name exist at different levels, **Ansible uses the one with the highest priority**, ignoring the rest.

---

### Example — Overriding Variables

We create the `inventory` file:

```ini
[all]
localhost app_name=nginx
```

And the playbook `vars_priority.yml`:

```yaml
---
- name: Variable priorities
  hosts: localhost
  gather_facts: false
  vars:
    app_name: apache2
  tasks:
    - name: Show defined variable
      ansible.builtin.debug:
        msg: "Application: {{ app_name }}"
```

#### Value from the playbook:

```bash
ansible-playbook vars_priority.yml
```

Output:

```shell
"msg": "Application: apache2"
```

#### Override from the command line:

```bash
ansible-playbook vars_priority.yml -e "app_name=nginx"
```

Output:

```shell
"msg": "Application: nginx"
```

Variables passed with `-e` have the **highest priority**.

---

## ⚙️ Environment Variables

You can access system variables with the *lookup plugin*:

```yaml
- name: Show current user
  ansible.builtin.debug:
    msg: "User: {{ lookup('env','USER') }}"
```

Practical usage example in a dynamic path:

```yaml
- name: Copy file to user home
  ansible.builtin.copy:
    src: test.txt
    dest: "{{ lookup('env','HOME') }}/test.txt"
```

---

## 💡 Dynamic Variables and Facts

Ansible can automatically gather remote system information (facts) if `gather_facts: true`.

Example:

```yaml
- name: Show host information
  hosts: localhost
  gather_facts: true
  tasks:
    - debug:
        msg: "Operating system: {{ ansible_distribution }} {{ ansible_distribution_version }}"
```

You can also define dynamic variables during execution with `set_fact`:

```yaml
- name: Calculate temporary path
  set_fact:
    tmp_file: "/tmp/{{ ansible_hostname }}_{{ ansible_date_time.hour }}.log"
```

---

## 🚨 Common Errors and Best Practices

### Common Errors

1. **Undefined variables**

    ```
    ERROR! 'pkg_name' is undefined
    The task includes an option with an undefined variable.
    The error was: 'pkg_name' is undefined
    ```

    → Use `default()` in your expressions: `{{ pkg_name | default('nginx',true) }}`
    
    → Adding `true` assigns the default value for empty strings as well

2. **Incorrect indentation**

    → Especially affects `vars:` and `vars_files:` blocks.

---

### Best Practices

!!! tip
    - Define variables **at the lowest possible level** (local rather than global).
    - Use `defaults/main.yml` in roles to ensure safe values.
    - Avoid generic names (`port`, `user`); use prefixes (`web_port`, `db_user`).
    - Document the purpose of your variables.

---

## 📚 Practical Exercise

To start the exercise, run:
```shell
lab start vars
```

Create a playbook named `vars_lab.yml` that:

1. Runs on `localhost`
2. Defines the variables:

    ```yaml
    web_port: 8080
    web_root: /tmp/demo
    ```
3. Creates the `{{ web_root }}` directory and inside it an `index.html` file with the content:

    ```
    Server listening on port {{ web_port }}
    ```
4. Test overriding `web_port` from the command line with `-e`.

To grade the exercise, run:
```shell
lab grade vars
```

!!! abstract
    - [Debug module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/debug_module.html)
    - [Copy module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/copy_module.html#parameter-content)

🔬 **Additional Challenge:**

  - Add a task that shows the full path of the created file using `debug:`
  - Add a task that shows the content of the created file using `debug:` (can be done in multiple steps)

!!! abstract
    - [Slurp module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/slurp_module.html)
