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

"""Embedded ansible filters used by the playbook"""

import sys


if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


def get_type(var, **kwargs):
    """Get type of the variable"""
    return type(var)


def merge_prometheus_config(generated_cfg, existing_cfg):
    """Merge existing and generated configurations of Prometheus"""
    new_cfg = []
    if not existing_cfg or not existing_cfg['scrape_configs']:
        return generated_cfg
    all_scrape_cfgs = existing_cfg['scrape_configs'] + generated_cfg
    job_names = []
    for cfg in all_scrape_cfgs:
        job_names.append(cfg['job_name'])
    job_names = [*dict.fromkeys(job_names)]
    for job_name in job_names:
        for cfg in all_scrape_cfgs:
            if cfg['job_name'] == job_name:
                new_cfg.append(cfg)
                break
    return new_cfg


class FilterModule(object):
    """Core Molecule filter plugins."""

    def filters(self):
        return {
            "get_type": get_type,
            "merge_prometheus_config": merge_prometheus_config,
        }
