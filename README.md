# Ansible JupyterHub

This repository contains production ready Ansible roles for deploying JupyterHub 
on HPC platforms. In addition, the admins can deploy node exporter, promtail, 
loki, Prometheus and Grafana stack for monitoring the Hub deployment. 
By default, the roles are configured to install 
[batchspawner](https://github.com/jupyterhub/batchspawner) 
for spawning jupyter servers, respectively. The user can change these default 
settings by appropriately modifying the JupyterHub configuration. More details 
are provided in docs.

## Getting started

For a very quick setup use following instructions

```
git clone https://gitlab.com/idris-cnrs/jupyter/ansible-jupyterhub.git
cd ansible-jupyterhub
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
```

Now we need to edit the [inventory.example](inventory.example) file to setup 
host names for different hosts and place it in the root of the repository 
naming `inventory`. Next we need to generate necessary certificates, tokens and
passwords that are needed for deploying JupyterHub and monitoring stack. This 
can be done by running following command

```
cd scripts
./gen-encryption-data -c -p -t
```

This will create a folder called `encryption` in the root of the repository with 
all necessary certificates, tokens and passwords. If the admins want to use 
external certificates, consult [docs](docs) folder how to set them up.

For the monitoring stack we will use basic authentication when supported and for 
that we will need admin passwords. These passwords are generated in the file 
[jp-adminrc](encryption/jp-adminrc). We need to source this file before running 
the playbook. If we want to run the roles with default configuration, 
use following commands

```
source encryption/jp-adminrc
ansible-playbook -i hostfile site.yml
```

Currently, only RHEL 8 and above is supported. In future support for Debian and 
Ubuntu distros will be added
