# Documentation for Ansible JupyterHub

This playbook deploys JupyterHub on HPC platforms using 
[batchspawner](https://github.com/jupyterhub/batchspawner) for spawning 
JupyterLab instances on compute nodes. These roles are made especially for HPC 
platforms that use batch schedulers to submit jobs. The current folder contain 
several documentation files that gives us an overview on how to configure and 
use playbook to install JupyterHub.

- [Architecture](architecture.md): The architecture of the JupyterHub 
installation is discussed in brief here along with important notes on security 
implications of the deployment. 
- [Configuration](configuration.md): A brief overview of several important variables 
that system admins must decide before installing the JupyterHub.
- [Inventory](inventory.md): Explanation of how inventory groups are organised.
- [Roles](roles.md): A very high level view of what each role does in the playbook.
- [Deployment](deployment.md): Few deployment examples on how to use the playbook.
