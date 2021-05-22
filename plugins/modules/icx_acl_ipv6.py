#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_acl_ipv6
author: "Ruckus Wireless (@Commscope)"
short_description: Configures ACL in Ruckus ICX 7000 series switches.
description:
  - Configures ACL in Ruckus ICX 7000 series switches.
notes:
  - Tested against ICX 10.1
options:
  acl_name:
    description: Specifies a unique ACL name.
    type: str
    required: true
  accounting:
    description: Enables/Disables accounting for the ipv6 ACL.
    type: str
    choices: ['enable', 'disable']
  rules:
    description: Inserts filtering rules in IPv6 access control lists.
    type: list
    elements: dict
    suboptions:
      remark:
        description: Adds a comment to describe entries in IPv6 ACL.
        type: dict
        suboptions:
          comment_text:
            description: Specifies the comment for the ACL entry, up to 256 alphanumeric characters.
            type: str
          state:
            description: Add/Delete the comment text for an ACL entry.
            type: str
            default: present
            choices: ['present', 'absent']
      seq_num:
        description: Enables you to assign a sequence number to the rule. Valid values range from 1 through 65000.
        type: int
      rule_type:
        description: Inserts filtering rules in IPv4 standard named or numbered ACLs that will deny/permit packets.
        type: str
        required: true
        choices: ['deny', 'permit']
      ip_protocol_name:
        description: Specifies the type of IPv6 packet to filter.
        type: str
        choices: ['ahp', 'esp', 'icmp', 'ipv6', 'sctp', 'tcp', 'udp']
      ip_protocol_num:
        description: Protocol number (from 0 to 255).
        type: int
      source:
        description: ipv6-source-prefix/prefix-length | host source-ipv6_address | any.
        type: dict
        required: true
        suboptions:
          host_ipv6_address:
            description: Specifies a host source IPv6 address. A prefix length of 128 is implied.
            type: str
          ipv6_prefix_prefix_length:
            description: Specifies a source prefix and prefix length that a packet must match for the specified action (deny or permit) to occur.
            type: str
          any:
            description: Specifies all source addresses.
            type: bool
      destination:
        description: ipv6-source-prefix/prefix-length | host source-ipv6_address | any.
        type: dict
        required: true
        suboptions:
          host_ipv6_address:
            description: Specifies a host destination IPv6 address. A prefix length of 128 is implied.
            type: str
          ipv6_prefix_prefix_length:
            description: Specifies a destination prefix and prefix length that a packet must match for the specified action (deny or permit) to occur.
            type: str
          any:
            description: Specifies all destination addresses.
            type: bool
      source_comparison_operators:
        description: If you specified tcp or udp, the following optional operators are available. Specify either port number or name for the operation.
        type: dict
        suboptions:
          operator:
            description: Specifies comparison operator.
            type: str
            choices: ['eq','gt','lt','neq','range']
          port_num:
            description: Specifies port numbers that satisfy the operation with the port number you enter.
            type: int
          port_name:
            description: Specifies port numbers that satisfy the operation with the numeric equivalent of the port name.
            type: str
            choices: ['ftp-data','ftp','ssh','telnet','smtp','dns','http','gppitnp','pop2','pop3','sftp','sqlserv','bgp','ldap','ssl','tftp','snmp']
          high_port_num:
            description: For range operator, specifies high port number.
            type: int
          high_port_name:
            description: For range operator, specifies higher port name.
            type: str
            choices: ['ftp-data','ftp','ssh','telnet','smtp','dns','http','gppitnp','pop2','pop3','sftp','sqlserv','bgp','ldap','ssl','tftp','snmp']
      destination_comparison_operators:
        description: If you specified tcp or udp, the following optional operators are available. Specify either port number or name for the operation.
        type: dict
        suboptions:
          operator:
            description: Specifies comparison operator.
            type: str
            choices: ['eq','gt','lt','neq','range']
          port_num:
            description: Specifies port numbers that satisfy the operation with the port number you enter.
            type: int
          port_name:
            description: Specifies port numbers that satisfy the operation with the numeric equivalent of the port name.
            type: str
            choices: ['ftp-data','ftp','ssh','telnet','smtp','dns','http','gppitnp','pop2','pop3','sftp','sqlserv','bgp','ldap','ssl','tftp','snmp']
          high_port_num:
            description: For range operator, specifies high port number.
            type: int
          high_port_name:
            description: For range operator, specifies higher port name.
            type: str
            choices: ['ftp-data','ftp','ssh','telnet','smtp','dns','http','gppitnp','pop2','pop3','sftp','sqlserv','bgp','ldap','ssl','tftp','snmp']
      established:
        description: (For TCP rules only) Filter packets that have the Acknowledgment (ACK) or Reset (RST) flag set.
        type: bool
        default: no
      icmp_num:
        description: Specifies a numbered message type. Use either icmp_num or icmp_type.
        type: int
      icmp_type:
        description: Specifies icmp type.
        type: str
        choices: ['beyond-scope','destination-unreachable','echo-reply','echo-request','header','hop-limit','mld-query','mld-reduction','mld-report',
                  'nd-na','nd-ns','next-header','no-admin','no-route','packet-too-big','parameter-option','parameter-problem',
                  'port-unreachable','reassembly-timeout','renum-command','renum-result','renum-seq-number',
                  'router-advertisement','router-renumbering','router-solicitation','time-exceeded','unreachable']
      fragments:
        description: Filters on IPv6 fragments with a non-zero fragment offset. Available only in IPv6 ACLs.
        type: bool
        default: no
      routing:
        description: Filters on IPv6 packets routed from the source. Available only in IPv6 ACLs.
        type: bool
        default: no
      dscp_matching:
        description: Filters by DSCP value. Values range from 0 through 63.
        type: int
      dscp_marking:
        description: Assigns the DSCP value that you specify to the packet. Values range from 0 through 63.
        type: int
      priority_matching:
        description: Filters by 802.1p priority, for rate limiting. Values range from 0 through 7.
        type: int
      priority_marking:
        description: Assigns the 802.1p value that you specify to the packet. Values range from 0 through 7.
        type: int
      internal_priority_marking:
        description: Assigns the identical 802.1p value and internal queuing priority (traffic class) that you specify to the packet [0-7].
        type: int
      traffic_policy_name:
        description: Enables the device to limit rate of inbound traffic and to count packets and bytes per packet to which ACL deny clauses are applied.
        type: str
      log:
        description: Enables SNMP traps and syslog messages for the rule.
        type: bool
        default: no
      mirror:
        description: Mirrors packets matching the rule.
        type: bool
        default: no
      state:
        description: Specifies whether to configure or remove rule.
        type: str
        default: present
        choices: ['present', 'absent']
  state:
    description: Create/Remove an IPv6 access control list (ACL).
    type: str
    default: present
    choices: ['present', 'absent']
"""
EXAMPLES = """
- name: create ipv6 acl and add rules
  community.network.icx_acl_ipv6:
    acl_name: acl1
    rules: |
      - rule_type: permit
        seq_num: 10
        ip_protocol_name: ipv6
        source:
          any: yes
        destination:
          any: yes
      - rule_type: permit
        ip_protocol_name: tcp
        source:
          host_ipv6_address: 2001:DB8:e0ac::2
        destination:
          host_ipv6_address: 2001:DB8:e0aa:0::24
        source_comparison_operators:
          operator: eq
          port_num: 22
        destination_comparison_operators:
          operator: range
          port_name: ftp
          high_port_name: http
        established: yes
        dscp_matching: 32
        state: absent
    state: present
- name: remove ipv6 acl
  community.network.icx_acl_ipv6:
    acl_name: acl1
    state: absent
"""
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(module, acl_name=None, accounting=None, rules=None, state=None):

    acl_cmds = []
    rules_acl_cmds = []

    if state == 'absent':
        cmd = "no ipv6 access-list {}".format(acl_name)
    else:
        cmd = "ipv6 access-list {}".format(acl_name)
    acl_cmds.append(cmd)

    if accounting == 'disable':
        cmd = "no enable accounting"
        acl_cmds.append(cmd)
    elif accounting == 'enable':
        cmd = "enable accounting"
        acl_cmds.append(cmd)

    if rules is not None:
        for rule in rules:
            if rule['remark'] is not None:
                if rule['remark']['state'] == 'absent':
                    cmd = "no remark {}".format(rule['remark']['comment_text'])
                else:
                    cmd = "remark {}".format(rule['remark']['comment_text'])
                rules_acl_cmds.append(cmd)
            cmd = ""
            if rule['state'] == 'absent':
                cmd += "no "
            if rule['seq_num'] is not None:
                cmd += "sequence {} ".format(rule['seq_num'])
            if rule['rule_type'] is not None:
                cmd += "{}".format(rule['rule_type'])

            if rule['ip_protocol_name'] is not None:
                cmd += " {}".format(rule['ip_protocol_name'])
            elif rule['ip_protocol_num'] is not None:
                cmd += " {}".format(rule['ip_protocol_num'])
            if rule['source']['host_ipv6_address'] is not None:
                cmd += " host {}".format(rule['source']['host_ipv6_address'])
            elif rule['source']['ipv6_prefix_prefix_length'] is not None:
                cmd += " {}".format(rule['source']['ipv6_prefix_prefix_length'])
            elif rule['source']['any']:
                cmd += " any"
            if rule['ip_protocol_name'] == "icmp":
                if rule['destination']['host_ipv6_address'] is not None:
                    cmd += " host {}".format(rule['destination']['host_ipv6_address'])
                elif rule['destination']['ipv6_prefix_prefix_length'] is not None:
                    cmd += " {}".format(rule['destination']['ipv6_prefix_prefix_length'])
                elif rule['destination']['any']:
                    cmd += " any"
                if rule['icmp_num'] is not None:
                    cmd += " {}".format(rule['icmp_num'])
                elif rule['icmp_type'] is not None:
                    cmd += " {}".format(rule['icmp_type'])
                if (rule['icmp_num'] is not None) or (rule['icmp_type'] is not None):
                    if rule['dscp_matching'] is not None:
                        cmd += " dscp-matching {}".format(rule['dscp_matching'])
                    if rule['dscp_marking'] is not None:
                        cmd += " dscp-marking {}".format(rule['dscp_marking'])
                    elif rule['log']:
                        cmd += " log"
                else:
                    if rule['dscp_matching'] is not None:
                        cmd += " dscp-matching {}".format(rule['dscp_matching'])
                        if rule['dscp_marking'] is not None:
                            cmd += " dscp-marking {}".format(rule['dscp_marking'])
                        elif rule['log']:
                            cmd += " log"
                    elif rule['dscp_marking'] is not None:
                        cmd += " dscp-marking {}".format(rule['dscp_marking'])

                    elif rule['traffic_policy_name'] is not None:
                        cmd += " traffic-policy {}".format(rule['traffic_policy_name'])
                        if rule['log']:
                            cmd += " log"
                        elif rule['mirror']:
                            cmd += " mirror"
                    else:
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"

            elif rule['ip_protocol_name'] == "ipv6":
                if rule['destination']['host_ipv6_address'] is not None:
                    cmd += " host {}".format(rule['destination']['host_ipv6_address'])
                elif rule['destination']['ipv6_prefix_prefix_length'] is not None:
                    cmd += " {}".format(rule['destination']['ipv6_prefix_prefix_length'])
                elif rule['destination']['any']:
                    cmd += " any"
                if rule['fragments']:
                    cmd += " fragments"
                elif rule['routing']:
                    cmd += " routing"
                if rule['dscp_matching'] is not None:
                    cmd += " dscp-matching {}".format(rule['dscp_matching'])
                if rule['priority_matching'] is not None:
                    cmd += " 802.1p-priority-matching {}".format(rule['priority_matching'])
                if rule['dscp_marking'] is not None:
                    cmd += " dscp-marking {}".format(rule['dscp_marking'])
                    if rule['priority_marking'] is not None:
                        cmd += " 802.1p-priority-marking {}".format(rule['priority_marking'])
                        if rule['internal_priority_marking'] is not None:
                            cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                            if rule['log']:
                                cmd += " log"
                            if rule['mirror']:
                                cmd += " mirror"
                elif rule['priority_marking'] is not None:
                    cmd += " 802.1p-priority-marking {}".format(rule['priority_marking'])
                    if rule['internal_priority_marking'] is not None:
                        cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                elif rule['internal_priority_marking'] is not None:
                    if rule['fragments'] is False:
                        cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                elif rule['traffic_policy_name'] is not None:
                    cmd += " traffic-policy {}".format(rule['traffic_policy_name'])
                    if rule['log']:
                        cmd += " log"
                    elif rule['mirror']:
                        cmd += " mirror"
                else:
                    if rule['log']:
                        cmd += " log"
                    if rule['mirror']:
                        cmd += " mirror"

            elif (rule['ip_protocol_name'] == "tcp") or (rule['ip_protocol_name'] == "udp"):
                if rule['source_comparison_operators'] is not None:
                    if rule['source_comparison_operators']['operator'] is not None:
                        if rule['source_comparison_operators']['port_num'] is not None:
                            cmd += " {} {}".format(rule['source_comparison_operators']['operator'], rule['source_comparison_operators']['port_num'])
                        elif rule['source_comparison_operators']['port_name'] is not None:
                            if rule['ip_protocol_name'] == "udp":
                                if rule['source_comparison_operators']['port_name'] in ['dns', 'gppitnp', 'sftp', 'sqlserv', 'ldap', 'ssl', 'tftp', 'snmp']:
                                    cmd += " {} {}".format(rule['source_comparison_operators']['operator'], rule['source_comparison_operators']['port_name'])
                            elif rule['ip_protocol_name'] == "tcp":
                                if rule['source_comparison_operators']['port_name'] not in ['tftp', 'snmp']:
                                    cmd += " {} {}".format(rule['source_comparison_operators']['operator'], rule['source_comparison_operators']['port_name'])
                        if rule['source_comparison_operators']['operator'] == 'range':
                            if rule['source_comparison_operators']['high_port_num'] is not None:
                                cmd += " {}".format(rule['source_comparison_operators']['high_port_num'])
                            elif rule['source_comparison_operators']['high_port_name'] is not None:
                                if rule['ip_protocol_name'] == "udp":
                                    if rule['source_comparison_operators']['high_port_name'] in ['dns', 'gppitnp', 'sftp', 'sqlserv', 'ldap', 'ssl', 'tftp', 'snmp']:
                                        cmd += " {}".format(rule['source_comparison_operators']['high_port_name'])
                                elif rule['ip_protocol_name'] == "tcp":
                                    if rule['source_comparison_operators']['high_port_name'] not in ['tftp', 'snmp']:
                                        cmd += " {}".format(rule['source_comparison_operators']['high_port_name'])
                if rule['destination']['host_ipv6_address'] is not None:
                    cmd += " host {}".format(rule['destination']['host_ipv6_address'])
                elif rule['destination']['ipv6_prefix_prefix_length'] is not None:
                    cmd += " {}".format(rule['destination']['ipv6_prefix_prefix_length'])
                elif rule['destination']['any']:
                    cmd += " any"
                if rule['destination_comparison_operators'] is not None:
                    if rule['destination_comparison_operators']['operator'] is not None:
                        if rule['destination_comparison_operators']['port_num'] is not None:
                            cmd += " {} {}".format(rule['destination_comparison_operators']['operator'], rule['destination_comparison_operators']['port_num'])
                        elif rule['destination_comparison_operators']['port_name'] is not None:
                            if rule['ip_protocol_name'] == "udp":
                                if rule['destination_comparison_operators']['port_name'] in ['dns', 'gppitnp', 'sftp', 'sqlserv', 'ldap', 'ssl', 'tftp', 'snmp']:
                                    cmd += " {} {}".format(rule['destination_comparison_operators']['operator'], rule['destination_comparison_operators']['port_name'])
                            elif rule['ip_protocol_name'] == "tcp":
                                if rule['destination_comparison_operators']['port_name'] not in ['tftp', 'snmp']:
                                    cmd += " {} {}".format(rule['destination_comparison_operators']['operator'], rule['destination_comparison_operators']['port_name'])
                        if rule['destination_comparison_operators']['operator'] == 'range':
                            if rule['destination_comparison_operators']['high_port_num'] is not None:
                                cmd += " {}".format(rule['destination_comparison_operators']['high_port_num'])
                            elif rule['destination_comparison_operators']['high_port_name'] is not None:
                                if rule['ip_protocol_name'] == "udp":
                                    if rule['destination_comparison_operators']['high_port_name'] in ['dns', 'gppitnp', 'sftp', 'sqlserv', 'ldap', 'ssl', 'tftp', 'snmp']:
                                        cmd += " {}".format(rule['destination_comparison_operators']['high_port_name'])
                                elif rule['ip_protocol_name'] == "tcp":
                                    if rule['destination_comparison_operators']['high_port_name'] not in ['tftp', 'snmp']:
                                        cmd += " {}".format(rule['destination_comparison_operators']['high_port_name'])
                if rule['ip_protocol_name'] == "tcp":
                    if rule['established']:
                        cmd += " established"
                if rule['dscp_matching'] is not None:
                    cmd += " dscp-matching {}".format(rule['dscp_matching'])
                if rule['priority_matching'] is not None:
                    cmd += " 802.1p-priority-matching {}".format(rule['priority_matching'])
                    # fragments or routing option applicable only after 802.1p-priority-matching
                    if rule['fragments']:
                        cmd += " fragments"
                    elif rule['routing']:
                        cmd += " routing"
                if rule['dscp_marking'] is not None:
                    cmd += " dscp-marking {}".format(rule['dscp_marking'])
                    if rule['priority_marking'] is not None:
                        cmd += " 802.1p-priority-marking {}".format(rule['priority_marking'])
                        if rule['internal_priority_marking'] is not None:
                            cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                            if rule['log']:
                                cmd += " log"
                            if rule['mirror']:
                                cmd += " mirror"
                elif rule['priority_marking'] is not None:
                    cmd += " 802.1p-priority-marking {}".format(rule['priority_marking'])
                    if rule['internal_priority_marking'] is not None:
                        cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                elif rule['internal_priority_marking'] is not None:
                    if rule['fragments'] is False:
                        cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                elif rule['traffic_policy_name'] is not None:
                    cmd += " traffic-policy {}".format(rule['traffic_policy_name'])
                    if rule['log']:
                        cmd += " log"
                    elif rule['mirror']:
                        cmd += " mirror"
                else:
                    if rule['log']:
                        cmd += " log"
                    if rule['mirror']:
                        cmd += " mirror"

            else:
                if rule['destination']['host_ipv6_address'] is not None:
                    cmd += " host {}".format(rule['destination']['host_ipv6_address'])
                elif rule['destination']['ipv6_prefix_prefix_length'] is not None:
                    cmd += " {}".format(rule['destination']['ipv6_prefix_prefix_length'])
                elif rule['destination']['any']:
                    cmd += " any"
                if rule['dscp_matching'] is not None:
                    cmd += " dscp-matching {}".format(rule['dscp_matching'])
                if rule['priority_matching'] is not None:
                    cmd += " 802.1p-priority-matching {}".format(rule['priority_matching'])
                    if rule['fragments']:
                        cmd += " fragments"
                    elif rule['routing']:
                        cmd += " routing"
                if rule['dscp_marking'] is not None:
                    cmd += " dscp-marking {}".format(rule['dscp_marking'])
                    if rule['priority_marking'] is not None:
                        cmd += " 802.1p-priority-marking {}".format(rule['priority_marking'])
                        if rule['internal_priority_marking'] is not None:
                            cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                            if rule['log']:
                                cmd += " log"
                            if rule['mirror']:
                                cmd += " mirror"
                elif rule['priority_marking'] is not None:
                    cmd += " 802.1p-priority-marking {}".format(rule['priority_marking'])
                    if rule['internal_priority_marking'] is not None:
                        cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                elif rule['internal_priority_marking'] is not None:
                    if rule['fragments'] is False:
                        cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                elif rule['traffic_policy_name'] is not None:
                    cmd += " traffic-policy {}".format(rule['traffic_policy_name'])
                    if rule['log']:
                        cmd += " log"
                    elif rule['mirror']:
                        cmd += " mirror"
                else:
                    if rule['log']:
                        cmd += " log"
                    if rule['mirror']:
                        cmd += " mirror"

            rules_acl_cmds.append(cmd)

    cmds = acl_cmds + rules_acl_cmds
    return cmds


def main():

    """entry point for module execution
    """
    remark_spec = dict(
        comment_text=dict(type='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    source_spec = dict(
        host_ipv6_address=dict(type='str'),
        ipv6_prefix_prefix_length=dict(type='str'),
        any=dict(type='bool')
    )
    source_comparison_operators_spec = dict(
        operator=dict(type='str', choices=['eq', 'gt', 'lt', 'neq', 'range']),
        port_num=dict(type='int'),
        port_name=dict(type='str', choices=['ftp-data', 'ftp', 'ssh', 'telnet', 'smtp', 'dns', 'http', 'gppitnp', 'pop2', 'pop3', 'sftp', 'sqlserv', 'bgp', 'ldap', 'ssl', 'tftp', 'snmp']),
        high_port_num=dict(type='int'),
        high_port_name=dict(type='str', choices=['ftp-data', 'ftp', 'ssh', 'telnet', 'smtp', 'dns', 'http', 'gppitnp', 'pop2', 'pop3', 'sftp', 'sqlserv', 'bgp', 'ldap', 'ssl', 'tftp', 'snmp'])
    )
    destination_spec = dict(
        host_ipv6_address=dict(type='str'),
        ipv6_prefix_prefix_length=dict(type='str'),
        any=dict(type='bool')
    )
    destination_comparison_operators_spec = dict(
        operator=dict(type='str', choices=['eq', 'gt', 'lt', 'neq', 'range']),
        port_num=dict(type='int'),
        port_name=dict(type='str', choices=['ftp-data', 'ftp', 'ssh', 'telnet', 'smtp', 'dns', 'http', 'gppitnp', 'pop2', 'pop3', 'sftp', 'sqlserv', 'bgp', 'ldap', 'ssl', 'tftp', 'snmp']),
        high_port_num=dict(type='int'),
        high_port_name=dict(type='str', choices=['ftp-data', 'ftp', 'ssh', 'telnet', 'smtp', 'dns', 'http', 'gppitnp', 'pop2', 'pop3', 'sftp', 'sqlserv', 'bgp', 'ldap', 'ssl', 'tftp', 'snmp'])
    )
    rules_spec = dict(
        remark=dict(type='dict', options=remark_spec),
        seq_num=dict(type='int'),
        rule_type=dict(type='str', choices=['deny', 'permit'], required=True),
        ip_protocol_name=dict(type='str', choices=['ahp', 'esp', 'icmp', 'ipv6', 'sctp', 'tcp', 'udp']),
        ip_protocol_num=dict(type='int'),
        source=dict(type='dict', required=True, options=source_spec, required_one_of=[['host_ipv6_address', 'ipv6_prefix_prefix_length', 'any']], mutually_exclusive=[['host_ipv6_address', 'ipv6_prefix_prefix_length', 'any']]),
        source_comparison_operators=dict(type='dict', options=source_comparison_operators_spec),
        destination=dict(type='dict', required=True, options=destination_spec, required_one_of=[['host_ipv6_address', 'ipv6_prefix_prefix_length', 'any']], mutually_exclusive=[['host_ipv6_address', 'ipv6_prefix_prefix_length', 'any']]),
        established=dict(type='bool', default='no'),
        destination_comparison_operators=dict(type='dict', options=destination_comparison_operators_spec),
        icmp_num=dict(type='int'),
        icmp_type=dict(type='str', choices=['beyond-scope', 'destination-unreachable', 'echo-reply', 'echo-request', 'header', 'hop-limit', 'mld-query', 'mld-reduction', 'mld-report', 'nd-na', 'nd-ns', 'next-header', 'no-admin', 'no-route', 'packet-too-big', 'parameter-option', 'parameter-problem', 'port-unreachable', 'reassembly-timeout', 'renum-command', 'renum-result', 'renum-seq-number', 'router-advertisement', 'router-renumbering', 'router-solicitation', 'time-exceeded', 'unreachable']),
        fragments=dict(type='bool', default='no'),
        routing=dict(type='bool', default='no'),
        dscp_matching=dict(type='int'),
        dscp_marking=dict(type='int'),
        priority_matching=dict(type='int'),
        priority_marking=dict(type='int'),
        internal_priority_marking=dict(type='int'),
        traffic_policy_name=dict(type='str'),
        log=dict(type='bool', default='no'),
        mirror=dict(type='bool', default='no'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    required_one_of = [['ip_protocol_name', 'ip_protocol_num']]
    mutually_exclusive = [['ip_protocol_name', 'ip_protocol_num']]
    argument_spec = dict(
        acl_name=dict(type='str', required=True),
        accounting=dict(type='str', choices=['enable', 'disable']),
        rules=dict(type='list', elements='dict', options=rules_spec, required_one_of=required_one_of, mutually_exclusive=mutually_exclusive),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    warnings = list()
    results = {'changed': False}
    acl_name = module.params["acl_name"]
    accounting = module.params["accounting"]
    rules = module.params["rules"]
    state = module.params["state"]

    if warnings:
        results['warnings'] = warnings

    commands = build_command(module, acl_name, accounting, rules, state)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True
    module.exit_json(**results)


if __name__ == '__main__':
    main()
