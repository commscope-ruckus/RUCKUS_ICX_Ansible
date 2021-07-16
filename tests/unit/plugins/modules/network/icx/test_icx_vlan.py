# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_vlan
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXVlanModule(TestICXModule):

    module = icx_vlan

    def setUp(self):
        super(TestICXVlanModule, self).setUp()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.icx_vlan.exec_command')
        self.exec_command = self.mock_exec_command.start()

        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_vlan.load_config')
        self.load_config = self.mock_load_config.start()

        self.mock_get_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_vlan.get_config')
        self.get_config = self.mock_get_config.start()

        self.set_running_config()

    def tearDown(self):
        super(TestICXVlanModule, self).tearDown()
        self.mock_exec_command.stop()
        self.mock_load_config.stop()
        self.mock_get_config.stop()

    def load_fixtures(self, commands=None):
        compares = None

        def load_file(*args, **kwargs):
            module = args
            for arg in args:
                if arg.params['check_running_config'] is True or arg.params['purge'] is True:
                    return load_fixture('icx_vlan_config').strip()
                else:
                    return ''

        self.get_config.side_effect = load_file
        self.load_config.return_value = None
        self.exec_command.return_value = (0, load_fixture('icx_vlan_config').strip(), None)

    def test_icx_vlan_all_options(self):
        set_module_args(dict(name='test_vlan', vlan_id=5, interfaces=dict(name=['ethernet 1/1/44']),
                             tagged=dict(name=['ethernet 1/1/40 to 1/1/43']), ip_dhcp_snooping=True, ip_arp_inspection=True,
                             stp=dict(type='802-1w', priority='20', enabled=True)))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 5',
            'vlan 5 name test_vlan',
            'untagged ethernet 1/1/44',
            'tagged ethernet 1/1/40 to 1/1/43',
            'spanning-tree 802-1w',
            'spanning-tree 802-1w priority 20',
            'exit',
            'ip dhcp snooping vlan 5',
            'ip arp inspection vlan 5'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_remove(self):
        set_module_args(dict(vlan_id=5, state='absent'))
        result = self.execute_module(changed=True)
        expected_commands = [
            'no vlan 5',
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_set_tagged_port(self):
        set_module_args(dict(name='test_vlan', vlan_id=5, tagged=dict(name=['ethernet 1/1/40 to 1/1/43', 'lag 44'])))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 5',
            'vlan 5 name test_vlan',
            'tagged ethernet 1/1/40 to 1/1/43',
            'tagged lag 44',
            'exit'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_add_untagged_port(self):
        set_module_args(dict(name='test_vlan', vlan_id=3, interfaces=dict(name=['ethernet 1/1/10', 'lag 5'])))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 3',
            'vlan 3 name test_vlan',
            'untagged lag 5',
            'untagged ethernet 1/1/10',
            'exit'
        ]
        self.assertEqual(set(result['commands']), set(expected_commands))

    def test_icx_vlan_purge_tagged_port(self):
        set_module_args(dict(vlan_id=3, tagged=dict(name=['ethernet 1/1/40 to 1/1/42', 'lag 44'], purge=True)))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 3',
            'tagged ethernet 1/1/40 to 1/1/42',
            'no tagged lag 13',
            'no tagged ethernet 1/1/31',
            'no tagged ethernet 1/1/10',
            'no tagged ethernet 1/1/9',
            'no tagged ethernet 1/1/11',
            'tagged lag 44',
            'exit'
        ]
        self.assertEqual(set(result['commands']), set(expected_commands))

    def test_icx_vlan_purge_untagged_port(self):
        set_module_args(dict(name='test_vlan', vlan_id=3, interfaces=dict(name=['ethernet 1/1/10', 'lag 5'], purge=True)))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 3',
            'vlan 3 name test_vlan',
            'untagged lag 5',
            'untagged ethernet 1/1/10',
            'no untagged ethernet 1/1/21',
            'no untagged ethernet 1/1/20',
            'no untagged ethernet 1/1/22',
            'no untagged ethernet 1/1/27',
            'no untagged lag 11',
            'no untagged lag 12',
            'exit'
        ]
        self.assertEqual(set(result['commands']), set(expected_commands))

    def test_icx_vlan_disable_ip_arp_inspection(self):
        set_module_args(dict(vlan_id=5, ip_arp_inspection=False))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 5',
            'exit',
            'no ip arp inspection vlan 5'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_disable_ip_dhcp_snooping(self):
        set_module_args(dict(vlan_id=5, ip_dhcp_snooping=False))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 5',
            'exit',
            'no ip dhcp snooping vlan 5'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_aggregate(self):
        aggregate = [
            dict(vlan_id=9, name='vlan_9', interfaces=dict(name=['ethernet 1/1/40 to 1/1/43', 'ethernet 1/1/44']), ip_arp_inspection=True),
            dict(vlan_id=7, name='vlan_7', tagged=dict(name=['ethernet 1/1/20 to 1/1/23', 'ethernet 1/1/24']), ip_dhcp_snooping=True),
        ]
        set_module_args(dict(aggregate=aggregate))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 9',
            'vlan 9 name vlan_9',
            'untagged ethernet 1/1/40 to 1/1/43',
            'untagged ethernet 1/1/44',
            'exit',
            'ip arp inspection vlan 9',
            'vlan 7',
            'vlan 7 name vlan_7',
            'tagged ethernet 1/1/20 to 1/1/23',
            'tagged ethernet 1/1/24',
            'exit',
            'ip dhcp snooping vlan 7',
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_interfaces_cndt(self):
        set_module_args(dict(vlan_id=3, associated_interfaces=['ethernet 1/1/20 to 1/1/22', 'ethernet 1/1/27', 'lag 11 to 12']))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 3',
            'exit'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_tagged_cndt(self):
        set_module_args(dict(vlan_id=3, associated_tagged=['ethernet 1/1/9 to 1/1/11', 'ethernet 1/1/31', 'lag 13']))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 3',
            'exit'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_purge(self):
        set_module_args(dict(vlan_id=3, purge=True))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 3',
            'exit',
            'no vlan 6',
            'no vlan 10',
            'no vlan 21']
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_stp_disable(self):
        stp_spec = dict(dict(type='rstp', enabled=False))
        set_module_args(dict(vlan_id=3, stp=stp_spec))
        result = self.execute_module(changed=True)
        expected_commands = [
            'vlan 3',
            'no spanning-tree',
            'exit'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_vlan_tagged_cndt_fail(self):
        set_module_args(dict(vlan_id=3, associated_tagged=['ethernet 1/1/30', 'lag 14']))
        result = self.execute_module(failed=True)

    def test_icx_vlan_invalid_args_vlan_id(self):
        set_module_args(dict(name='test_vlan', vlan_id='vlan1', interfaces=dict(name=['ethernet 1/1/44'])))
        result = self.execute_module(failed=True)

    def test_icx_vlan_invalid_args_ip_dhcp_snooping(self):
        set_module_args(dict(vlan_id=5, ip_dhcp_snooping='present'))
        result = self.execute_module(failed=True)
