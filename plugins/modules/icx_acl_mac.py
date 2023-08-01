#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_acl_mac
author: "Ruckus Wireless (@Commscope)"
short_description: Configures ACL in Ruckus ICX 7000 series switches.
description:
  - Configures ACL in Ruckus ICX 7000 series switches.
options:
  acl_name:
    description: Specifies a unique ACL name.
    type: str
    required: true
  accounting:
    description: Enables/Disables accounting for the ipv6 ACL.
    type: str
    choices: ['enable', 'disable']
  rule:
    description: Inserts filtering rules in mac access control list
    type: list
    elements: dict
    suboptions:
      rule_type:
        description: Inserts filtering rules in IPv4 standard named or numbered ACLs that will deny/permit packets.
        type: str
        required: true
        choices: ['deny', 'permit']
      source:
        description: source_mac_address | source_mask | any
        type: dict
        required: true
        suboptions:
          source_mac_address:
            description: HHHH.HHHH.HHHH Source Ethernet MAC address.
            type: str
          source_mask:
            description: HHHH.HHHH.HHHH Source mask
            type: str
          any:
            description: Matches any.
            type: bool
            default: no
      destination:
        description: destination_mac_address destination_mask | any
        type: dict
        required: true
        suboptions:
          destination_mac_address:
            description: HHHH.HHHH.HHHH Destination Ethernet MAC address.
            type: str
          destination_mask:
            description: HHHH.HHHH.HHHH Destination mask
            type: str
          any:
            description: Matches any.
            type: bool
            default: no
      log:
        description: Enables SNMP traps and syslog messages for the rule.
        type: bool
        default: no
      mirror:
        description: Mirrors packets matching the rule.
        type: bool
        default: no
      ether_type:
        description: Specifies whether to configure or remove rule.
        type: str
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
- name: create mac acl and add rules
  commscope.icx.icx_acl_mac:
    acl_name: mac123
    rule:
      - rule_type: permit
        source:
          source_mac_address: 1111.2222.3333
          source_mask: ffff.ffff.ffff
          any: yes
        destination:
          destination_mac_address: 4444.5555.6666
          destination_mask: ffff.ffff.ffff
          any: yes
      - rule_type: permit
        source:
          source_mac_address: 1111.2222.3333
          source_mask: ffff.ffff.ffff
          any: yes
        destination:
          destination_mac_address: 4444.5555.6666
          destination_mask: ffff.ffff.ffff
          any: yes
        state: absent
      - rule_type: permit
        source:
          source_mac_address: 1111.2222.3333
          source_mask: ffff.ffff.ffff
        destination:
          any: yes
        log: yes
        mirror: yes
        ether_type: 0800

- name: create only mac acl
  icx_acl_mac:
    acl_name: mac123
  register: output

- name: remove mac acl
  icx_acl_mac:
    acl_name: mac123
    state: absent
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(module, acl_name=None, accounting=None, rule=None, state=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """

    acl_cmds = []
    rule_acl_cmds = []
    if state == 'absent':
        cmd = "no mac access-list {0}".format(acl_name)
    else:
        cmd = "mac access-list {0}".format(acl_name)
    acl_cmds.append(cmd)
    if accounting == 'disable':
        cmd = "no enable accounting"
        acl_cmds.append(cmd)
    elif accounting == 'enable':
        cmd = "enable accounting"
        acl_cmds.append(cmd)

    if rule is not None:
        for elements in rule:
            if elements['state'] == 'absent':
                cmd = "no"
                if elements['rule_type'] is not None:
                    cmd += " {0}".format(elements['rule_type'])
            else:
                if elements['rule_type'] is not None:
                    cmd = "{0}".format(elements['rule_type'])

            if elements['source']['source_mac_address'] is not None:
                cmd += " {0}".format(elements['source']['source_mac_address'])
                if elements['source']['source_mask'] is not None:
                    cmd += " {0}".format(elements['source']['source_mask'])
            elif elements['source']['any'] is not None:
                cmd += " any"
            if elements['destination']['destination_mac_address'] is not None:
                cmd += " {0}".format(elements['destination']['destination_mac_address'])
                if elements['destination']['destination_mask'] is not None:
                    cmd += " {0}".format(elements['destination']['destination_mask'])
            elif elements['destination']['any'] is not None:
                cmd += " any"
            if elements['ether_type']:
                cmd += " ether-type {0}".format(elements['ether_type'])
            if elements['log']:
                cmd += " log"
            if elements['mirror']:
                cmd += " mirror"
            rule_acl_cmds.append(cmd)
    cmds = acl_cmds + rule_acl_cmds
    return cmds


def main():
    """ main entry point for module execution
    """

    source_spec = dict(
        source_mac_address=dict(type='str'),
        source_mask=dict(type='str'),
        any=dict(type='bool', default='no')
    )

    destination_spec = dict(
        destination_mac_address=dict(type='str'),
        destination_mask=dict(type='str'),
        any=dict(type='bool', default='no')
    )

    rule_spec = dict(
        rule_type=dict(type='str', choices=['deny', 'permit'], required=True),
        source=dict(type='dict', options=source_spec, required=True),
        destination=dict(type='dict', options=destination_spec, required=True),
        log=dict(type='bool', default='no'),
        mirror=dict(type='bool', default='no'),
        ether_type=dict(type='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    argument_spec = dict(
        acl_name=dict(type='str', required=True),
        accounting=dict(type='str', choices=['enable', 'disable']),
        rule=dict(type='list', elements='dict', options=rule_spec),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    required_one_of = [['acl_name', 'rule', 'state']]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=required_one_of)

    warnings = list()
    results = {'changed': False}
    acl_name = module.params["acl_name"]
    accounting = module.params["accounting"]
    rule = module.params["rule"]
    state = module.params["state"]

    if warnings:
        results['warnings'] = warnings

    commands = build_command(module, acl_name, accounting, rule, state)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
