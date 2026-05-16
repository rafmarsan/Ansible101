<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 6: Configuring Web Servers

## 🎯 General Objective

By the end of this module, you will be able to:

1. Install and configure Apache using a **complete role**
2. Install and configure Nginx as a **reverse proxy** to Apache
3. Use **templates**, **handlers**, **variables**, and **roles**
4. Run everything in a **playbook** that orchestrates both roles

---

## ✍🏻 Exercise Commands

To start the exercise, run:
```shell
lab start webservers
```

To grade the exercise, run:
```shell
lab grade webservers
```

---

## 📘 **Installing and configuring Apache using roles**
Add the following content to the generated `apache` role

### 🏗️ Role Structure

```
roles/
  apache/
    tasks/
      main.yml
      install.yml
    templates/
      httpd.conf.j2
    handlers/
      main.yml
    defaults/
      main.yml
```

**defaults/main.yml**
```yaml
apache_port: 8080
apache_docroot: /var/www/html
```

**templates/httpd.conf.j2**
```jinja2
Listen {{ apache_port }}

<VirtualHost *:{{ apache_port }}>
  DocumentRoot "{{ apache_docroot }}"
  ErrorLog /var/log/httpd/error.log
  CustomLog /var/log/httpd/access.log combined
</VirtualHost>
```

**tasks/main.yml**
```yaml
- name: Load installation module
  ansible.builtin.include_tasks: install.yml
```

**tasks/install.yml**
```yaml
- name: Install Apache
  become: true
  ansible.builtin.package:
    name: httpd
    state: present

- name: Ensure Apache is enabled and running
  become: true
  ansible.builtin.service:
    name: httpd
    enabled: yes
    state: started

- name: Disable default listener in Apache
  become: true
  ansible.builtin.replace:
    path: /etc/httpd/conf/httpd.conf
    regexp: '^Listen 80'
    replace: '# Listen 80'

- name: Copy Apache configuration
  become: true
  ansible.builtin.template:
    src: httpd.conf.j2
    dest: /etc/httpd/conf.d/main.conf
  notify: "Restart Apache"

# Execute all pending handlers, instead of
# waiting until tasks on the host finish
- ansible.builtin.meta: flush_handlers
```

**handlers/main.yml**
```yaml
- name: Restart Apache
  become: true
  ansible.builtin.service:
    name: httpd
    state: restarted
```

---

## 📘 **Installing and configuring Nginx reverse proxy**
Add the following content to the generated `nginx` role

### 🏗️ Role Structure

```
roles/
  nginx/
    tasks/
      main.yml
      install.yml
    templates/
      nginx.conf.j2
      reverse-proxy.conf.j2
    handlers/
      main.yml
    defaults/
      main.yml
```

**defaults/main.yml**
```yaml
nginx_listen_port: 80
nginx_upstream_host: "127.0.0.1"
nginx_upstream_port: 8080
```

**templates/reverse-proxy.conf.j2**
```jinja
server {
    listen {{ nginx_listen_port }};
    location / {
      proxy_pass http://{{ nginx_upstream_host }}:{{ nginx_upstream_port }};
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**templates/nginx.conf.j2**
```
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

# Settings for a HTTP server.
#    server {
#        #listen       80 default_server;
#        #listen       [::]:80 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

# Settings for a TLS enabled server.
#
#    server {
#        listen       443 ssl http2 default_server;
#        listen       [::]:443 ssl http2 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        ssl_certificate "/etc/pki/nginx/server.crt";
#        ssl_certificate_key "/etc/pki/nginx/private/server.key";
#        ssl_session_cache shared:SSL:1m;
#        ssl_session_timeout  10m;
#        ssl_ciphers PROFILE=SYSTEM;
#        ssl_prefer_server_ciphers on;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}
```

**tasks/main.yml**
```yaml
- name: Load installation module
  ansible.builtin.include_tasks: install.yml
```

**tasks/install.yml**
```yaml
---
- name: Install Nginx
  become: true
  ansible.builtin.package:
    name: nginx
    state: present

- name: Copy main config
  become: true
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf

- name: Copy reverse proxy config
  become: true
  ansible.builtin.template:
    src: reverse-proxy.conf.j2
    dest: /etc/nginx/conf.d/reverse-proxy.conf
  notify: "Reload Nginx"

- name: Ensure Nginx is running
  become: true
  ansible.builtin.service:
    name: nginx
    enabled: yes
    state: started
```

**handlers/main.yml**

```yaml
- name: Reload Nginx
  become: true
  ansible.builtin.service:
    name: nginx
    state: reloaded
```

---

## 📘 **Main Playbook**

Responsible for orchestrating the execution of roles

**webservers.yml**
```yaml
---
- hosts: webservers
  gather_facts: false
  roles:
    - role: apache
    - role: nginx
```

Key points:

- How **one role depends on the output of the other** (`apache_port` → reverse proxy '`nginx_upstream_port`')
- How to **pass variables to the role** correctly (their scope is at the play level)
- How to handle **independent handlers**
- How to separate responsibilities: **Apache** serves content, **Nginx** exposes it

!!! info
    After running the playbook `ansible-playbook webservers.yml` **without errors**, you should see the default Apache page at [`http://localhost:8080`](http://localhost:8080)

    ![Apache default](assets/images/apache_default.png){ width="300px" }

---

## 📚 **Exercise 1 — Change the Apache port**

Change the default Apache port:
```yaml
apache_port: 9090
nginx_upstream_port: 9090
```
→ Modify the upstream port in the nginx configuration as well

??? tip "Solution"
    **apache/defaults/main.yml** : `apache_port: 8080` → `apache_port: 9090`     
    **ngnix/defaults/main.yml** : `nginx_upstream_port: 8080` → `nginx_upstream_port: 9090`

---

## 📚 **Exercise 2 — Add an HTML page from template**

Add to the Apache role:
```
templates/index.html.j2
tasks/install.yml → Add task to deploy the template
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Lab Webservers</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f9;
      color: #333;
      text-align: center;
      padding-top: 50px;
    }
    h1 {
      color: #0066cc;
    }
    p {
      font-size: 1.2em;
    }
    .box {
      margin: 30px auto;
      padding: 20px;
      border: 2px solid #0066cc;
      border-radius: 8px;
      width: 60%;
      background-color: #fff;
    }
  </style>
</head>
<body>
  <div class="box">
    <h1>Apache is working!</h1>
    <p>You have reached <strong>/var/www/html/index.html</strong></p>
    <p>If you see this page, your <em>VirtualHost</em> configuration is correct.</p>
  </div>
</body>
</html>
```

??? tip "Solution"
    Add the task at the end of **apache/tasks/install.yml**
    ```yaml
    - name: Deploy custom page
      ansible.builtin.template:
        src: index.html.j2
        dest: "{{ apache_docroot }}/index.html"
    ```
    Copy the HTML into **apache/templates/index.html.j2**

---

## 📚 **Exercise 3 — Add health-check in Nginx**

Add to the `reverse-proxy.conf.j2` template:
```
location /health {
  return 200 "OK\n";
}
```

??? tip "Solution"
    **templates/reverse-proxy.conf.j2** should look like this:
    ```
    server {
      listen {{ nginx_listen_port }};
      location / {
        proxy_pass http://{{ nginx_upstream_host }}:{{ nginx_upstream_port }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
      }
      location /health {
        return 200 "OK\n";
      }
    }
    ```
