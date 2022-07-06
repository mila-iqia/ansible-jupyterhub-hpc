# Description of roles

Here we provide a brief overview of what each role does in the playbook.

## validation

This role validates the environment by checking the Ansible version and OS 
versions on the hosts.

## preflights

This role generates all the necessary certificates, tokens and passwords 
before running the installation tasks.

## setup_hosts

This role installs the common dependencies before installing JupyterHub stack. 
Notably these include nginx, PostgreSQL, *etc*.

## setup_jupyterhub

This role installs JupyterHub and its dependencies. It also generates the 
configuration files for JupyterHub and Jupyter notebook that will be used as 
system-wide configuration files. If admins would like to further customise 
JupyterHub and Jupyter notebook configuration, they can add it to the respective 
files in [templates](../roles/setup_jupyterhub/templates) folder.

## setup_nginx

All the nginx related configuration and certificate installation is done here.

## setup_node_exporter

Install and configure for node exporter. 

## setup_prometheus

Install and configure for Prometheus.

## setup_promtail

Install and configure for Promtail. 

## setup_loki

Install and configure for Grafana Loki. 

## setup_grafana

Install and configure for grafana.

## setup_logrotate

This role sets up the logrotate configuration for JupyterHub, Grafana and nginx.
