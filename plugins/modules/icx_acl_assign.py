#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_acl_assign
author: "Ruckus Wireless (@Commscope)"
short_description: Configures ACL in Ruckus ICX 7000 series switches.
description:
  - Configures ACL Assign in Ruckus ICX 7000 series switches.
options:
  ip_access_group:
    description: Applies IPv4 access control lists (ACLs) to traffic entering or exiting an interface.
      Specify acl_name/acl_num. Specify ethernet/lag/vlan
    type: dict
    suboptions:
      acl_num:
        description: Specifies an ACL number. You can specify from 1 through 99 for standard ACLs and from 100 through 199 for extended ACLs.
                     Valid only in 8090.
        type: int
      acl_name:
        description: Specifies a valid ACL name.
        type: str
      in_out:
        description: Applies the ACL to inbound or outbound traffic on the port.
        type: str
        choices: ['in','out']
      ethernet:
        description: Applies ACL to ethernet interface. Format - 1/1/1
        type: str
      lag:
        description: Applies ACL to lag interface.
        type: int
      vlan:
        description: Applies ACL to vlan through virtual routing interface.
        type: dict
        suboptions:
          vlan_num:
            description: Router interface ve
            type: int
          interfaces:
            description: Applies ACL to single/range of ethernet and lag interfaces of the vlan.
                         For eg - [ethernet 1/1/2, ethernet 1/1/20 to 1/1/30, lag 10, lag 10 to 20]
            type: list
            elements: str
      mirror_port:
        description: Configures ACL-based inbound mirroring.
        type: dict
        suboptions:
          ethernet:
            description: Specifies the mirror port to which the monitored port traffic is copied.
            type: str
          state:
            description: Configures/Removes the ACL mirror port.
            type: str
            default: present
            choices: ['present', 'absent']
      logging:
        description: Enables/Disables logging for matched statements in the ACL that also include a log action.
        type: str
        choices: ['enable','disable']
      frag_deny:
        description: Denies all IP fragments on the port.
        type: bool
        default: no
      state:
        description: Specifies whether to configure or remove ip access-group.
        type: str
        default: present
        choices: ['present', 'absent']
  ipv6_access_group:
    description: Applies an IPv6 ACL to an interface. Added in 8095.
      Specify acl_name/acl_num. Specify ethernet/lag/vlan
    type: dict
    suboptions:
      acl_name:
        description: Specifies a valid ACL name.
        type: str
      in_out:
        description: Applies the ACL to inbound or outbound traffic on the port.
        type: str
        choices: ['in','out']
      ethernet:
        description: Applies ACL to ethernet interface. Format-1/1/1
        type: str
      lag:
        description: Applies ACL to lag interface.
        type: int
      vlan:
        description: Applies ACL to vlan through virtual routing interface.
        type: dict
        suboptions:
          vlan_num:
            description: Router interface ve
            type: int
          interfaces:
            description: Applies ACL to single/range of ethernet and lag interfaces of the vlan.
                         For eg - [ethernet 1/1/2, ethernet 1/1/20 to 1/1/30, lag 10, lag 10 to 20]
            type: list
            elements: str
      mirror_port:
        description: Configures ACL-based inbound mirroring.
        type: dict
        suboptions:
          ethernet:
            description: Specifies the mirror port to which the monitored port traffic is copied.
            type: str
          state:
            description: Configures/Removes the ACL mirror port.
            type: str
            default: present
            choices: ['present', 'absent']
      logging:
        description: Enables/Disables logging for matched statements in the ACL that also include a log action.
        type: str
        choices: ['enable','disable']
      state:
        description: Specifies whether to configure or remove ip access-group.
        type: str
        default: present
        choices: ['present', 'absent']
  mac_access_group:
    description: Binds an access-list filter to an interface. Added in 8095.Specify ethernet/lag/vlan
    type: dict
    suboptions:
      mac_acl_name:
        description: MAC ACL name.
        type: str
        required: true
      ethernet:
        description: Applies ACL to ethernet interface. Format- 1/1/1
        type: str
      lag:
        description: Applies ACL to lag interface.
        type: int
      vlan:
        description: Applies ACL to vlan through virtual routing interface.
        type: dict
        suboptions:
          vlan_num:
            description: Router interface ve
            type: int
          interfaces:
            description: Applies ACL to single/range of ethernet and lag interfaces of the vlan.
                         For eg-[ethernet 1/1/2, ethernet 1/1/20 to 1/1/30, lag 10, lag 10 to 20]
            type: list
            elements: str
      mirror_port:
        description: Configures ACL-based inbound mirroring.
        type: dict
        suboptions:
          ethernet:
            description: Specifies the mirror port to which the monitored port traffic is copied.
            type: str
          state:
            description: Configures/Removes the ACL mirror port.
            type: str
            default: present
            choices: ['present', 'absent']
      logging:
        description: Enables/Disables logging for matched statements in the ACL that also include a log action.
        type: str
        choices: ['enable','disable']
      state:
        description: Specifies whether to configure or remove MAC access-group.
        type: str
        default: present
        choices: ['present', 'absent']
  default_acl:
    description: Configures the default ACL for failed, timed-out, or guest user sessions.
    type: dict
    suboptions:
      ip_type:
        description: Specifies an IPv4 or IPv6 ACL.
        type: str
        required: true
        choices: ['ipv4','ipv6']
      acl_name:
        description: Name or extended name of the ACL.
        type: str
      acl_id:
        description: ID of standard or numbered ACL (IPv4 only).
        type: int
      in_out:
        description: Specifies incoming or outgoing authentication.
        type: str
        choices: ['in','out']
      state:
        description: Specifies whether to configure or remove rule.
        type: str
        default: present
        choices: ['present', 'absent']
"""
EXAMPLES = """
- name: ipv4,ipv6,MAC ACLs assign to same ethernet interface
  community.network.icx_acl_assign:
    ip_access_group:
      acl_name: scale12
      in_out: in
      ethernet: 1/1/3
    ipv6_access_group:
      acl_name: scale12
      in_out: in
      ethernet: 1/1/3
      logging: enable
    mac_access_group:
      mac_acl_name: mac_acl
      ethernet: 1/1/3
  register: output

- name: ipv4,ipv6,MAC ACLs assign to same lag interface
  community.network.icx_acl_assign:
    ip_access_group:
      acl_name: scale12
      in_out: in
      lag: 3
    ipv6_access_group:
      acl_name: scale12
      in_out: in
      lag: 3
      logging: enable
    mac_access_group:
      mac_acl_name: mac_acl
      lag: 3
      logging: disable
  register: output

- name: ipv4,ipv6,MAC ACLs assign to vlan interfaces
  community.network.icx_acl_assign:
    ip_access_group:
      acl_name: scale12
      in_out: in
      vlan:
        vlan_num: 10
    ipv6_access_group:
      acl_name: scale12
      in_out: in
      vlan:
        vlan_num: 2066
      logging: enable
    mac_access_group:
      mac_acl_name: mac_acl
      vlan:
        vlan_num: 20
  register: output

- name: Each acl assigned to same vlan, but different ethernet and lag of the vlan
  community.network.icx_acl_assign:
    ip_access_group:
      acl_name: scale12
      in_out: in
      vlan:
        vlan_num: 555
        interfaces:
          - lag 10
    ipv6_access_group:
      acl_name: scale12
      in_out: in
      vlan:
        vlan_num: 555
        interfaces:
          - ethernet 1/1/3
      logging: enable
    mac_access_group:
      mac_acl_name: mac_acl
      vlan:
        vlan_num: 555
        interfaces:
          - ethernet 1/1/15 to 1/1/16
    default_acl:
      ip_type: ipv4
      acl_id: 10
      in_out: in
  register: output

- name: show command
  debug:
    msg: '{{ output }}'

"""
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(
        module, ip_access_group=None, ipv6_access_group=None,
        mac_access_group=None, default_acl=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """
    cmds = []
    if ip_access_group is not None:
        if ip_access_group['ethernet'] is not None:
            cmd = "interface ethernet {0}".format(ip_access_group['ethernet'])
            cmds.append(cmd)
            if ip_access_group['mirror_port'] is not None:
                if ip_access_group['mirror_port']['state'] == 'absent':
                    cmd = "no acl-mirror-port ethernet {0}".format(ip_access_group['mirror_port']['ethernet'])
                else:
                    cmd = "acl-mirror-port ethernet {0}".format(ip_access_group['mirror_port']['ethernet'])
                cmds.append(cmd)

        elif ip_access_group['lag'] is not None:
            cmd = "interface lag {0}".format(ip_access_group['lag'])
            cmds.append(cmd)

        elif ip_access_group['vlan'] is not None:
            if ip_access_group['vlan']['vlan_num'] is not None:
                cmd = "vlan {0}".format(ip_access_group['vlan']['vlan_num'])
            cmds.append(cmd)

        if ip_access_group['state'] == 'absent':
            cmd = "no ip access-group"
        else:
            cmd = "ip access-group"

        if ip_access_group['frag_deny']:
            cmd += " frag deny"

        elif ip_access_group['acl_num'] is not None:
            cmd += " {0} {1}".format(ip_access_group['acl_num'], ip_access_group['in_out'])
            if ip_access_group['in_out'] == 'in':
                if ip_access_group['vlan'] is not None:
                    if ip_access_group['vlan']['interfaces'] is not None:
                        for elements in ip_access_group['vlan']['interfaces']:
                            cmd += " {0}".format(elements)

            if ip_access_group['logging'] is not None:
                cmd += ' logging {0}'.format(ip_access_group['logging'])

        else:
            cmd += " {0} {1}".format(ip_access_group['acl_name'], ip_access_group['in_out'])
            if ip_access_group['in_out'] == 'in':
                if ip_access_group['vlan'] is not None:
                    if ip_access_group['vlan']['interfaces'] is not None:
                        for elements in ip_access_group['vlan']['interfaces']:
                            cmd += " {0}".format(elements)

            if ip_access_group['logging'] is not None:
                cmd += ' logging {0}'.format(ip_access_group['logging'])
        cmds.append(cmd)
        cmds.append('exit')

    if ipv6_access_group is not None:
        if ipv6_access_group['ethernet'] is not None:
            cmd = "interface ethernet {0}".format(ipv6_access_group['ethernet'])
            cmds.append(cmd)
            if ipv6_access_group['mirror_port'] is not None:
                if ipv6_access_group['mirror_port']['state'] == 'absent':
                    cmd = "no acl-mirror-port ethernet {0}".format(ipv6_access_group['mirror_port']['ethernet'])
                else:
                    cmd = "acl-mirror-port ethernet {0}".format(ipv6_access_group['mirror_port']['ethernet'])
                cmds.append(cmd)

        elif ipv6_access_group['lag'] is not None:
            cmd = "interface lag {0}".format(ipv6_access_group['lag'])
            cmds.append(cmd)

        elif ipv6_access_group['vlan'] is not None:
            if ipv6_access_group['vlan']['vlan_num'] is not None:
                cmd = "vlan {0}".format(ipv6_access_group['vlan']['vlan_num'])
            cmds.append(cmd)

        if ipv6_access_group['state'] == 'absent':
            cmd = "no ipv6 access-group"
        else:
            cmd = "ipv6 access-group"
        if ipv6_access_group['acl_name'] is not None:
            cmd += " {0} {1}".format(ipv6_access_group['acl_name'], ipv6_access_group['in_out'])

            if ipv6_access_group['in_out'] == 'in':
                if ipv6_access_group['vlan'] is not None:
                    if ipv6_access_group['vlan']['interfaces'] is not None:
                        for elements in ipv6_access_group['vlan']['interfaces']:
                            cmd += " {0}".format(elements)

            if ipv6_access_group['logging'] is not None:
                cmd += ' logging {0}'.format(ipv6_access_group['logging'])
        cmds.append(cmd)
        cmds.append('exit')

    if mac_access_group is not None:
        if mac_access_group['ethernet'] is not None:
            cmd = "interface ethernet {0}".format(mac_access_group['ethernet'])
            cmds.append(cmd)
            if mac_access_group['mirror_port'] is not None:
                if mac_access_group['mirror_port']['state'] == 'absent':
                    cmd = "no acl-mirror-port ethernet {0}".format(mac_access_group['mirror_port']['ethernet'])
                else:
                    cmd = "acl-mirror-port ethernet {0}".format(mac_access_group['mirror_port']['ethernet'])
                cmds.append(cmd)
        elif mac_access_group['lag'] is not None:
            cmd = "interface lag {0}".format(mac_access_group['lag'])
            cmds.append(cmd)
        elif mac_access_group['vlan'] is not None:
            if mac_access_group['vlan']['vlan_num'] is not None:
                cmd = "vlan {0}".format(mac_access_group['vlan']['vlan_num'])
            cmds.append(cmd)

        if mac_access_group['state'] == 'absent':
            cmd = "no mac access-group"
        else:
            cmd = "mac access-group"
        if mac_access_group['mac_acl_name'] is not None:
            cmd += " {0} in".format(mac_access_group['mac_acl_name'])
            if mac_access_group['vlan'] is not None:
                if mac_access_group['vlan']['interfaces'] is not None:
                    for elements in mac_access_group['vlan']['interfaces']:
                        cmd += " {0}".format(elements)

            if mac_access_group['logging'] is not None:
                cmd += ' logging {0}'.format(mac_access_group['logging'])

        cmds.append(cmd)
        cmds.append('exit')
    if default_acl is not None:
        default_cmds = 'authentication'
        cmds.append(default_cmds)
        if default_acl['state'] == 'absent':
            cmd = "no default-acl {0}".format(default_acl['ip_type'])
        else:
            cmd = "default-acl {0}".format(default_acl['ip_type'])

        if default_acl['acl_name'] is not None:
            cmd += " {0}".format(default_acl['acl_name'])
        else:
            cmd += " {0}".format(default_acl['acl_id'])
        if default_acl['in_out'] is not None:
            cmd += " {0}".format(default_acl['in_out'])
        cmds.append(cmd)
        cmds.append('exit')
    return cmds


def main():
    """entry point for module execution
    """
    vlan_spec = dict(
        vlan_num=dict(type='int'),
        interfaces=dict(type='list', elements='str')
    )
    mirror_port_spec = dict(
        ethernet=dict(type='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    ip_access_group_spec = dict(
        acl_num=dict(type='int'),
        acl_name=dict(type='str'),
        in_out=dict(type='str', choices=['in', 'out']),
        ethernet=dict(type='str'),
        lag=dict(type='int'),
        vlan=dict(type='dict', options=vlan_spec),
        mirror_port=dict(type='dict', options=mirror_port_spec),
        logging=dict(type='str', choices=['enable', 'disable']),
        frag_deny=dict(type='bool', default='no'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    ipv6_access_group_spec = dict(
        acl_name=dict(type='str'),
        in_out=dict(type='str', choices=['in', 'out']),
        ethernet=dict(type='str'),
        lag=dict(type='int'),
        vlan=dict(type='dict', options=vlan_spec),
        mirror_port=dict(type='dict', options=mirror_port_spec),
        logging=dict(type='str', choices=['enable', 'disable']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    mac_access_group_spec = dict(
        mac_acl_name=dict(type='str', required=True),
        ethernet=dict(type='str'),
        lag=dict(type='int'),
        vlan=dict(type='dict', options=vlan_spec),
        mirror_port=dict(type='dict', options=mirror_port_spec),
        logging=dict(type='str', choices=['enable', 'disable']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    default_acl_spec = dict(
        ip_type=dict(type='str', required=True, choices=['ipv4', 'ipv6']),
        acl_name=dict(type='str'),
        acl_id=dict(type='int'),
        in_out=dict(type='str', choices=['in', 'out']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    required_one_of = [['acl_name', 'acl_num', 'frag_deny']]
    mutually_exclusive = [('acl_name', 'frag_deny'), ('acl_num', 'frag_deny'), ('acl_name', 'acl_num')]
    argument_spec = dict(
        ip_access_group=dict(type='dict', options=ip_access_group_spec, required_one_of=required_one_of, mutually_exclusive=mutually_exclusive),
        ipv6_access_group=dict(type='dict', options=ipv6_access_group_spec),
        mac_access_group=dict(type='dict', options=mac_access_group_spec),
        default_acl=dict(type='dict', options=default_acl_spec)
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    ip_access_group = module.params["ip_access_group"]
    ipv6_access_group = module.params["ipv6_access_group"]
    mac_access_group = module.params["mac_access_group"]
    default_acl = module.params["default_acl"]

    if warnings:
        results['warnings'] = warnings

    commands = build_command(
        module, ip_access_group, ipv6_access_group,
        mac_access_group, default_acl)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
