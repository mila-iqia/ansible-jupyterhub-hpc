# Description of roles

Here we provide a brief overview of what each role does in the playbook.

## validation

This role validates the environment by checking the Ansible version and OS
versions on the hosts.

## preflights

This role generates all the necessary certificates, tokens and passwords
before running the installation tasks.

## common

This role installs the common dependencies before installing JupyterHub stack.
Notably these include nginx, PostgreSQL, *etc*.

## jupyterhub

This role installs JupyterHub and its dependencies. It also generates the
configuration files for JupyterHub and Jupyter notebook that will be used as
system-wide configuration files.

## nginx

All the nginx related configuration and certificate installation is done here.

## monitoring

Setup necessary facts for monitoring related components.

## logrotate

This role sets up the logrotate configuration for JupyterHub, Grafana and nginx.
