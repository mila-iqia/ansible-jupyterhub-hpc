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

"""Verification tests for common role"""

import os
import pytest
import yaml
import testinfra.utils.ansible_runner

# We run tests against these hosts
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("packages",
                         ['git', 'htop', 'nano', 'tree', 'net-tools', 
                          'python3-psycopg2'])
def test_package(host, packages):
    p = host.package(packages)
    assert p.is_installed


def test_micromamba(host):
    f = host.file('/usr/local/bin/micromamba')
    assert f.is_file
