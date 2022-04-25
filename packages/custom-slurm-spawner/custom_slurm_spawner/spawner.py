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

"""Main file that contains classes to override in base and slurm spawner"""

import os
import re
import copy
import shlex
import json
import subprocess
import pwd

from batchspawner import SlurmSpawner
from batchspawner import JobStatus
from batchspawner import format_template

from traitlets import Unicode, Dict, default


class CustomSlurmSpawner(SlurmSpawner):
    """
    This class is derived from the base SlurmSpawner and we can customize
    the spawner according to our HPC platform
    """
    
    # Jupyterhub env bin directory path. We add this to PATH to make sure
    # binaries are available to SLURM job
    req_jupyter_bin_path = Unicode(
        "",
        help="Path to the bin dir where jupyerhub and servers are installed"
    ).tag(config=True)
    
    # Xues cling bins path
    req_cling_bin_path = Unicode(
        "",
        help="Path to the bin dir where Xeus Cling is installed"
    ).tag(config=True)
    
    # Julia bins path
    req_julia_bin_path = Unicode(
        "",
        help="Path to the bin dir where Julia is installed"
    ).tag(config=True)
    
    # R bins path
    req_r_bin_path = Unicode(
        "",
        help="Path to the bin dir where R is installed"
    ).tag(config=True)

    # Additional #SBATCH directives to be formed based on Spawner form options
    req_sbatch = Unicode(
        "",
        help="#SBATCH directives to include into job submission script",
    ).tag(config=True)

    # List of modules to be loaded in the job script
    req_modules = Unicode(
        "",
        help="List of modules to be loaded in the job submission script",
    ).tag(config=True)
    
    def _batch_script_default(self):
        """SLURM batch script placeholder"""
        return """#!/bin/bash
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --output={{homedir}}/jupyterhub_slurm.out
#SBATCH --error={{homedir}}/jupyterhub_slurm.err
#SBATCH --chdir={{homedir}}
#SBATCH --export={{keepvars}}
#SBATCH --account={{account}}
{% if sbatch %}{{sbatch}} {% endif %}

echo "< Hi, My name is stegosaurus. The logs that you are looking
for are at ${HOME}/jupyter_slurm_logs/jupyter-${SLURM_JOB_ID}.out.
I am just a placeholder ¯\_(ツ)_/¯ >
 ----------------------------------------------------------------"

cat << 'END_STEG'
o                             .       .
 o                           / `.   .' "
  o                  .---.  <    > <    >  .---.
   o                 |    \  \ - ~ ~ - /  /    |
         _____          ..-~             ~-..-~
        |     |   \~~~\.'                    `./~~~/
       ---------   \__/                        \__/
      .'  O    \     /               /       \  "
     (_____,    `._.'               |         }  \/~~~/
      `----.          /       }     |        /    \__/
            `-.      |       /      |       /      `. ,~~|
                ~-.__|      /_ - ~ ^|      /- _      `..-'
                     |     /        |     /     ~-.     `-. _  _  _
                     |_____|        |_____|         ~ - . _ _ _ _ _>
END_STEG

export JUPYTER_LOG_DIR={{homedir}}/jupyter_slurm_logs
mkdir -p ${JUPYTER_LOG_DIR}

{ set -xeo pipefail;
  trap 'echo SIGTERM received' TERM;
  
  export _WORK_SYMLNK=$HOME/work;
  export _SCRATCH_SYMLNK=$HOME/scratch;
  if [ ! -z "${WORK}" ] && [ ! -L "${_WORK_SYMLNK}" ]; then ln -s ${WORK} ${_WORK_SYMLNK}; fi;
  if [ ! -z "${SCRATCH}" ] && [ ! -L "${_SCRATCH_SYMLNK}" ]; then ln -s ${SCRATCH} ${_SCRATCH_SYMLNK}; fi;

  echo "=============================================================================="
  echo "SLURM job details: ";
  echo "=============================================================================="
  scontrol show -dd job ${SLURM_JOB_ID}
  echo "=============================================================================="

  {% if jupyter_bin_path %}export PATH={{ jupyter_bin_path }}:$PATH; {% endif %}
  {% if julia_bin_path %}export PATH={{ julia_bin_path }}:$PATH; {% endif %}
  {% if r_bin_path %}export PATH={{ r_bin_path }}:$PATH; {% endif %}
  
  CERTS_DIR=$(dirname ${JUPYTERHUB_SSL_KEYFILE})
  mkdir -p ${CERTS_DIR}
  echo "${JUPYTERHUB_SSL_KEYFILE_CERT}" > ${JUPYTERHUB_SSL_KEYFILE}
  echo "${JUPYTERHUB_SSL_CERTFILE_CERT}" > ${JUPYTERHUB_SSL_CERTFILE}
  echo "${JUPYTERHUB_SSL_CLIENT_CA_CERT}" > ${JUPYTERHUB_SSL_CLIENT_CA}
  
  {% if modules %}module load {{ modules }}; {% endif %}

  which jupyterhub-singleuser;
  {{cmd}};
  echo "jupyterhub-singleuser ended gracefully"; 
} > ${JUPYTER_LOG_DIR}/jupyter-${SLURM_JOB_ID}.out 2>${JUPYTER_LOG_DIR}/jupyter-${SLURM_JOB_ID}.err
"""
    
    def get_avail_modfiles(self):
        """Get available module files. We use this list to provide
        an autocomplete functionality for modules form data. This helps
        user to get list of modules without having to know their exact
        names"""
        # First check TCL modules
        mod_cmd = os.getenv('MODULES_CMD', default='')
        # If TCL module is not installed on system, check for LMOD
        if not mod_cmd:
            mod_cmd = os.getenv('LMOD_CMD', default='')
        # Bail if MODULES_CMD or LMOD_CMD is not set.
        if not mod_cmd:
            return json.dumps([])
        # Command to get available modules
        cmd = f'{mod_cmd} python avail'
        # Use shlex to split command string
        cmd = shlex.split(cmd)
        # Execute command that will give list of available modules
        completed = subprocess.run(cmd, shell=False, check=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        # Decode the output and splitlines
        mod_output = completed.stdout.decode().splitlines()
        # Make them into a list
        avail_mods = []
        for line in mod_output:
            line = line.split()
            for mod in line:
                # Ignore paths and ------ lines
                if mod.startswith('-') or mod.startswith('/'):
                    continue
                # Some of the module names comes with aux info in 
                # paranthesis. We need to remove it before loading
                # module
                re_search = re.search(r"\(([^)]*)\)", mod)
                if re_search:
                    mod = mod.replace(re_search.group(), '').strip()
                avail_mods.append(mod)
        # Stringify the list so that we can pass it to Js
        return json.dumps(avail_mods)

    def _options_form_default(self):
        """Create a form for the user to choose the configuration for the
        SLURM job"""
        # Get existing spawning profiles
        # user_spawn_profiles = self.read_spawning_preferences()
        # Get profile names
        # opts_string = ''
        # for profile in user_spawn_profiles.keys():
        #     opts_string += f'<option value="{profile}">{profile}</option>\n'
        # Stringify dict
        # spawn_profiles = json.dumps(user_spawn_profiles, indent=2)
        # Get available module files
        mod_files = self.get_avail_modfiles()
        return """<strong>
  <p>
    The following fields are used in SLURM batch script submission.
  </p>
</strong>
<br>
<div class="form-group row">
  <div class="col-sm-6">
    <label for="account">Account</label>
    <span class="help-icon" data-toggle="tooltip" data-placement="top" title="SLURM Account.">
      <span class="fa fa-question-circle"></span>
    </span>
    <input id="account" name="account" class="form-control" size="15" type="text" placeholder="e.g. myacc"></input>
  </div>
  <div class="col-sm-6">
    <label for="walltime">Time</label>
    <span class="help-icon" data-toggle="tooltip" data-placement="top" title="Requested time for SLURM reservation.">
      <span class="fa fa-question-circle"></span>
    </span>
    <input id="walltime" name="walltime" class="form-control" size="15" type="text" placeholder="e.g. 01:00:00 for 1 hour"></input>
  </div>
</div>
<div class="form-group row">
  <div class="col-sm-6">
    <label for="nodes">Number of nodes</label>
    <span class="help-icon" data-toggle="tooltip" data-placement="top" title="Number of nodes in SLURM reservation.">
      <span class="fa fa-question-circle"></span>
    </span>
    <input id="nodes" name="nodes" class="form-control" size="15" type="text" placeholder="e.g. 1"></input>
  </div>
  <div class="col-sm-6">
    <label for="gpus">Number of GPUs per node</label>
    <span class="help-icon" data-toggle="tooltip" data-placement="top" title="Number of GPUs per node in SLURM reservation. If number of nodes requested are more than 1, all GPUs on node will be reserved irrespective of requested number of GPUs per node.">
      <span class="fa fa-question-circle"></span>
    </span>
    <input id="gpus" name="gpus" class="form-control" size="15" type="text" placeholder="e.g. 1"></input>
  </div>
</div>
<div class="form-group row">
  <div class="col-sm-6">
    <label for="sbatch">Extra SBATCH directives (one per line)</label>
    <span class="help-icon" data-toggle="tooltip" data-placement="top" title="Any extra SLURM #SBATCH directives the user wishes to use.">
      <span class="fa fa-question-circle"></span>
    </span>
    <textarea id="sbatch" name="sbatch" class="form-control" placeholder="#SBATCH --exclusive"></textarea>
  </div>
  <div class="form-group row">
    <div class="col-sm-6">
      <label for="modules">List of modules (one per line)</label>
      <span class="help-icon" data-toggle="tooltip" data-placement="top" title="List of modules that will be loaded before launching jupyterlab server.">
        <span class="fa fa-question-circle"></span>
      </span>
      <textarea id="modules" name="modules" class="form-control" placeholder="python/3.7.6"></textarea>
    </div>
  </div>
</div>
<div class="form-group row">
  <div class="col-sm-6">
    <label for="env">Environment variables (one per line)</label>
    <span class="help-icon" data-toggle="tooltip" data-placement="top" title="Custom environment variables can be defined here. Shell parameter expansions and subshells are not supported.">
      <span class="fa fa-question-circle"></span>
    </span>
    <textarea id="env" name="env" class="form-control" placeholder="WHOAMI=JUPYTERHUB"></textarea>
  </div>
</div>
<script src="/hub/static/components/jquery-ui/jquery.min.js" type="text/javascript" charset="utf-8"></script>
<link rel="stylesheet" type="text/css" href="/hub/static/components/jquery-ui/jquery-ui.css" />
<script src="/hub/static/components/jquery-ui/jquery-ui.min.js" type="text/javascript" charset="utf-8"></script>
<script>
  $(function() {{
    var availableTags = {mod_files};
    var minWordLength = 2;
    function split(val) {{
      return val.split('\\n');
    }}
    function extractLast(term) {{
      return split(term).pop();
    }}
    $("#modules")
      .bind("keydown", function(event) {{
        if (event.keyCode === $.ui.keyCode.TAB && $(this).data("ui-autocomplete").menu.active) {{
          event.preventDefault();
        }}
      }}).autocomplete({{
        minLength: minWordLength,
        source: function(request, response) {{
          var term = extractLast(request.term);
          if (term.length >= minWordLength) {{
            response($.ui.autocomplete.filter(availableTags, term));
          }}
        }},
        focus: function() {{
          return false;
        }},
        select: function(event, ui) {{
          var terms = split(this.value);
          terms.pop();
          terms.push(ui.item.value);
          terms.push("");
          this.value = terms.join("\\n");
          return false;
        }}
      }});
  }});
</script>""".format(mod_files=mod_files)
            
    def check_formdata(self, formdata):
        """Do basic sanity checks on form data"""
        # List of valid walltime regex patterns
        walltime_rgx = r'(\d{1,2}:\d{1,2}:\d{1,2}$)|'  # hh:mm:ss
        walltime_rgx += r'(\d{1,2}:\d{1,2}$)|'  # mm:ss
        walltime_rgx += r'(\d{1,2}$)|'  # mm
        walltime_rgx += r'(\d{1,2}-\d{1,2}:\d{1,2}:\d{1,2}$)|'  # dd-hh:mm:ss
        walltime_rgx += r'(\d{1,2}-\d{1,2}:\d{1,2}$)|'  # dd-hh:mm
        walltime_rgx += r'(\d{1,2}-\d{1,2}$)'  # dd-hh
        
        # Check if walltime is valid
        walltime = formdata.get('walltime', [''])[0].strip()
        if walltime:
            if not re.match(walltime_rgx, walltime):
                err_msg = (f'Time {walltime} is not a valid format. '
                           f'Check SLURM documentation for list of allowed '
                           f'time formats')
                self.log.exception(err_msg)
                raise Exception(err_msg)
            
        # Check if number of nodes is int type
        for field in ['nodes', 'gpus']:
            value = formdata.get(field, [''])[0].strip()
            if value:
                try:
                    _ = int(value)
                except TypeError:
                    err_msg = f'Number of {field} must be an integer'
                    self.log.exception(err_msg)
                    raise Exception(err_msg)
    
        # Check SBATCH directives
        sb_drtvs = formdata.get('sbatch', [''])
        for line in sb_drtvs[0].splitlines():
            if line:
                if not re.match(r"^#SBATCH\s+", line):
                    err_msg = f'Formatting error in directive {line}'
                    self.log.exception(err_msg)
                    raise Exception(err_msg)
                invalid_patterns = ['-- ', ' =', '= ', ' = ', '|', '&', ';']
                for pattn in invalid_patterns:
                    if pattn in line:
                        err_msg = f'Formatting error in directive {line}'
                        self.log.exception(err_msg)
                        raise Exception(err_msg)

        # Check env variables
        # First check the env_input respect the regex patterns
        # These are effectively environment variables that should contain
        # certain set of characters. We check it with regex patterns to avoid
        # injections that may trigger arbitrary code execution on the server
        env_input = formdata.get('env', [''])
        for line in env_input[0].splitlines():
            if line:
                if not re.match(r"^([a-zA-Z0-9_-]*)=([a-zA-Z0-9:$()_/-]*)$", line):
                    err_msg = (f'Forbidden character found in environment '
                               f'variable {line}. Allowed characters '
                               f'are a-z, A-Z, 0-9, -, _, /, :, $, (, )')
                    self.log.exception(err_msg)
                    raise Exception(err_msg)
                
    def options_from_form(self, formdata):
        """Parse the form and add options to the SLURM job script"""
        
        self.log.debug('Making basic sanity checks on spawner form data')
        self.check_formdata(formdata)
        
        # self.log.debug('Saving spawning preferences')
        # self.save_spawning_preferences(formdata)
        
        self.log.info('Reading options for spawner form')
        options = {
            'profile': formdata.get('profile', [''])[0].strip(),
            'account': formdata.get('account', [''])[0].strip(),
            'sbatch': '',
        }

        # Get SBATCH directives
        walltime = formdata.get('walltime', [''])[0].strip()
        if walltime:
            options['sbatch'] += f'#SBATCH --time={walltime}\n'
        nodes = formdata.get('nodes', [''])[0].strip()
        if nodes:
            options['sbatch'] += f'#SBATCH --nodes={nodes}\n'
        gpus = formdata.get('gpus', [''])[0].strip()
        if gpus:
            options['sbatch'] += f'#SBATCH --gres=gpu:{gpus}\n'
        sbatch_directives = formdata.get('sbatch', [''])
        for line in sbatch_directives[0].splitlines():
            if line:
                options['sbatch'] += f'{line.strip()}\n'
                
        # Get environment variables
        options['env'] = env = {}
        env_input = formdata.get('env', [''])
        for line in env_input[0].splitlines():
            if line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip()
        
        # Get list of modules
        modules = []
        mod_input = formdata.get('modules', [''])
        for line in mod_input[0].splitlines():
            if line:
                modules.append(line.strip())
        options['modules'] = " ".join(modules)
        return options

    def get_args(self):
        """Return arguments to pass to the notebook server"""
        argv = super().get_args()
        if self.user_options.get('argv'):
            argv.extend(self.user_options['argv'])
        return argv

    def get_env(self):
        """Update the env variables"""
        env = super().get_env()
        if self.user_options.get('env'):
            env.update(self.user_options['env'])
        return env
    
    # We are overriding the original method to remove sudo prefix
    # for job quering
    # sudo is not needed, at least for SLURM, to check the job status
    # of jobs of different users
    async def query_job_status(self):
        """Check job status, return JobStatus object."""
        if self.job_id is None or len(self.job_id) == 0:
            self.job_status = ""
            return JobStatus.NOTFOUND
        subvars = self.get_req_subvars()
        subvars["job_id"] = self.job_id
        cmd = " ".join(
            (
                format_template(self.batch_query_cmd, **subvars),
            )
        )
        self.log.debug("Spawner querying job: " + cmd)
        try:
            self.job_status = await self.run_command(cmd)
        except RuntimeError as e:
            # e.args[0] is stderr from the process
            self.job_status = e.args[0]
        except Exception as e:
            self.log.error("Error querying job " + self.job_id)
            self.job_status = ""

        if self.state_isrunning():
            return JobStatus.RUNNING
        elif self.state_ispending():
            return JobStatus.PENDING
        elif self.state_isunknown():
            return JobStatus.UNKNOWN
        else:
            return JobStatus.NOTFOUND

    async def move_certs(self, paths):
        """This method takes cert paths, moves to a path where user
        can read them and sets ownership for them. Typically this can
        be HOME of the user. However, we cannot access HOME directory
        of the user from the host where JupyterHub is running.

        So we "mock" this method as if we moved the certificates but
        in reality we only set paths where certificates can be found
        in the user HOME directory. We then read the certificates and
        save them into env variables. We export these env variables to
        user environment. When we spawn the SLURM job, we
        create the certificates within the SLURM job at the same path
        we return with this method using the env variables that we set
        here.
        Arguments:
            paths (dict): a list of paths for key, cert, and CA
        Returns:
            dict: a list (potentially altered) of paths for key, cert,
            and CA
        """

        local_key = paths['keyfile']
        local_cert = paths['certfile']
        local_ca = paths['cafile']

        user = self.user.name
        server_name = self.name
        if not server_name:
            server_name = 'default'

        # Create dir for user's certs wherever we're starting
        home = pwd.getpwnam(self.user.name).pw_dir
        hub_dir = f"{home}/.jupyterhub"
        out_dir = f"{hub_dir}/jupyterhub-certs/{server_name}"

        self.log.info("Internal SSL certs for user %s will be moved to %s",
                      user, out_dir)

        remote_key = os.path.join(out_dir, os.path.basename(local_key))
        remote_cert = os.path.join(out_dir, os.path.basename(local_cert))
        remote_ca = os.path.join(out_dir, os.path.basename(local_ca))
        
        # Create env variables that store cert, key and ca information
        # We also need the name of the files so we create another
        # env variable for each component to save basename of path
        with open(local_key, 'r') as f:
            self.user_options['env']['JUPYTERHUB_SSL_KEYFILE_CERT'] = f.read()
        with open(local_cert, 'r') as f:
            self.user_options['env']['JUPYTERHUB_SSL_CERTFILE_CERT'] = f.read()
        with open(local_ca, 'r') as f:
            self.user_options['env']['JUPYTERHUB_SSL_CLIENT_CA_CERT'] = f.read()

        return {
            "keyfile": remote_key,
            "certfile": remote_cert,
            "cafile": remote_ca
        }
