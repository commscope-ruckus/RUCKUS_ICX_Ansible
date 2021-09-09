# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_mct
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAclAssignModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_dot1x module '''
    module = icx_mct

    def setUp(self):
        super(TestICXAclAssignModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_mct.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.icx_mct.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAclAssignModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None

    def test_icx_mct_all_options(self):
        ''' Test for successful mct with all options'''
        set_module_args(dict(cluster_name='test', cluster_id=100, rbridge_id=dict(id=10), session_vlan=dict(vlan_id=3000),
                             keep_alive_vlan=dict(vlan_id=3001), icl=dict(name='ICL', ethernet='1/1/2'), peer=dict(ip='1.1.1.1', disable_fast_failover=True,
                             rbridge=dict(id=2, icl_name='ICL'), timers=dict(keep_alive=20, hold_time=30)), client_interfaces='present',
                             client_auto_detect=dict(config=dict(deploy_all=True), ethernet=dict(port='1/1/1'), start=dict(config_deploy_all=True)),
                             deploy='present', client=[dict(name='client_1', rbridge_id=dict(id=2), client_interface=dict(lag=10), deploy='present')]))
        expected_commands = [
            'cluster test 100',
            'rbridge-id 10',
            'session-vlan 3000',
            'keep-alive-vlan 3001',
            'icl ICL ethernet 1/1/2',
            'peer 1.1.1.1 rbridge-id 2 icl ICL',
            'peer 1.1.1.1 disable-fast-failover',
            'peer 1.1.1.1 timers keep-alive 20 hold-time 30',
            'client-interfaces shutdown',
            'client-auto-detect config deploy-all',
            'client-auto-detect ethernet 1/1/1',
            'client-auto-detect start config-deploy-all',
            'deploy',
            'client client_1',
            'rbridge-id 2',
            'client-interface lag 10',
            'deploy']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_mct_all_options_remove(self):
        ''' Test for removing mct with all options'''
        set_module_args(dict(cluster_name='test', cluster_id=100, rbridge_id=dict(id=10, state='absent'), session_vlan=dict(vlan_id=3000, state='absent'),
                             keep_alive_vlan=dict(vlan_id=3001, state='absent'), icl=dict(name='ICL', ethernet='1/1/2', state='absent'),
                             peer=dict(ip='1.1.1.1', disable_fast_failover=False, rbridge=dict(id=2, icl_name='ICL', state='absent'),
                             timers=dict(keep_alive=20, hold_time=30, state='absent')), client_interfaces='absent',
                             client_auto_detect=dict(config=dict(deploy_all=True, state='absent'), ethernet=dict(port='1/1/1', state='absent'),
                             start=dict(config_deploy_all=False, state='absent'), stop=False), deploy='absent',
                             client=[dict(name='client_1', rbridge_id=dict(id=2, state='absent'), client_interface=dict(lag=10, state='absent'),
                                          deploy='absent')]))
        expected_commands = [
            'cluster test 100',
            'no deploy',
            'no rbridge-id 10',
            'no keep-alive-vlan 3001',
            'no peer 1.1.1.1 disable-fast-failover',
            'no peer 1.1.1.1 timers keep-alive 20 hold-time 30',
            'no peer 1.1.1.1 rbridge-id 2 icl ICL',
            'no icl ICL ethernet 1/1/2',
            'no session-vlan 3000',
            'no client-interfaces shutdown',
            'no client-auto-detect config deploy-all',
            'no client-auto-detect ethernet 1/1/1',
            'client client_1',
            'no deploy',
            'no rbridge-id 2',
            'no client-interface lag 10']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_mct_remove_client(self):
        ''' Test for removing client'''
        set_module_args(dict(cluster_id=100, client=[dict(name='client_1', rbridge_id=dict(id=2, state='absent'),
                             state='absent')]))
        expected_commands = [
            'cluster 100',
            'no client client_1']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_mct_remove_cluster(self):
        ''' Test for removing mct cluster'''
        set_module_args(dict(cluster_name='test', cluster_id=100, state='absent', rbridge_id=dict(id=10), client=[dict(name='client_1')]))
        expected_commands = [
            'no cluster test 100']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_mct_client_isolation(self):
        ''' Test for successful mct client_isolation'''
        set_module_args(dict(cluster_id=100, rbridge_id=dict(id=10), session_vlan=dict(vlan_id=3000),
                             icl=dict(name='ICL', ethernet='1/1/2'), peer=dict(ip='1.1.1.1', rbridge=dict(id=2, icl_name='ICL')),
                             client_isolation='present', deploy='present'))
        expected_commands = [
            'cluster 100',
            'rbridge-id 10',
            'session-vlan 3000',
            'icl ICL ethernet 1/1/2',
            'peer 1.1.1.1 rbridge-id 2 icl ICL',
            'client-isolation strict',
            'deploy']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_mct_remove_client_isolation(self):
        ''' Test for removing client_isolation and other configured options '''
        set_module_args(dict(cluster_id=100, rbridge_id=dict(id=10, state='absent'), session_vlan=dict(vlan_id=3000,
                             state='absent'), icl=dict(name='ICL', ethernet='1/1/2', state='absent'), peer=dict(ip='1.1.1.1',
                             rbridge=dict(id=2, icl_name='ICL', state='absent')), client_isolation='absent', deploy='absent'))
        expected_commands = [
            'cluster 100',
            'no deploy',
            'no rbridge-id 10',
            'no peer 1.1.1.1 rbridge-id 2 icl ICL',
            'no icl ICL ethernet 1/1/2',
            'no session-vlan 3000',
            'no client-isolation strict']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_mct_auto_detect_stop(self):
        ''' Test for stop auto-config process'''
        set_module_args(dict(cluster_id=100, client_auto_detect=dict(stop=True)))
        expected_commands = [
            'cluster 100',
            'client-auto-detect stop']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_dot1x_no_arg_cluster_id(self):
        ''' Test without cluster id'''
        set_module_args(dict(cluster_name='test', rbridge_id=dict(id=10)))
        result = self.execute_module(failed=True)
