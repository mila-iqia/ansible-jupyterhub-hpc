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

"""Verification tests for nginx role"""

import os
import pytest
import yaml
import testinfra.utils.ansible_runner

# We run tests against these hosts
testinfra_hosts = ['slurmcontroller']

# Directories that are expected to exist
expected_dirs = ['/etc/nginx/ssl']

# Systemd service files that are expected to exist
expected_cert_files = ['/etc/nginx/ssl/cert/slurmcontroller.crt',
                       '/etc/nginx/ssl/private/slurmcontroller.key',
                       '/etc/nginx/ssl/slurmcontroller.dhparam.pem', 
                       '/etc/logrotate.d/nginx']

# System services that are expected to run
expected_services = ['nginx']

# Server running on ports
expected_nginx_ports = ['80', '443']


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


@pytest.mark.parametrize("services", expected_services)
def test_service(host, services):
    s = host.service(services)
    assert s.is_enabled
    assert s.is_running

@pytest.mark.parametrize("ports", expected_nginx_ports)
def test_nginx_ports(host, ports):
    s = host.socket(f'tcp://0.0.0.0:{ports}')
    assert s.is_listening
