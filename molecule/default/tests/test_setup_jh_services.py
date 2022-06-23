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

"""Verification tests for setup_jupyterhub_services role"""

import os
import pytest
import yaml


# We run tests against these hosts
testinfra_hosts = ['slurmcontroller']

# Read all ansible vars
ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
hostvars = ansible_vars['hostvars']['slurmcontroller']

# Expected directories to exist
expected_dirs = ['/var/log/jupyterhub', '/var/log/jupyterhub-proxy']

# Systemd service files that are expected to exist
expected_service_files = ['/etc/sysconfig/jupyterhub-proxy',
                          '/etc/sysconfig/jupyterhub',
                          '/etc/systemd/system/jupyterhub-proxy.service',
                          '/etc/systemd/system/jupyterhub.service']

# System services that are expected to run
expected_services = ['jupyterhub', 'jupyterhub-proxy']


@pytest.mark.parametrize("dirs", expected_dirs)
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists

@pytest.mark.parametrize("service_files", expected_service_files)
def test_service_files(host, service_files):
    f = host.file(service_files)
    assert f.is_file
    assert f.exists
    

@pytest.mark.parametrize("services", expected_services)
def test_service(host, services):
    s = host.service(services)
    assert s.is_enabled
    assert s.is_running
