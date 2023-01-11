#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_aaa_authentication
author: "Ruckus Wireless (@Commscope)"
short_description: Configures AAA authentication in Ruckus ICX 7000 series switches
description:
  - Configures AAA authentication in Ruckus ICX 7000 series switches.
options:
  dot1x:
    description: Enables 802.1X and MAC authentication."none" is not supported from 9.0.0
    default: null
    type: dict
    suboptions:
      primary_method:
        description: Primary authentication method.
        type: str
        required: true
        choices: ['radius','none']
      backup_method1:
        description: Backup authentication method if primary method fails.
        type: str
        choices: ['none']
      state:
        description: Specifies whether to configure or remove authentication.
        type: str
        default: present
        choices: ['present', 'absent']
  enable:
    description: Configures the AAA authentication method for securing access to the Privileged EXEC level and global configuration levels of the CLI.
                 Only one of method-list or implicit-user should be provided. If the configured primary authentication fails due to an error,
                 the device tries the backup authentication methods in the order they appear in the list.
                 Only local, radius and tacacs+ methods are supported from 9.0.0
    default: null
    type: dict
    suboptions:
      primary_method:
        description: Primary authentication method.
        type: str
        choices: ['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']
      backup_method_list:
        description: Backup authentication method if primary method fails.
        type: list
        elements: str
        choices: ['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']
      implicit_user:
        description: Configures the device to prompt only for a password when a user attempts to
                     gain Super User access to the Privileged EXEC and global configuration levels of the CLI.
        type: bool
      state:
        description: Specifies whether to configure or remove the authentication method.
        type: str
        default: present
        choices: ['present', 'absent']
  login:
    description: Configures the AAA authentication method for securing access to the Privileged EXEC level and global configuration levels of the CLI.
                 Only one of metod-list or implicit-user should be provided.
                 Only local, radius, tacacs+ methods are supported from 9.0.0
    default: null
    type: dict
    suboptions:
      primary_method:
        description: Primary authentication method.
        type: str
        choices: ['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']
      backup_method_list:
        description: Backup authentication method if primary method fails.
        type: list
        elements: str
        choices: ['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']
      privilege_mode:
        description: Configures the device to enter the privileged EXEC mode after a successful login through Telnet or SSH..
        type: bool
        default: false
      state:
        description: Specifies whether to configure or remove the authentication method.
        type: str
        default: present
        choices: ['present', 'absent']
  snmp_server:
    description: Configures the AAA authentication method for SNMP server access.
                 Only local, radius, tacacs+ methods are supported from 9.0.0
    default: null
    type: dict
    suboptions:
      primary_method:
        description: Primary authentication method.
        type: str
        required: true
        choices: ['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']
      backup_method_list:
        description: Backup authentication method if primary method fails.
        type: list
        elements: str
        choices: ['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']
      state:
        description: Specifies whether to configure or remove the authentication method.
        type: str
        default: present
        choices: ['present', 'absent']
  web_server:
    description: Configures the AAA authentication method to access the device through the Web Management Interface.
                 Only local, radius, tacacs+ methods are supported from 9.0.0
    default: null
    type: dict
    suboptions:
      primary_method:
        description: Primary authentication method.
        type: str
        required: true
        choices: ['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']
      backup_method_list:
        description: Backup authentication method if primary method fails.
        type: list
        elements: str
        choices: ['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']
      state:
        description: Specifies whether to configure or remove the authentication method.
        type: str
        default: present
        choices: ['present', 'absent']
"""
EXAMPLES = """
- name: configure aaa authentication dot1x and enable
  community.network.icx_aaa_authentication:
    dot1x:
      primary_method: none
      state: present
    enable:
      primary_method: radius
      backup_method_list:
        - enable
        - line
      state: present
- name: disable aaa authentication for web-server
  community.network.icx_aaa_authentication:
    web-server:
      primary_method: tacacs+
      backup_method_list:
        - radius
        - none
      state: absent
"""
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(module, dot1x=None, enable=None, login=None, snmp_server=None, web_server=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """
    cmds = []
    if dot1x is not None:
        if dot1x['state'] == 'absent':
            cmd = "no aaa authentication dot1x default"
        else:
            cmd = "aaa authentication dot1x default"
        if dot1x['primary_method'] is not None:
            cmd += " {0}".format(dot1x['primary_method'])
            if dot1x['backup_method1'] is not None:
                cmd += " {0}".format(dot1x['backup_method1'])
        cmds.append(cmd)

    if enable is not None:
        if enable['primary_method'] is not None:
            if enable['state'] == 'absent':
                cmd = "no aaa authentication enable default {0}".format(enable['primary_method'])
            else:
                cmd = "aaa authentication enable default {0}".format(enable['primary_method'])
            if enable['backup_method_list'] is not None:
                cmd += " " + " ".join(enable['backup_method_list'])
            cmds.append(cmd)
        elif enable['implicit_user'] is not None:
            if enable['implicit_user']:
                cmd = "aaa authentication enable implicit-user"
            else:
                cmd = "no aaa authentication enable implicit-user"
            cmds.append(cmd)

    if login is not None:
        if login['primary_method'] is not None:
            if login['state'] == 'absent':
                cmd = "no aaa authentication login default {0}".format(login['primary_method'])
            else:
                cmd = "aaa authentication login default {0}".format(login['primary_method'])
            if login['backup_method_list'] is not None:
                cmd += " " + " ".join(login['backup_method_list'])
            cmds.append(cmd)
        elif login['privilege_mode'] is not None:
            if login['state'] == 'absent':
                cmd = "no aaa authentication login privilege-mode"
            else:
                cmd = "aaa authentication login privilege-mode"
            cmds.append(cmd)

    if snmp_server is not None:
        if snmp_server['state'] == 'absent':
            cmd = "no aaa authentication snmp-server default {0}".format(snmp_server['primary_method'])
        else:
            cmd = "aaa authentication snmp-server default {0}".format(snmp_server['primary_method'])
        if snmp_server['backup_method_list'] is not None:
            cmd += " " + " ".join(snmp_server['backup_method_list'])
        cmds.append(cmd)

    if web_server is not None:
        if web_server['state'] == 'absent':
            cmd = "no aaa authentication web-server default {0}".format(web_server['primary_method'])
        else:
            cmd = "aaa authentication web-server default {0}".format(web_server['primary_method'])
        if web_server['backup_method_list'] is not None:
            cmd += " " + " ".join(web_server['backup_method_list'])
        cmds.append(cmd)

    return cmds


def main():
    """entry point for module execution
    """
    dot1x_spec = dict(
        primary_method=dict(type='str', required=True, choices=['radius', 'none']),
        backup_method1=dict(type='str', choices=['none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    enable_spec = dict(
        primary_method=dict(type='str', choices=['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
        backup_method_list=dict(type='list', elements='str', choices=['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
        implicit_user=dict(type='bool'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    login_spec = dict(
        primary_method=dict(type='str', choices=['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
        backup_method_list=dict(type='list', elements='str', choices=['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
        privilege_mode=dict(type='bool', default=False),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    snmp_server_spec = dict(
        primary_method=dict(type='str', required=True, choices=['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
        backup_method_list=dict(type='list', elements='str', choices=['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    web_server_spec = dict(
        primary_method=dict(type='str', required=True, choices=['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
        backup_method_list=dict(type='list', elements='str', choices=['enable', 'line', 'local', 'radius', 'tacacs', 'tacacs+', 'none']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    argument_spec = dict(
        dot1x=dict(type='dict', options=dot1x_spec),
        enable=dict(type='dict', options=enable_spec),
        login=dict(type='dict', options=login_spec),
        snmp_server=dict(type='dict', options=snmp_server_spec),
        web_server=dict(type='dict', options=web_server_spec)
    )
    required_one_of = [['dot1x', 'enable', 'login', 'snmp_server', 'web_server']]
    module = AnsibleModule(argument_spec=argument_spec,
                           required_one_of=required_one_of,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    dot1x = module.params["dot1x"]
    enable = module.params["enable"]
    login = module.params["login"]
    snmp_server = module.params["snmp_server"]
    web_server = module.params["web_server"]

    if warnings:
        results['warnings'] = warnings
    commands = build_command(module, dot1x, enable, login, snmp_server, web_server)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)
        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
