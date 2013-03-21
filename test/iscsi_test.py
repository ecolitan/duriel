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

import unittest
from duriel.iscsi import Iscsi

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
        
        #return a dict
        self.assertEqual(dict, type(Iscsi().parse_sys_iscsi_config(self.etc_default_iscsitarget_path)))
        
        # Should raise IOError no such file if path incorrect
        self.assertRaises(IOError, Iscsi().parse_sys_iscsi_config, self.false_path)
        
        #dict must contain keys ISCSITARGET_ENABLE
        self.assertTrue('ISCSITARGET_ENABLE' in Iscsi().parse_sys_iscsi_config(self.etc_default_iscsitarget_path))
        
    def test_parse_ietd_config(self):
        # parse_ietd_config()
        
        returned_obj = Iscsi().parse_ietd_config(self.ietd_config_path)
        # return a dict 
        self.assertEqual(dict, type(returned_obj))
        
        # Should raise IOError no such file if path incorrect
        self.assertRaises(IOError, Iscsi().parse_ietd_config, self.false_path)
        
        # global and target keys must be type dict
        self.assertEqual(dict, type(returned_obj['global']))
        self.assertEqual(dict, type(returned_obj['target']))
        
    def test_test_iqn(self):
        # parse_ietd_config.test_iqn()
        # target keys must be checked to be an "iSCSI Qualified Name"
        
        fake_name = 'iqn.com.example:storage.disk2.sys1.xyz'
        good_name1 = 'iqn.2001-04.com.example:storage.disk2.sys1.xyz'
        good_name2 = 'iqn.2001-04.com.example'
        good_name3 = 'iqn.9846-34.com.example.test.sertver5'
        
        self.assertTrue(not Iscsi().test_iqn(fake_name))
        self.assertTrue(Iscsi().test_iqn(good_name1))
        self.assertTrue(Iscsi().test_iqn(good_name2))
        self.assertTrue(Iscsi().test_iqn(good_name3))
        
    
suite = unittest.TestLoader().loadTestsFromTestCase(TestIscsi)
unittest.TextTestRunner(verbosity=2).run(suite)