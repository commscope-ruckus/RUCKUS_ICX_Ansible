# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_flex_common
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAclAssignModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_flex_common module '''
    module = icx_flex_common

    def setUp(self):
        super(TestICXAclAssignModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_flex_common.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.icx_flex_common.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAclAssignModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None

    def test_icx_flex_auth_all_options(self):
        ''' Test for successful flex auth with all options'''
        set_module_args(dict(global_auth=dict(auth_default_vlan=dict(vlan_id=12), re_authentication='present', restricted_vlan=dict(vlan_id=20),
                             voice_vlan=dict(vlan_id=32), critical_vlan=dict(vlan_id=30), auth_fail_action=dict(restricted_vlan=True, voice_vlan=True),
                             auth_timeout_action=dict(critical_vlan=True, voice_vlan=True)), interface_auth=dict(interface='1/1/3',
                             auth_default_vlan=dict(vlan_id=10), voice_vlan=dict(vlan_id=100), auth_fail_action=dict(restricted_vlan=True, vlan_id=55),
                             auth_timeout_action=dict(critical_vlan=True, vlan_id=40), use_radius_server=dict(ip_address='10.10.10.1'))))
        expected_commands = [
            'authentication',
            'auth-default-vlan 12',
            're-authentication',
            'restricted-vlan 20',
            'voice-vlan 32',
            'critical-vlan 30',
            'auth-fail-action restricted-vlan voice voice-vlan',
            'auth-timeout-action critical-vlan voice voice-vlan',
            'exit',
            'interface ethernet 1/1/3',
            'authentication auth-default-vlan 10',
            'authentication voice-vlan 100',
            'authentication fail-action restricted-vlan 55',
            'authentication timeout-action critical-vlan 40',
            'use-radius-server 10.10.10.1',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_flex_auth_all_options_remove(self):
        ''' Test for removing flex auth with all options'''
        set_module_args(dict(global_auth=dict(auth_default_vlan=dict(vlan_id=12, state='absent'), re_authentication='absent',
                             restricted_vlan=dict(vlan_id=20, state='absent'), voice_vlan=dict(vlan_id=32, state='absent'),
                             critical_vlan=dict(vlan_id=30, state='absent'), auth_fail_action=dict(restricted_vlan=True, voice_vlan=True,
                             state='absent'), auth_timeout_action=dict(critical_vlan=True, voice_vlan=True, state='absent')),
                             interface_auth=dict(interface='1/1/3', auth_default_vlan=dict(vlan_id=10, state='absent'),
                             voice_vlan=dict(vlan_id=100, state='absent'), auth_fail_action=dict(restricted_vlan=True, vlan_id=55, state='absent'),
                             auth_timeout_action=dict(critical_vlan=True, vlan_id=40, state='absent'),
                             use_radius_server=dict(ip_address='10.10.10.1', state='absent'))))
        expected_commands = [
            'authentication',
            'no auth-default-vlan 12',
            'no re-authentication',
            'no restricted-vlan 20',
            'no voice-vlan 32',
            'no critical-vlan 30',
            'no auth-fail-action restricted-vlan voice voice-vlan',
            'no auth-timeout-action critical-vlan voice voice-vlan',
            'exit',
            'interface ethernet 1/1/3',
            'no authentication auth-default-vlan 10',
            'no authentication voice-vlan 100',
            'no authentication fail-action restricted-vlan 55',
            'no authentication timeout-action critical-vlan 40',
            'no use-radius-server 10.10.10.1',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_flex_auth_fail_timeout_action(self):
        ''' Test for successful flex auth with fail and timeout action options'''
        set_module_args(dict(global_auth=dict(auth_fail_action=dict(restricted_vlan=True), auth_timeout_action=dict(success=True)),
                             interface_auth=dict(interface='1/1/5', auth_fail_action=dict(restricted_vlan=True), auth_timeout_action=dict(failure=True))))
        expected_commands = [
            'authentication',
            'auth-fail-action restricted-vlan',
            'auth-timeout-action success',
            'exit',
            'interface ethernet 1/1/5',
            'authentication fail-action restricted-vlan',
            'authentication timeout-action failure',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_flex_auth_fail_timeout_action_remove(self):
        ''' Test for removing flex auth fail and timeout action options'''
        set_module_args(dict(global_auth=dict(auth_fail_action=dict(restricted_vlan=True, state='absent'), auth_timeout_action=dict(success=True,
                             state='absent')), interface_auth=dict(interface='1/1/5', auth_fail_action=dict(restricted_vlan=True, state='absent'),
                             auth_timeout_action=dict(failure=True, state='absent'))))
        expected_commands = [
            'authentication',
            'no auth-fail-action restricted-vlan',
            'no auth-timeout-action success',
            'exit',
            'interface ethernet 1/1/5',
            'no authentication fail-action restricted-vlan',
            'no authentication timeout-action failure',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_flex_auth_no_arg_auth_default_vlan_id(self):
        ''' Test for removing flex auth with all options'''
        set_module_args(dict(global_auth=dict(auth_default_vlan=dict(state='present'))))
        result = self.execute_module(failed=True)
