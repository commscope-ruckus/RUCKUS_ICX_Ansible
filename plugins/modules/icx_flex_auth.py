#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_flex_auth
author: "Ruckus Wireless (@Commscope)"
short_description: Configures flexible authentication in Ruckus ICX 7000 series switches.
description:
  - Configures flexible authentication in Ruckus ICX 7000 series switches.
notes:
  - Tested against ICX 10.1
options:
  global_auth:
    description: Configure flexible authentication globally.
    type: dict
    suboptions:
      auth_default_vlan:
        description: Specifies the auth-default VLAN globally.
        type: dict
        suboptions:
          vlan_id:
            description: Specifies the VLAN ID of the auth-default VLAN.
            type: int
            required: true
          state:
            description: Enable/Disable auth-default VLAN.
            type: str
            default: present
            choices: ['present', 'absent']
      re_authentication:
        description: Periodically re-authenticates clients connected to MAC authentication-enabled interfaces and 802.1X-enabled interfaces.
        type: str
        choices: ['present', 'absent']
      restricted_vlan:
        description: Configures a specific VLAN as the restricted VLAN for all ports on the device to place the client port when the authentication fails.
        type: dict
        suboptions:
          vlan_id:
            description: Specifies the identification number of the restricted VLAN.
            type: int
            required: true
          state:
            description: Enable/Disable the restricted VLAN.
            type: str
            default: present
            choices: ['present', 'absent']
      voice_vlan:
        description: Creates a voice VLAN at the global level.
        type: dict
        suboptions:
          vlan_id:
            description: Specifies the VLAN identifier. The range is from 1 through 4095 (excluding all reserved VLANs).
            type: int
            required: true
          state:
            description: Configures/removes the global voice VLAN configuration.
            type: str
            default: present
            choices: ['present', 'absent']
      critical_vlan:
        description: Specifies the VLAN into which the client should be placed when the RADIUS server times out while authenticating or re-authenticating users.
        type: dict
        suboptions:
          vlan_id:
            description: Specifies the VLAN ID of the specific critical VLAN.
            type: int
            required: true
          state:
            description: Enable/Disable critical VLAN by removing the client from the VLAN.
            type: str
            default: present
            choices: ['present', 'absent']
      auth_fail_action:
        description: Configures, at a global level, the action taken after 802.1X and MAC authentication failure.
        type: dict
        suboptions:
          restricted_vlan:
            description: Places the client in the restricted VLAN after authentication failure.
            type: bool
            required: true
          voice_vlan:
            description: Places the client in the voice VLAN after authentication failure.
            type: bool
          state:
            description: Enable/Disable authentication failure action configuration.
            type: str
            default: present
            choices: ['present', 'absent']
      auth_timeout_action:
        description: Configures, at a global level, the action taken when external server authentication times out.
        type: dict
        suboptions:
          critical_vlan:
            description: Places the client in the critical VLAN after RADIUS timeout.
            type: bool
          voice_vlan:
            description: Places the client in the voice VLAN after RADIUS timeout.
            type: bool
          failure:
            description: Specifies that RADIUS timeout causes authentication failure.
            type: bool
          success:
            description: Specifies that RADIUS timeout causes authentication success.
            type: bool
          state:
            description: Enable/Disable authentication timeout action configuration.
            type: str
            default: present
            choices: ['present', 'absent']
  interface_auth:
    description: Configure flexible authentication at the interface level.
    type: dict
    suboptions:
      interface:
        description: Specifies the interface.  For eg - ethernet 1/1/2
        type: list
        elements: str
        required: true
      auth_default_vlan:
        description: Specifies the authentication default VLAN at the interface level.
        type: dict
        suboptions:
          vlan_id:
            description: Specifies the VLAN ID of the auth-default VLAN.
            type: int
            required: true
          state:
            description: Enable/Disable auth-default VLAN.
            type: str
            default: present
            choices: ['present', 'absent']
      voice_vlan:
        description: Creates a voice VLAN ID for a port or for a group of ports.
        type: dict
        suboptions:
          vlan_id:
            description: pecifies a valid VLAN ID. Valid values range from 1 through 4095.
            type: int
            required: true
          state:
            description: Configures/removes the voice VLAN ID from the port.
            type: str
            default: present
            choices: ['present', 'absent']
      auth_fail_action:
        description: Specifies the authentication failure action to move the client port to the restricted VLAN after authentication failure for both MAC
                     authentication and 802.1X authentication on an interface.
        type: dict
        suboptions:
          restricted_vlan:
            description: Specifies the failure action to move the client port to the restricted VLAN after authentication failure.
            type: bool
            required: true
          vlan_id:
            description: Specifies the ID of the VLAN to be configured as restricted VLAN.
            type: int
          state:
            description: Enable/Disable authentication failure action.
            type: str
            default: present
            choices: ['present', 'absent']
      auth_timeout_action:
        description: Configures the authentication timeout actions to specify the action for the RADIUS server if an authentication timeout occurs.
        type: dict
        suboptions:
          critical_vlan:
            description: On initial authentication, specifies that the client be moved to the client to the designated critical VLAN after authentication
                         timeout. This command applies only to data traffic.
            type: bool
          vlan_id:
            description: Specifies the ID of the VLAN to be configured as critical VLAN.
            type: int
          failure:
            description: Specifies the RADIUS timeout action to carry out the configured failure action. If the failure action is not configured, the client's
                         MAC address is blocked in the hardware. Once the failure timeout action is enabled, use the no form of the command to reset
                         the RADIUS timeout behavior to retry.
            type: bool
          success:
            description: Considers the client as authenticated after RADIUS timeout. After the timeout action is enabled as success, use the no form of
                         the command to set the RADIUS timeout behavior to retry.
            type: bool
          state:
            description: Enable/Disable authentication timeout action configuration.
            type: str
            default: present
            choices: ['present', 'absent']
      use_radius_server:
        description: Maps a RADIUS server to a port.
        type: dict
        suboptions:
          ip_address:
            description: The IP address of the RADIUS server(A.B.C.D).
            type: str
            required: true
          state:
            description: Configures/removes the mapping of the RADIUS server to the port.
            type: str
            default: present
            choices: ['present', 'absent']
"""
EXAMPLES = """
- name: configure flexible authentication globally
  commscope.icx.icx_flex_auth:
    global_auth:
      auth_default_vlan:
        vlan_id: 2
      re_authentication: present
      restricted_vlan:
        vlan_id: 5
        state: present
      voice_vlan:
        vlan_id: 10
        state: present
- name: configure at a particular interface
  commscope.icx.icx_flex_auth:
    interface_auth:
      interface:
        - 1/1/15
      auth_timeout_action:
        success: yes
      use_radius_server:
        ip_address: 10.10.10.1
        state: present
- name: remove flex auth configurations
  commscope.icx.icx_flex_auth:
    global_auth:
      auth_default_vlan:
        vlan_id: 2
        state: absent
      re_authentication: absent
      restricted_vlan:
        vlan_id: 5
        state: absent
    interface_auth:
      interface:
        - 1/1/15
      auth_timeout_action:
        success: yes
        state: absent
      use_radius_server:
        ip_address: 10.10.10.1
        state: absent
"""
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(
        module, global_auth=None, interface_auth=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """
    cmds = []

    if global_auth is not None:
        cmd = 'authentication'
        cmds.append(cmd)
        if global_auth['auth_default_vlan'] is not None:
            if global_auth['auth_default_vlan']['state'] == 'absent':
                cmd = "no auth-default-vlan {0}".format(global_auth['auth_default_vlan']['vlan_id'])
            else:
                cmd = "auth-default-vlan {0}".format(global_auth['auth_default_vlan']['vlan_id'])
            cmds.append(cmd)
        if global_auth['re_authentication'] is not None:
            if global_auth['re_authentication'] == 'absent':
                cmd = "no re-authentication"
            else:
                cmd = "re-authentication"
            cmds.append(cmd)
        if global_auth['restricted_vlan'] is not None:
            if global_auth['restricted_vlan']['state'] == 'absent':
                cmd = "no restricted-vlan {0}".format(global_auth['restricted_vlan']['vlan_id'])
            else:
                cmd = "restricted-vlan {0}".format(global_auth['restricted_vlan']['vlan_id'])
            cmds.append(cmd)
        if global_auth['voice_vlan'] is not None:
            if global_auth['voice_vlan']['state'] == 'absent':
                cmd = "no voice-vlan {0}".format(global_auth['voice_vlan']['vlan_id'])
            else:
                cmd = "voice-vlan {0}".format(global_auth['voice_vlan']['vlan_id'])
            cmds.append(cmd)
        if global_auth['critical_vlan'] is not None:
            if global_auth['critical_vlan']['state'] == 'absent':
                cmd = "no critical-vlan {0}".format(global_auth['critical_vlan']['vlan_id'])
            else:
                cmd = "critical-vlan {0}".format(global_auth['critical_vlan']['vlan_id'])
            cmds.append(cmd)
        if global_auth['auth_fail_action'] is not None:
            if global_auth['auth_fail_action']['state'] == 'absent':
                cmd = "no auth-fail-action"
            else:
                cmd = "auth-fail-action"
            if global_auth['auth_fail_action']['restricted_vlan']:
                cmd += " restricted-vlan"
                if global_auth['auth_fail_action']['voice_vlan']:
                    cmd += " voice voice-vlan"
            cmds.append(cmd)
        if global_auth['auth_timeout_action'] is not None:
            if global_auth['auth_timeout_action']['state'] == 'absent':
                cmd = "no auth-timeout-action"
            else:
                cmd = "auth-timeout-action"
            if global_auth['auth_timeout_action']['critical_vlan']:
                cmd += " critical-vlan"
                if global_auth['auth_timeout_action']['voice_vlan']:
                    cmd += " voice voice-vlan"
            elif global_auth['auth_timeout_action']['failure']:
                cmd += " failure"
            elif global_auth['auth_timeout_action']['success']:
                cmd += " success"
            cmds.append(cmd)
        cmds.append('exit')

    if interface_auth is not None:
        cmd = "interface"
        for ethernet in interface_auth['interface']:
            cmd += " ethernet {0}".format(ethernet)
        cmds.append(cmd)
        if interface_auth['auth_default_vlan'] is not None:
            if interface_auth['auth_default_vlan']['state'] == 'absent':
                cmd = "no authentication auth-default-vlan {0}".format(interface_auth['auth_default_vlan']['vlan_id'])
            else:
                cmd = "authentication auth-default-vlan {0}".format(interface_auth['auth_default_vlan']['vlan_id'])
            cmds.append(cmd)
        if interface_auth['voice_vlan'] is not None:
            if interface_auth['voice_vlan']['state'] == 'absent':
                cmd = "no authentication voice-vlan {0}".format(interface_auth['voice_vlan']['vlan_id'])
            else:
                cmd = "authentication voice-vlan {0}".format(interface_auth['voice_vlan']['vlan_id'])
            cmds.append(cmd)
        if interface_auth['auth_fail_action'] is not None:
            if interface_auth['auth_fail_action']['state'] == 'absent':
                cmd = "no authentication fail-action"
            else:
                cmd = "authentication fail-action"
            if interface_auth['auth_fail_action']['restricted_vlan']:
                cmd += " restricted-vlan"
                if interface_auth['auth_fail_action']['vlan_id']:
                    cmd += " {0}".format(interface_auth['auth_fail_action']['vlan_id'])
            cmds.append(cmd)
        if interface_auth['auth_timeout_action'] is not None:
            if interface_auth['auth_timeout_action']['state'] == 'absent':
                cmd = "no authentication timeout-action"
            else:
                cmd = "authentication timeout-action"
            if interface_auth['auth_timeout_action']['critical_vlan']:
                cmd += " critical-vlan"
                if interface_auth['auth_timeout_action']['vlan_id']:
                    cmd += " {0}".format(interface_auth['auth_timeout_action']['vlan_id'])
            elif interface_auth['auth_timeout_action']['failure']:
                cmd += " failure"
            elif interface_auth['auth_timeout_action']['success']:
                cmd += " success"
            cmds.append(cmd)
        if interface_auth['use_radius_server'] is not None:
            if interface_auth['use_radius_server']['state'] == 'absent':
                cmd = "no use-radius-server {0}".format(interface_auth['use_radius_server']['ip_address'])
            else:
                cmd = "use-radius-server {0}".format(interface_auth['use_radius_server']['ip_address'])
            cmds.append(cmd)
        cmds.append('exit')

    return cmds


def main():
    """entry point for module execution
    """

    auth_default_vlan_spec = dict(
        vlan_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    restricted_vlan_spec = dict(
        vlan_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    voice_vlan_spec = dict(
        vlan_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    critical_vlan_spec = dict(
        vlan_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    auth_fail_action_spec = dict(
        restricted_vlan=dict(type='bool', required=True),
        voice_vlan=dict(type='bool'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    auth_timeout_action_spec = dict(
        critical_vlan=dict(type='bool'),
        voice_vlan=dict(type='bool'),
        failure=dict(type='bool'),
        success=dict(type='bool'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    required_one_of = [['critical_vlan', 'failure', 'success']]
    mutually_exclusive = [('critical_vlan', 'failure', 'success')]
    global_auth_spec = dict(
        auth_default_vlan=dict(type='dict', options=auth_default_vlan_spec),
        re_authentication=dict(type='str', choices=['present', 'absent']),
        restricted_vlan=dict(type='dict', options=restricted_vlan_spec),
        voice_vlan=dict(type='dict', options=voice_vlan_spec),
        critical_vlan=dict(type='dict', options=critical_vlan_spec),
        auth_fail_action=dict(type='dict', options=auth_fail_action_spec),
        auth_timeout_action=dict(type='dict', options=auth_timeout_action_spec, required_one_of=required_one_of,
                                 mutually_exclusive=mutually_exclusive)
    )
    auth_fail_action_spec = dict(
        restricted_vlan=dict(type='bool', required=True),
        vlan_id=dict(type='int'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    auth_timeout_action_spec = dict(
        critical_vlan=dict(type='bool'),
        vlan_id=dict(type='int'),
        failure=dict(type='bool'),
        success=dict(type='bool'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    required_one_of = [['critical_vlan', 'failure', 'success']]
    mutually_exclusive = [('critical_vlan', 'failure', 'success')]
    use_radius_server_spec = dict(
        ip_address=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    interface_auth_spec = dict(
        interface=dict(type='list', elements='str', required=True),
        auth_default_vlan=dict(type='dict', options=auth_default_vlan_spec),
        voice_vlan=dict(type='dict', options=voice_vlan_spec),
        auth_fail_action=dict(type='dict', options=auth_fail_action_spec),
        auth_timeout_action=dict(type='dict', options=auth_timeout_action_spec, required_one_of=required_one_of,
                                 mutually_exclusive=mutually_exclusive),
        use_radius_server=dict(type='dict', options=use_radius_server_spec)
    )
    argument_spec = dict(
        global_auth=dict(type='dict', options=global_auth_spec),
        interface_auth=dict(type='dict', options=interface_auth_spec)
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    global_auth = module.params["global_auth"]
    interface_auth = module.params["interface_auth"]

    if warnings:
        results['warnings'] = warnings

    commands = build_command(
        module, global_auth, interface_auth)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
