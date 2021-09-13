# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_static_route
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXStaticRouteModule(TestICXModule):

    module = icx_static_route

    def setUp(self):
        super(TestICXStaticRouteModule, self).setUp()
        self.mock_get_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_static_route.get_config')
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_static_route.load_config')
        self.load_config = self.mock_load_config.start()
        self.set_running_config()

    def tearDown(self):
        super(TestICXStaticRouteModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        compares = None

        def load_file(*args, **kwargs):
            module = args
            for arg in args:
                if arg.params['check_running_config'] is True or arg.params['purge'] is True:
                    return load_fixture('icx_static_route_config.txt').strip()
                else:
                    return ''

        self.get_config.side_effect = load_file
        self.load_config.return_value = None

    def test_icx_static_route_all_options(self):
        set_module_args(dict(prefix='192.126.23.0', mask='255.255.255.0', next_hop='10.10.14.3', admin_distance='40'))
        result = self.execute_module(changed=True)
        expected_commands = [
            'ip route 192.126.23.0 255.255.255.0 10.10.14.3 distance 40'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_all_options_remove(self):
        set_module_args(dict(prefix='192.126.23.0', mask='255.255.255.0', next_hop='10.10.14.3', admin_distance='40', state='absent'))
        result = self.execute_module(changed=True)
        expected_commands = [
            'no ip route 192.126.23.0 255.255.255.0 10.10.14.3'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_config(self):
        set_module_args(dict(prefix='192.126.0.0/16', next_hop='10.10.14.2'))
        result = self.execute_module(changed=True)
        expected_commands = [
            'ip route 192.126.0.0 255.255.0.0 10.10.14.2'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_aggregate(self):
        aggregate = [
            dict(prefix='192.126.23.0/24', next_hop='10.10.14.3'),
            dict(prefix='192.126.0.0', mask='255.255.0.0', next_hop='10.10.14.3', admin_distance='40')
        ]
        set_module_args(dict(aggregate=aggregate))
        result = self.execute_module(changed=True)
        expected_commands = [
            'ip route 192.126.23.0 255.255.255.0 10.10.14.3',
            'ip route 192.126.0.0 255.255.0.0 10.10.14.3 distance 40'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_aggregate_remove(self):
        aggregate = [
            dict(prefix='192.126.23.0/24', next_hop='10.10.14.3', state='absent'),
            dict(prefix='192.126.0.0', mask='255.255.0.0', next_hop='10.10.14.3', admin_distance='40', state='absent')
        ]
        set_module_args(dict(aggregate=aggregate))
        result = self.execute_module(changed=True)
        expected_commands = [
            'no ip route 192.126.23.0 255.255.255.0 10.10.14.3',
            'no ip route 192.126.0.0 255.255.0.0 10.10.14.3'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_config_purge(self):
        set_module_args(dict(prefix='172.16.10.0/32', next_hop='10.10.14.6', admin_distance=5, purge=True))
        result = self.execute_module(changed=True)
        expected_commands = [
            'ip route 172.16.10.0 255.255.255.255 10.10.14.6 distance 5',
            'no ip route 172.16.0.0 255.255.0.0 10.0.0.8',
            'no ip route 172.16.10.0 255.255.255.0 10.0.0.8',
            'no ip route 192.0.0.0 255.0.0.0 10.10.15.3',
            'no ip route 192.126.0.0 255.255.0.0 10.10.14.31',
            'no ip route 192.126.23.0 255.255.255.0 10.10.14.31',
            'no ip route 192.128.0.0 255.255.0.0 10.10.14.3',
            'no ip route 192.128.0.0 255.255.0.0 10.10.15.3',
            'no ip route 192.128.0.0 255.255.0.0 10.10.15.31'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_purge(self):
        set_module_args(dict(prefix='192.0.0.0/8', next_hop='10.10.15.3', purge=True))
        result = self.execute_module(changed=True)
        expected_commands = [
            'no ip route 172.16.0.0 255.255.0.0 10.0.0.8',
            'no ip route 172.16.10.0 255.255.255.0 10.0.0.8',
            'no ip route 192.126.0.0 255.255.0.0 10.10.14.31',
            'no ip route 192.126.23.0 255.255.255.0 10.10.14.31',
            'no ip route 192.128.0.0 255.255.0.0 10.10.14.3',
            'no ip route 192.128.0.0 255.255.0.0 10.10.15.3',
            'no ip route 192.128.0.0 255.255.0.0 10.10.15.31'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_no_args_next_hop(self):
        ''' Test without next_hop'''
        set_module_args(dict(prefix='192.126.0.0/16', admin_distance=4))
        result = self.execute_module(failed=True)

    def test_icx_static_route_invalid_args_admin_distance(self):
        ''' Test for invalid admin_distance'''
        set_module_args(dict(prefix='192.126.0.0/16', next_hop='10.10.14.2', admin_distance='10.10.1.1'))
        result = self.execute_module(failed=True)

    def test_icx_static_route_invalid_args_prefix_mask(self):
        ''' Test with mask and prefix-length of the mask '''
        set_module_args(dict(prefix='192.126.0.0/16', mask='255.255.0.0', next_hop='10.10.14.2'))
        result = self.execute_module(failed=True)
