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

"""Verification tests to for logrotate role"""

import os
import pytest
import yaml

# We run tests against these hosts
testinfra_hosts = ['slurmcontroller']

# Read all ansible vars
# ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
# hostvars = ansible_vars['hostvars']['slurmcontroller']

# Directories that are expected to exist
expected_dirs = ['/etc/logrotate.d']

# Systemd service files that are expected to exist
expected_cfg_files = ['/etc/logrotate.d/jupyterhub',
                      '/etc/logrotate.d/jupyterhub-proxy',
                      '/etc/logrotate.d/nginx', '/etc/logrotate.d/grafana']


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
