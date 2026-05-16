# Ansible101

**A hands-on project to introduce professionals to the exciting world of Ansible in a practical and dynamic way.**

🌐 **English** | [Español](README.md)

---

This repository contains:

- Learning material structured by modules
- A practical lab that runs locally
- Example roles to learn Ansible best practices
- Exercises covering everything from variables to web servers and databases

The course starts from scratch and uses a local lab environment for hands-on practice.

## 🌐 Full Documentation

All detailed explanations, examples and step-by-step guides are available on the **course page**:

👉 [View full documentation](https://rafmarsan.github.io/Ansible101/)

> Follow the link to start learning with the interactive lab.

## 🚀 Contents

1. **Topic 1:** Introduction to Ansible
2. **Topic 2:** Ansible Fundamentals
3. **Topic 3:** Variable Priority in Ansible
4. **Topic 4:** Tasks, Roles and Handlers
5. **Topic 5:** Templates and Jinja2 in Ansible
6. **Topic 6:** Web Server Configuration with Apache / Nginx
7. **Topic 7:** Database Management with PostgreSQL
8. **Topic 8:** Final Project: Full Automation of a Web Application

## 💻 Local Lab

The project includes a CLI to spin up a local test lab:

```shell
# Initialize the lab
lab init

# Run exercises
lab start <exercise_name>

# Check your progress
lab grade <exercise_name>
```

## 📦 Installation / Usage

For users who just want to try the project:

```shell
pip install https://github.com/rafmarsan/Ansible101/releases/download/vX.Y.Z/lab-X.Y.Z-py3-none-any.whl
lab --help
```

> For developers who want to modify or build from source, see [cliapp/README.md](cliapp/README.md).

## 📚 Resources

- [Official Ansible Documentation](https://docs.ansible.com/)
- [Ansible Roles Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)

## 📝 [LICENSE](./LICENSE)

GNU GENERAL PUBLIC LICENSE Version 3
