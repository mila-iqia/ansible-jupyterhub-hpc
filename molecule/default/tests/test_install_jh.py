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

"""Verification tests for install_jupyterhub role"""

import os
import pytest
import yaml
import testinfra.utils.ansible_runner


# We run tests against these hosts
testinfra_hosts = ['slurmcontroller']

# Read all ansible vars
ansible_vars = yaml.safe_load(open('/tmp/ansible-vars.yml', 'r'))
hostvars = ansible_vars['hostvars']['slurmcontroller']

# Directories that are expected to exist
expected_dirs = [hostvars['jupyter_config_dir'], hostvars['jupyter_share_dir'], hostvars['jupyter_templates_dir'], hostvars['jupyterhub_config_dir'],   hostvars['ipython_config_dir']]

# Config files that are expected to exist
expected_cfg_files = [os.path.join(hostvars['jupyterhub_config_dir'], 'jupyterhub_config.py'), os.path.join(hostvars['jupyter_config_dir'], 'jupyter_notebook_config.py')]

# Pip packages that are expected to exist
expected_pip_pkgs = [p.split('==')[0] for p in hostvars['jupyterlab_pip_extensions']]
# Packages cdsdasboards, jupyter_bokeh and jupyterlab_latex 
# needs to be renamed as they will be installed with slight name
# difference
expected_pip_pkgs.remove('cdsdashboards[user]')
expected_pip_pkgs.remove('jupyter_bokeh')
expected_pip_pkgs.remove('jupyterlab_latex')
expected_pip_pkgs.extend(['jupyter-bokeh', 'jupyterlab-latex'])
    

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
    

@pytest.mark.parametrize("pip_pkgs", expected_pip_pkgs)
def test_pip_pkgs(host, pip_pkgs):
    p = host.pip.get_packages(pip_path=f'{hostvars["jupyterhub_env_bin_path"]}/pip')
    assert pip_pkgs in p

