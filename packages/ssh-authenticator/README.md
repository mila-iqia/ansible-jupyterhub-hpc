# Jupyter SSH authenticator

This project is the extension of basic SSH authenticator developed in https://github.com/andreas-h/sshauthenticator. Essentially, some sanity checks are included in the original authenticator developed by the author. Also, logging is enabled in the authenticator as it is necessary in production deployments to track the users that are trying to log into the hub.


## Configuration

We need to do minimal configuration for this authenticator to work. This can be directly added to the JupyterHub configuration file. Before setting up the configuration, we need to enable the authenticator using

```
c.JupyterHub.authenticator_class = 'sshauthenticator.SSHAuthenticator'
```

Most important configuration parameters are

```
c.SSHAuthenticator.server_address = 'sshauthhost.example.com'
c.SSHAuthenticator.server_port = 22
```

where `server_address` is th host that will authenticate the user by attempting to establish a SSH connection and `server_port` is the SSH port which will be defaulted to 22. **Note** that `server_port` should be a `int` type.

Additionally, there is one more configuration parameter

```
c.SSHAuthenticator.valid_username_regex = r"[a-zA-Z0-9]*"
```

If specified, the username is matched against this regex pattern and all the usernames that do not match will be automatically denied even before attempting SSH connection. It helps to reduce the brute force attacks.
