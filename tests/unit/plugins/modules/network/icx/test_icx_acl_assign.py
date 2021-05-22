# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules.network.icx import icx_acl_assign
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAclAssignModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_acl_assign module '''
    module = icx_acl_assign

    def setUp(self):
        super(TestICXAclAssignModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.network.icx.icx_acl_assign.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.network.icx.icx_acl_assign.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAclAssignModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None

    def test_icx_acl_assign_all_options(self):
        ''' Test for successful acl assign with all options'''
        set_module_args(dict(ip_access_group=dict(acl_name='scale12', in_out='in', ethernet='1/1/3', mirror_port=dict(ethernet='3/1/10'), logging='enable'),
                             ipv6_access_group=dict(acl_name='scale12', in_out='in', lag='7'),
                             mac_access_group=dict(mac_acl_name='mac_acl1', vlan=dict(vlan_num='10', interfaces=['ethernet 1/1/3']), logging='enable'),
                             default_acl=dict(ip_type='ipv4', acl_name='guest', in_out='in')))
        expected_commands = [
            'interface ethernet 1/1/3',
            'acl-mirror-port ethernet 3/1/10',
            'ip access-group scale12 in logging enable',
            'exit',
            'interface lag 7',
            'ipv6 access-group scale12 in',
            'exit',
            'vlan 10',
            'mac access-group mac_acl1 in ethernet 1/1/3 logging enable',
            'exit',
            'authentication',
            'default-acl ipv4 guest in',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_assign_all_options_remove(self):
        ''' Test for removing acl assign with all options'''
        set_module_args(dict(ip_access_group=dict(acl_name='scale12', in_out='in', ethernet='1/1/3',
                                                  mirror_port=dict(ethernet='3/1/10', state='absent'),
                                                  logging='enable', state='absent'),
                             ipv6_access_group=dict(acl_name='scale12', in_out='in', lag='7', state='absent'),
                             mac_access_group=dict(mac_acl_name='mac_acl1', vlan=dict(vlan_num='10',
                                                   interfaces=['ethernet 1/1/3']), logging='enable', state='absent'),
                             default_acl=dict(ip_type='ipv4', acl_name='guest', in_out='in', state='absent')))
        expected_commands = [
            'interface ethernet 1/1/3',
            'no acl-mirror-port ethernet 3/1/10',
            'no ip access-group scale12 in logging enable',
            'exit',
            'interface lag 7',
            'no ipv6 access-group scale12 in',
            'exit',
            'vlan 10',
            'no mac access-group mac_acl1 in ethernet 1/1/3 logging enable',
            'exit',
            'authentication',
            'no default-acl ipv4 guest in',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_assign_ip_access_group(self):
        ''' Test for successful ip_access_group'''
        set_module_args(dict(ip_access_group=dict(in_out='in', ethernet='1/1/2', frag_deny='yes')))
        expected_commands = ['interface ethernet 1/1/2', 'ip access-group frag deny', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_assign_ipv6_access_group(self):
        ''' Test for successful ipv6_access_group'''
        set_module_args(dict(ipv6_access_group=dict(acl_name='scale123', in_out='in', vlan=dict(vlan_num='555',
                                                    interfaces=['ethernet 1/1/2']), logging='enable')))
        expected_commands = ['vlan 555', 'ipv6 access-group scale123 in ethernet 1/1/2 logging enable', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_assign_mac_access_group(self):
        ''' Test for successful mac_access_group'''
        set_module_args(dict(mac_access_group=dict(mac_acl_name='mac_acl1', lag='25')))
        expected_commands = ['interface lag 25', 'mac access-group mac_acl1 in', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_default_acl(self):
        ''' Test for successful default acl'''
        set_module_args(dict(default_acl=dict(ip_type='ipv4', acl_name='guest', in_out='out', state='present')))
        expected_commands = ['authentication', 'default-acl ipv4 guest out', 'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_assign_invalid_arg_ip_access_group(self):
        ''' Test for invalid in_out'''
        set_module_args(dict(ip_access_group=dict(acl_name='scale12', acl_num='123', in_out='aa', ethernet='1/1/2', lag='25',
                                                  vlan=dict(vlan_num='555', interfaces=['ethernet 1/1/2']), logging='enable', frag_deny='yes')))
        result = self.execute_module(failed=True)

    def test_icx_acl_assign_invalid_arg_ipv6_access_group(self):
        ''' Test for invalid lag'''
        set_module_args(dict(ipv6_access_group=dict(acl_name='scale12', in_out='in', ethernet='1/1/2', lag='aa', vlan=dict(vlan_num='555',
                             interfaces=['ethernet 1/1/2']), logging='enable')))
        result = self.execute_module(failed=True)

    def test_icx_acl_assign_invalid_arg_mac_access_group(self):
        ''' Test for invalid ethernet'''
        set_module_args(dict(ip_access_group=dict(mac_acl_name='mac_acl', ethernet='111', lag='25',
                             vlan=dict(vlan_num='555', interfaces=['ethernet 1/1/2']), logging='aaa')))
        result = self.execute_module(failed=True)

    def test_icx_invalid_args_default_acl(self):
        ''' Test for invalid in_out '''
        set_module_args(dict(default_acl=dict(ip_type='ipv4', acl_name='guest', in_out='aa', state='present')))
        result = self.execute_module(failed=True)
