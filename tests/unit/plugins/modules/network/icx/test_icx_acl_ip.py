# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_acl_ip
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXAclIpModule(TestICXModule):
    ''' Class used for Unit Tests agains icx_acl_ip module '''
    module = icx_acl_ip

    def setUp(self):
        super(TestICXAclIpModule, self).setUp()
        self.mock_load_config = patch('ansible_collections.commscope.icx.plugins.modules.icx_acl_ip.load_config')
        self.load_config = self.mock_load_config.start()
        self.mock_exec_command = patch('ansible_collections.commscope.icx.plugins.modules.icx_acl_ip.exec_command')
        self.exec_command = self.mock_exec_command.start()

    def tearDown(self):
        super(TestICXAclIpModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_exec_command.stop()

    def load_fixtures(self, commands=None):
        self.load_config.return_value = None

    def test_icx_acl_ip_extended_all_options(self):
        ''' Test for successful extended acl ipV4 and rules with all options'''
        set_module_args(dict(acl_type='extended', acl_name='acl1',
                             extended_rules=[(dict(seq_num='10', rule_type='permit', ip_protocol_name='ip',
                                                   source=dict(host='yes', ip_address='1.1.1.1'), destination=dict(ip_address='2.2.2.2', mask='0.0.0.0'),
                                                   precedence='routine', tos='normal', dscp_matching='21', dscp_marking='8', priority_matching='6',
                                                   priority_marking='6', internal_priority_marking='3', log='yes', mirror='yes')),
                                             (dict(remark=dict(comment_text='This Denies icmp traffic'), seq_num='20',
                                                   rule_type='deny', ip_protocol_name='icmp', source=dict(any='yes'), destination=dict(ip_address='1.1.1.1',
                                                   mask='0.0.0.0'), icmp_num='25', precedence='priority', tos='max-reliability', dscp_matching='21',
                                                   dscp_marking='8', priority_matching='6', traffic_policy_name='policy1', log='yes', mirror='yes')),
                                             (dict(seq_num='30', rule_type='permit', ip_protocol_name='tcp', source=dict(ip_address='2.2.2.2', mask='0.0.0.0'),
                                                   destination=dict(any='yes'), source_comparison_operators=dict(operator='eq', port_num='22'),
                                                   destination_comparison_operators=dict(operator='range', port_name='ftp',
                                                   high_port_name='http'), established='yes', precedence='network', tos='min-delay', dscp_matching='32',
                                                   dscp_marking='8', priority_matching='6', internal_marking='7'))]))
        expected_commands = ['ip access-list extended acl1',
                             'sequence 10 permit ip host 1.1.1.1 2.2.2.2 0.0.0.0 precedence routine tos normal dscp-matching 21 802.1p-priority-matching 6 dscp-marking 8 802.1p-priority-marking 6 internal-priority-marking 3 log mirror',
                             'remark This Denies icmp traffic',
                             'sequence 20 deny icmp any 1.1.1.1 0.0.0.0 25 precedence priority tos max-reliability dscp-matching 21 802.1p-priority-matching 6 dscp-marking 8 traffic-policy policy1 log mirror',
                             'sequence 30 permit tcp 2.2.2.2 0.0.0.0 eq 22 any range ftp http established precedence network tos min-delay dscp-matching 32 802.1p-priority-matching 6 dscp-marking 8 802.1p-and-internal-marking 7']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_ip_extended_all_options_remove(self):
        ''' Test for removing extended acl ipV4 and rules with all options'''
        set_module_args(dict(acl_type='extended', acl_name='acl1', state='absent',
                             extended_rules=[(dict(seq_num='10', rule_type='permit', ip_protocol_name='ip', source=dict(host='yes', ip_address='1.1.1.1'),
                                                   destination=dict(ip_address='2.2.2.2', mask='0.0.0.0'), precedence='routine', tos='normal', dscp_matching='21', dscp_marking='8', priority_matching='6', priority_marking='6', internal_priority_marking='3', log='yes', mirror='yes', state='absent')),
                                             (dict(remark=dict(comment_text='This Denies icmp traffic', state='absent'), seq_num='20', rule_type='deny', ip_protocol_name='icmp', source=dict(any='yes'), destination=dict(ip_address='1.1.1.1', mask='0.0.0.0'), icmp_num='25', precedence='priority', tos='max-reliability', dscp_matching='21', dscp_marking='8', priority_matching='6', traffic_policy_name='policy1', log='yes', mirror='yes', state='absent')),
                                             (dict(seq_num='30', rule_type='permit', ip_protocol_name='tcp', source=dict(ip_address='2.2.2.2', mask='0.0.0.0'), destination=dict(any='yes'), source_comparison_operators=dict(operator='eq', port_num='22'), destination_comparison_operators=dict(operator='range', port_name='ftp', high_port_name='http'), established='yes', precedence='network', tos='min-delay', dscp_matching='32', dscp_marking='8', priority_matching='6', internal_marking='7', state='absent'))]))
        expected_commands = ['no ip access-list extended acl1',
                             'no sequence 10 permit ip host 1.1.1.1 2.2.2.2 0.0.0.0 precedence routine tos normal dscp-matching 21 802.1p-priority-matching 6 dscp-marking 8 802.1p-priority-marking 6 internal-priority-marking 3 log mirror',
                             'no remark This Denies icmp traffic',
                             'no sequence 20 deny icmp any 1.1.1.1 0.0.0.0 25 precedence priority tos max-reliability dscp-matching 21 802.1p-priority-matching 6 dscp-marking 8 traffic-policy policy1 log mirror',
                             'no sequence 30 permit tcp 2.2.2.2 0.0.0.0 eq 22 any range ftp http established precedence network tos min-delay dscp-matching 32 802.1p-priority-matching 6 dscp-marking 8 802.1p-and-internal-marking 7']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_ip_extended_enable_accounting(self):
        ''' Test for successful extended acl ipV4 enable accounting'''
        set_module_args(dict(acl_type='extended', acl_name='acl1', accounting='enable'))
        expected_commands = ['ip access-list extended acl1',
                             'enable accounting']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_ip_extended_disable_accounting(self):
        ''' Test for successful extended acl ipV4 disable accounting'''
        set_module_args(dict(acl_type='extended', acl_name='acl1', accounting='disable'))
        expected_commands = ['ip access-list extended acl1',
                             'no enable accounting']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_ip_standard_all_options(self):
        ''' Test for successful standard ipv4 and rule with all options'''
        set_module_args(dict(acl_type='standard', acl_name='acl1', accounting='enable',
                             standard_rules=[(dict(seq_num='10', rule_type='permit', host='yes', source_ip='2.2.2.2', log='yes', mirror='yes'))]))
        expected_commands = ['ip access-list standard acl1',
                             'enable accounting',
                             'sequence 10 permit host 2.2.2.2 log mirror']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_ip_standard_all_options_remove(self):
        ''' Test for removing standard ipv4 and rule with all options'''
        set_module_args(dict(acl_type='standard', acl_name='acl1', state='absent', accounting='disable',
                             standard_rules=[(dict(seq_num='10', rule_type='permit', host='yes', source_ip='2.2.2.2', log='yes', mirror='yes', state='absent'))]))
        expected_commands = ['no ip access-list standard acl1',
                             'no enable accounting',
                             'no sequence 10 permit host 2.2.2.2 log mirror']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_ip_extended_deny(self):
        ''' Test for successful extended acl ipV4 deny'''
        set_module_args(dict(acl_type='extended', acl_name='acl1',
                             extended_rules=[(dict(rule_type='deny', ip_protocol_name='ip', source=dict(any='yes'), destination=dict(any='yes'), precedence='routine', log='yes')),
                                             (dict(rule_type='deny', ip_protocol_name='icmp', source=dict(any='yes'), destination=dict(ip_address='1.1.1.1', mask='0.0.0.0'), icmp_num='25', tos='max-reliability', dscp_matching='21')),
                                             (dict(rule_type='deny', ip_protocol_name='tcp', source=dict(any='yes'), destination=dict(any='yes'), source_comparison_operators=dict(operator='eq', port_num='22'), precedence='network'))]))
        expected_commands = ['ip access-list extended acl1',
                             'deny ip any any precedence routine log',
                             'deny icmp any 1.1.1.1 0.0.0.0 25 tos max-reliability dscp-matching 21',
                             'deny tcp any eq 22 any precedence network']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_ip_standard_deny(self):
        ''' Test for successful standard acl ipV4 deny rule'''
        set_module_args(dict(acl_type='standard', acl_name='acl1',
                             standard_rules=[(dict(seq_num='10', rule_type='deny', any='yes'))]))
        expected_commands = ['ip access-list standard acl1',
                             'sequence 10 deny any']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_ip_extended_permit(self):
        ''' Test for successful extended acl ipV4 permit rule'''
        set_module_args(dict(acl_type='extended', acl_name='acl1',
                             extended_rules=[(dict(rule_type='permit', ip_protocol_name='ip', source=dict(host='yes', ip_address='1.1.1.1'), destination=dict(any='yes'), traffic_policy_name='policy1')),
                                             (dict(rule_type='permit', ip_protocol_name='icmp', source=dict(any='yes'), destination=dict(ip_address='1.1.1.1', mask='0.0.0.0'), icmp_num='25')),
                                             (dict(rule_type='permit', ip_protocol_name='tcp', source=dict(any='yes'), destination=dict(any='yes'), source_comparison_operators=dict(operator='eq', port_num='22'), destination_comparison_operators=dict(operator='range', port_name='ftp')))]))
        expected_commands = ['ip access-list extended acl1',
                             'permit ip host 1.1.1.1 any traffic-policy policy1',
                             'permit icmp any 1.1.1.1 0.0.0.0 25',
                             'permit tcp any eq 22 any range ftp']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_acl_ip_standard_permit(self):
        ''' Test for successful standard acl ipV4 permit rule'''
        set_module_args(dict(acl_type='standard', acl_name='acl1',
                             standard_rules=[(dict(rule_type='deny', any='yes', log='yes'))]))
        expected_commands = ['ip access-list standard acl1',
                             'deny any log']
        result = self.execute_module(changed=True)
        self.assertEqual(result['commands'], expected_commands)

    def test_icx_invalid_args_acl_ip_standard(self):
        ''' Test for invalid rule_type'''
        set_module_args(dict(acl_type='standard', acl_name='acl1',
                             standard_rules=[(dict(seq_num='20', rule_type='aa', any='yes', log='yes'))]))
        result = self.execute_module(failed=True)

    def test_icx_invalid_args_acl_ip_extended(self):
        ''' Test for invalid seq_num'''
        set_module_args(dict(acl_name='acl1',
                             extended_rules=[(dict(seq_num='aa', rule_type='permit', ip_protocol_name='ip', source=dict(host='yes', ip_address='1.1.1.1'), destination=dict(any='yes')))]))
        result = self.execute_module(failed=True)
