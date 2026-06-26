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

"""Verification tests for node exporter"""

import os
import pytest
import yaml
import testinfra.utils.ansible_runner

# We run tests against these hosts
testinfra_hosts = ['slurmcluster']

# Systemd service files that are expected to exist
expected_cfg_files = ['/etc/node_exporter/web_config.yml']

# System services that are expected to run
expected_services = ['node_exporter']

# Rest of the ports run at IP address of the machine
expected_ports = ['9100']

# Read all ansible vars
# ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
# hostvars = ansible_vars['hostvars']['slurmcontroller']

@pytest.mark.parametrize("cfg_files", expected_cfg_files)
def test_config_files(host, cfg_files):
    f = host.file(cfg_files)
    assert f.is_file
    assert f.exists


@pytest.mark.xfail(reason="issues with bcrypt not hashing passwords correctly")
@pytest.mark.parametrize("services", expected_services)
def test_service(host, services):
    s = host.service(services)
    assert s.is_enabled
    assert s.is_running


@pytest.mark.xfail(reason="issues with bcrypt not hashing passwords correctly")
@pytest.mark.parametrize("ports", expected_ports)
def test_ports(host, ports):
    s = host.socket(
        f'tcp://127.0.0.1:{ports}')
    assert s.is_listening
