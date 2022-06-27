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

"""Verification tests to check if all monitoring services are running"""

import os
import pytest
import yaml

# We run tests against these hosts
testinfra_hosts = ['slurmcontroller']

# Read all ansible vars
ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
hostvars = ansible_vars['hostvars']['slurmcontroller']

# Directories that are expected to exist
expected_dirs = ['/etc/grafana', '/etc/grafana', '/etc/prometheus',
                 '/etc/node_exporter', '/etc/promtail', '/etc/loki']

# Systemd service files that are expected to exist
expected_cfg_files = ['/var/lib/grafana/dashboards/jupyterhub-dashboard.json',
                      '/etc/grafana/grafana.ini',
                      '/etc/prometheus/prometheus.yml',
                      '/etc/promtail/promtail.yml',
                      '/etc/node_exporter/config.yaml', '/etc/loki/loki.yml']

# System services that are expected to run
expected_services = ['grafana-server', 'prometheus', 'node_exporter',
                     'promtail', 'loki']


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


@pytest.mark.parametrize("services", expected_services)
def test_service(host, services):
    s = host.service(services)
    assert s.is_enabled
    assert s.is_running
