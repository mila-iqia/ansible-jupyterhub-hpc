# Group variables

All group variables are placed in the [group_vars](../group_vars) folder in 
the root of the repository. Each variable is described in detail as comments in 
the file. Below we give high level overview of each file and what it configures

## all.yaml

We can configure where to install monitoring services using `install_mon_stack` 
variable defined in this file. Similarly, the use of self-signed certificates 
can also be configured using `self_signed_certs` variable. Similarly, the 
variable `install_cds_dashboards` control whether to install 
[ContainDS Dashboards](https://cdsdashboards.readthedocs.io/en/stable/). 
Rest of the variables defined in this file need not be changed unless we want to 
change names and/or locations of TLS certificates.

## grafana.yaml

All configuration related to Grafana is placed here. We use the officially 
supported [Ansible role for installing Grafana](https://github.com/cloudalchemy/ansible-grafana).
Thus if we want to change and/or add more configuration options, we need to 
consult the available 
[configuration options](https://github.com/cloudalchemy/ansible-grafana/blob/master/defaults/main.yml) 
in the official repository.

## grafana_loki.yaml

This file configures Grafana loki. Most of the variables do not need 
modification. The important ones that needs review are `loki_config_period` and 
`loki_config_http_port`.

## jupyterhub.yaml

The following are important variables that we need to look at

- `jupyter_env_prefix`: We use conda environment to install all JupyterHub 
related stack. This variable controls the location of that environment. Ideally 
we should use a location on shared file system where all compute nodes can 
access the binaries and libraries.
- `slurm_bin_path`: We need to all absolute paths to SLURM utility commands like 
`squeue`, `sbatch` and `scancel` to sudoers list so that the service user that 
runs the JupyterHub can use `sudo` for these commands. This variable sets the 
location of these SLURM binaries.
- `use_postgresql_db`: By default JupyterHub uses `sqlite3` database for keeping 
track of the state of JupyterHub. In production environments, JupyterHub 
developers advise to use traditional RDBMS database, such as PostgreSQL. Setting 
this variable to `true` will install PostgreSQL and sets up a database for 
JupyterHub
- `jupyterhub_admin_users`: List of administrator users for JupyterHub

## nginx.yaml

The important variable in this file is `nginx_run_as_service_user` which controls 
whether nginx will be run as `root` or a normal user. For enhanced security we 
recommend it to set to `true` so that nginx will run as normal user and we use 
capabilities for binding the ports less than 1024. We can also set the `http` 
and `https` ports where nginx reverse proxy will run.

## node_exporter.yaml

The configuration of node exporter is provided in this file. More details can be 
found at [ansible-node-exporter](https://github.com/cloudalchemy/ansible-node-exporter).

## prometheus.yaml

More details on the Prometheus configuration can be found at 
[ansible-prometheus](https://github.com/cloudalchemy/ansible-prometheus).

## promtail.yaml

This file configures Promtail and the role used to install and configure it can 
be found at [ansible-role-promtail](https://github.com/patrickjahns/ansible-role-promtail).


# Host variables

Similarly, host variables are placed at [host_vars](../host_vars) and an example 
file [hostname.example](../host_vars/hostname.example) is provided. List of 
packages that will be installed alongside JupyterHub and their versions can be 
specified here. It also contains variables like `install_cpp_kernel` that can be 
used to configure whether to install different kernels like C++, Julia, R.
