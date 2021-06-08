# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_acl_mac
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAclMacModule(TestICXModule):
    """ Class used for Unit tests agains icx_acl_mac module"""

    module = icx_acl_mac

    def setUp(self):
        super(TestICXAclMacModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_acl_mac.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.icx_acl_mac.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAclMacModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None

    def test_icx_acl_mac_all_options(self):
        ''' Test for successful acl  with all options'''
        set_module_args(dict(acl_name='mac123', accounting='enable',
                             rule=[(dict(rule_type='permit', source=dict(any='yes'), destination=dict(any='yes'), ether_type='0800',
                                         log='yes', mirror='yes')),
                                   (dict(rule_type='permit', source=dict(source_mac_address='1111.2222.3333', source_mask='ffff.ffff.ffff'),
                                         destination=dict(destination_mac_address='4444.5555.6666', destination_mask='ffff.ffff.ffff'),
                                         ether_type='0800', log='yes', mirror='yes')),
                                   (dict(rule_type='permit', source=dict(source_mac_address='1111.2222.3333', source_mask='ffff.ffff.ffff'),
                                         destination=dict(any='yes'), ether_type='0800', log='yes', mirror='yes'))]))
        expected_commands = ['mac access-list mac123',
                             'enable accounting',
                             'permit any any ether-type 0800 log mirror',
                             'permit 1111.2222.3333 ffff.ffff.ffff 4444.5555.6666 ffff.ffff.ffff ether-type 0800 log mirror',
                             'permit 1111.2222.3333 ffff.ffff.ffff any ether-type 0800 log mirror'
                             ]
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_mac_all_options_remove(self):
        ''' Test for removing acl mac with all options'''
        set_module_args(dict(acl_name='mac123', state='absent', accounting='disable',
                             rule=[(dict(rule_type='permit', source=dict(any='yes'), destination=dict(any='yes'),
                                         ether_type='0800', log='yes', mirror='yes', state='absent')),
                                   (dict(rule_type='permit', source=dict(source_mac_address='1111.2222.3333', source_mask='ffff.ffff.ffff'),
                                         destination=dict(destination_mac_address='4444.5555.6666', destination_mask='ffff.ffff.ffff'),
                                         ether_type='0800', log='yes', mirror='yes', state='absent')),
                                   (dict(rule_type='permit', source=dict(source_mac_address='1111.2222.3333', source_mask='ffff.ffff.ffff'),
                                         destination=dict(any='yes'), ether_type='0800', log='yes', mirror='yes', state='absent'))]))
        expected_commands = ['no mac access-list mac123',
                             'no enable accounting',
                             'no permit any any ether-type 0800 log mirror',
                             'no permit 1111.2222.3333 ffff.ffff.ffff 4444.5555.6666 ffff.ffff.ffff ether-type 0800 log mirror',
                             'no permit 1111.2222.3333 ffff.ffff.ffff any ether-type 0800 log mirror']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_mac_permit_acl(self):
        ''' Test for successful mac rule permit acl'''
        set_module_args(dict(acl_name='mac123',
                             rule=[(dict(rule_type='permit', source=dict(source_mac_address='1111.2222.3333'),
                                         destination=dict(destination_mac_address='4444.5555.6666'), ether_type='0800'))]))

        expected_commands = ['mac access-list mac123', 'permit 1111.2222.3333 4444.5555.6666 ether-type 0800']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_mac_deny_acl(self):
        ''' Test for successful mac rule deny acl'''
        set_module_args(dict(acl_name='mac123',
                             rule=[(dict(rule_type='deny', source=dict(source_mac_address='1111.2222.3333'),
                                         destination=dict(destination_mac_address='4444.5555.6666'), ether_type='0800', mirror='yes'))]))

        expected_commands = ['mac access-list mac123', 'deny 1111.2222.3333 4444.5555.6666 ether-type 0800 mirror']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_invalid_mac_acl_deny(self):
        ''' Test for invalid mac_rule_type'''
        set_module_args(dict(acl_name='mac123',
                             rule=[(dict(rule_type='aa', source=dict(source_mac_address='1111.2222.3333'), destination=dict(any='yes'), log='yes'))]))
        result = self.execute_module(failed=True)
