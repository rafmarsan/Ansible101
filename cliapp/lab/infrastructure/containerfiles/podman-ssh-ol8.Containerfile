# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# podman run -d --name web1 --hostname web1 --systemd=always --privileged -p 2232:22 -p 8080:80 lab-ssh-ol8
# podman run -d --name web1 --hostname web1 -p 2232:22 -p 8080:80 lab-ssh-ol8
FROM oraclelinux:8.10 as BASE

RUN yum update && yum install -y openssh-server sudo unzip systemd ncurses lsof glibc-langpack-en procps binutils file iproute && \
  yum clean all && \
  ssh-keygen -A

RUN yum install -y java-11-openjdk && yum clean all

FROM BASE
# Crear usuario ansible
RUN groupadd -g 5000 ansible && \
    useradd -m -u 5000 -g ansible -s /bin/bash ansible && \
    usermod -aG wheel ansible && \
    echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    mkdir -p /home/ansible/.ssh && \
    chown -R ansible:ansible /home/ansible/.ssh && \
    chmod 700 /home/ansible/.ssh

# Añadir clave pública
RUN echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICU2l2lDVI5HquRM/mXLcVY76RF/S8PeQJRYIlcPvEhN user@ansible-lab" \
    > /home/ansible/.ssh/authorized_keys && \
    chown ansible:ansible /home/ansible/.ssh/authorized_keys && \
    chmod 600 /home/ansible/.ssh/authorized_keys

EXPOSE 22

# Habilitar el servicio SSH para que inicie con systemd
RUN systemctl enable sshd

# Establecer el punto de entrada con systemd
CMD [ "/usr/sbin/init" ]
