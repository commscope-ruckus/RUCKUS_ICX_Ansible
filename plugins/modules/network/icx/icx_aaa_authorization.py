#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_aaa_authorization
author: "Ruckus Wireless (@Commscope)"
short_description: Configures AAA authorization in Ruckus ICX 7000 series switches.
description:
 - Configures AAA authorization in Ruckus ICX 7000 series switches.
notes:
 - Tested against ICX 10.1
options:
  coa_enable:
    description: Enables RADIUS Change of Authorization (CoA).
    type: dict
    suboptions:
      state:
        description: Specifies whether to configure or remove authorization.
        type: str
        default: present
        choices: ['present', 'absent']
  coa_ignore:
    description: Discards the specified RADIUS Change of Authorization (CoA) messages.
    type: dict
    suboptions:
      request:
        description: Specifies which message request to ignore.
        required: true
        type: str
        choices: ['disable-port', 'dm-request', 'flip-port', 'modify-acl', 'reauth-host']
      state:
        description: Specifies whether to configure or remove authorization.
        type: str
        default: present
        choices: ['present', 'absent']
  commands:
    description: Configures the AAA authorization configuration parameters for EXEC commands.
    type: dict
    suboptions:
      privilege_level:
        description: Configures the device to perform AAA authorization for the commands available at the specified privilege level. Valid values are 0,4 and 5.
        type: int
        required: true
        choices: [0,4,5]
      primary_method:
        description: Primary authorization method.
        type: str
        required: true
        choices: ['radius', 'tacacs+', 'none']
      backup_method1:
        description: Backup authorization method if primary method fails.
        type: str
        choices: ['radius', 'tacacs+', 'none']
      backup_method2:
        description: Backup authorization method if primary and backup method1 fails.
        type: str
        choices: ['none']
      state:
        description: Specifies whether to configure or remove authorization.
        type: str
        default: present
        choices: ['present', 'absent']
  exec_:
    description: Determines the user privilege level when users are authenticated.
    type: dict
    suboptions:
      primary_method:
        description: Primary authorization method.
        type: str
        required: true
        choices: ['radius', 'tacacs+', 'none']
      backup_method1:
        description: Backup authorization method if primary method fails.
        type: str
        choices: ['radius', 'tacacs+', 'none']
      backup_method2:
        description: Backup authorization method if primary and backup1 methods fails.
        type: str
        choices: ['none']
      state:
        description: Specifies whether to configure or remove authorization.
        type: str
        default: present
        choices: ['present', 'absent']
"""
EXAMPLES = """
- name: configure aaa authorization coa_enable and coa_ignore
  community.network.icx_aaa_authorization:
    coa_enable:
      state: present
    coa_ignore:
      request: flip-port
      state: present
- name: disable aaa authorization for commands
  community.network.icx_aaa_authorization:
    commands:
      privilege_level: 0
      primary_method: radius
      backup_method1: tacacs+
      state: absent
"""

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(module, coa_enable=None, coa_ignore=None, commands=None, exec_=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """
    cmds = []

    if coa_enable is not None:
        if coa_enable['state'] == 'absent':
            cmd = "no aaa authorization coa enable"
        else:
            cmd = "aaa authorization coa enable"
        cmds.append(cmd)

    if coa_ignore is not None:
        if coa_ignore['state'] == 'absent':
            cmd = "no aaa authorization coa ignore {0}".format(coa_ignore['request'])
        else:
            cmd = "aaa authorization coa ignore {0}".format(coa_ignore['request'])
        cmds.append(cmd)

    if commands is not None:
        if commands['state'] == 'absent':
            cmd = "no aaa authorization commands {0} default".format(commands['privilege_level'])
        else:
            cmd = "aaa authorization commands {0} default".format(commands['privilege_level'])

        if commands['primary_method'] is not None:
            cmd += " {0}".format(commands['primary_method'])
            if commands['backup_method1'] is not None:
                cmd += " {0}".format(commands['backup_method1'])
                if commands['backup_method2'] is not None:
                    cmd += " {0}".format(commands['backup_method2'])
        cmds.append(cmd)

    if exec_ is not None:
        if exec_['state'] == 'absent':
            cmd = "no aaa authorization exec default"
        else:
            cmd = "aaa authorization exec default"

        if exec_['primary_method'] is not None:
            cmd += " {0}".format(exec_['primary_method'])
            if exec_['backup_method1'] is not None:
                cmd += " {0}".format(exec_['backup_method1'])
                if exec_['backup_method2'] is not None:
                    cmd += " {0}".format(exec_['backup_method2'])
        cmds.append(cmd)

    return cmds


def main():
    """entry point for module execution
    """

    coa_enable_spec = dict(
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    coa_ignore_spec = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        request=dict(type='str', required=True, choices=['disable-port', 'dm-request', 'flip-port', 'modify-acl', 'reauth-host'])
    )
    commands_spec = dict(
        privilege_level=dict(type='int', required=True, choices=[0, 4, 5]),
        primary_method=dict(type='str', required=True, choices=['radius', 'tacacs+', 'none']),
        backup_method1=dict(type='str', choices=['radius', 'tacacs+', 'none']),
        backup_method2=dict(type='str', choices=['none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    exec_spec = dict(
        primary_method=dict(type='str', required=True, choices=['radius', 'tacacs+', 'none']),
        backup_method1=dict(type='str', choices=['radius', 'tacacs+', 'none']),
        backup_method2=dict(type='str', choices=['none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    argument_spec = dict(
        coa_ignore=dict(type='dict', options=coa_ignore_spec),
        coa_enable=dict(type='dict', options=coa_enable_spec),
        commands=dict(type='dict', options=commands_spec),
        exec_=dict(type='dict', options=exec_spec)
    )

    required_one_of = [['coa_enable', 'coa_ignore', 'commands', 'exec_']]
    module = AnsibleModule(argument_spec=argument_spec,
                           required_one_of=required_one_of,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    coa_enable = module.params["coa_enable"]
    coa_ignore = module.params["coa_ignore"]
    commands = module.params["commands"]
    exec_ = module.params["exec_"]

    if warnings:
        results['warnings'] = warnings

    commands = build_command(module, coa_enable, coa_ignore, commands, exec_)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
