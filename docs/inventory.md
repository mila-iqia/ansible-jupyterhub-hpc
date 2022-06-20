# Host groups

An example [inventory.example](../inventory.example) file is 
provided with the repository and we can modify it appropriately according to 
our needs. Currently, we have the following set of host groups that will be used in the 
playbook. 

- `jupyterhub`: The host where JupyterHub and its supporting components like 
`configurable-http-proxy`, `jupyterlab`, *etc*, will be installed. All the 
JupyterHub related tokens, certificates will also be stored on this host. This 
is the main host for installing JupyterHub.
- `compute`: We need to provide a list of hostnames of all compute nodes in the 
HPC platform where we want to be able to spawn JupyterLab instances. Nothing 
will be installed on these nodes. We need this just to add them as Subject 
Alternative Names (SAN) in the internal self signed certificates that Hub will 
generate for each spawn. If we do not add them to the certificate, JupyterHub 
which will be running on `jupyterhub` host and JupyterLab that will be running 
on compute node of the HPC platform will not be able to communicate.
- `nginx`: By default, it will be the same host as the `jupyterhub` host. We can 
configure it to be different host than `jupyterhub` by removing `children` 
keyword from the header in the [hostfile](../hostfile)
- `node_exporter`: This is the host where we collect the metrics and send them 
to Prometheus. This should be same host as the `jupyterhub` host and we should 
not change it.
- `promtail`: Promtail should run on same host as `nginx` to send the `nginx` 
logs to Loki and eventually display them as Grafana dashboards. We should not 
change this group as well.
- `prometheus`: The host where we would like to deploy Prometheus. It can be 
same host as `jupyterhub` or different one. 
- `grafana_loki`: Host where logs sent by Promtail are processed and sent to 
Grafana dashboards. By default it will be installed on same host as `jupyterhub` 
but it can be installed on different host as well
- `grafana`: The host where Grafana will be installed. Similar to `prometheus`, 
by default same host as `jupyterhub` is used but can be configured otherwise.
- `jupyterhubstack`: This is ensemble of all hosts bar compute nodes and 
normally there is no need to modify it in the file.