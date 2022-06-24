FROM geerlingguy/docker-debian11-ansible:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install apt-utils -y && apt-get install munge vim git mariadb-server wget curl gnupg2 -y

RUN apt-get install slurm-client slurmd slurmd slurmdbd slurmctld -y
RUN apt-get install sudo -y && apt-get install python3.9 python3-pip -y && useradd --shell /bin/bash --home-dir /home/admin -p $(openssl passwd -1 admin) admin && echo "admin     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY munge.key /etc/munge/munge.key
RUN chown munge:munge /etc/munge/munge.key && chmod 400 /etc/munge/munge.key

COPY slurm.conf /etc/slurm/
COPY cgroup.conf /etc/slurm/

EXPOSE 6817 6818 6819 3306

WORKDIR /home/admin

# The VOLUME and CMD directives are the ones from the upstream image 
# geerlingguy/docker-centos8-ansible we used to build this image
# The entrypoint script will be used as prepare.yaml tasks to start
# SLURM service and configure slurm.conf file

VOLUME ["/sys/fs/cgroup"]

CMD ["/lib/systemd/systemd"]
