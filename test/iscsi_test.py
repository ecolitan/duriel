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

import os
import unittest
from duriel.iscsi import Iscsi, IscsiError

test_data_path = '{0}/test/test_data'.format(os.getcwd())

class TestIscsi(unittest.TestCase):
  
    def setUp(self):
        self.ietd_version = '1.4.20.3'
        self.ietadm_version = '1.4.20.3'
        self.ietd_bin_path = '/usr/sbin/ietd'
        self.ietadm_bin_path = '/usr/sbin/ietadm'
        self.false_path = '/This/Is/A/False/Path'
        self.etc_default_iscsitarget_path = '/etc/default/iscsitarget'
        self.ietd_config_path = '/etc/iet/ietd.conf'
        
    def test_get_ietd_version(self):
        # get_ietd_version()
        self.assertEqual(self.ietd_version, Iscsi().get_ietd_version(self.ietd_bin_path))
        
        # Should raise OSError "no such file" if path incorrect
        self.assertRaises(OSError, Iscsi().get_ietd_version, self.false_path)
        # raise OSError no such file if path incorrect
        self.assertRaises(OSError, Iscsi().get_ietd_version, self.false_path)
        
    def test_get_ietadm_version(self):
        # get_ietadm_version()
        self.assertEqual(self.ietadm_version, Iscsi().get_ietadm_version(self.ietadm_bin_path))
        
        # raise OSError no such file if path incorrect
        self.assertRaises(OSError, Iscsi().get_ietadm_version, self.false_path)
        
    def test_parse_sys_iscsi_config(self):
        # parse_sys_iscsi_config()
        
        # Should raise IOError no such file if path incorrect
        self.assertRaises(IOError, Iscsi().parse_sys_iscsi_config, self.false_path)
        
        valid1 = {
            'ISCSITARGET_ENABLE': 'false',
            'ISCSITARGET_OPTIONS': '""'
        }
        
        valid1_file = '{0}/default.iscsitarget.valid1'.format(test_data_path)
        
        self.assertEqual(valid1, Iscsi().parse_sys_iscsi_config(valid1_file))
        
    def test_test_valid_iqn(self):
        # parse_ietd_config.test_valid_iqn()
        # target keys must be checked to be an "iSCSI Qualified Name"
        
        fake_name = 'iqn.com.example:storage.disk2.sys1.xyz'
        good_name1 = 'iqn.2001-04.com.example:storage.disk2.sys1.xyz'
        good_name2 = 'iqn.2001-04.com.example'
        good_name3 = 'iqn.9846-34.com.example.test.sertver5'
        
        self.assertTrue(not Iscsi().test_valid_iqn(fake_name))
        self.assertTrue(Iscsi().test_valid_iqn(good_name1))
        self.assertTrue(Iscsi().test_valid_iqn(good_name2))
        self.assertTrue(Iscsi().test_valid_iqn(good_name3))
                
    def test_parse_ietd_config(self):
        # parse_ietd_config()
        #self.maxDiff = None
        
        # Should raise IOError no such file if path incorrect
        self.assertRaises(IOError, Iscsi().parse_ietd_config, self.false_path)
        
        # parse test_data/ietd.conf.validx files correctly
        valid1 = {
            'global': {
                'IncomingUser': ['joe', 'secret']
            },
            'target': {
                'iqn.2001-04.com.example': {},
                'iqn.2001-04.com.example:storage.disk2.sys1.xyz': {
                    'IncomingUser': ['joe', 'secret'],
                    'OutgoingUser': ['jim', '12charpasswd']
                }
            }
        }
            
        valid2 = {
            'global':{
                'iSNSServer': ['192.168.1.16'],
                'iSNSAccessControl': ['No'],
                'IncomingUser': ['joe', 'secret'],
                'OutgoingUser': ['jack', '12charsecret']
            },
            'target':{
                'iqn.2001-04.com.example:storage.disk2.sys1.xyz': {
                    'Lun': ['0', 'Path=/dev/sdc,Type=fileio,ScsiId=xyz,ScsiSN=xyz'],
                    'MaxConnections': ['1'],
                    'MaxSessions': ['0']
                    }
            }
        }
            
        valid1_file = '{0}/ietd.conf.valid1'.format(test_data_path)
        valid2_file = '{0}/ietd.conf.valid2'.format(test_data_path)
        invalid1_file = '{0}/ietd.conf.invalid1'.format(test_data_path)
        invalid2_file = '{0}/ietd.conf.invalid2'.format(test_data_path)
                                                
        self.assertEqual(valid1, Iscsi().parse_ietd_config(valid1_file))
        self.assertEqual(valid2, Iscsi().parse_ietd_config(valid2_file))
        
        # raise IscsiError for invalid config file syntax
        self.assertRaises(IscsiError, Iscsi().parse_ietd_config, invalid1_file)
        self.assertRaises(IscsiError, Iscsi().parse_ietd_config, invalid2_file)
        
    def test_parse_target_allow(self):
        #parse_target_allow()
        
        # Should raise IOError no such file if path incorrect
        self.assertRaises(IOError, Iscsi().parse_target_allow, self.false_path)
        
        valid1_file = '{0}/targets.allow.valid1'.format(test_data_path)
        
        valid1 = {
            'iqn.2001-04.com.example:storage.disk1.sys1.xyz': ['192.168.0.0/16'],
            'iqn.2001-04.com.example:storage.disk1.sys2.xyz': ['[3ffe:302:11:1:211:43ff:fe31:5ae2]', '192.168.22.24'],
            'iqn.2001-04.com.example:storage.disk1.sys3.xyz': ['ALL'],
            'iqn.2001-04.com.example:storage.disk1.sys4.xyz': ['192.168.22.3'],
            'ALL': ['192.168.0.0/16']
        }
        
        self.assertEqual(valid1, Iscsi().parse_target_allow(valid1_file))
    
suite = unittest.TestLoader().loadTestsFromTestCase(TestIscsi)
unittest.TextTestRunner(verbosity=2).run(suite)
