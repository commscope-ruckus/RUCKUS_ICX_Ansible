# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_vxlan
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAclAssignModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_vxlan module '''
    module = icx_vxlan

    def setUp(self):
        super(TestICXAclAssignModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_vxlan.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.icx_vxlan.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAclAssignModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None

    def test_icx_vxlan_all_options(self):
        ''' Test for successful vxlan with all options'''
        set_module_args(dict(overlay_gateway='gate1', overlay_gateway_type='present', ip_interface=dict(interface_id=1),
                             map_vlan=[dict(vlan_id=30, vni_id=100), dict(vlan_id=40, vni_id=200)],
                             site=[dict(site_name='site1', ip=dict(address='1.1.1.1'), extend_vlan=[dict(vlan_id=30), dict(vlan_id=40)]),
                                   dict(site_name='site2', ip=dict(address='2.2.2.2'), extend_vlan=[dict(vlan_id=30), dict(vlan_id=40)])]))
        expected_commands = [
            'overlay-gateway gate1',
            'type layer2-extension',
            'ip interface loopback 1',
            'map vlan 30 to vni 100',
            'map vlan 40 to vni 200',
            'site site1',
            'ip address 1.1.1.1',
            'extend vlan add 30',
            'extend vlan add 40',
            'exit',
            'site site2',
            'ip address 2.2.2.2',
            'extend vlan add 30',
            'extend vlan add 40',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vxlan_all_options_remove(self):
        ''' Test for removing vxlan with all options'''
        set_module_args(dict(overlay_gateway='gate1', overlay_gateway_type='absent', ip_interface=dict(interface_id=1, state='absent'),
                             map_vlan=[dict(vlan_id=30, vni_id=100, state='absent'), dict(vlan_id=40, vni_id=200, state='absent')],
                             site=[dict(site_name='site1', state='absent', ip=dict(address='1.1.1.1'), extend_vlan=[dict(vlan_id=30), dict(vlan_id=40)]),
                                   dict(site_name='site2', ip=dict(address='2.2.2.2'), state='absent', extend_vlan=[dict(vlan_id=30), dict(vlan_id=40)])]))
        expected_commands = [
            'overlay-gateway gate1',
            'no ip interface loopback 1',
            'no site site1',
            'no site site2',
            'no map vlan 30 to vni 100',
            'no map vlan 40 to vni 200',
            'no type layer2-extension']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vxlan_config_overlay_gateway(self):
        ''' Test for configuring overlay_gateway with some options'''
        set_module_args(dict(overlay_gateway='gate1', overlay_gateway_type='present', ip_interface=dict(interface_id=1),
                             map_vlan=[dict(vlan_id=40, vni_id=200)]))
        expected_commands = [
            'overlay-gateway gate1',
            'type layer2-extension',
            'ip interface loopback 1',
            'map vlan 40 to vni 200']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vxlan_remove_overlay_gateway(self):
        ''' Test for removing  overlay_gateway'''
        set_module_args(dict(overlay_gateway='gate1', state='absent', overlay_gateway_type='present'))
        expected_commands = [
            'no overlay-gateway gate1']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vxlan_config_site_remove(self):
        ''' Test for removing remote site configurations'''
        set_module_args(dict(overlay_gateway='gate1', site=[dict(site_name='site1', ip=dict(address='1.1.1.1', state='absent'),
                             extend_vlan=[dict(vlan_id=30, state='absent')])]))
        expected_commands = [
            'overlay-gateway gate1',
            'site site1',
            'no ip address 1.1.1.1',
            'no extend vlan add 30',
            'exit']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vxlan_no_arg_overlay_gateway(self):
        ''' Test for configuring vxlan without overlay_gateway name'''
        set_module_args(dict(overlay_gateway_type='present', ip_interface=dict(interface_id=1),
                             map_vlan=[dict(vlan_id=40, vni_id=200)]))
        result = self.execute_module(failed=True)
