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
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

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
    name="sshauthenticator",
    packages=find_packages(),

    version="1.0.0",
    
    description="""SSH authenticator for JupyterHub.""",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    
    author="Mahendra Paipuri",
    author_email="mahendra.paipuri@idris.fr",
    
    keywords=["Interactive", "SSH", "Authenticator", "Web", "Jupyter"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],

    entry_points={
        'jupyterhub.authenticators': [
            'myservice = sshauthenticator:SSHAuthenticator',
        ],
    },
    
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
