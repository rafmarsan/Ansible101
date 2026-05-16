<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 4: Managing *Tasks*, *Roles*, and *Handlers*

## 🎯 Objectives

By the end of this module, you will be able to:

1. Organize tasks within a playbook in a clean and structured way.
2. Create and use **roles** to separate logic and reuse code.
3. Define and execute **handlers** to manage restarts, reloads, or conditional actions.
4. Apply structural best practices in Ansible projects.

---

## 🧠 Theory

### What are *Tasks*?

**Tasks** are the set of actions that Ansible executes on the hosts: installing packages, creating files, managing services, etc., relying on the different modules. They are defined inside `tasks:` in a playbook or in external files.

Basic example:

```yaml
tasks:
  - name: Install Nginx
    ansible.builtin.package:
      name: nginx
      state: present
```

Tasks are executed **top-down** in the order they appear.

---

### Separating Tasks into Files

For large playbooks, it is common to move tasks to external files. This allows for cleaner and more structured playbooks:

#### `main.yml`

```yaml
- hosts: localhost
  tasks:
    - name: Include tasks
      ansible.builtin.include_tasks: tasks/web.yml
```

#### `tasks/web.yml`

```yaml
- name: Create web directory
  ansible.builtin.file:
    path: /tmp/web
    state: directory
```

---
## 🏗️ Roles

**Roles** are the standard and recommended way to **organize, modularize, and reuse** logic in Ansible.
A role encapsulates:

- Defaults
- Tasks
- Vars
- Handlers
- Files
- Templates

!!! abstract
    [Link](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_reuse_roles.html) to the official documentation

---

### Internal structure of a role

Typical structure:

```
roles/
└── webserver/
    ├── tasks/
    │   ├── main.yml
    │   └── install.yml
    │   └── configure.yml
    ├── handlers/
    │   └── main.yml
    ├── templates/
    │   └── index.html.j2
    ├── files/
    │   └── static_file.txt
    ├── vars/
    │   └── main.yml
    ├── defaults/
    │   └── main.yml
    ├── meta/
    │   └── main.yml
    └── README.md
```

It is not mandatory to use all folders, but **tasks/** and **templates/** are usually essential.

---

### **How does a role work internally?**

**The entry point is always `tasks/main.yml`**. It is equivalent to the `main()` of a program.

Example:

```yaml
# roles/webserver/tasks/main.yml
- name: Install packages
  ansible.builtin.include_tasks: install.yml

- name: Configure files
  ansible.builtin.include_tasks: configure.yml
```

`main.yml` internally **orchestrates** the role, **sequentially** executing other task files. It can also contain all the logic directly, but it is not a recommended practice for maintainability.

This allows splitting the logic:

- `install.yml` → package installation
- `configure.yml` → templates, permissions, etc.
- `validate.yml` → final checks

Typical order:

1. `tasks/main.yml`
2. Any include/import within main
3. handlers *at the end of the play*, if they were notified

---

### **Internal role variables**

**`defaults/main.yml`**

- **Lowest** priority in Ansible.
- Perfect for default values that the user can override.

Example:

```yaml
# roles/webserver/defaults/main.yml
web_port: 80
web_root: /var/www/html
```

**`vars/main.yml`**

- High priority.
- Not recommended except for special cases.

Example:

```yaml
# roles/webserver/vars/main.yml
nginx_package_name: nginx
```

---

### **Role templates and files**

They are accessed inside the role without relative paths:

```yaml
ansible.builtin.template:
  src: index.html.j2
  dest: "{{ web_root }}/index.html"
```

```yaml
ansible.builtin.copy:
  src: static_file.txt
  dest: /tmp/static_file.txt
```

---

### **Dependencies between roles**

They are declared in: `roles/webserver/meta/main.yml`

```yaml
dependencies:
  - role: common
  - role: firewall
```

---

### **Complete role example**
We have the `webserver` role, its parts would be:

1. `roles/webserver/tasks/main.yml`

```yaml
- name: Include installation
  ansible.builtin.include_tasks: install.yml

- name: Include configuration
  ansible.builtin.include_tasks: configure.yml
```

2. `roles/webserver/tasks/install.yml`

```yaml
- name: Install nginx
  ansible.builtin.package:
    name: nginx
    state: present
```

3. `roles/webserver/tasks/configure.yml`

```yaml
- name: Deploy index.html
  ansible.builtin.template:
    src: index.j2
    dest: "{{ web_root }}/index.html"
  notify: Reload nginx
```

4. `roles/webserver/handlers/main.yml`

```yaml
- name: Reload nginx
  ansible.builtin.service:
    name: nginx
    state: reloaded
```

---

### **Using a role in a playbook**

```yaml
- hosts: webservers
  roles:
    - webserver
```

Or with parameters:

```yaml
- hosts: webservers
  roles:
    - role: webserver
      web_port: 8080
```

---

## 🔥 Handlers

**Handlers** are special tasks that are executed **only when notified** by another task.

**Typical example: restart a service only when there are changes**

```yaml
tasks:
  - name: Copy configuration file
    ansible.builtin.template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx

handlers:
  - name: Restart nginx
    ansible.builtin.service:
      name: nginx
      state: restarted
```

Features:

- They are only executed **if there were changes** in the notifying task
- They are executed **at the end of the play**, after all tasks
- They can be notified multiple times, but are executed only once
- They can be inside a **role** in its `handlers/` folder

!!! tip
    You can force handlers to execute at a given moment without waiting for the end
    ```yaml
    - ansible.builtin.meta: flush_handlers
    ```

---

### 🧬 Chaining Handlers

You can **chain** handlers using `notify` inside a handler:

```yaml
handlers:
  - name: Reload nginx
    ansible.builtin.service:
      name: nginx
      state: reloaded
    notify: Restart nginx

  - name: Restart nginx
    ansible.builtin.service:
      name: nginx
      state: restarted
```

---
## 🚨 Common Errors and Best Practices

### Common Errors
1. **Difference between `include_tasks` and `import_tasks`**

    - `import_tasks` → **static**, parsed at parse time
    - `include_tasks` → **dynamic**, evaluated at runtime

    Example:
    ```yaml
    import_tasks: install.yml
    when: some_condition
    ```
    → Does not work: `import_tasks` ignores the `when`


### Best Practices

!!! tip
    - Split `tasks/main.yml` into multiple includes for clarity
    - Put modifiable variables in `defaults/`, not in `vars/`
    - Use variable names prefixed with the role name: `webserver_port`, `webserver_root`
    - Keep roles self-contained: do not rely on the project
    - Use handlers **only** for idempotent and necessary actions
    - Avoid absolute paths within the role when you can parameterize
    - Document the role (README.md inside the role)

---

## 📚 Practical Exercise

Create a role named `webdemo` that encapsulates the logic of the previous topic's exercise.

To start the exercise, run:
```shell
lab start role
```
This will generate the structure:

```
webdemo/
├── defaults/
│   └── main.yml
├── tasks/
│   └── main.yml
└── ...
```

**1. Define the default variables of the role**

In `webdemo/defaults/main.yml`:
```yaml
web_port: 8080
web_root: /tmp/demo
```

**2. Implement the role tasks**

In `webdemo/tasks/main.yml`:
```yaml
---
- name: Include logic
  ansible.builtin.include_tasks: action.yml
```

In `webdemo/tasks/action.yml`:
```yaml
---
- name: Create web_root directory
  ansible.builtin.file:
    path: "{{ web_root }}"
    state: directory

- name: Create index.html file
  ansible.builtin.copy:
    content: "Server listening on port {{ web_port }}"
    dest: "{{ web_root }}/index.html"
```

**3. Create a playbook that uses the role**

Create `site.yml`:
```yaml
---
- name: Run webdemo role
  hosts: localhost
  gather_facts: false
  roles:
    - role: webdemo
```

**4. Run the full playbook**

```bash
ansible-playbook site.yml -v
```

To grade the exercise, run:
```shell
lab grade role
```

🔬 **Additional Challenge**

  - Add a task that shows the full path of the created file using `debug:`
  - Add a task that shows the content of the created file using `debug:` (can be done in multiple steps)

```yaml
- name: Show full path of the created file
  ansible.builtin.debug:
    msg: "Created file: {{ web_root }}/index.html"

- name: Read content of the created file
  ansible.builtin.slurp:
    src: "{{ web_root }}/index.html"
  register: index_raw

- name: Show content of the created file
  ansible.builtin.debug:
    msg: "{{ index_raw.content | b64decode }}"
```

**5. Run and test overriding variables with `-e`**

```bash
ansible-playbook site.yml -e web_port=9090
```
