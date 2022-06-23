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

"""Verification tests for setup_monitoring role"""

import os
import pytest
import yaml


# We run tests against these hosts
testinfra_hosts = ['slurmcontroller']

# Read all ansible vars
ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
hostvars = ansible_vars['hostvars']['slurmcontroller']

# Directories that are expected to exist
expected_dirs = [hostvars['remote_path_node_exporter_ssl'], hostvars['remote_path_prometheus_ssl'], hostvars['remote_path_grafana_ssl']]

# Systemd service files that are expected to exist
expected_cert_files = [os.path.join(hostvars['remote_path_node_exporter_ssl'], hostvars['ssl_key_name_node_exporter']), os.path.join(hostvars['remote_path_node_exporter_ssl'], hostvars['ssl_cert_name_node_exporter']), os.path.join(hostvars['remote_path_prometheus_ssl'], hostvars['ssl_key_name_prometheus']), os.path.join(hostvars['remote_path_prometheus_ssl'], hostvars['ssl_cert_name_prometheus']), os.path.join(hostvars['remote_path_grafana_ssl'], hostvars['ssl_key_name_grafana']), os.path.join(hostvars['remote_path_grafana_ssl'], hostvars['ssl_cert_name_grafana'])]
    

@pytest.mark.parametrize("dirs", expected_dirs)
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists
   

@pytest.mark.parametrize("cert_files", expected_cert_files)
def test_cert_files(host, cert_files):
    f = host.file(cert_files)
    assert f.is_file
    assert f.exists
