# Ansible JupyterHub

This repository contains production ready Ansible roles for deploying JupyterHub on HPC platforms. By default, the roles are configured to install custom implementations of [SSHAuthenticator](https://github.com/andreas-h/sshauthenticator) and [batchspawner](https://github.com/jupyterhub/batchspawner) for authenticating into Hub and spawning jupyter servers, respectively. The user can change these default settings by appropriately modifying the JupyterHub configuration. More details are provided in docs.

## Getting started

For a very quick setup use following instructions

```
git clone https://gitlab.com/i2461/jupyter/ansible-jupyterhub.git
cd ansible-jupyterhub
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
```
Now we need to edit the [inventory.example](inventory.example) file to setup host names for different hosts and place it in the root of the repository naming `inventory`.  If we want to run the roles with default configuration, use following commands

```
ansible-playbook -i inventory site.yml
```

Currently, only RHEL 8 and above is supported. In future support for Debian and Ubuntu distros will be added

