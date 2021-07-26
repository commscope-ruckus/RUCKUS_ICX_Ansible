#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_flex_dot1x
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
        default: no
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
        required: true
      state:
        description: Enable/Disable this functionality
        type: str
        default: present
        choices: ['present', 'absent']
  max_reauth_req:
    description: Configure the maximum number of times (attempts) EAP-request/identity frames are sent for
                 reauthentication after the first authentication attempt.
    type: dict
    suboptions:
      count:
        description: Specifies the number of EAP frame re-transmissions. This is a number from 1 through 10. The default is 2.
        type: int
        required: true
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
        required: true
      state:
        description: Enable/Disable this functionality
        type: str
        default: present
        choices: ['present', 'absent']
  port_control:
    description: Controls port-state authorization and configures the port control type to activate authentication on an 802.1X-enabled interface.
                 Required when enable(state=present).
    type: dict
    suboptions:
      auto:
        description: Enables authentication on a port. It places the controlled port in the unauthorized state until
                     authentication takes place between the client and authentication server.
        type: bool
      force_authorized:
        description: Places the controlled port unconditionally in the authorized state, allowing all traffic to pass between the client and the authenticator.
        type: bool
      force_unauthorized:
        description: Places the controlled port unconditionally in the unauthorized state, denying any traffic to pass between the client and the authenticator.
        type: bool
      all:
        description: Enables 802.1x authentication on all interfaces.
        type: bool
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
  radius_server_dead_time:
    description: Configures the interval at which the test user message is sent to the server to
                 check the status of non-responding servers that are marked as dead.
    type: dict
    suboptions:
      time:
        description: The time interval between successive server requests to check the availability of the RADIUS server in minutes.
                     The valid values are from 1 through 5 minutes.
        type: int
        required: true
      state:
        description: Configure/Removes the dead time interval.
        type: str
        default: present
        choices: ['present', 'absent']
  radius_server_test:
    description: Sets the user name to be used in the RADIUS request packets for RADIUS dead server detection.
    type: dict
    suboptions:
      user_name:
        description: The false user name used in the server test.
        type: str
        required: true
      state:
        description: Enable/Disable the configuration to send RADIUS request packets with false usernames for RADIUS dead server detection.
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
        module, enable=None, guest_vlan=None, max_reauth_req=None, max_req=None,
        port_control=None, timeout=None, radius_server_dead_time=None, radius_server_test=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """
    cmds = []
    auth_cmds = []
    cmd = 'authentication'
    cmds.append(cmd)
    if enable is not None:
        if enable['state'] == 'absent':
            cmd = "no dot1x enable"
            if not enable['all'] and enable['ethernet'] is None:
                cmds.append(cmd)
        else:
            cmd = "dot1x enable"
            cmds.append(cmd)
        if enable['all']:
            cmd += " all"
            cmds.append(cmd)
        elif enable['ethernet'] is not None:
            for elements in enable['ethernet']:
                cmd += " ethernet {0}".format(elements)
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
    if guest_vlan is not None:
        if guest_vlan['state'] == 'absent':
            cmd = "no dot1x guest-vlan {0}".format(guest_vlan['vlan_id'])
        else:
            cmd = "dot1x guest-vlan {0}".format(guest_vlan['vlan_id'])
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
    cmds.append('exit')
    if radius_server_dead_time is not None:
        if radius_server_dead_time['state'] == 'absent':
            cmd = "no radius-server dead-time {0}".format(radius_server_dead_time['time'])
        else:
            cmd = "radius-server dead-time {0}".format(radius_server_dead_time['time'])
        auth_cmds.append(cmd)
    if radius_server_test is not None:
        if radius_server_test['state'] == 'absent':
            cmd = "no radius-server test {0}".format(radius_server_test['user_name'])
        else:
            cmd = "radius-server test {0}".format(radius_server_test['user_name'])
        auth_cmds.append(cmd)
    if len(cmds) == 2:
        return auth_cmds
    else:
        cmds.extend(auth_cmds)
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
        vlan_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    max_reauth_req_spec = dict(
        count=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    max_req_spec = dict(
        count=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    port_control_spec = dict(
        auto=dict(type='bool'),
        force_authorized=dict(type='bool'),
        force_unauthorized=dict(type='bool'),
        all=dict(type='bool'),
        ethernet=dict(type='list', elements='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    required_one_of = [['auto', 'force_authorized', 'force_unauthorized'], ['all', 'ethernet']]
    mutually_exclusive = [('auto', 'force_authorized', 'force_unauthorized'), ('all', 'ethernet')]
    timeout_spec = dict(
        quiet_period=dict(type='int'),
        supplicant=dict(type='int'),
        tx_period=dict(type='int'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    radius_server_dead_time_spec = dict(
        time=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    radius_server_test_spec = dict(
        user_name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    argument_spec = dict(
        enable=dict(type='dict', options=enable_spec, mutually_exclusive=[('all', 'ethernet')]),
        guest_vlan=dict(type='dict', options=guest_vlan_spec),
        max_reauth_req=dict(type='dict', options=max_reauth_req_spec),
        max_req=dict(type='dict', options=max_req_spec),
        port_control=dict(type='dict', options=port_control_spec, mutually_exclusive=mutually_exclusive, required_one_of=required_one_of),
        timeout=dict(type='dict', options=timeout_spec, required_one_of=[['quiet_period', 'supplicant', 'tx_period']]),
        radius_server_dead_time=dict(type='dict', options=radius_server_dead_time_spec),
        radius_server_test=dict(type='dict', options=radius_server_test_spec)
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    enable = module.params["enable"]
    guest_vlan = module.params["guest_vlan"]
    max_reauth_req = module.params["max_reauth_req"]
    max_req = module.params["max_req"]
    port_control = module.params["port_control"]
    timeout = module.params["timeout"]
    radius_server_dead_time = module.params["radius_server_dead_time"]
    radius_server_test = module.params["radius_server_test"]

    if warnings:
        results['warnings'] = warnings

    commands = build_command(
        module, enable, guest_vlan, max_reauth_req, max_req, port_control,
        timeout, radius_server_dead_time, radius_server_test)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
