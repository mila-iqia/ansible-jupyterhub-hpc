# Configuration

All the important variables of the playbook are placed in [config.yml](../config.yml) 
file and we need to modify these variables appropriately based on the platform. The 
following table gives a brief overview of the different configuration variables

## Generic configuration variables

| **Name**            | **Default value**                      | **Description**                                                                                                                                                |
|---------------------|----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `slurm_bin_path`    | `/usr/bin`                             | Location of SLURM utility binaries. We run JupyterHub as normal system user without any extra privileges except for `sbatch`, `squeue` and `scancel` commands. |
| `conda_prefix`      | `/opt/conda`                           | Location where conda is installed                                                                                                                              |                                                                                             |
| `install_mon_stack` | `True`                                 | Install node exporter, promtail, Prometheus, Loki and Grafana stack                                                                                            |                                                                                                                                                              |

## TLS configuration

The playbook offers to deploy JupyterHub with either self-signed certificates or
certificates signed by an external CA. For testing purposes, self-signed certificates 
might suffice, however, for the production deployments, we recommend to use 
certificates signed by external CA. The playbook is configured to generate 
self-signed certificates and they will be signed by CA that is named as 
`jupyterhub-ca`. This is done as one of the preflight tasks and the certificates 
will be placed at `admin/tls` folder for different hosts.

In case certificates by external CA are used, the deployer must make sure that 
certificates exist at `admin/tls` folder. For example, if the hostname is 
`server.example.com`, we must make sure certificate and key must exist at
`admin/tls/server.example.com/server.example.com.crt` and 
`admin/tls/server.example.com/server.example.com.key`, respectively.

| **Name**            | **Default value**                      | **Description**                                                                                                                                                |
|---------------------|----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `self_signed_certs` | `True`                                 | Use self signed certificates. If set to `False` make sure the certificates exist at `admin/tls/<inventory_hostname>` folder                                    |
| `local_tls_dir`     | `{{ playbook_dir }}/admin/tls`         | Location on Ansible controller machine where TLS certificates are stored                                                                                       |
| `local_tokens_dir`  | `{{ playbook_dir }}/admin/tokens`      | Location on Ansible controller machine where tokens are stored                                                                                                 |
| `local_passwd_dir`  | `{{ playbook_dir }}/admin/credentials` | Location on Ansible controller machine where passwords are stored                                                                                              |                                                                                                                                                              |                                                                                                                                                      |

## JupyterHub

| **Name**                        | **Default value**                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | **Description**                                                                                                                                                                                             |
|---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `install_cds_dashboards`        | `True`                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Install and configure CDS dashboards inside JupyterHub env                                                                                                                                                  |
| `jupyterhub_pkgs`               | `["python=3.9.0",   "jupyterhub=2.3.0",   "jupyterlab=3.2.9",   "notebook=6.4.8"]`                                                                                                                                                                                                                                                                                                                                                                                                 | List of packages to install in JupyterHub env                                                                                                                                                               |
| `jupyterhub_deps`               | `["batchspawner==1.1", "psycopg2-binary==2.9.3"]`                                                                                                                                                                                                                                                                                                                                                                                                                                  | List of jupyterHub dependencies                                                                                                                                                                             |
| `jupyterlab_extensions`         | `["jupyterlab-git==0.34.2", "jupyter-resource-usage==0.6.1", "jupyterlab-topbar==0.6.1", "jupyterlab-system-monitor==0.8.0", "jupyterlab_latex==3.1.0", "jupyter_bokeh==3.0.2", "jupyterlab-lsp==3.10.0", "jupyterlab-gitlab==3.0.0", "jupyterlab-quickopen==1.2.0", "ipywidgets==7.6.3", "plotly==5.6.0", "cdsdashboards==0.6.0", "cdsdashboards[user]==0.6.0", "voila==0.3.5", "streamlit==1.7.0", "dash==2.0.0", "dask-labextension==5.2.0", "sidecar==0.5.1", "bokeh==2.4.2"]` | List of JupyterLab extensions                                                                                                                                                                               |
| `jupyter_env_prefix`            | `/opt/jupyter`                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Directory where JupyterHub conda environment will be created. Ideally this path must be on a shared file system where all compute nodes can access                                                          |
| `jupyter_env_name`              | `jupyterhub`                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Name of the JupyterHub conda environment                                                                                                                                                                    |
| `jupyterhub_system_group`       | `jupyter`                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Name of the JupyterHub system user                                                                                                                                                                          |
| `jupyterhub_srv_dir`            | `/srv/jupyterhub`                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Directory to place all JupyterHub related files, tokens, _etc_. This can be local to the host on which JupyterHub will be deployed and there is no necessity for this folder to be on a shared file system  |
| `jupyterhub_internal_certs_dir` | `{{ jupyterhub_srv_dir }}/internal-ssl`                                                                                                                                                                                                                                                                                                                                                                                                                                            | Directory where TLS certificates for internal communication between JupyterHub components will be placed                                                                                                    |
| `use_postgresql_db`             | `True`                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Use PostgreSQL for JupyterHub database                                                                                                                                                                      |
| `jupyterhub_db_name`            | `jupyterhub`                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | The name of the database in case PostgreSQL DB is used                                                                                                                                                      |
| `jupyterhub_log_dir`            | `/var/log/jupyterhub`                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Directory where JupyterHub logs are placed                                                                                                                                                                  |
| `jupyterhub_admin_users`        | `[]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | List of JupyterHub admin users                                                                                                                                                                              |

## Nginx

| **Name**           | **Default value** | **Description** |
|--------------------|-------------------|-----------------|
| `nginx_https_port` | `443`             | HTTPS port      |
| `nginx_http_port`  | `80`              | HTTP port       |

## Node exporter

More configuration details on node exporter role can be found at
[ansible-node-exporter](https://github.com/cloudalchemy/ansible-node-exporter). 
The list of variables used in the config file of this playbook are listed below

| **Name**                | **Default value**          | **Description**       |
|-------------------------|----------------------------|-----------------------|
| `node_exporter_version` | `1.1.2`                    | Node exporter version |
| `node_exporter_port`    | `9100`                     | Node exporter port    |
| `node_exporter_address` | `{{ inventory_hostname }}` | Node exporter address |

## Prometheus

More details on the Prometheus configuration can be found at 
[ansible-prometheus](https://github.com/cloudalchemy/ansible-prometheus). The 
following variables are provided in config file in the current playbook. Note 
that there is no need to provide scrape configuration as it will be generated 
dynamically as role task and added to prometheus configuration

| **Name**                | **Default value**                                                                                                                                                                                                                                                               | **Description**              |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| `prometheus_version`    | `2.33.0`                                                                                                                                                                                                                                                                        | Prometheus version           |
| `prometheus_port`       | `9090`                                                                                                                                                                                                                                                                          | Prometheus port              |
| `prometheus_address`    | `{{ inventory_hostname }}`                                                                                                                                                                                                                                                      | Prometheus address           |
| `prometheus_web_config` | `tls_server_config:   cert_file: "/etc/prometheus/ssl/cert/{{ inventory_hostname }}.crt"    key_file: "/etc/prometheus/ssl/private/{{ inventory_hostname }}.key" basic_auth_users:      prometheus: "{{ lookup('file', local_passwds_dir + '/prometheus_hashed_passwd') }}"`    | Prometheus web configuration |


## Promtail

This file configures Promtail and the role used to install and configure it can 
be found at [ansible-role-promtail](https://github.com/patrickjahns/ansible-role-promtail).

| **Name**                 | **Default value**                                                                               | **Description**                                                                                     |
|--------------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| `promtail_version`       | `2.4.2`                                                                                         | Promtail version                                                                                    |
| `promtail_config_server` | `http_listen_address: "{{ inventory_hostname }}" http_listen_port: 9080 grpc_listen_port: 9081` | Promtail server configuration. Note that `http_listen_port` and `grpc_listen_port` must be integers |

## Grafana Loki

| **Name**                   | **Default value**          | **Description**                         |
|----------------------------|----------------------------|-----------------------------------------|
| `loki_version`             | `2.4.1`                    | Loki version                            |
| `loki_config_http_address` | `{{ inventory_hostname }}` | Loki HTTP address                       |
| `loki_config_http_port`    | `3100`                     | Loki port                               |
| `loki_config_store`        | `/var/lib/loki`            | Location where Loki data will be stored |
| `loki_config_period`       | `168h`                     | Retention period                        |
| `loki_config_auth`         | `False`                    | Loki authentification                   |

## Grafana

For more configuration options, we need to 
consult the available 
[configuration options](https://github.com/cloudalchemy/ansible-grafana/blob/master/defaults/main.yml) 
in the official repository. Similar to Prometheus, Grafana data sources and 
dashboards configurations are generated as role tasks automatically and hence 
there is no need to provide it in the configuration variables.

| **Name**                 | **Default value**                                                                                                                                     | **Description**                                         |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| `grafana_port`           | `3000`                                                                                                                                                | Grafana port                                            |
| `grafana_address`        | `{{ inventory_hostname }}`                                                                                                                            | Grafana address                                         |
| `grafana_server`         | `protocol: "https" cert_key: "/etc/grafana/ssl/private/{{ inventory_hostname }}.key" cert_file: "/etc/grafana/ssl/cert/{{ inventory_hostname }}.crt"` | Grafana server configuration                            |
| `grafana_security`       | `admin_user: "grafana" admin_password: "{{ lookup('file', local_passwds_dir + '/grafana_passwd') }}" allow_embedding: true`                           | Grafana auth configuration                              |
| `grafana_dashboards_dir` | `{{ playbook_dir }}/grafana-dashboards`                                                                                                               | Locations where custom dashboards of grafana are placed |
