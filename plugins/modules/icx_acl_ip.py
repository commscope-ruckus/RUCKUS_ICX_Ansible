#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_acl_ip
author: "Ruckus Wireless (@Commscope)"
short_description: Configures ACL in Ruckus ICX 7000 series switches.
description:
  - Configures ACL in Ruckus ICX 7000 series switches.
notes:
  - Tested against ICX 10.1
options:
  acl_type:
    description: Specifies standard/extended access control list.
      Standard - Contains rules that permit or deny traffic based on source addresses that you specify.
                 The rules are applicable to all ports of the specified address.
      Extended - Contains rules that permit or deny traffic according to source and destination addresses, as well as other parameters.
                 For example, you can also filter by port, protocol (TCP or UDP), and TCP flags.
    type: str
    required: true
    choices: ['standard','extended']
  acl_name:
    description: Specifies a unique ACL name.
    type: str
  acl_id:
    description: Specifies a unique ACL number.
    type: int
  accounting:
    description: Enables/Disables accounting for the ipv6 ACL.
    type: str
    choices: ['enable', 'disable']
  standard_rules:
    description: Inserts filtering rules in standard named or numbered ACLs that will deny or permit packets.
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
      host:
        description: Specifies the source as host.
        type: bool
      source_ip:
        description: Specifies a source address for which you want to filter the subnet.
          Format - IPv4address/mask | IPv4 address | IPv6 address | ipv6-source-prefix/prefix-length
        type: str
      mask:
        description: Defines a mask, whose effect is to specify a subnet that includes the source address that you specified.
        type: str
      hostname:
        description: Specifies the known hostname of the source host
        type: str
      any:
        description: Specifies all source addresses.
        type: bool
      log:
        description: Enables logging for the rule. Used in conjunction with the logging enable command at the ip access-list command configuration level.
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
  extended_rules:
    description: Inserts filtering rules in extended named or numbered ACLs. Specify either protocol name or number.
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
        description: Specifies the type of IPv4 packet to filter.
        type: str
        choices: ['icmp','igmp','ip','ospf','tcp','udp','esp','gre','ipv6','pim','rsvp']
      ip_protocol_num:
        description: Protocol number (from 0 to 255).
        type: int
      source:
        description: host hostname or A.B.C.D | A.B.C.D or A.B.C.D/L | any.
        type: dict
        required: true
        suboptions:
          host:
            description: Specifies the source as host.
            type: bool
          ip_address:
            description: Specifies a source IPv4 address for which you want to filter the subnet.
            type: str
          mask:
            description: Defines a mask, whose effect is to specify a subnet that includes the source address that you specified.
            type: str
          hostname:
            description: Specifies the known hostname of the source host
            type: str
          any:
            description: Specifies all source addresses.
            type: bool
      destination:
        description: host hostname or A.B.C.D | A.B.C.D or A.B.C.D/L | any
        type: dict
        required: true
        suboptions:
          host:
            description: Specifies the destination as host.
            type: bool
          ip_address:
            description: Specifies a destination address for which you want to filter the subnet.
              Format - IPv4address/mask | IPv4 address | IPv6 address | ipv6-source-prefix/prefix-length
            type: str
          mask:
            description: Defines a subnet mask that includes the destination address that you specified.
            type: str
          hostname:
            description: Specifies the known hostname of the destination host.
            type: str
          any:
            description: Specifies all destination addresses.
            type: bool
      source_comparison_operators:
        description: If you specified tcp or udp, the following optional operators are available. Specify either port number or name for the operation.
        type: dict
        suboptions:
          operator:
            description: Specifies comparison operator
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
        description: Specifies a numbered message type. Use this format if the rule also needs to include precedence, tos , one of the
            DSCP options, one of the 802.1p options, internal-priority-marking , or traffic-policy.
        type: int
      icmp_type:
        description: Specifies icmp type.
        type: str
        choices: ['any-icmp-type','echo','echo-reply','information-request','mask-reply','mask-request','parameter-problem','redirect',
                  'source-quench','time-exceeded','timestamp-reply','timestamp-request','unreachable']
      precedence:
        description: Specifies a precedence-name.
          0 or routine - Specifies routine precedence.
          1 or priority - Specifies priority precedence.
          2 or immediate - Specifies immediate precedence.
          3 or flash - Specifies flash precedence.
          4 or flash-override - Specifies flash-override precedence.
          5 or critical - Specifies critical precedence.
          6 or internet - Specifies internetwork control precedence.
          7 or network - Specifies network control precedence.
        type: str
        choices: ['routine','priority','immediate','flash','flash-override','critical','internet','network']
      tos:
        description: Specifies a type of service (ToS). Enter either a supported tos-name or the equivalent tos-value.
          0 or normal - Specifies normal ToS.
          1 or min-monetary-cost - Specifies min monetary cost ToS.
          2 or max-reliability - Specifies max reliability ToS.
          4 or max-throughput - Specifies max throughput ToS.
          8 or min-delay - Specifies min-delay ToS.
        type: str
        choices: ['normal','min-monetary-cost','max-reliability','max-throughput','min-delay']
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
        description: Assigns the internal queuing priority (traffic class) that you specify to the packet. Values range from 0 through 7.
        type: int
      internal_marking:
        description: Assigns the identical 802.1p value and internal queuing priority (traffic class) that you specify to the packet [0-7]
        type: int
      traffic_policy_name:
        description: Enables the device to limit rate of inbound traffic and to count packets and bytes per packet to which ACL deny clauses are applied.
        type: str
      log:
        type: bool
        default: no
        description: Enables SNMP traps and Syslog messages for the rule. In addition, logging must be enabled using the logging enable command.
      mirror:
        type: bool
        default: no
        description: Mirrors packets matching the rule.
      state:
        description: Specifies whether to configure or remove rule.
        type: str
        default: present
        choices: ['present', 'absent']
  state:
    description: Specifies whether to create or delete ACL.
    type: str
    default: present
    choices: ['present', 'absent']
"""
EXAMPLES = """
- name: create ipv4 acl and add rules
  community.network.icx_acl_ip:
    acl_type: standard
    acl_name: acl1
    standard_rules:
      - rule_type: permit
        seq_num: 10
        any: yes
        log: yes
- name: create ipv4 acl and add rules
  community.network.icx_acl_ip:
    acl_type: extended
    acl_id: 112
    extended_rules:
      - rule_type: deny
        ip_protocol_name: tcp
        source:
          host: yes
          ip_address: 1.1.1.1
        destination:
          any: yes
        precedence: routine
        state: absent
- name: remove ipv4 acl
  community.network.icx_acl_ip:
    acl_type: standard
    acl_name: acl1
    state: absent
"""

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(module, acl_type=None, acl_name=None, acl_id=None, accounting=None, standard_rules=None, extended_rules=None, state=None):

    acl_cmds = []
    if state == 'absent':
        cmd = "no ip access-list {}".format(acl_type)
    else:
        cmd = "ip access-list {}".format(acl_type)
    if acl_name is not None:
        cmd += " {}".format(acl_name)
    else:
        cmd += " {}".format(acl_id)
    acl_cmds.append(cmd)

    if accounting == 'disable':
        cmd = "no enable accounting"
        acl_cmds.append(cmd)
    elif accounting == 'enable':
        cmd = "enable accounting"
        acl_cmds.append(cmd)

    extended_rule_cmds = []
    standard_rule_cmds = []

    if acl_type == 'standard':
        if standard_rules is not None:
            for rule in standard_rules:
                if rule['remark'] is not None:
                    if rule['remark']['state'] == 'absent':
                        cmd = "no remark {}".format(rule['remark']['comment_text'])
                    else:
                        cmd = "remark {}".format(rule['remark']['comment_text'])
                    standard_rule_cmds.append(cmd)
                cmd = ""
                if rule['state'] == 'absent':
                    cmd += "no "
                if rule['seq_num'] is not None:
                    cmd += "sequence {} ".format(rule['seq_num'])
                if rule['rule_type'] is not None:
                    cmd += "{}".format(rule['rule_type'])

                if rule['host']:
                    if rule['hostname'] is not None:
                        cmd += " host {}".format(rule['hostname'])
                    else:
                        cmd += " host {}".format(rule['source_ip'])
                elif rule['any']:
                    cmd += " any"
                elif rule['hostname'] is not None:
                    cmd += " {}".format(rule['hostname'])
                    if rule['mask'] is not None:
                        cmd += " {}".format(rule['mask'])
                else:
                    cmd += " {}".format(rule['source_ip'])
                    if rule['mask'] is not None:
                        cmd += " {}".format(rule['mask'])

                if rule['log']:
                    cmd += " log"
                if rule['mirror']:
                    cmd += " mirror"
                standard_rule_cmds.append(cmd)

    elif acl_type == 'extended':
        if extended_rules is not None:
            for rule in extended_rules:
                if rule['remark'] is not None:
                    if rule['remark']['state'] == 'absent':
                        cmd = "no remark {}".format(rule['remark']['comment_text'])
                    else:
                        cmd = "remark {}".format(rule['remark']['comment_text'])
                    extended_rule_cmds.append(cmd)
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
                if rule['source']['host']:
                    if rule['source']['hostname'] is not None:
                        cmd += " host {}".format(rule['source']['hostname'])
                    elif rule['source']['ip_address'] is not None:
                        cmd += " host {}".format(rule['source']['ip_address'])
                elif rule['source']['any']:
                    cmd += " any"
                else:
                    if rule['source']['ip_address'] is not None:
                        cmd += " {}".format(rule['source']['ip_address'])
                        if rule['source']['mask'] is not None:
                            cmd += " {}".format(rule['source']['mask'])
                if (rule['ip_protocol_name'] == "tcp") or (rule['ip_protocol_name'] == "udp"):
                    if rule['source_comparison_operators'] is not None:
                        if rule['source_comparison_operators']['operator'] is not None:
                            cmd += " {}".format(rule['source_comparison_operators']['operator'])
                            if rule['source_comparison_operators']['port_num'] is not None:
                                cmd += " {}".format(rule['source_comparison_operators']['port_num'])
                            elif rule['source_comparison_operators']['port_name'] is not None:
                                if rule['ip_protocol_name'] == "udp":
                                    if rule['source_comparison_operators']['port_name'] in ['dns', 'gppitnp', 'sftp', 'sqlserv', 'ldap', 'ssl', 'tftp', 'snmp']:
                                        cmd += " {}".format(rule['source_comparison_operators']['port_name'])
                                elif rule['ip_protocol_name'] == "tcp":
                                    if rule['source_comparison_operators']['port_name'] not in ['tftp', 'snmp']:
                                        cmd += " {}".format(rule['source_comparison_operators']['port_name'])
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

                if rule['destination']['host']:
                    if rule['destination']['hostname'] is not None:
                        cmd += " host {}".format(rule['destination']['hostname'])
                    elif rule['destination']['ip_address'] is not None:
                        cmd += " host {}".format(rule['destination']['ip_address'])
                elif rule['destination']['any']:
                    cmd += " any"
                else:
                    if rule['destination']['ip_address'] is not None:
                        cmd += " {}".format(rule['destination']['ip_address'])
                        if rule['destination']['mask'] is not None:
                            cmd += " {}".format(rule['destination']['mask'])
                if rule['ip_protocol_name'] == "icmp":
                    if rule['icmp_num'] is not None:
                        cmd += " {}".format(rule['icmp_num'])
                    elif rule['icmp_type'] is not None:
                        cmd += " {}".format(rule['icmp_type'])
                if (rule['ip_protocol_name'] == "tcp") or (rule['ip_protocol_name'] == "udp"):
                    if rule['destination_comparison_operators'] is not None:
                        if rule['destination_comparison_operators']['operator'] is not None:
                            cmd += " {}".format(rule['destination_comparison_operators']['operator'])
                            if rule['destination_comparison_operators']['port_num'] is not None:
                                cmd += " {}".format(rule['destination_comparison_operators']['port_num'])
                            elif rule['destination_comparison_operators']['port_name'] is not None:
                                if rule['ip_protocol_name'] == "udp":
                                    if rule['destination_comparison_operators']['port_name'] in ['dns', 'gppitnp', 'sftp', 'sqlserv', 'ldap', 'ssl', 'tftp', 'snmp']:
                                        cmd += " {}".format(rule['destination_comparison_operators']['port_name'])
                                elif rule['ip_protocol_name'] == "tcp":
                                    if rule['destination_comparison_operators']['port_name'] not in ['tftp', 'snmp']:
                                        cmd += " {}".format(rule['destination_comparison_operators']['port_name'])
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
                if rule['precedence'] is not None:
                    cmd += " precedence {}".format(rule['precedence'])
                if rule['tos'] is not None:
                    cmd += " tos {}".format(rule['tos'])
                if rule['dscp_matching'] is not None:
                    cmd += " dscp-matching {}".format(rule['dscp_matching'])
                if rule['priority_matching'] is not None:
                    cmd += " 802.1p-priority-matching {}".format(rule['priority_matching'])
                if rule['dscp_marking'] is not None:
                    cmd += " dscp-marking {}".format(rule['dscp_marking'])
                    # log and mirror are not applicable for dscp marking
                    if rule['internal_marking'] is not None:
                        cmd += " 802.1p-and-internal-marking {}".format(rule['internal_marking'])
                    # command ends with 802.1p-and-internal-marking
                    elif rule['priority_marking'] is not None:
                        cmd += " 802.1p-priority-marking {}".format(rule['priority_marking'])
                        if rule['internal_priority_marking'] is not None:
                            cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                            if rule['log']:
                                cmd += " log"
                            if rule['mirror']:
                                cmd += " mirror"
                    elif rule['internal_priority_marking'] is not None:
                        cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                    elif rule['traffic_policy_name'] is not None:
                        cmd += " traffic-policy {}".format(rule['traffic_policy_name'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                else:
                    if rule['internal_marking'] is not None:
                        if (rule['dscp_matching'] is None) and (rule['priority_matching'] is None):
                            cmd += " 802.1p-and-internal-marking {}".format(rule['internal_marking'])
                    elif rule['priority_marking'] is not None:
                        cmd += " 802.1p-priority-marking {}".format(rule['priority_marking'])
                        if rule['internal_priority_marking'] is not None:
                            cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                            if rule['log']:
                                cmd += " log"
                            if rule['mirror']:
                                cmd += " mirror"
                    elif rule['internal_priority_marking'] is not None:
                        cmd += " internal-priority-marking {}".format(rule['internal_priority_marking'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                    elif rule['traffic_policy_name'] is not None:
                        cmd += " traffic-policy {}".format(rule['traffic_policy_name'])
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"
                    else:
                        if rule['log']:
                            cmd += " log"
                        if rule['mirror']:
                            cmd += " mirror"

                extended_rule_cmds.append(cmd)

    cmds = acl_cmds + standard_rule_cmds + extended_rule_cmds

    return cmds


def main():
    """entry point for module execution
    """
    remark_spec = dict(
        comment_text=dict(type='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    source_spec = dict(
        host=dict(type='bool'),
        ip_address=dict(type='str'),
        mask=dict(type='str'),
        hostname=dict(type='str'),
        any=dict(type='bool')
    )
    destination_spec = dict(
        host=dict(type='bool'),
        ip_address=dict(type='str'),
        mask=dict(type='str'),
        hostname=dict(type='str'),
        any=dict(type='bool')
    )
    source_comparison_operators_spec = dict(
        operator=dict(type='str', choices=['eq', 'gt', 'lt', 'neq', 'range']),
        port_num=dict(type='int'),
        port_name=dict(type='str', choices=['ftp-data', 'ftp', 'ssh', 'telnet', 'smtp', 'dns', 'http', 'gppitnp', 'pop2', 'pop3', 'sftp', 'sqlserv', 'bgp', 'ldap', 'ssl', 'tftp', 'snmp']),
        high_port_num=dict(type='int'),
        high_port_name=dict(type='str', choices=['ftp-data', 'ftp', 'ssh', 'telnet', 'smtp', 'dns', 'http', 'gppitnp', 'pop2', 'pop3', 'sftp', 'sqlserv', 'bgp', 'ldap', 'ssl', 'tftp', 'snmp'])
    )
    destination_comparison_operators_spec = dict(
        operator=dict(type='str', choices=['eq', 'gt', 'lt', 'neq', 'range']),
        port_num=dict(type='int'),
        port_name=dict(type='str', choices=['ftp-data', 'ftp', 'ssh', 'telnet', 'smtp', 'dns', 'http', 'gppitnp', 'pop2', 'pop3', 'sftp', 'sqlserv', 'bgp', 'ldap', 'ssl', 'tftp', 'snmp']),
        high_port_num=dict(type='int'),
        high_port_name=dict(type='str', choices=['ftp-data', 'ftp', 'ssh', 'telnet', 'smtp', 'dns', 'http', 'gppitnp', 'pop2', 'pop3', 'sftp', 'sqlserv', 'bgp', 'ldap', 'ssl', 'tftp', 'snmp'])
    )
    standard_rules_spec = dict(
        remark=dict(type='dict', options=remark_spec),
        seq_num=dict(type='int'),
        rule_type=dict(type='str', required=True, choices=['deny', 'permit']),
        host=dict(type='bool'),
        source_ip=dict(type='str'),
        mask=dict(type='str'),
        hostname=dict(type='str'),
        any=dict(type='bool'),
        log=dict(type='bool', default='no'),
        mirror=dict(type='bool', default='no'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    extended_rules_spec = dict(
        remark=dict(type='dict', options=remark_spec),
        seq_num=dict(type='int'),
        rule_type=dict(type='str', required=True, choices=['deny', 'permit']),
        ip_protocol_name=dict(type='str', choices=['icmp', 'igmp', 'ip', 'ospf', 'tcp', 'udp', 'esp', 'gre', 'ipv6', 'pim', 'rsvp']),
        ip_protocol_num=dict(type='int'),
        source=dict(type='dict', required=True, options=source_spec, required_one_of=[['host', 'ip_address', 'any']], required_if=[('host', True, ('ip_address', 'hostname'), True)]),
        destination=dict(type='dict', required=True, options=destination_spec, required_one_of=[['host', 'ip_address', 'any']], required_if=[('host', True, ('ip_address', 'hostname'), True)]),
        source_comparison_operators=dict(type='dict', options=source_comparison_operators_spec),
        destination_comparison_operators=dict(type='dict', options=destination_comparison_operators_spec),
        established=dict(type='bool', default='no'),
        icmp_num=dict(type='int'),
        icmp_type=dict(type='str', choices=['any-icmp-type', 'echo', 'echo-reply', 'information-request', 'mask-reply', 'mask-request', 'parameter-problem', 'redirect', 'source-quench', 'time-exceeded', 'timestamp-reply', 'timestamp-request', 'unreachable']),
        precedence=dict(type='str', choices=['routine', 'priority', 'immediate', 'flash', 'flash-override', 'critical', 'internet', 'network']),
        tos=dict(type='str', choices=['normal', 'min-monetary-cost', 'max-reliability', 'max-throughput', 'min-delay']),
        dscp_matching=dict(type='int'),
        dscp_marking=dict(type='int'),
        priority_matching=dict(type='int'),
        priority_marking=dict(type='int'),
        internal_priority_marking=dict(type='int'),
        internal_marking=dict(type='int'),
        traffic_policy_name=dict(type='str'),
        log=dict(type='bool', default='no'),
        mirror=dict(type='bool', default='no'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    required_one_of = [['hostname', 'source_ip', 'any', 'host']]
    mutually_exclusive = [['ip_protocol_name', 'ip_protocol_num']]
    argument_spec = dict(
        acl_type=dict(type='str', required=True, choices=['standard', 'extended']),
        acl_name=dict(type='str'),
        acl_id=dict(type='int'),
        accounting=dict(type='str', choices=['enable', 'disable']),
        standard_rules=dict(type='list', elements='dict', options=standard_rules_spec, required_one_of=required_one_of, required_if=[('host', True, ('source_ip', 'hostname'), True)]),
        extended_rules=dict(type='list', elements='dict', options=extended_rules_spec, required_one_of=[['ip_protocol_name', 'ip_protocol_num']], mutually_exclusive=mutually_exclusive),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    required_one_of = [['acl_name', 'acl_id']]
    mutually_exclusive = [['acl_name', 'acl_id']]
    module = AnsibleModule(argument_spec=argument_spec,
                           required_one_of=required_one_of,
                           mutually_exclusive=mutually_exclusive,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    acl_type = module.params["acl_type"]
    acl_name = module.params["acl_name"]
    acl_id = module.params["acl_id"]
    accounting = module.params["accounting"]
    standard_rules = module.params.get("standard_rules")
    extended_rules = module.params.get("extended_rules")
    state = module.params["state"]

    if warnings:
        results['warnings'] = warnings
    commands = build_command(module, acl_type, acl_name, acl_id, accounting, standard_rules, extended_rules, state)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
