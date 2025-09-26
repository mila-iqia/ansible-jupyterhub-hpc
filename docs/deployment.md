# Deployment

The following examples show some modes of deploying JupyterHub using the current
Ansible playbook.

## Inventory

We can deploy JupyterHub and the monitoring stack in one machine by using an
inventory file as follows

```ini
[jupyterhub]
server.example.com

[prometheus]
server.example.com

[grafana]
server.example.com

[nginx:children]
jupyterhub

[node_exporter:children]
jupyterhub
```

The playbooks are designed to be able to update the configurations of
existing Prometheus and Grafana installations on the machine. However, it is not
very well tested.

## Playbook

A sample playbook is shown as follows:

```yaml
- name: Import JupyterHub collection
  ansible.builtin.import_playbook: mahendrapaipuri.ansible_jupyterhub_hpc.deploy.yml
  # Any variables that needs customization can be declared here
  # vars:
  #   jupyterhub_service_name: jupyterhub.example.com
```

## Using Self-Signed Certificates

By default playbook will use self signed certificates for nginx. The created CA `jupyterhub-ca`
is installed to remote machines at at `/etc/pki/tls` for RedHat flavoured OS and `/etc/ssl`
for Debian flavoured OS.

## Using External Certificates

If TLS certificates issued by external CA are used, make sure that we place them
on the remote machines at `/etc/pki/tls` for RedHat flavoured OS and `/etc/ssl`
for Debian flavoured OS. It is important that the certificate and key names should
match the name of `jupyterhub_service_name`.

## Skip Monitoring Services

If we wish not to install monitoring services, set `install_mon_stack` to
`false` as follows:

```yaml
- name: Import JupyterHub collection
  ansible.builtin.import_playbook: mahendrapaipuri.ansible_jupyterhub_hpc.deploy.yml
  # Any variables that needs customization can be declared here
  vars:
    install_mon_stack: false
```

## Update Configurations

If we changed JupyterHub configuration and wish to update the configuration
file, we can use

```bash
ansible-playbook -i inventory deploy.yml --tags "configure_jupyterhub"
```

Similarly, `nginx` configuration can be updated using

```bash
ansible-playbook -i inventory deploy.yml --tags "configure_nginx"
```

After these steps, we need to manually restart JupyterHub, JupyterHub proxy
and/or nginx services.
