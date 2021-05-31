# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_aaa_authentication
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAaaAuthenticationModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_aaa_authentication module '''
    module = icx_aaa_authentication

    def setUp(self):
        super(TestICXAaaAuthenticationModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_aaa_authentication.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.icx_aaa_authentication.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAaaAuthenticationModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None

    def test_icx_aaa_authentication_all_options(self):
        ''' Test for successful aaa authentication with all options'''
        set_module_args(dict(dot1x=dict(primary_method='radius', backup_method1='none'),
                             enable=dict(primary_method='enable', backup_method_list=['line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
                             login=dict(primary_method='enable', backup_method_list=['line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
                             snmp_server=dict(primary_method='enable', backup_method_list=['line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
                             web_server=dict(primary_method='enable', backup_method_list=['line', 'local', 'radius', 'tacacs', 'tacacs+', 'none'])))
        expected_commands = ['aaa authentication dot1x default radius none',
                             'aaa authentication enable default enable line local radius tacacs tacacs+ none',
                             'aaa authentication login default enable line local radius tacacs tacacs+ none',
                             'aaa authentication snmp-server default enable line local radius tacacs tacacs+ none',
                             'aaa authentication web-server default enable line local radius tacacs tacacs+ none']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authentication_all_options_no_backup(self):
        ''' Test for successful aaa authentication with no backup_method options'''
        set_module_args(dict(dot1x=dict(primary_method='radius'),
                             enable=dict(primary_method='enable'),
                             login=dict(primary_method='enable'),
                             snmp_server=dict(primary_method='enable'),
                             web_server=dict(primary_method='enable')))
        expected_commands = ['aaa authentication dot1x default radius',
                             'aaa authentication enable default enable',
                             'aaa authentication login default enable',
                             'aaa authentication snmp-server default enable',
                             'aaa authentication web-server default enable']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authentication_all_options_remove(self):
        ''' Test for removiong aaa authentication with all options'''
        set_module_args(dict(dot1x=dict(primary_method='radius', backup_method1='none', state='absent'),
                             enable=dict(primary_method='enable', backup_method_list=['line', 'local', 'radius', 'tacacs', 'tacacs+', 'none'], state='absent'),
                             login=dict(primary_method='enable', backup_method_list=['line', 'local', 'radius', 'tacacs', 'tacacs+', 'none'], state='absent'),
                             snmp_server=dict(primary_method='enable', backup_method_list=['line', 'local', 'radius', 'tacacs', 'tacacs+', 'none'],
                                              state='absent'),
                             web_server=dict(primary_method='enable', backup_method_list=['line', 'local', 'radius', 'tacacs', 'tacacs+', 'none'],
                                             state='absent')))
        expected_commands = ['no aaa authentication dot1x default radius none',
                             'no aaa authentication enable default enable line local radius tacacs tacacs+ none',
                             'no aaa authentication login default enable line local radius tacacs tacacs+ none',
                             'no aaa authentication snmp-server default enable line local radius tacacs tacacs+ none',
                             'no aaa authentication web-server default enable line local radius tacacs tacacs+ none']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authentication_all_options_no_backup_remove(self):
        ''' Test for removing aaa authentication with no backup_method options'''
        set_module_args(dict(dot1x=dict(primary_method='radius', state='absent'),
                             enable=dict(primary_method='enable', state='absent'),
                             login=dict(primary_method='enable', state='absent'),
                             snmp_server=dict(primary_method='enable', state='absent'),
                             web_server=dict(primary_method='enable', state='absent')))
        expected_commands = ['no aaa authentication dot1x default radius',
                             'no aaa authentication enable default enable',
                             'no aaa authentication login default enable',
                             'no aaa authentication snmp-server default enable',
                             'no aaa authentication web-server default enable']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authentication_dot1x_enable(self):
        ''' Test for successful aaa authentication for dot1x and enable'''
        set_module_args(dict(dot1x=dict(primary_method='radius', state='present'), enable=dict(primary_method='enable',
                             backup_method_list=['line', 'local'], state='present')))
        expected_commands = ['aaa authentication dot1x default radius', 'aaa authentication enable default enable line local']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authentication_login_snmp_server(self):
        ''' Test for successful aaa authentication for login and snmp_server'''
        set_module_args(dict(login=dict(privilege_mode=True, state='present'), snmp_server=dict(primary_method='enable', state='present')))
        expected_commands = ['aaa authentication login privilege-mode', 'aaa authentication snmp-server default enable']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authentication_web_server(self):
        ''' Test for successful aaa authentication for web_server'''
        set_module_args(dict(web_server=dict(primary_method='tacacs', state='present')))
        expected_commands = ['aaa authentication web-server default tacacs']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authentication_invalid_arg_dot1x(self):
        ''' Test for invalid primary_method'''
        set_module_args(dict(dot1x=dict(primary_method='aaa', state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_authentication_invalid_arg_enable(self):
        ''' Test for invalid backup_method_list'''
        set_module_args(dict(enable=dict(primary_method='aaa', backup_method_list=['line'], state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_authentication_invalid_arg_login(self):
        ''' Test for invalid backup_method_list'''
        set_module_args(dict(login=dict(primary_method='enable', backup_method_list=['aaa'], state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_authentication_invalid_arg_snmp_server(self):
        ''' Test for invalid backup_method_list'''
        set_module_args(dict(snmp_server=dict(primary_method='enable', backup_method_list=['aaa'], state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_authentication_invalid_arg_web_server(self):
        ''' Test for invalid backup_method_list'''
        set_module_args(dict(web_server=dict(primary_method='enable', backup_method_list=['aaa'], state='present')))
        result = self.execute_module(failed=True)
