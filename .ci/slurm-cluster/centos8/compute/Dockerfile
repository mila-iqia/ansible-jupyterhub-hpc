FROM geerlingguy/docker-centos8-ansible:latest

RUN yum update -y && yum install munge vim git mariadb-server wget -y

RUN yum install slurm slurm-devel slurm-slurmd slurm-slurmdbd slurm-slurmctld -y
RUN yum install sudo -y && yum install python3.9 python3-pip -y && useradd -m admin -s /usr/bin/bash -d /home/admin && echo "admin:admin" | chpasswd && echo "admin     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY munge.key /etc/munge/munge.key
RUN chown munge:munge /etc/munge/munge.key && chmod 400 /etc/munge/munge.key

COPY slurm.conf /etc/slurm/
COPY cgroup.conf /etc/slurm/

EXPOSE 6817 6818 6819

# The VOLUME and CMD directives are the ones from the upstream image 
# geerlingguy/docker-centos8-ansible we used to build this image
# The entrypoint script will be used as prepare.yaml tasks to start
# SLURM service and configure slurm.conf file

VOLUME ["/sys/fs/cgroup"]

CMD ["/usr/lib/systemd/systemd"]
