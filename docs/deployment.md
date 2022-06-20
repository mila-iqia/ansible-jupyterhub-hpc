# Deployment

The following examples show some modes of deploying JupyterHub using the current 
Ansible playbook.

## Using Self-Signed Certificates

After we have created the necessary certificates, tokens and passwords 
as briefed in [scripts](scripts.md) file and setting up the 
[hostfile](../hostfile), we can start installing using

```
source encryption/jp-adminrc
ansible-playbook -i hostfile site.yml
```

## Using External Certificates

Currently, we do not support using external certificates for some services and 
self-signed certificates for others. If we want to use, the easiest approach is 
to first create self-signed certificates and then replace the TLS certificates 
and keys in each folder with the external ones with same name. Then we can 
run same set of commands to start installation as shown in above example

## Skip Monitoring Services

If we wish not to install monitoring services, we can use `--skip-tags` flag of 
`ansible-playbook` as follows

```
source encryption/jp-adminrc
ansible-playbook -i hostfile site.yml --skip-tags "monitoring"
```

## Update Configurations

If we changed JupyterHub configuration and wish to update the configuration 
file, we can use

```
source encryption/jp-adminrc
ansible-playbook -i hostfile site.yml --tags "install_jh_config"
```

Similarly, `nginx` configuration can be updated using

```
source encryption/jp-adminrc
ansible-playbook -i hostfile site.yml --tags "install_nginx_config"
```




