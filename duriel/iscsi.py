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

import sys
import subprocess
import re

class Iscsi():
    def __init__(self):
        pass
        
    def get_ietd_version(self, ietd_bin_path='/usr/sbin/ietd'):
        '''
        Return ietd version number.
        '''
        #TODO ietd_bin_path should be in config as a variable
        return subprocess.check_output([ietd_bin_path, "--version"]).split(' ')[-1].rstrip()
        
    def get_ietadm_version(self, ietadm_bin_path='/usr/sbin/ietadm'):
        '''
        Return ietadm version number.
        '''
        #TODO ietd_bin_path should be in config as a variable
        return subprocess.check_output([ietadm_bin_path, "--version"]).split(' ')[-1].rstrip()
        
    def parse_sys_iscsi_config(self, etc_default_iscsitarget='/etc/default/iscsitarget'):
        '''
        Return dictionary with /etc/default/iscsitarget keys
        '''
        #TODO etc_default_iscsitarget should be in config as a variable
        
        sys_iscsi_config = {}
        with open(etc_default_iscsitarget) as f:
            for line in f:
                li = line.strip()
                if (not li.startswith('#') and li):
                    sys_iscsi_config[li.split('=')[0]] = li.split('=')[-1]
            
        return sys_iscsi_config
        
    def parse_ietd_config(self, ietd_config_path='/etc/iet/ietd.conf'):
        '''
        Return dict with ietd.conf info
        '''
        #TODO ietd_config_path should be in config as a variable
        
        
        ietd_conf = {}
        ietd_conf['global'] = {}
        ietd_conf['target'] = {}
        with open(ietd_config_path) as f:
            pass
            
            
        return ietd_conf
        
    def test_iqn(self, iqn):
        valid_iqn = re.compile('''iqn\.\d{4}-\d{2}(\.\w{1,64}){1,16}(:(\.?\w{1,64}){1,16})?''')
        if re.match(valid_iqn, iqn):
            return True
        else:
            return False
        
    
#~ a=Iscsi()
#~ print a.test_iqn('iqn.2001-04.com.example:storage.disk2.sys1.xyz')
