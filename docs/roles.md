# Description of roles

Here we provide a brief overview of what each role does in the playbook.

## env_validation

This role validates the environment by checking the Ansible version and OS 
versions on the hosts.

## preflight_checks

This role checks if all the necessary certificates, tokens and passwords are 
generated before running the installation tasks.

## common

This role installs the common dependencies before installing JupyterHub stack. 
Notably these include nginx, PostgreSQL, *etc*.

## install_jupyterhub

This role installs JupyterHub and its dependencies listed in 
[host_vars](../host_vars). It also generates the configuration files for 
JupyterHub and Jupyter notebook that will be used as system-wide configuration 
files.

## install_kernels

This role installs the C++, R and Julia kernels when configured to do so.

## setup_jupyterhub

This role sets up JupyterHub by installing certificates, tokens and keys on the 
host.

## nginx

All the nginx related configuration and certificate installation is done here.

## setup_monitoring

We use roles from Ansible Galaxy to install Prometheus, node exporter, Grafana 
and Promtail. Before doing so, we need some pre-processing steps like creating 
service users and groups, giving them appropriate permissions to read tokens, 
*etc*. These sort of tasks are done within this role.

## grafana_loki

This role installs and configures Grafana Loki.

## setup_jupyterhub_services

This role creates the systemd service files for JupyterHub and configurable HTTP 
proxy. In addition it enables them and starts them.

## logrotate

This role sets up the logrotate configuration for JupyterHub and nginx.