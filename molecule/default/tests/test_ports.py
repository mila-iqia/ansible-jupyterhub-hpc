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

"""Verification tests for web servers running on different ports"""

import os
import pytest
import yaml


# We run tests against these hosts
testinfra_hosts = ['slurmcontroller']

# Read all ansible vars
ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
hostvars = ansible_vars['hostvars']['slurmcontroller']

# Server running on ports
expected_nginx_ports = ['80', '443']
# Rest of the ports run at IP address of the machine
expected_ports = ['9090', '9100', '8081', 
                  '9080', '3100', '3000']
    

@pytest.mark.parametrize("ports", expected_nginx_ports)
def test_nginx_ports(host, ports):
    s = host.socket(f'tcp://0.0.0.0:{ports}')
    assert s.is_listening
    

@pytest.mark.parametrize("ports", expected_ports)
def test_ports(host, ports):
    s = host.socket(f'tcp://{hostvars["ansible_all_ipv4_addresses"][0]}:{ports}')
    assert s.is_listening


def test_postgresql_port(host):
    s = host.socket('tcp://127.0.0.1:5432')
    assert s.is_listening
