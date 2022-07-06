# Deployment

The following examples show some modes of deploying JupyterHub using the current 
Ansible playbook.

## All in one

We can deploy JupyterHub and the monitoring stack in one machine by using an 
inventory file as follows

```
[jupyterhub]
server.example.com

[prometheus]
server.example.com

[loki]
server.example.com

[grafana]
server.example.com

[nginx:children]
jupyterhub

[node_exporter:children]
jupyterhub

[promtail:children]
nginx
```

The playbook also supports to install Prometheus, Grafana and Grafana Loki on 
different machines. 

```
[jupyterhub]
server1.example.com

[prometheus]
server2.example.com

[loki]
server3.example.com

[grafana]
server4.example.com

[nginx:children]
jupyterhub

[node_exporter:children]
jupyterhub

[promtail:children]
nginx
```

The playbooks are designed to be able to update the configurations of 
existing Prometheus and Grafana installations on the machine. However, it is not 
very well tested.

## Using Self-Signed Certificates

Make sure we set `self_signed_certs` variable in [config.yml](../config.yml) to 
`True` and then we need to simply run

```
ansible-playbook -i hostfile site.yml
```

This will create TLS certificates and keys signed by `jupyterhub-ca` and place 
them in `admin/tls` folder on Ansible controller and also copies them to remote 
machines. 

## Using External Certificates

If TLS certificates issued by external CA are used, make sure that we place them 
in `admin/tls` folder before running the playbook. For instance, if we want to 
deploy JupyterHub on machine `server.example.com` then we must ensure that we 
have files at `admin/tls/server.example.com/server.example.com.crt` and 
`admin/tls/server.example.com/server.example.com.key` before running the playbook.
It is important that folder, certificate and key names should match the name of 
the host in the inventory file.

## Skip Monitoring Services

If we wish not to install monitoring services, set `install_mon_stack` to 
`False` and run the playbook

## Update Configurations

If we changed JupyterHub configuration and wish to update the configuration 
file, we can use

```
ansible-playbook -i hostfile site.yml --tags "configure_jupyterhub"
```

Similarly, `nginx` configuration can be updated using

```
source encryption/jp-adminrc
ansible-playbook -i hostfile site.yml --tags "configure_nginx"
```

After these steps, we need to manually restart JupyterHub, JupyterHub proxy 
and/or nginx services.
