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
testinfra_hosts = ['slurmcontroller']

# Read all ansible vars
ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
hostvars = ansible_vars['hostvars']['slurmcontroller']

@pytest.mark.parametrize("packages", hostvars['dev_tools']
                         + ['conda', 'postgresql-server', 
                           'python3-psycopg2'])
def test_package(host, packages):
    p = host.package(packages)
    assert p.is_installed
   

def test_conda_config(host):
    f = host.file('/opt/conda/.condarc')
    assert f.is_file
