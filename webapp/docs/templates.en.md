<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 5: Templates and Jinja2 in Ansible

## 🎯 Objectives

By the end of this module, you will be able to:

1. Understand what a **template** is and why it is fundamental in Ansible
2. Use **Jinja2** to generate dynamic files using variables, filters, and logical structures
3. Differentiate between simple templates and advanced logic-based configurations
4. Properly integrate templates within roles and playbooks
5. Apply best practices to keep templates clean, readable, and maintainable

---

## 🧠 Theory

### What is a Template in Ansible?

A **template** is a text file that uses **Jinja2** syntax to generate dynamic content.
They are typically used for:

* Service configurations (`nginx.conf`, `php.ini`, `my.cnf`, `sshd_config`, etc.)
* Scripts with parameters
* Environment `.env` files
* Multi-host configurations

They are processed with the module:

```yaml
ansible.builtin.template
```

Templates *always* live in:

```
templates/
```

within the role or the project.

---

### What is Jinja2?

**Jinja2** is a template engine that allows you to:

* Insert variables
* Create conditionals (`if`)
* Iterations (`for`)
* Apply filters (`| lower`, `| default()`, etc.)

Basic example:

```jinja2
server {
    listen {{ web_port }};
    root {{ web_root }};
}
```

---

## 📄 Essential Jinja2 Syntax

### **Variables**

```jinja2
User: {{ user_name }}
```

### **Conditionals**

```jinja2
{% if enable_ssl %}
ssl on;
{% else %}
ssl off;
{% endif %}
```

### **Loops**

```jinja2
{% for host in groups['webservers'] %}
server {{ host }};
{% endfor %}
```

### **Useful filters**

```jinja2
{{ web_root | default('/var/www/html') }}

{{ app_name | upper }}

{{ servers | join(', ') }}
```

---

## ⚙️ Using Templates in Playbooks and Roles

### Basic example in a playbook

```yaml
- hosts: web
  tasks:
    - name: Generate Nginx configuration file
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        mode: '0644'
```

### Example within a role

```
roles/
└── webserver/
    ├── tasks/main.yml
    └── templates/nginx.conf.j2
```

`tasks/main.yml`:

```yaml
- name: Nginx configuration template
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: "/etc/nginx/conf.d/{{ inventory_hostname }}.conf"
```

---

## 📚 Real Examples of Jinja2 in Configuration

### 1. Configuration with a backend list

Template:
```jinja2
upstream backend {
{% for srv in backend_servers %}
  server {{ srv }}:{{ backend_port }};
{% endfor %}
}
```

Playbook:
```yaml
vars:
  backend_servers:
    - 10.0.0.10
    - 10.0.0.11
  backend_port: 9000
```

---

### 2. Conditional log configuration

```jinja2
{% if enable_debug %}
error_log /var/log/nginx/error.log debug;
{% else %}
error_log /var/log/nginx/error.log warn;
{% endif %}
```

---

### 3. Create a dynamic `.env` file

```jinja2
APP_ENV={{ app_env }}
DEBUG={{ debug | default(false) }}
DB_HOST={{ db.host }}
DB_USER={{ db.user }}
DB_PASS={{ db.pass }}
```

---

## 🚨 Common Errors and Best Practices

### Common Errors

1. **Undefined variables**

  Solution: `{{ var | default('value') }}`

2. **Misplaced spaces in the delimiter**

    ```jinja2
    {%if enabled%}   # ❌ No spaces after {%
    {% if enabled%}  # ❌ Missing space before %}
    ```
    {% and %} must be separated from the content by a space
    ```
    {% if enabled %}
    ```

---

### Best Practices

!!! tip
    - Use `default()` on ALL critical variables.
    - Use comments inside the template (`#`) to document decisions.
    - Avoid hardcoding paths; use variables (`{{ config_dir }}`).
    - Prefer explicitly named variables: `nginx_log_format` instead of `log`.
    - Test the template with `ansible-playbook --check` before reloading a sensitive service.
