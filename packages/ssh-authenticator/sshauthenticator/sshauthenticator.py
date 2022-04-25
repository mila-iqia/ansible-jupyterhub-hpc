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

"""Main module"""

import re

from jupyterhub.auth import Authenticator

from tornado import gen

from paramiko import SSHClient
from paramiko import SSHException
from paramiko import AuthenticationException
from paramiko import AutoAddPolicy

from traitlets import Unicode
from traitlets import Int


class SSHAuthenticator(Authenticator):
    """This SSH authenticator is the extension of original work developed
    at https://github.com/andreas-h/sshauthenticator. Here we add logging
    to log users that are trying to connect to Hub proxy.

    The idea of this authenticator is we can use login nodes of HPC platforms
    as host machine to connect.
    """

    server_address = Unicode(
        "",
        help="""
        Address of host machine to connect. This machine must have
        local accounts of the users.
        """,
    ).tag(config=True)

    server_port = Int(
        "",
        help="""
        Port on which to contact host machine.
        """,
    ).tag(config=True)

    valid_username_regex = Unicode(
        "",
        help="""
        Regex for validating usernames - those that do not match this regex will be rejected.
        This is checked before authenticating and usernames that do not match the pattern
        will not be authenticated.
        """,
    ).tag(config=True)
    
    default_group_name = Unicode(
        "",
        help="""
        If the Authenticator.manage_groups is enabled, we can add the users to a default group.
        This variable defines the name of such a default group.
        """,
    ).tag(config=True)

    @gen.coroutine
    def authenticate(self, handler, data):
        """Main method to authenticate"""

        username = data['username']
        password = data['password']

        self.log.info("User %s is attempting to authenticate", username)

        # Sanity checks
        if not self.server_address:
            self.log.warning(
                "No server address configured to attempt SSH connection"
            )
            return None

        if not self.server_port:
            self.server_port = 22
            self.log.warning(
                "No server port configured. Using default value of 22"
            )

        # Protect against invalid usernames
        if self.valid_username_regex:
            if not re.match(self.valid_username_regex, username):
                self.log.warning(
                    "username:%s Illegal characters in username, must match regex %s", username,
                    self.valid_username_regex,
                )
                return None

        # No empty passwords!
        if password is None or password.strip() == "":
            self.log.warning("username:%s Login denied for blank password", username)
            return None
        
        # Check default group name provided is manage_groups is enabled
        if self.manage_groups and self.default_group_name == "":
            self.log.warning(
                "Manage groups is enabled without giving a default group name. "
                "Using default as group name"
            )
            self.default_group_name = "default"

        with SSHClient() as ssh:
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            try:
                ssh.connect(self.server_address, port=self.server_port,
                            username=username,
                            password=password)
            except (SSHException, AuthenticationException):
                self.log.warning("User %s authentication failed", username)
                return None
            self.log.info("User %s succesfully authenticated", username)
            if self.manage_groups:
                self.log.info("Adding User %s to group %s", username, self.default_group_name)
                return {"name": username, "groups": [self.default_group_name]}
            return username
