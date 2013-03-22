'''
    duriel: Backup Xen Guest LVM Images.
    Copyright (C) <2012-2013>  <Aaron Cossey (aaron dot cossey at gmail dot com)>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import subprocess
from subprocess import Popen
import os

class RemoteExec():
    def __init__(self, connect_info):
        """
        Instanciate RemoteExec with connection information.
        
        'connect_info' = {
            'hostname'      : '',
            'hostip'        : '',
            'username'      : '',
            'private_key'   : '',
            'password'      : '',
            'port'          : Int,
        }
        """
        self.ssh_bin = '/usr/bin/ssh'
        self.connect_info = connect_info

    def __unicode__(self):
        return self.connect_info.hostname
            
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        return self

    def exec_remote_command(self, _command):
        """Calls ssh to execute a remote command.
        Returns: host_info - stdout output from command
        """
        command_string = [self.ssh_bin,
                          '-i', self.connect_info['private_key'],
                          '-p', str(self.connect_info['port']),
                          '-l', self.connect_info['username'],
                          self.connect_info['hostip'],
                          _command]
        
        proc = Popen(command_string,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=False)
        returned_string, error = proc.communicate()
        
        return (returned_string, error)
