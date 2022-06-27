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

# We run tests against these hosts
testinfra_hosts = ['slurmcontroller']

# Read all ansible vars
ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
hostvars = ansible_vars['hostvars']['slurmcontroller']

# Directories that are expected to exist
expected_dirs = [hostvars['jupyterhub_srv_dir'],
                 hostvars['jupyterhub_internal_certs_dir'],
                 '/var/lib/pgsql/data',
                 '/etc/systemd/system/postgresql.service.d']

# Config files that are expected to exist
expected_cfg_files = ['/etc/systemd/system/postgresql.service.d/stop.conf',
                      os.path.join(hostvars['jupyterhub_srv_dir'],
                                   'nodelist.txt', '/etc/sudoers.d/jupyter')]

# Token files that are expected to exist
expected_token_files = [
    os.path.join(hostvars['jupyterhub_srv_dir'], 'cookie_secret'),
    os.path.join(hostvars['jupyterhub_srv_dir'], 'proxy_auth_token'),
    os.path.join(hostvars['jupyterhub_srv_dir'], 'crypt_key'),
    os.path.join(hostvars['jupyterhub_srv_dir'], 'db_passwd'),
    os.path.join(hostvars['jupyterhub_srv_dir'], 'metrics_token')]


@pytest.mark.parametrize("dirs", expected_dirs)
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("cfg_files", expected_cfg_files)
def test_config_files(host, cfg_files):
    f = host.file(cfg_files)
    assert f.is_file
    assert f.exists


@pytest.mark.parametrize("token_files", expected_token_files)
def test_config_files(host, token_files):
    f = host.file(token_files)
    assert f.is_file
    assert f.exists


def test_service(host):
    s = host.service('postgresql')
    assert s.is_enabled
    assert s.is_running
