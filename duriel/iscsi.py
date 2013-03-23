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
        
    def test_valid_iqn(self, iqn):
        valid_iqn = re.compile('''iqn\.\d{4}-\d{2}(\.\w{1,64}){1,16}(:(\.?\w{1,64}){1,16})?''')
        if re.match(valid_iqn, iqn):
            return True
        else:
            return False        
            
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
        
        testlist=[]
        ietd_conf = {}
        ietd_conf['global'] = {}
        ietd_conf['target'] = {}
        inTarget = False
        
        with open(ietd_config_path) as f:
            for line in f:
                li = line.strip()
                if (li.lstrip().startswith('#') or not li):
                    continue
                
                if li.split(' ')[0] == 'Target':
                    if not self.test_valid_iqn(li.split()[1]):
                        raise IscsiError('Syntax Error in Config. Invalid Target iqn.')
                    #test that iqn doesnt already exist as a key
                    if li.split()[1] in ietd_conf['target']:
                        raise IscsiError('Syntax Error in Config. Iqn must be unique')
                        
                    #create target
                    ietd_conf['target'][li.split()[1]] = {}
                    
                    #Set inTarget to the iqn
                    inTarget = li.split()[1]
                    continue
                    
                if not inTarget:
                    # Must be a line in 'global config'
                    
                    #test that directive doesn't already exists as key in global config'
                    if li.split()[0] in ietd_conf['global']:
                        raise IscsiError('Syntax Error in Config. global directives must be unique.')
                        
                    #decide which parts of multi-arg assignment are valid and which are in-line comments
                    directive = li.split()[0]
                    assignment = li.split()[1:]
                    
                    for position, word in enumerate(assignment):
                        if word[0] == '#':
                            assignment = assignment[0:position]
                        
                    #add directive and values to global 
                    ietd_conf['global'][directive] = assignment
                    continue
                    
                else:
                    #Must be inside a target block
                    
                    #test directive not already key in target
                    if li.split()[0] in ietd_conf['target'][inTarget]:
                        raise IscsiError('Syntax Error in Config. target directives must be unique.')
                        
                    #decide which parts of multi-arg assignment are valid and which are in-line comments
                    directive = li.split()[0]
                    assignment = li.split()[1:]
                    
                    for position, word in enumerate(assignment):
                        if word[0] == '#':
                            assignment = assignment[0:position]
                        
                    #add directive and value to target
                    ietd_conf['target'][inTarget][directive] = assignment
                    continue
        
        return ietd_conf
        
    def parse_target_allow(self, target_config_path='/etc/iet/targets.allow'):
        #TODO target_config_path should be in config
        
        allowed_targets = {}
        
        with open(target_config_path) as f:
            for line in f:
                li = line.strip()
                if (li.lstrip().startswith('#') or not li):
                    continue
                    
                directive = li.split()[0]
                assignment = li.split()[1:]
                
                #remove commas from assignment words
                for position, word in enumerate(assignment):
                    if word[-1] == ',':
                        assignment[position] = word[0:-1]
                    
                #save directive and assignment to allowed_targets
                allowed_targets[directive] = assignment
                
                #Stop parsing file if target "ALL" encountered
                if directive == 'ALL':
                    break
                    
        return allowed_targets
        
    def parse_initiator_allow(self, initiator_config_path='/etc/iet/initiators.allow'):
        #TODO initiator_config_path should be in config
        
        allowed_initiators = {}
        
        with open(initiator_config_path) as f:
            for line in f:
                li = line.strip()
                if (li.lstrip().startswith('#') or not li):
                    continue
                    
                directive = li.split()[0]
                assignment = li.split()[1:]
                
                #remove commas from assignment words
                for position, word in enumerate(assignment):
                    if word[-1] == ',':
                        assignment[position] = word[0:-1]
                    
                #save directive and assignment to allowed_initiators
                allowed_initiators[directive] = assignment
                
                #Stop parsing file if initiator "ALL" encountered
                if directive == 'ALL':
                    break
                    
        return allowed_initiators
        
class IscsiError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        print self.msg
    
    
#~ a=Iscsi()
#~ print a.test_valid_iqn('iqn.2001-04.com.example:storage.disk2.sys1.xyz')
