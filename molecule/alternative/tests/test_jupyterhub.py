# Copyright 2022 IDRIS / jupyter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Verification tests for setup_jupyterhub role"""

import os
import pytest
import yaml
import testinfra.utils.ansible_runner

# We run tests against these hosts
testinfra_hosts = ['slurmcontroller']

# Read all ansible vars
# ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
# hostvars = ansible_vars['hostvars']['slurmcontroller']

# Directories that are expected to exist
expected_dirs = [
    '/opt/jupyter/jupyterhub/etc/jupyterhub', 
    '/opt/jupyter/jupyterhub/share/jupyterhub',
    '/opt/jupyter/jupyterhub/share/jupyterhub/templates',
    '/opt/jupyter/jupyterhub/etc/ipython', '/var/log/jupyterhub', 
    '/srv/jupyterhub', '/srv/jupyterhub/internal-ssl', 
    '/var/lib/pgsql/data', '/var/log/jupyterhub-proxy',
    '/etc/systemd/system/postgresql.service.d'
]

# Config files that are expected to exist
expected_cfg_files = [
    '/opt/jupyter/jupyterhub/etc/jupyterhub/jupyterhub_config.py',
    '/opt/jupyter/jupyterhub/etc/jupyter/jupyter_notebook_config.py',
    '/etc/systemd/system/postgresql.service.d/stop.conf', 
    '/srv/jupyterhub/nodelist.txt', 
    '/etc/sudoers.d/jupyter',
    '/etc/logrotate.d/jupyterhub', 
    '/etc/logrotate.d/jupyterhub-proxy'
]

# Token files that are expected to exist
expected_token_files = [
    '/srv/jupyterhub/cookie_secret',
    '/srv/jupyterhub/proxy_auth_token',
    '/srv/jupyterhub/crypt_key',
    '/srv/jupyterhub/db_passwd',
    '/srv/jupyterhub/metrics_token'
]

# Pip packages that are expected to exist
expected_pip_pkgs = [
    'batchspawner', 'psycopg2-binary', 'jupyter-server-proxy',
    'cdsdashboards'
]

# System services that are expected to run
expected_services = ['jupyterhub', 'jupyterhub-proxy']

# Rest of the ports run at IP address of the machine
expected_ports = ['8081']


@pytest.mark.parametrize("dirs", expected_dirs)
def test_directories(host, dirs):
    os_name = host.check_output('cat /etc/*-release | grep ^ID=').strip()
    if dirs == '/var/lib/pgsql/data' and os_name in ['ID=debian', 'ID=ubuntu']:
        dirs = '/var/lib/postgresql/data'
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("cfg_files", expected_cfg_files)
def test_config_files(host, cfg_files):
    f = host.file(cfg_files)
    assert f.is_file
    assert f.exists
    
@pytest.mark.parametrize("token_files", expected_token_files)
def test_token_files(host, token_files):
    f = host.file(token_files)
    assert f.is_file
    assert f.exists


@pytest.mark.parametrize("pip_pkgs", expected_pip_pkgs)
def test_pip_pkgs(host, pip_pkgs):
    p = host.pip.get_packages(
        pip_path=f'/opt/jupyter/jupyterhub/bin/pip'
    )
    assert pip_pkgs in p

@pytest.mark.parametrize("services", expected_services)
def test_service(host, services):
    s = host.service(services)
    assert s.is_enabled
    assert s.is_running


@pytest.mark.parametrize("ports", expected_ports)
def test_ports(host, ports):
    ip_addr = host.check_output('hostname -I').strip()
    s = host.socket(
        f'tcp://{ip_addr}:{ports}')
    assert s.is_listening
