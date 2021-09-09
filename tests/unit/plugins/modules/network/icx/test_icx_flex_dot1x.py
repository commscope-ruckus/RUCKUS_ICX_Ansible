# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_flex_dot1x
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAclAssignModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_flex_dot1x module '''
    module = icx_flex_dot1x

    def setUp(self):
        super(TestICXAclAssignModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_flex_dot1x.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.icx_flex_dot1x.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAclAssignModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None

    def test_icx_dot1x_all_options(self):
        ''' Test for successful dot1x with all options'''
        set_module_args(dict(enable=dict(all=True), guest_vlan=dict(vlan_id=12), max_reauth_req=dict(count=4),
                             max_req=dict(count=3), port_control=dict(auto='yes', all=True), timeout=dict(supplicant=32)))
        expected_commands = [
            'authentication',
            'dot1x enable',
            'dot1x enable all',
            'dot1x port-control auto all',
            'dot1x guest-vlan 12',
            'dot1x max-reauth-req 4',
            'dot1x max-req 3',
            'dot1x timeout supplicant 32',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_all_options_remove(self):
        ''' Test for removing dot1x with all options'''
        set_module_args(dict(enable=dict(all=True, state='absent'), guest_vlan=dict(vlan_id=12, state='absent'),
                             max_reauth_req=dict(count=4, state='absent'), max_req=dict(count=3, state='absent'),
                             port_control=dict(auto='yes', all=True, state='absent'), timeout=dict(supplicant=32, state='absent')))
        expected_commands = [
            'authentication',
            'no dot1x port-control auto all',
            'no dot1x enable all',
            'no dot1x guest-vlan 12',
            'no dot1x max-reauth-req 4',
            'no dot1x max-req 3',
            'no dot1x timeout supplicant 32',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_enable_ethernet(self):
        ''' Test for enabling dot1x on the specified interface '''
        set_module_args(dict(enable=dict(ethernet='1/1/9')))
        expected_commands = [
            'authentication',
            'dot1x enable',
            'dot1x enable ethernet 1/1/9',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_port_control_ethernet(self):
        ''' Test for enabling port control dot1x on the specified interface '''
        set_module_args(dict(enable=dict(all=True), port_control=dict(force_unauthorized=True, ethernet='1/1/15')))
        expected_commands = [
            'authentication',
            'dot1x enable',
            'dot1x enable all',
            'dot1x port-control force-unauthorized ethernet 1/1/15',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_timeout(self):
        ''' Test for enabling dot1x timout '''
        set_module_args(dict(timeout=dict(quiet_period=32, state='present')))
        expected_commands = [
            'authentication',
            'dot1x timeout quiet-period 32',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_radius_server_dead_time(self):
        ''' Test for enabling dot1x radius_server_dead_time '''
        set_module_args(dict(radius_server_dead_time=dict(time=4)))
        expected_commands = ['radius-server dead-time 4']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_radius_server_test(self):
        ''' Test for enabling dot1x radius_server_test '''
        set_module_args(dict(radius_server_test=dict(user_name='test_user')))
        expected_commands = ['radius-server test test_user']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_radius_server_dead_time_remove(self):
        ''' Test for enabling dot1x radius_server_dead_time '''
        set_module_args(dict(radius_server_dead_time=dict(time=4, state='absent')))
        expected_commands = ['no radius-server dead-time 4']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_radius_server_test_remove(self):
        ''' Test for enabling dot1x radius_server_test '''
        set_module_args(dict(radius_server_test=dict(user_name='test_user', state='absent')))
        expected_commands = ['no radius-server test test_user']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_no_arg_guest_vlan_id(self):
        ''' Test for enabling dot1x radius_server_dead_time '''
        set_module_args(dict(port_control=dict(auto='yes', all=True),
                             guest_vlan=dict(state='present')))
        result = self.execute_module(failed=True)

    def test_icx_dot1x_no_required_arg_timeout(self):
        ''' Test for enabling dot1x timout without required parameter '''
        set_module_args(dict(timeout=dict(state='present')))
        result = self.execute_module(failed=True)

    def test_icx_dot1x_no_required_arg_port_control(self):
        ''' Test for enabling port control dot1x without required parameter'''
        set_module_args(dict(port_control=dict(ethernet='1/1/1')))
        result = self.execute_module(failed=True)

    def test_icx_dot1x_mutually_exclusive_arg_port_control(self):
        ''' Test for enabling port control dot1x with mutually exclusive arguments'''
        set_module_args(dict(port_control=dict(force_unauthorized=True, auto=True, ethernet='1/1/1')))
        result = self.execute_module(failed=True)
