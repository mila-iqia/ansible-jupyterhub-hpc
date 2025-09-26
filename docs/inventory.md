# Host groups

An example [inventory.example](../inventory.example) file is
provided with the repository and we can modify it appropriately according to
our needs. Currently, we have the following set of host groups that will be used in the
playbook.

- `jupyterhub`: The host where JupyterHub and its supporting components like
`configurable-http-proxy`, `jupyterlab`, *etc*, will be installed. All the
JupyterHub related tokens, certificates will also be stored on this host. This
is the main host for installing JupyterHub.

- `nginx`: By default, it will be the same host as the `jupyterhub` host. We can
configure it to be different host than `jupyterhub` by removing `children`
keyword from the header in the [hostfile](../hostfile)

- `node_exporter`: This is the host where we collect the metrics and send them
to Prometheus. This should be same host as the `jupyterhub` host and we should
not change it.

- `prometheus`: The host where we would like to deploy Prometheus. It can be
same host as `jupyterhub` or different one.

- `grafana`: The host where Grafana will be installed. Similar to `prometheus`,
by default same host as `jupyterhub` is used but can be configured otherwise.
