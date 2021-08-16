#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_vxlan
author: "Ruckus Wireless (@Commscope)"
short_description: Configures all aspects of VxLAN  implementation in Ruckus ICX 7000 series switches.
description:
  - Configures all aspects of VxLAN implementation in Ruckus ICX 7000 series switches.
notes:
  - Tested against ICX 10.1
options:
  overlay_gateway:
    description: Configures an overlay-gateway name and enters gateway configuration mode. name can be up to 64 characters in length.
    type: str
    required: true
  state:
    description: Specifies whether to Configure/remove overlay-gateway configuration.
    type: str
    default: present
    choices: ['present', 'absent']
  overlay_gateway_type:
    description: Set the overlay-gateway type (layer2-extension).
    type: str
    choices: ['present', 'absent']
  ip_interface:
    description: Configures IP interface for VXLAN overlay-gateway(use a loopback interface).
    type: dict
    suboptions:
      interface_id:
        description: Specifies the loopback interface ID.
        type: int
        required: true
      state:
        description: Specifies whether to Configure/remove the loopback interface.
        type: str
        default: present
        choices: ['present', 'absent']
  map_vlan:
    description: Map a VLAN you intend to extend over the VXLAN segment (that is, over the overlay-gateway) to a VXLAN Network Identifier (VNI).
                 A maximum of 256 VLAN, VNI pairs can be configured.
                 The default VLAN (typically, VLAN 1) cannot be mapped to a VNI or extended over a VXLAN segment.
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description: Identifies the VLAN to map to the VNI. Value range can be from 1 through 4095.
        type: int
        required: true
      vni_id:
        description: Identifies the VXLAN Network Identifier (or VXLAN segment ID). Value range can be from 1 through 16777215.
        type: int
        required: true
      state:
        description: Specifies whether to Configure/remove the VLAN to VNI mapping.
        type: str
        default: present
        choices: ['present', 'absent']
  site:
    description: Create one remote site for the VXLAN overlay-gateway and configure the IP address for the site.
                     Only IPv4 tunnels are supported. A maximum of 32 remote sites can be created.
    type: list
    elements: dict
    suboptions:
      site_name:
        description: Specifies the name of the remote site. name can be up to 64 characters in length.
        type: str
        required: true
      state:
        description: Specifies whether to Configure/remove the remote site.
        type: str
        default: present
        choices: ['present', 'absent']
      ip:
        description: Configure remote site IP address.
        type: dict
        suboptions:
          address:
            description: Configures the IP address, in A.B.C.D format.
            type: str
            required: true
          state:
            description: Specifies whether to Configure/remove remote site IP address.
            type: str
            default: present
            choices: ['present', 'absent']
      extend_vlan:
        description: Extend the mapped VLAN to the remote site.
        type: list
        elements: dict
        suboptions:
          vlan_id:
            description: Specifies the VLAN to be extended to the VXLAN remote site.
            type: int
            required: true
          state:
            description: Specifies whether to Configure/remove the extended VLAN.
            type: str
            default: present
            choices: ['present', 'absent']
"""

EXAMPLES = """
- name: configure VxLAN overlay-gateway
  commscope.icx.icx_vxlan:
    overlay_gateway: gate1
    type: present
    ip_interface:
      interface_id: 1
      state: present
    map_vlan:
      - vlan_id: 21
        vni_id: 100
        state: present
      - vlan_id: 23
        vni_id: 300
    site:
      - site_name: site1
        ip:
          address: 1.1.1.1
          state: present
        extend_vlan:
         - vlan_id: 21
         - vlan_id: 23
           state: present

- name: remove overlay-gateway configuration.
  commscope.icx.icx_vxlan:
    overlay_gateway: gate1
    state: present

"""
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(
        module, overlay_gateway=None, state=None, overlay_gateway_type=None, ip_interface=None, map_vlan=None, site=None):
    cmds = []
    if state == 'absent':
        cmd = "no overlay-gateway {0}".format(overlay_gateway)
    else:
        cmd = "overlay-gateway {0}".format(overlay_gateway)
    cmds.append(cmd)
    if state == 'present':
        if overlay_gateway_type is not None:
            if overlay_gateway_type == 'present':
                cmd = "type layer2-extension"
                cmds.append(cmd)
        if ip_interface is not None:
            if ip_interface['state'] == 'absent':
                cmd = "no ip interface loopback {0}".format(ip_interface['interface_id'])
            else:
                cmd = "ip interface loopback {0}".format(ip_interface['interface_id'])
            cmds.append(cmd)
        if map_vlan is not None:
            for vlan in map_vlan:
                if vlan['state'] == 'present':
                    cmd = "map vlan {0} to vni {1}".format(vlan['vlan_id'], vlan['vni_id'])
                    cmds.append(cmd)
        if site is not None:
            for sites in site:
                if sites['state'] == 'present':
                    cmd = "site {0}".format(sites['site_name'])
                    cmds.append(cmd)
                    if sites['ip'] is not None:
                        if sites['ip']['state'] == 'absent':
                            cmd = "no ip address {0}".format(sites['ip']['address'])
                        else:
                            cmd = "ip address {0}".format(sites['ip']['address'])
                        cmds.append(cmd)
                    if sites['extend_vlan'] is not None:
                        for vlans in sites['extend_vlan']:
                            if vlans['state'] == 'absent':
                                cmd = "no extend vlan add {0}".format(vlans['vlan_id'])
                            else:
                                cmd = "extend vlan add {0}".format(vlans['vlan_id'])
                            cmds.append(cmd)
                    cmds.append('exit')
                else:
                    cmd = "no site {0}".format(sites['site_name'])
                    cmds.append(cmd)
        if map_vlan is not None:
            for vlan in map_vlan:
                if vlan['state'] == 'absent':
                    cmd = "no map vlan {0} to vni {1}".format(vlan['vlan_id'], vlan['vni_id'])
                    cmds.append(cmd)
        if overlay_gateway_type is not None:
            if overlay_gateway_type == 'absent':
                cmd = "no type layer2-extension"
                cmds.append(cmd)
    return cmds


def main():
    """entry point for module execution
    """

    ip_interface_spec = dict(
        interface_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    map_vlan_spec = dict(
        vlan_id=dict(type='int', required=True),
        vni_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    ip_spec = dict(
        address=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    extend_vlan_spec = dict(
        vlan_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    site_spec = dict(
        site_name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        ip=dict(type='dict', options=ip_spec),
        extend_vlan=dict(type='list', elements='dict', options=extend_vlan_spec)
    )
    argument_spec = dict(
        overlay_gateway=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        overlay_gateway_type=dict(type='str', choices=['present', 'absent']),
        ip_interface=dict(type='dict', options=ip_interface_spec),
        map_vlan=dict(type='list', elements='dict', options=map_vlan_spec),
        site=dict(type='list', elements='dict', options=site_spec)
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    overlay_gateway = module.params["overlay_gateway"]
    state = module.params["state"]
    overlay_gateway_type = module.params["overlay_gateway_type"]
    ip_interface = module.params["ip_interface"]
    map_vlan = module.params["map_vlan"]
    site = module.params["site"]

    if warnings:
        results['warnings'] = warnings

    commands = build_command(
        module, overlay_gateway, state, overlay_gateway_type, ip_interface, map_vlan, site)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
