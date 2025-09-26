# Ansible playbook for deploying JupyterHub on HPC platforms

This repository contains production ready Ansible playbook for deploying JupyterHub
on HPC platforms. In addition, the admins can deploy node exporter,
Prometheus and Grafana stack for monitoring the Hub deployment.
By default, playbook is configured to install
[batchspawner.SlurmSpawner](https://github.com/jupyterhub/batchspawner)
for spawning jupyter servers. The admins can change these default
settings by appropriately modifying the JupyterHub configuration. More details
are provided in docs.

## Getting started

For a very quick setup use following instructions. We recommend to use
a virtual environment on the Ansible controller machine to install ansible.

First install Python prerequisites in the created virtual environment.

```bash
pip install -r https://gitlab.com/idris-cnrs/jupyter/ansible-jupyterhub-hpc/-/raw/main/requirements.txt
```

Next install Ansible prerequisites including the collection itself.

```bash
ansible-galaxy role install -r https://gitlab.com/idris-cnrs/jupyter/ansible-jupyterhub-hpc/-/raw/main/requirements.yml
ansible-galaxy collection install git+https://gitlab.com/idris-cnrs/jupyter/ansible-jupyterhub-hpc.git,main
```

All the important configuration details for the deployment are placed in
[group_vars](./playbooks/group_vars) file. An example inventory file is provided as
[inventory.example](inventory.example). More details in [docs](docs/).

## Usage

This collection can be imported into playbooks and customized based on your
deployments. First create an inventory file based on [inventory.example](inventory.example).
Now create a sample playbook with following content as `deploy.yml`:

```yaml
- hosts: all
  tasks:
    - ansible.builtin.debug:
        msg: Deploying JupyterHub

- name: Import JupyterHub collection
  ansible.builtin.import_playbook: mahendrapaipuri.ansible_jupyterhub_hpc.deploy.yml
  # Any variables that needs customization can be declared here
  vars:
    jupyterhub_service_name: jupyterhub.example.com
```

Once the inventory file and playbook file are created, playbook can be executed using:

```bash
ansible-playbook -i inventory deploy.yml
```

Once the execution of playbook is finished successfully, it will create a
`jupyterhub-admin-rc` file in the `/root` of the remote JupyterHub host with
all the secrets used in the deployment.

Currently, only RHEL 8/9, Rockylinux 8/9, Debian 11/12 and Ubunutu 22/24 are supported.
