# Changelog

## v2.2.1

### Changed
- **Namespace Rename**: Updated the role's namespace to conform with new naming conventions.
- **Variable Restructuring**: Moved all user-configurable variables to `defaults/main.yml` and cleaned up `vars/main.yml` to allow proper overriding via `group_vars` and `host_vars`.

### Removed
- **Deprecated Ansible `conda` Module**: Replaced the native `conda:` module with direct `micromamba` execution (`ansible.builtin.command`) to speed up dependency resolution and improve installation reliability.

### Fixed
- Fixed a variable evaluation failure on Debian 13 .

## v2.2.0

- Fix bug on configuring alternative subject names for JupyterHub
- Update CI infra

## v2.1.0

- Make spawner form configurable

## v2.0.1

- Use FQDN for custom filters

## v2.0.0

- Major refactoring of collections to simplify deployment
- Removal of less critical components like Grafana loki and promtail

## v0.1

- initial release containing ansible roles for deploying jupyterhub on HPC platforms
