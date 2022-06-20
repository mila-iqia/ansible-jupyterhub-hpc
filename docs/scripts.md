# Scripts

An utility script is provided in [gen-encryption-data](scripts/gen-encryption-data) 
folder that can be used to 
generate self-signed certificates using [Certipy](https://github.com/ly4k/Certipy). 
Besides creating certificates, the script also generates tokens and passwords 
that we will need during the installation process. More details of the script 
can be obtained by running it with `--help` flag

```
# Root of the repository
$ cd scripts
$ ./gen-encryption-data --help
usage: gen-encrypt-data [-h] [-c] [-t] [-p] [-d] [-r]

optional arguments:
  -h, --help            show this help message and exit
  -c, --certs           Generate self-signed certificates for TLS.
  -t, --tokens          Generate tokens for JupyterHub deployment.
  -p, --passwords       Generate passwords for monitoring services.
  -d, --dhparam         Generate diffie-hellman keys for nginx reverse proxy.
  -r, --remove_existing
                        Remove existing data and generate new ones.
```

Before we start the following commands, we need to make sure that we have a 
[hostfile](hostfile) in the root of the repository with all the hosts properly 
configured. The script will need this file to get hostnames which will be 
eventually used in the generation of certificates.

We will use Diffie-Hellman key for enhanced security for nginx reverse proxy. To 
generate it, we need to run the following command,

```
./gen-encryption-data --dhparam
```

Note that this will take a while to generate this key. Following we need to 
create certificates, tokens and passwords using 

```
./gen-encryption-data --certs --tokens --passwords
```

This will create a folder `encryption` that will have the following contents

```
encryption/
├── jp-adminrc
├── nginx_proxy.dhparam.pem
├── ssl
│ ├── certipy.json
│ ├── grafana
│ │ ├── grafana.crt
│ │ └── grafana.key
│ ├── grafana-ca
│ │ ├── grafana-ca.crt
│ │ └── grafana-ca.key
│ ├── nginx
│ │ ├── nginx.crt
│ │ └── nginx.key
│ ├── nginx-ca
│ │ ├── nginx-ca.crt
│ │ └── nginx-ca.key
│ ├── node_exporter
│ │ ├── node_exporter.crt
│ │ └── node_exporter.key
│ ├── node_exporter-ca
│ │ ├── node_exporter-ca.crt
│ │ └── node_exporter-ca.key
│ ├── prometheus
│ │ ├── prometheus.crt
│ │ └── prometheus.key
│ └── prometheus-ca
│     ├── prometheus-ca.crt
│     └── prometheus-ca.key
└── tokens
    ├── cookie_secret
    ├── crypt_key
    ├── db_passwd
    ├── metrics_token
    └── proxy_auth_token

10 directories, 24 files
```

- The file [jp-adminrc](../encryption/jp-adminrc) will have all the admin passwords 
for the monitoring services. 
- The folder [ssl](../encryption/ssl) contains both TLS and CA certificates for 
each service that we will use in the installation.
- Finally [tokens](../encryption/tokens) has all the tokens that we will need 
for installing JupyterHub.

In case if admins want to re-generate the certificates and/or tokens and/or 
passwords, we can use the flag `-r` on the CLI when asking for a given component. 
For instance, if we want to re-generate the certificates

```
./gen-encryption-data -r -c
```
