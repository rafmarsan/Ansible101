<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 8: Final Project — Complete Web Application Automation

## 🎯 General Objective

By the end of this module you will be able to:

1. Integrate **Apache**, **Nginx**, and **PostgreSQL** in a single automated project.
2. Deploy a **dynamic web application** that lists employees stored in PostgreSQL.
3. Apply everything learned: roles, handlers, templates, variables, and best practices.
4. Build a **master playbook** capable of spinning up a complete architecture of web server + reverse proxy + database.

---

## ✍🏻 Exercise Commands

To start the exercise, run:
```shell
lab start final
```

---

## 🏗️ Project Architecture

```
+----------------+      +------------+      +------------+
│ Web Application│ ---> │   NGINX    │ ---> │   APACHE   │
│ (employees)    │      │  Reverse   │      │  WebServer │
+----------------+      +------------+      +------------+
                                                   │
                                                   ▼
                                             +------------+
                                             │ PostgreSQL │
                                             +------------+
```

---

## 📘 Project Structure

The final project requires **3 independent roles**:

```
roles/
  postgresql/
  apache/
  nginx/
```

and a *master playbook*:

```
site.yml
```

---

## 📘 1. Role: postgresql

We will use what was built in [topic 7: Database Management with PostgreSQL](config_databases.en.md).

Configure the default port back to: **5432**

We add a **dynamic query** to obtain employees from Ansible in **postgresql/tasks/database.yml** with the output format being JSON:

??? tip "Solution"
    **postgresql/defaults/main.yml** : `postgresql_port: 5433` → `postgresql_port: 5432`     

    Add in **postgresql/tasks/database.yml**:
    ```yaml
    - name: Get list of employees
      become: true
      become_user: postgres
      become_flags: -i
      ansible.builtin.shell:
        cmd: psql -p {{ postgresql_port }} -d "postgres" -t -A -F"," -c "SELECT json_agg(employees ORDER BY id) FROM employees;"
      register: employees_list
    ```

## 📘 2. Role: apache

We will use what was built in [topic 6: Configuring Web Servers](config_webservers.en.md).

Configure the default port back to: **8080**

We will have to modify the **index.html** template to show the list of employees from the `query_output` variable. To do this:

- Create the file **apache/tasks/deploy.yml**
- Move the template deployment task inside
- Create a previous task to retrieve the employee list from the context of db1 using `hostvars`
- Convert the variable containing the employee list into an iterable object **from JSON**
- Add **deploy.yml** to **main.yml** inside the Apache role

!!! info
    Variables defined at runtime do so in the **host context**, to use them in other contexts we must use their explicit definition: 
    ```
    hostvars['<server_name>']['<variable_name>']
    ```

??? tip "Solution"
    **apache/defaults/main.yml** : `apache_port: 9090` → `apache_port: 8080`

    **apache/tasks/deploy.yml** :
    ```yaml
    - name: Retrieve the list of employees from the db1 context
      ansible.builtin.set_fact:
        employees_list: "{{ hostvars['db1']['employees_list']['stdout'] | from_json }}"

    - name: Deploy the custom page
      become: true
      ansible.builtin.template:
        src: index.html.j2
        dest: "{{ apache_docroot }}/index.html"
    ```

    **apache/tasks/main.yml** :
    ```yaml
    ---
    - name: Load installation module
      ansible.builtin.include_tasks: install.yml

    - name: Load deployment module
      ansible.builtin.include_tasks: deploy.yml
    ```

    **apache/templates/index.html.j2** :
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>List of Employees</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          background-color: #f4f4f9;
          color: #333;
          text-align: center;
          padding-top: 50px;
        }
        h1 { color: #0066cc; }
        table {
          margin: 30px auto;
          border-collapse: collapse;
          width: 60%;
          background-color: #fff;
        }
        th, td {
          border: 1px solid #0066cc;
          padding: 8px;
        }
        th {
          background-color: #e6f0ff;
        }
      </style>
    </head>
    <body>
      <h1>List of employees</h1>
      <table>
        <thead>
          <tr>
            <th>User</th>
            <th>Creation Date</th>
          </tr>
        </thead>
        <tbody>
          {% for emp in employees_list %}
          <tr>
            <td>{{ emp.username }}</td>
            <td>{{ emp.created_at }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </body>
    </html>
    ```

---

## 📘 3. Role: nginx

After changing the default port in Apache, reconfigure the upstream port to **8080**

??? tip "Solution"
    **nginx/defaults/main.yml** : `nginx_upstream_port: 9090` -> `nginx_upstream_port: 8080`


---

## 📘 Main Playbook

Create the main playbook to orchestrate the entire flow.

!!! note
    Since we have more than one server, we have to add conditions so that
    the webservers logic is only launched on `web1` and the database logic
    on `db1`, the servers generated by the lab for each technology

    ## Note on the use of groups in the Ansible inventory

    When working with multiple servers, it is important to properly structure the Ansible inventory.
    Ansible allows you to **group hosts** into logical categories (e.g., `webservers`, `dbservers`) and also create **composite groups** using `:children`.

    ```ini
    [webservers]
    web1 ansible_host=web1

    [dbservers]
    db1 ansible_host=db1

    [app:children]
    webservers
    dbservers
    ```
    ### What does this inventory mean?

    - **webservers**: contains nodes dedicated to web services.
    - **dbservers**: contains nodes with databases.
    - **app:children**: a group that automatically includes *all hosts* from `webservers` and `dbservers`.

    This allows you to easily run a playbook:

    ```sh
    ansible-playbook -i inventory site.yml
    ```

    The playbook will be applied to both **web1** and **db1**, without the need to list them individually.

**site.yml**
```yaml
---
- hosts: app
  gather_facts: true
  any_errors_fatal: true
  roles:
    - role: postgresql
      when: inventory_hostname == 'db1'
    - role: apache
      when: inventory_hostname == 'web1'
    - role: nginx
      when: inventory_hostname == 'web1'
```

!!! info
    The example shown above uses inventories in **INI format**, which is the most common and simple. However, Ansible also allows defining inventories in **YAML** and **JSON**, which provides more flexibility and clarity in complex structures.
    ```yaml
    all:
      children:
        webservers:
          hosts:
            web1:
              ansible_host: web1
        dbservers:
          hosts:
            db1:
              ansible_host: db1
        app:
          children:
            webservers: {}
            dbservers: {}
    ```

      - Both inventories represent exactly the **same logical structure**.
      - The **YAML** format is more verbose, but very useful when you need complex variables, nested groups, or extensive definitions.
      - Ansible automatically detects the format based on the **file extension**:
        + `.ini` → classic INI inventory
        + `.yaml` / `.yml` → YAML inventory
        + `.json` → JSON inventory
      - [Official documentation: inventory_guide](https://docs.ansible.com/projects/ansible/latest/inventory_guide/intro_inventory.html)

---

## 🚀 Expected Execution

After running:

```shell
ansible-playbook site.yml
```

you should be able to access from your browser at:

```
http://localhost:8080/
```

and see a **dynamic list of employees** obtained from PostgreSQL (the number of entries may vary depending on how many times the playbook is launched)

![Final project](assets/images/employees_list.png){ width="700px" }
