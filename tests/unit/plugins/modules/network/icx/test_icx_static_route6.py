# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_static_route6
from .icx_module import TestICXModule, load_fixture


class TestICXStaticRouteModule6(TestICXModule):

    module = icx_static_route6

    def setUp(self):
        super(TestICXStaticRouteModule6, self).setUp()
        self.mock_get_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_static_route6.get_config')
        self.get_config = self.mock_get_config.start()
        self.mock_run_commands = patch('ansible_collections.commscope.icx.plugins.modules.icx_static_route6.run_commands')
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_static_route6.load_config')
        self.load_config = self.mock_load_config.start()
        self.set_running_config()

    def tearDown(self):
        super(TestICXStaticRouteModule6, self).tearDown()
        self.mock_get_config.stop()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None):
        compares = None

        def load_file(*args, **kwargs):
            module = args
            output = list()
            for arg in args:
                if arg.params['check_running_config'] is True or arg.params['purge'] is True:
                    output.append(load_fixture('icx_static_route_config6.txt'))
                    return output
                else:
                    return ''

        self.run_commands.side_effect = load_file
        self.load_config.return_value = None

    def test_icx_static_route__all_options(self):
        set_module_args(dict(prefix='6666:1:1::/64', next_hop='6666:1:1::', admin_distance='40'))
        result = self.execute_module(changed=True)
        expected_commands = [
            'ipv6 route 6666:1:1::/64  6666:1:1:: distance 40'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route__all_options_remove(self):
        set_module_args(dict(prefix='6666:1:1::/64', next_hop='6666:1:1::', admin_distance='40', state='absent'))
        result = self.execute_module(changed=True)
        expected_commands = [
            'no ipv6 route 6666:1:1::/64 6666:1:1::'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_config(self):
        set_module_args(dict(prefix='6666:1:2::0/64', next_hop='6666:1:2::0'))
        result = self.execute_module(changed=True)
        expected_commands = [
            'ipv6 route 6666:1:2::/64  6666:1:2::'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_aggregate(self):
        aggregate = [
            dict(prefix='6666:1:3::/64', next_hop='6666:1:3::', admin_distance=1),
            dict(prefix='6666:1:2::/64', next_hop='6666:1:2::', admin_distance=40)
        ]
        set_module_args(dict(aggregate=aggregate))
        result = self.execute_module(changed=True)
        expected_commands = [
            'ipv6 route 6666:1:3::/64  6666:1:3:: distance 1',
            'ipv6 route 6666:1:2::/64  6666:1:2:: distance 40',
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_aggregate_remove(self):
        aggregate = [
            dict(prefix='6666:1:3::/64', next_hop='6666:1:3::', admin_distance=1, state='absent'),
            dict(prefix='6666:1:2::/64', next_hop='6666:1:2::', admin_distance=40, state='absent')
        ]
        set_module_args(dict(aggregate=aggregate))
        result = self.execute_module(changed=True)
        expected_commands = [
            'no ipv6 route 6666:1:3::/64 6666:1:3::',
            'no ipv6 route 6666:1:2::/64 6666:1:2::',
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_config_purge(self):
        set_module_args(dict(prefix='6666:1:1::/64', next_hop='6666:1:1::', purge=True))
        result = self.execute_module(changed=True)
        expected_commands = [
            'no ipv6 route 6666:1:14::/64  6666:1:4::',
            'no ipv6 route 6666:1:2::/64  6666:1:2::',
            'ipv6 route 6666:1:1::/64  6666:1:1::'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_purge(self):
        set_module_args(dict(prefix='6666:1:2::/64', next_hop='6666:1:2::', purge=True))
        result = self.execute_module(changed=True)
        expected_commands = [
            'no ipv6 route 6666:1:14::/64  6666:1:4::'
        ]
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_static_route_no_args_prefix(self):
        ''' Test without prefix'''
        set_module_args(dict(next_hop='6666:1:4::', admin_distance=4))
        result = self.execute_module(failed=True)

    def test_icx_static_route_invalid_args_admin_distance(self):
        ''' Test for invalid admin_distance'''
        set_module_args(dict(prefix='6666:1:2::/64', next_hop='6666:1:4::', admin_distance='10.10.1.1'))
        result = self.execute_module(failed=True)

    def test_icx_static_route_invalid_args_purge(self):
        ''' Test for invalid purge'''
        set_module_args(dict(prefix='6666:1:2::/64', next_hop='6666:1:4::', purge='enable'))
        result = self.execute_module(failed=True)
