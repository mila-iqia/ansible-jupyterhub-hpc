#!/usr/bin/env python
# coding: utf-8

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


import os
import sys

from distutils.dir_util import copy_tree
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

# WARNING: THE FOLLOWING PIECE OF CODE IS SORRRTTT OF A HACK
# WE WANT TO AUTOMATIZE THIS AND WE COULD HAVE DONE IT WITHIN ANSIBLE.
# BUT THE SHARED FILES THAT WE ARE DISTRIBUTING WITH THIS PACKAGE ARE DEPENDENT
# ON PACKAGE PER SE. THAT IS WHY WE DO NECESSARY DATA MANIPULATION HERE!

# The following piece of code needs jupyterhub to be installed in the env
# There are no guarantee that it will work when jupyterhub installation is
# not found. This will also bail if installation is being done system wide ie
# if share directory of env is /usr/local/share
#
# What we are doing here is simply moving the js files in share/ folder of
# the repo to env/share/jupyterhub/components folder so that they can be
# served from hub. We use these js in the spawner form and they are needed
# for better UI experience
#
# env share folder path
env_share_path = os.path.join(sys.prefix, 'share', 'jupyterhub')
# bail if env is system wide
if not env_share_path.startswith('/usr'):
    # share folder
    share_folder = os.path.join(HERE, 'share', 'static', 'jquery')
    # create a dir for jquery-ui
    jq_ui = os.path.join(env_share_path, 'static', 'components', 'jquery-ui')
    os.makedirs(jq_ui, exist_ok=True)
    # copy contents of share to sys.prefix/share/jupyterhub
    copy_tree(share_folder, jq_ui)
    # Set proper permissions
    os.system(f'chown -R 775 {jq_ui}')

with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_desc = f.read()

# setuptools requirements
install_requires = []
with open("requirements.txt") as f:
    for line in f.readlines():
        req = line.strip()
        if not req or req.startswith(("-e", "#")):
            continue
        install_requires.append(req)

setup(
    name="custom_slurm_spawner",
    packages=find_packages(),

    version="1.0.0",

    description="""Custom Spawner:
    A SLURM spawner for Jupyterhub to spawn
    notebooks on HPC platforms.
    """,
    long_description=long_desc,
    long_description_content_type="text/markdown",

    author="Mahendra Paipuri",
    author_email="mahendra.paipuri@idris.fr",

    keywords=["Interactive", "Interpreter", "Shell", "Web", "Jupyter"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],

    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
