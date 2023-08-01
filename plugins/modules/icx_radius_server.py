#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)



from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_flex_radius_server
author: "Ruckus Wireless (@Commscope)"
short_description: Configures radius server in Ruckus ICX 7000 series switches.
description:
  - Configures radius server in Ruckus ICX 7000 series switches.
options:
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
name: task-1 config radius server dead time and test
    commscope.icx.icx_radius_server:
      radius_server_dead_time:
        time: 4
        state: present
      radius_server_test:
        user_name: test_user
        state: present
    register: output

name: task-2 unconfig radius server dead time and test
    commscope.icx.icx_radius_server:
      radius_server_dead_time:
        time: 4
        state: absent
      radius_server_test:
        user_name: test_user
        state: absent
    register: output
"""

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(
        module, radius_server_dead_time=None, radius_server_test=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """
    cmds = []
    cmd = 'authentication'
    cmds.append(cmd)
    if radius_server_dead_time is not None:
        if radius_server_dead_time['state'] == 'absent':
            cmd = "no radius-server dead-time {0}".format(radius_server_dead_time['time'])
        else:
            cmd = "radius-server dead-time {0}".format(radius_server_dead_time['time'])
        cmds.append(cmd)
    if radius_server_test is not None:
        if radius_server_test['state'] == 'absent':
            cmd = "no radius-server test {0}".format(radius_server_test['user_name'])
        else:
            cmd = "radius-server test {0}".format(radius_server_test['user_name'])
        cmds.append(cmd)
   
    return cmds

def main():
    """
    entry point for module execution
    """
    radius_server_dead_time_spec = dict(
        time=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    radius_server_test_spec = dict(
        user_name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    argument_spec = dict(radius_server_dead_time=dict(type='dict', options=radius_server_dead_time_spec),
        radius_server_test=dict(type='dict', options=radius_server_test_spec)
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    radius_server_dead_time = module.params["radius_server_dead_time"]
    radius_server_test = module.params["radius_server_test"]

    if warnings:
        results['warnings'] = warnings
    commands = build_command(
        module, radius_server_dead_time, radius_server_test)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
                                  



