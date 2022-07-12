# Ansible playbook for deploying JupyterHub on HPC platforms

This repository contains production ready Ansible playbook for deploying JupyterHub 
on HPC platforms. In addition, the admins can deploy node exporter, promtail, 
loki, Prometheus and Grafana stack for monitoring the Hub deployment. 
By default, playbook is configured to install 
[batchspawner](https://github.com/jupyterhub/batchspawner) 
for spawning jupyter servers. The admins can change these default 
settings by appropriately modifying the JupyterHub configuration. More details 
are provided in docs.

## Getting started

For a very quick setup use following instructions. We recommend to use 
a conda environment on the Ansible controller machine to install. More 
details on how to create environment can be found at 
[conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). 
Assuming we have a conda environment created and activated, we need to 
setup the environment as follows

```
git clone https://gitlab.com/idris-cnrs/jupyter/ansible-jupyterhub-hpc.git
cd ansible-jupyterhub-hpc
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
```

Now we need to edit the [inventory.example](inventory.example) file to setup 
host names for different hosts and place it in the root of the repository 
naming `inventory`. 

All the important configuration details for the deployment are placed in 
[config.yml](config.yml) file. More details on different variables in the 
[config.yml](config.yml) file are detailed in [docs](docs/). 
The admins can modify this file appropriately 
to suit their platforms. The following command will run the playbook

```
ansible-playbook -i inventory site.yml
```

Once the execution of playbook is finished successfully, it will create a 
folder `admin` in the root of the playbook directory that contains self signed 
TLS certificates, tokens and passwords of the deployment.

Currently, only RHEL 8, CentOS 8, Rockylinux 8, Debian 11 and Ubunutu 22 are supported.
