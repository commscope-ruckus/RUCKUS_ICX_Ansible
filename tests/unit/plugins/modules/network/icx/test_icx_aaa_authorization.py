# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules.network.icx import icx_aaa_authorization
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAaaAuthorizationModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_aaa_authorization module '''
    module = icx_aaa_authorization

    def setUp(self):
        super(TestICXAaaAuthorizationModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.network.icx.icx_aaa_authorization.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.network.icx.icx_aaa_authorization.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAaaAuthorizationModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None

    def test_icx_aaa_authorization_all_options(self):
        ''' Test for successful aaa authorization with all options'''
        set_module_args(dict(coa_enable=dict(state='present'),
                             coa_ignore=dict(request='dm-request'),
                             commands=dict(privilege_level=0, primary_method='radius', backup_method1='tacacs+', backup_method2='none'),
                             exec_=dict(primary_method='radius', backup_method1='tacacs+', backup_method2='none')))
        expected_commands = ['aaa authorization coa enable',
                             'aaa authorization coa ignore dm-request',
                             'aaa authorization commands 0 default radius tacacs+ none',
                             'aaa authorization exec default radius tacacs+ none']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authorization_all_options_no_backup(self):
        ''' Test for successful aaa authorization without backup_method options'''
        set_module_args(dict(coa_enable=dict(state='present'),
                             coa_ignore=dict(request='dm-request'),
                             commands=dict(privilege_level=0, primary_method='radius'),
                             exec_=dict(primary_method='radius')))
        expected_commands = ['aaa authorization coa enable',
                             'aaa authorization coa ignore dm-request',
                             'aaa authorization commands 0 default radius',
                             'aaa authorization exec default radius']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authorization_all_options_remove(self):
        ''' Test for removiong aaa authorization with all options'''
        set_module_args(dict(coa_enable=dict(state='absent'),
                             coa_ignore=dict(request='dm-request', state='absent'),
                             commands=dict(privilege_level=0, primary_method='radius', backup_method1='tacacs+', backup_method2='none', state='absent'),
                             exec_=dict(primary_method='radius', backup_method1='tacacs+', backup_method2='none', state='absent')))
        expected_commands = ['no aaa authorization coa enable',
                             'no aaa authorization coa ignore dm-request',
                             'no aaa authorization commands 0 default radius tacacs+ none',
                             'no aaa authorization exec default radius tacacs+ none']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authorization_all_options_no_backup_remove(self):
        ''' Test for removing aaa authorization without backup_method options'''
        set_module_args(dict(coa_enable=dict(state='absent'),
                             coa_ignore=dict(request='dm-request', state='absent'),
                             commands=dict(privilege_level=0, primary_method='radius', state='absent'),
                             exec_=dict(primary_method='radius', state='absent')))
        expected_commands = ['no aaa authorization coa enable',
                             'no aaa authorization coa ignore dm-request',
                             'no aaa authorization commands 0 default radius',
                             'no aaa authorization exec default radius']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authorization_coa_enable_coa_ignore(self):
        ''' Test for successful aaa authorization for coa_ignore and commands'''
        set_module_args(dict(coa_enable=dict(state='present'), coa_ignore=dict(request='dm-request', state='present')))
        expected_commands = ['aaa authorization coa enable', 'aaa authorization coa ignore dm-request']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authorization_commands_exec_(self):
        ''' Test for successful aaa authorization for exec_'''
        set_module_args(dict(commands=dict(privilege_level=0, primary_method='radius', state='present'), exec_=dict(primary_method='radius', state='present')))
        expected_commands = ['aaa authorization commands 0 default radius', 'aaa authorization exec default radius']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_aaa_authorization_invalid_args_coa_ignore(self):
        ''' Test for invalid request'''
        set_module_args(dict(coa_ignore=dict(request='aaa', state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_authorization_invalid_args_commands(self):
        ''' Test for invalid privilege_level'''
        set_module_args(dict(commands=dict(privilege_level=2, primary_method='radius', state='present')))
        result = self.execute_module(failed=True)

    def test_icx_aaa_authorization_invalid_args_exec_(self):
        ''' Test for invalid primary_method'''
        set_module_args(dict(exec_=dict(primary_method='aaa', backup_method1='tacacs+', state='present')))
        result = self.execute_module(failed=True)
