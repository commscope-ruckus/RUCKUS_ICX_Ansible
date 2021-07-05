#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_dot1x
author: "Ruckus Wireless (@Commscope)"
short_description: Configures dot1x in Ruckus ICX 7000 series switches.
description:
  - Configures dot1x in Ruckus ICX 7000 series switches.
notes:
  - Tested against ICX 10.1
options:
  enable:
    description: Enables 802.1X authentication globally.
    type: dict
    suboptions:
      all:
        description: Enables 802.1x authentication on all interfaces.
        type: bool
      ethernet:
        description: Enables 802.1x authentication on the specified interface or range of interfaces. For eg - [ethernet 1/1/2, ethernet 1/1/20 to 1/1/30]
        type: list
        elements: str
      state:
        description: Specifies whether to enables/disables authentication on all interfaces
        type: str
        default: present
        choices: ['present', 'absent']
  guest_vlan:
    description: Specifies the VLAN into which the port should be placed when the client's response to the dot1x requests for authentication times out.
    type: dict
    suboptions:
      vlan_id:
        description: Specifies the VLAN ID of the guest VLAN.
        type: int
      state:
        description: Enable/Disable this functionality
        type: str
        default: present
        choices: ['present', 'absent']
  macauth_override:
    description: Sets an override option so that MAC authentication is attempted when 802.1X authentication fails for the client.
    type: str
    choices: ['present', 'absent']
  max_reauth_req:
    description: Configure the maximum number of times (attempts) EAP-request/identity frames are sent for
                 reauthentication after the first authentication attempt.
    type: dict
    suboptions:
      count:
        description: Specifies the number of EAP frame re-transmissions. This is a number from 1 through 10. The default is 2.
        type: int
      state:
        description: Enable/Disable this functionality
        type: str
        default: present
        choices: ['present', 'absent']
  max_req:
    description: Configures the retransmission parameter that defines the maximum number of times
                 EAP request/challenge frames are retransmitted when EAP response/identity frame is not received from the client.
    type: dict
    suboptions:
      count:
        description: Specifies the number of EAP frame re-transmissions. Th range is from from 1 through 10. The default value is 2.
        type: int
      state:
        description: Enable/Disable this functionality
        type: str
        default: present
        choices: ['present', 'absent']
  port_control:
    description: Controls port-state authorization and configures the port control type to activate authentication on an 802.1X-enabled interface.
    type: dict
    suboptions:
      auto:
        description: Enables authentication on a port. It places the controlled port in the unauthorized state until
                     authentication takes place between the client and authentication server.
        type: bool
        default: no
      force_authorized:
        description: Places the controlled port unconditionally in the authorized state, allowing all traffic to pass between the client and the authenticator.
        type: bool
        default: no
      force_unauthorized:
        description: Places the controlled port unconditionally in the unauthorized state, denying any traffic to pass between the client and the authenticator.
        type: bool
        default: no
      all:
        description: Enables 802.1x authentication on all interfaces.
        type: bool
        default: no
      ethernet:
        description: Enables 802.1x authentication on the specified interface or range of interfaces. For eg - [ethernet 1/1/2, ethernet 1/1/20 to 1/1/30]
        type: list
        elements: str
      state:
          description: Enable/Disable this functionality
          type: str
          default: present
          choices: ['present', 'absent']
  timeout:
    description: Configures the timeout parameters that determine the time interval for client reauthentication and EAP retransmissions.
    type: dict
    suboptions:
      quiet_period:
        description: Specifies the time, in seconds, the device waits before trying to re-authenticate the client.
                     The quiet period can be from 1 through 4294967295 seconds. The default is 60 seconds.
        type: int
      supplicant:
        description: By default, when the ICX device relays an EAP-Request frame from the RADIUS server to the client,
                     it expects to receive a response from the client within 30 seconds. You can optionally specify
                     the wait interval using the supplicant seconds parameters. The value is 1 through 4294967295.
        type: int
      tx_period:
        description: Specifies the EAP request retransmission interval, in seconds, with the client.
                     By default, if the device does not receive an EAP-response/identity frame from a client, the device waits 30 seconds,
                     then retransmits the EAP-request/identity frame.
        type: int
      state:
        description: Enable/Disable this functionality
        type: str
        default: present
        choices: ['present', 'absent']
"""

EXAMPLES = """
- name: Enables dot1x on the specified interface
  commscope.icx.icx_dot1x:
    enable:
      ethernet: 1/1/9
      state: present
- name: Specifies the guest VLAN
  commscope.icx.icx_dot1x:
    guest_vlan:
      vlan_id: 12
      state: present
- name: Sets an override option
  commscope.icx.icx_dot1x:
    macauth_override: present
- name: disables max-reauth-req
  commscope.icx.icx_dot1x:
    max_reauth_req:
      count: 4
      state: absent
"""

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(
        module, enable=None, guest_vlan=None, macauth_override=None, max_reauth_req=None, max_req=None,
        port_control=None, timeout=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """
    cmds = []
    cmd = 'authentication'
    cmds.append(cmd)
    if enable is not None:
        if enable['state'] == 'absent':
            cmd = "no dot1x enable"
        else:
            cmd = "dot1x enable"
        if enable['all']:
            cmd += " all"
        elif enable['ethernet'] is not None:
            for elements in enable['ethernet']:
                cmd += " ethernet {0}".format(elements)
        cmds.append(cmd)
    if guest_vlan is not None:
        if guest_vlan['state'] == 'absent':
            cmd = "no dot1x guest-vlan {0}".format(guest_vlan['vlan_id'])
        else:
            cmd = "dot1x guest-vlan {0}".format(guest_vlan['vlan_id'])
        cmds.append(cmd)
    if macauth_override is not None:
        if macauth_override == 'present':
            cmd = "dot1x macauth-override"
        else:
            cmd = "no dot1x macauth-override"
        cmds.append(cmd)
    if max_reauth_req is not None:
        if max_reauth_req['state'] == 'absent':
            cmd = "no dot1x max-reauth-req {0}".format(max_reauth_req['count'])
        else:
            cmd = "dot1x max-reauth-req {0}".format(max_reauth_req['count'])
        cmds.append(cmd)
    if max_req is not None:
        if max_reauth_req['state'] == 'absent':
            cmd = "no dot1x max-req {0}".format(max_req['count'])
        else:
            cmd = "dot1x max-req {0}".format(max_req['count'])
        cmds.append(cmd)

    if port_control is not None:
        if port_control['state'] == 'absent':
            cmd = "no dot1x port-control"
        else:
            cmd = "dot1x port-control"
        if port_control['auto']:
            cmd += " auto"
        elif port_control['force_authorized']:
            cmd += " force-authorized"
        elif port_control['force_unauthorized']:
            cmd += " force-unauthorized"
        if port_control['all']:
            cmd += " all"
        elif port_control['ethernet'] is not None:
            for elements in port_control['ethernet']:
                cmd += " ethernet {0}".format(elements)
        cmds.append(cmd)

    if timeout is not None:
        if timeout['state'] == 'absent':
            cmd = "no dot1x timeout"
        else:
            cmd = "dot1x timeout"
        if timeout['quiet_period'] is not None:
            cmd += " quiet-period {0}".format(timeout['quiet_period'])
        elif timeout['supplicant'] is not None:
            cmd += " supplicant {0}".format(timeout['supplicant'])
        elif timeout['tx_period'] is not None:
            cmd += " tx-period {0}".format(timeout['tx_period'])
        cmds.append(cmd)

    return cmds


def main():
    """entry point for module execution
    """
    enable_spec = dict(
        all=dict(type='bool', default=False),
        ethernet=dict(type='list', elements='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    guest_vlan_spec = dict(
        vlan_id=dict(type='int'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    max_reauth_req_spec = dict(
        count=dict(type='int'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    max_req_spec = dict(
        count=dict(type='int'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    port_control_spec = dict(
        auto=dict(type='bool', default=False),
        force_authorized=dict(type='bool', default=False),
        force_unauthorized=dict(type='bool', default=False),
        all=dict(type='bool', default=False),
        ethernet=dict(type='list', elements='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    timeout_spec = dict(
        quiet_period=dict(type='int'),
        supplicant=dict(type='int'),
        tx_period=dict(type='int'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    argument_spec = dict(
        enable=dict(type='dict', options=enable_spec),
        guest_vlan=dict(type='dict', options=guest_vlan_spec),
        macauth_override=dict(type='str', choices=['present', 'absent']),
        max_reauth_req=dict(type='dict', options=max_reauth_req_spec),
        max_req=dict(type='dict', options=max_req_spec),
        port_control=dict(type='dict', options=port_control_spec),
        timeout=dict(type='dict', options=timeout_spec),
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    enable = module.params["enable"]
    guest_vlan = module.params["guest_vlan"]
    macauth_override = module.params["macauth_override"]
    max_reauth_req = module.params["max_reauth_req"]
    max_req = module.params["max_req"]
    port_control = module.params["port_control"]
    timeout = module.params["timeout"]

    if warnings:
        results['warnings'] = warnings

    commands = build_command(
        module, enable, guest_vlan, macauth_override, max_reauth_req, max_req, port_control, timeout)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
