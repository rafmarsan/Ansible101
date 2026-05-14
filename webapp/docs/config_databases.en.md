<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 7: Database Management with PostgreSQL

## 🎯 General Objective

By the end of this module, you will be able to:

1. Install and configure PostgreSQL 16 using a **dedicated role**
2. Initialize the cluster (databases, users, and permissions) using Ansible
3. Execute SQL queries from a playbook

---

## 🛞 Exercise Commands

To start the exercise, run:
```shell
lab start databases
```

To grade the exercise, run:
```shell
lab grade databases
```

---

## 📘 Installing and Configuring PostgreSQL using roles

### 🏗️ Role Structure

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
# any system user can connect to any database without a password using the Unix socket
local   all             all                                     trust
# any host can connect via TCP/IP, but must use a password
host    all             all             0.0.0.0/0               md5
```

---

**tasks/main.yml**
```yaml
- name: Install PostgreSQL
  ansible.builtin.include_tasks: install.yml

- name: Configure PostgreSQL
  ansible.builtin.include_tasks: configure.yml
```

---

**tasks/install.yml**
```yaml
---
- name: Install official PostgreSQL repository
  become: true
  ansible.builtin.dnf:
    name: "https://download.postgresql.org/pub/repos/yum/reporpms/EL-{{ ansible_distribution_major_version }}-{{ ansible_architecture }}/pgdg-redhat-repo-latest.noarch.rpm"
    state: present
    disable_gpg_check: true

- name: Disable PostgreSQL from AppStream
  become: true
  ansible.builtin.shell: dnf -qy module disable postgresql
  ignore_errors: true

- name: Install PostgreSQL Server
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
- name: Initialize repository
  become: true
  ansible.builtin.shell: /usr/pgsql-{{ postgresql_version }}/bin/postgresql-{{ postgresql_version }}-setup initdb
  args:
    creates: "/var/lib/pgsql/{{ postgresql_version }}/data/PG_VERSION"

- name: Configure service
  become: true
  ansible.builtin.service:
    name: postgresql-{{ postgresql_version }}
    enabled: true
    state: started

- name: Copy pg_hba.conf
  become: true
  become_user: postgres
  ansible.builtin.template:
    src: pg_hba.conf.j2
    dest: "/var/lib/pgsql/{{ postgresql_version }}/data/pg_hba.conf"
  notify: Restart PostgreSQL

- name: Activate listener
  become: true
  become_user: postgres
  ansible.builtin.replace:
    path: /var/lib/pgsql/{{ postgresql_version }}/data/postgresql.conf
    regexp: "^#listen_addresses = 'localhost'"
    replace: "listen_addresses = '{{ postgresql_listen_address }}'"
  notify: Restart PostgreSQL

- name: Activate port
  become: true
  become_user: postgres
  ansible.builtin.replace:
    path: /var/lib/pgsql/{{ postgresql_version }}/data/postgresql.conf
    regexp: '^\s*#?\s*port\s*=.*$'
    replace: 'port = {{ postgresql_port }}'
  notify: Restart PostgreSQL

- ansible.builtin.meta: flush_handlers

- name: Wait for {{ postgresql_port }} to be active
  become: true
  ansible.builtin.wait_for:
    host: localhost
    port: "{{ postgresql_port }}"
    delay: 5
    timeout: 60
    state: started

- name: Test connection to instance
  become: true
  become_user: postgres
  become_flags: -i
  ansible.builtin.shell:
    cmd: psql -p {{ postgresql_port }} -t -c "select version();"
  register: version_output

- name: Set password for 'postgres' user
  become: true
  become_user: postgres
  become_flags: -i
  ansible.builtin.shell:
    cmd: psql -p {{ postgresql_port }} -c "ALTER USER postgres WITH PASSWORD '{{ postgresql_db_password }}';"

- name: Show installed version
  ansible.builtin.debug:
    msg: 
      - "Installed version:"
      - "{{ version_output.stdout | trim }}"
```

---

**handlers/main.yml**
```yaml
- name: Restart PostgreSQL
  become: true
  ansible.builtin.service:
    name: "postgresql-{{ postgresql_version }}"
    state: restarted
```

---

## 📘 Main Playbook

**databases.yml**
```yaml
---
- hosts: dbservers
  gather_facts: true
  roles:
    - role: postgresql
```

!!! info "Running the playbook"
    After running the playbook **without errors**
    ```shell
    ansible-playbook databases.yml
    ```
    you should be able to log into the machine with
    ```shell
    ssh db1
    ```
    change to the `postgres` user with
    ```shell
    sudo su - postgres
    ```
    and log into the instance with the command
    ```shell
    psql
    ```

---

## 📚 Exercise 1 — Change the PostgreSQL port

Modify:
```yaml
postgresql_port: 5433
```

And test the connection, using `ansible_123` as the password:
```bash
psql -h localhost -p 5433
```

??? tip "Solution"
    In **postgresql/defaults/main.yml** modify `postgresql_port: 5433`. PostgreSQL will automatically restart via the handler.
---

## 📚 Exercise 2 — Add a table

!!! danger
    For the lab we will use the **postgres** database, but this is NOT a good practice.

Create the file **postgresql/tasks/database.yml**:
```yaml
- name: Create employees table
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
    REMEMBER to add the new file **database.yml** in **postgresql/tasks/main.yml**
    ??? tip "Solution"
        ```yaml
        - name: Creation of tables and users
          ansible.builtin.include_tasks: database.yml
        ```

---

## 📚 Exercise 3 — Insert data from Ansible

Add a task in **postgresql/tasks/database.yml**:
```yaml
- name: Insert admin user
  become: true
  become_user: postgres
  become_flags: -i
  ansible.builtin.shell: |
    psql -p {{ postgresql_port }} -d "postgres" -c "INSERT INTO empleados (username) VALUES ('admin');"
```

---

## 📚 Exercise 4 — Create multiple users dynamically

Add a list in **defaults/main.yml**:
```yaml
postgresql_initial_users:
  - alice
  - bob
  - charlie
```

Add a task in **postgresql/tasks/database.yml**:
```yaml
- name: Insert initial users
  become: true
  become_user: postgres
  become_flags: -i
  ansible.builtin.shell:
    cmd: psql -p {{ postgresql_port }} -d "postgres" -c "INSERT INTO empleados (username) VALUES ('{{ employee_name }}');"
  loop: "{{ postgresql_initial_users }}"
  loop_control:
    loop_var: employee_name
```

!!! info "Validate"
    After running the playbook **without errors**
    ```shell
    ansible-playbook databases.yml
    ```
    you should be able to log into the machine with
    ```shell
    ssh db1
    ```
    change to the `postgres` user with
    ```shell
    sudo su - postgres
    ```
    and log into the instance with the command
    ```shell
    export PGPORT=5433
    psql
    ```
    ```sql
    select * from empleados;
    ```
    and see something like:
    ```
    postgres=# select * from empleados;
    id | username |         created_at
    ----+----------+----------------------------
      1 | admin    | 2025-11-27 20:55:37.380092
      2 | alice    | 2025-11-27 20:55:37.802237
      3 | bob      | 2025-11-27 20:55:38.21942
      4 | charlie  | 2025-11-27 20:55:38.629579
    ```
