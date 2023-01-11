#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: icx_mct
author: "Ruckus Wireless (@Commscope)"
short_description: Configures mct in Ruckus ICX 7000 series switches.
description:
  - Configures mct in Ruckus ICX 7000 series switches.
options:
  cluster_name:
    description: Specifies the cluster name as an ASCII string. The cluster name can be up to 64 characters in length.
    type: str
  cluster_id:
    description: Specifies the cluster ID. The ID value range can be from 1 through 4095.
    type: int
    required: true
  state:
    description: Specifies whether to Configure/remove the MCT cluster configuration.
    type: str
    default: present
    choices: ['present', 'absent']
  rbridge_id:
    description: Specifies local rbridge id of the Cluster.
    type: dict
    suboptions:
      id:
        description: Specifies Cluster RBridge ID. The ID value range can be from 1 through 4095.
        type: int
        required: true
      state:
        description: Specifies whether to Configure/remove the rbridge id.
        type: str
        default: present
        choices: ['present', 'absent']
  session_vlan:
    description: Assign a session vlan for cluster management.
    type: dict
    suboptions:
      vlan_id:
        description: Specifies cluster session vlan id. The ID value range can be from 1 through 4089)
        type: int
        required: true
      state:
        description: Specifies whether to Configure/remove the session vlan id.
        type: str
        default: present
        choices: ['present', 'absent']
  keep_alive_vlan:
    description: Configures a keep-alive VLAN for the cluster.
    type: dict
    suboptions:
      vlan_id:
        description: Specifies the VLAN number. The values can be from 1 through 4089.
        type: int
        required: true
      state:
        description: Specifies whether to Configure/remove the keep-alive VLAN configuration.
        type: str
        default: present
        choices: ['present', 'absent']
  icl:
    description: Define the inter chassis link properties.
    type: dict
    suboptions:
      name:
        description: Specifies Inter Chassis Link Name (up to 64 characters)
        type: str
        required: true
      ethernet:
        description: Specifies ethernet port.
        type: str
      lag:
        description: Specifies lag interface.
        type: int
      state:
        description: Specifies whether to Configure/remove the inter chassis link.
        type: str
        default: present
        choices: ['present', 'absent']
  peer:
    description: Define the cluster peer information.
    type: dict
    suboptions:
      ip:
        description: Specifies the IP address of the cluster peer device.
        type: str
        required: true
      disable_fast_failover:
        description: Disables the MCT fast-failover mode for the peer.
        type: bool
      rbridge:
        description: defines Cluster peer rbridge id.
        type: dict
        suboptions:
          id:
            description: Specifies Cluster peer rbridge id. The ID value range can be from 1 through 4095.
            type: int
            required: true
          icl_name:
            description: Specifies mapped ICL Name (up to 64 characters)
            type: str
          state:
            description: Specifies whether to Configure/remove cluster peer rbridge id.
            type: str
            default: present
            choices: ['present', 'absent']
      timers:
        description: Configures the keep-alive and hold-time timers for cluster peer.
        type: dict
        suboptions:
          keep_alive:
            description: Specifies the keep-alive interval in seconds. The value can range from 0 through 21845 seconds.
                         default value is 10 seconds.
            type: int
            required: true
          hold_time:
            description: Specifies the hold-time interval in seconds. The value can range from 3 through 65535 seconds
                        (or 0 if the keep-alive timer is set to 0)
                        default value is 90 seconds.
            type: int
            required: true
          state:
            description: Specifies whether to Configure timers or remove timers and sets to the default values.
            type: str
            default: present
            choices: ['present', 'absent']
  client_interfaces:
    description: Shuts down all the local client interfaces in the cluster.
    type: str
    choices: ['present', 'absent']
  client_isolation:
    description: Isolates the client from the network when Cluster Communication Protocol (CCP) is not operational.
    type: str
    choices: ['present', 'absent']
  client_auto_detect:
    description: Define Cluster Client Automatic Detection.
    type: dict
    suboptions:
      config:
        description: Configures the automatically detected cluster clients into the running configuration and deploys all of the automatically detected clients.
        type: dict
        suboptions:
          deploy_all:
            description: Deploys all automatically detected cluster clients.
            type: bool
          state:
            description: Specifies whether to configure/remove deployed automatically detected cluster clients.
            type: str
            default: present
            choices: ['present', 'absent']
      ethernet:
        description: Enables cluster client automatic configuration on a specific port or range of ports.
        type: dict
        suboptions:
          port:
            description: Specifies the Ethernet port on which you want to enable the cluster client automatic configuration.
            type: str
            required: true
          state:
            description: Specifies whether to enable/disable the cluster client automatic configuration on the ports.
            type: str
            default: present
            choices: ['present', 'absent']
      start:
        description: Starts the cluster client automatic configuration.
        type: dict
        suboptions:
          config_deploy_all:
            description: Configures and deploys all automatically detected clients.
            type: bool
          state:
            description: Specifies whether to configure/remove deployed automatically detected cluster clients.
            type: str
            default: present
            choices: ['present', 'absent']
      stop:
        description: Stops the automatic configuration process of the running cluster client.
        type: bool
  deploy:
    description: specify to  deploy the cluster client.
    type: str
    choices: ['present', 'absent']
  client:
    description: Define to configure the cluster client properties.
    type: list
    elements: dict
    suboptions:
      name:
        description: Specifies the name of the client. The client name can be up to 64 characters in length.
        type: str
        required: true
      rbridge_id:
        description: Define a rbridge id to the Client
        type: dict
        suboptions:
          id:
            description: Specifies Cluster Client RBridge ID. The ID value range can be from 1 through 4095
            type: int
            required: true
          state:
            description: Specifies whether to Configure/remove the rbridge id.
            type: str
            default: present
            choices: ['present', 'absent']
      client_interface:
        description: Configures the physical port or static LAG port as the Cluster Client Edge Port (CCEP).
        type: dict
        suboptions:
          ethernet:
            description: Configures the specified Ethernet port as the client CCEP.
            type: str
          lag:
            description: Configures the specified LAG as the client CCEP.
            type: int
          state:
            description: Specifies whether to Configure/remove the port.
            type: str
            default: present
            choices: ['present', 'absent']
      deploy:
        description: specify to  deploy the cluster client.
        type: str
        choices: ['present', 'absent']
      state:
        description: Specifies whether to Configure/removes the cluster client.
        type: str
        default: present
        choices: ['present', 'absent']

"""

EXAMPLES = """
- name: configure mct
  commscope.icx.icx_mct:
    cluster_name: test
    cluster_id: 100
    state: present
    rbridge_id:
      id: 10
      state: present
    session_vlan:
      vlan_id: 3000
    keep_alive_vlan:
      vlan_id: 3001
- name: configure icl, peer
  commscope.icx.icx_mct:
    cluster_id: 100
    icl:
      name: 'ICL'
      lag: 2
    peer:
      ip: 10.1.1.2
      rbridge:
        id: 2
        icl_name: ICL
    deploy: present
- name: configure mct client
  commscope.icx.icx_mct:
    cluster_id: 100
    client:
      name: client_1
      rbridge_id:
        id: 200
      client_interface:
        lag: 5
      deploy: present
      state: present
- name: removing mct cluster
  commscope.icx.icx_mct:
    cluster_id: 100
    state: absent
"""
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import ConnectionError, exec_command
from ansible_collections.commscope.icx.plugins.module_utils.network.icx.icx import load_config


def build_command(
        module, cluster_name=None, cluster_id=None, state=None, rbridge_id=None, session_vlan=None, keep_alive_vlan=None,
        icl=None, peer=None, client_interfaces=None, client_isolation=None,
        client_auto_detect=None, deploy=None, client=None):
    cmds = []
    if state == 'absent':
        cmd = "no cluster"
    else:
        cmd = "cluster"
    if cluster_name is not None:
        cmd += " {0}".format(cluster_name)
    if cluster_id is not None:
        cmd += " {0}".format(cluster_id)
    cmds.append(cmd)
    if state == 'present':
        if deploy == 'absent':
            cmd = "no deploy"
            cmds.append(cmd)
        if rbridge_id is not None:
            if rbridge_id['state'] == 'absent':
                cmd = "no rbridge-id {0}".format(rbridge_id['id'])
            else:
                cmd = "rbridge-id {0}".format(rbridge_id['id'])
            cmds.append(cmd)
        if session_vlan is not None:
            if session_vlan['state'] == 'present':
                cmd = "session-vlan {0}".format(session_vlan['vlan_id'])
                cmds.append(cmd)
        if keep_alive_vlan is not None:
            if keep_alive_vlan['state'] == 'absent':
                cmd = "no keep-alive-vlan {0}".format(keep_alive_vlan['vlan_id'])
            else:
                cmd = "keep-alive-vlan {0}".format(keep_alive_vlan['vlan_id'])
            cmds.append(cmd)
        if icl is not None:
            if icl['state'] == 'present':
                cmd = "icl {0}".format(icl['name'])
                if icl['ethernet'] is not None:
                    cmd += " ethernet {0}".format(icl['ethernet'])
                elif icl['lag'] is not None:
                    cmd += " lag {0}".format(icl['lag'])
                cmds.append(cmd)
        if peer is not None:
            if peer['rbridge'] is not None:
                if peer['rbridge']['state'] == 'present':
                    cmd = "peer {0} rbridge-id {1}".format(peer['ip'], peer['rbridge']['id'])
                    if peer['rbridge']['icl_name'] is not None:
                        cmd += " icl {0}".format(peer['rbridge']['icl_name'])
                    cmds.append(cmd)
            if peer['disable_fast_failover'] is not None:
                if peer['disable_fast_failover']:
                    cmd = "peer {0} disable-fast-failover".format(peer['ip'])
                else:
                    cmd = "no peer {0} disable-fast-failover".format(peer['ip'])
                cmds.append(cmd)
            if peer['timers'] is not None:
                if peer['timers']['state'] == 'absent':
                    cmd = "no peer {0} timers".format(peer['ip'])
                else:
                    cmd = "peer {0} timers".format(peer['ip'])

                if peer['timers']['keep_alive'] is not None:
                    cmd += " keep-alive {0}".format(peer['timers']['keep_alive'])
                if peer['timers']['hold_time'] is not None:
                    cmd += " hold-time {0}".format(peer['timers']['hold_time'])
                cmds.append(cmd)
            if peer['rbridge'] is not None:
                if peer['rbridge']['state'] == 'absent':
                    cmd = "no peer {0} rbridge-id {1}".format(peer['ip'], peer['rbridge']['id'])
                    if peer['rbridge']['icl_name'] is not None:
                        cmd += " icl {0}".format(peer['rbridge']['icl_name'])
                    cmds.append(cmd)
        if icl is not None:
            if icl['state'] == 'absent':
                cmd = "no icl {0}".format(icl['name'])
                if icl['ethernet'] is not None:
                    cmd += " ethernet {0}".format(icl['ethernet'])
                elif icl['lag'] is not None:
                    cmd += " lag {0}".format(icl['lag'])
                cmds.append(cmd)
        if session_vlan is not None:
            if session_vlan['state'] == 'absent':
                cmd = "no session-vlan {0}".format(session_vlan['vlan_id'])
                cmds.append(cmd)

        if client_interfaces is not None:
            if client_interfaces == 'absent':
                cmd = "no client-interfaces shutdown"
            else:
                cmd = "client-interfaces shutdown"
            cmds.append(cmd)
        if client_isolation is not None:
            if client_isolation == 'absent':
                cmd = "no client-isolation strict"
            elif client_isolation == 'present':
                cmd = "client-isolation strict"
            cmds.append(cmd)
        if client_auto_detect is not None:
            if client_auto_detect['config'] is not None:
                if client_auto_detect['config']['state'] == 'absent':
                    cmd = "no client-auto-detect config"
                else:
                    cmd = "client-auto-detect config"
                if client_auto_detect['config']['deploy_all']:
                    cmd += " deploy-all"
                cmds.append(cmd)
            if client_auto_detect['stop']:
                cmd = "client-auto-detect stop"
                cmds.append(cmd)
            if client_auto_detect['ethernet'] is not None:
                if client_auto_detect['ethernet']['state'] == 'absent':
                    cmd = "no client-auto-detect ethernet {0}".format(client_auto_detect['ethernet']['port'])
                else:
                    cmd = "client-auto-detect ethernet {0}".format(client_auto_detect['ethernet']['port'])
                cmds.append(cmd)
            if client_auto_detect['start'] is not None:
                if client_auto_detect['start']['state'] == 'present':
                    cmd = "client-auto-detect start"
                    if client_auto_detect['start']['config_deploy_all']:
                        cmd += " config-deploy-all"
                    cmds.append(cmd)
        if deploy == 'present':
            cmd = "deploy"
            cmds.append(cmd)
        if client is not None:
            for clients in client:
                if clients['name'] is not None:
                    if clients['state'] == 'absent':
                        cmd = "no client {0}".format(clients['name'])
                    else:
                        cmd = "client {0}".format(clients['name'])
                    cmds.append(cmd)
                if clients['state'] == 'present':
                    if clients['deploy'] == 'absent':
                        cmd = "no deploy"
                        cmds.append(cmd)
                    if clients['rbridge_id'] is not None:
                        if clients['rbridge_id']['state'] == 'absent':
                            cmd = "no rbridge-id {0}".format(clients['rbridge_id']['id'])
                        else:
                            cmd = "rbridge-id {0}".format(clients['rbridge_id']['id'])
                        cmds.append(cmd)
                    if clients['client_interface'] is not None:
                        if clients['client_interface']['state'] == 'absent':
                            cmd = "no client-interface"
                        else:
                            cmd = "client-interface"
                        if clients['client_interface']['ethernet'] is not None:
                            cmd += " ethernet {0}".format(clients['client_interface']['ethernet'])
                        elif clients['client_interface']['lag'] is not None:
                            cmd += " lag {0}".format(clients['client_interface']['lag'])
                        cmds.append(cmd)
                if clients['deploy'] == 'present':
                    cmd = "deploy"
                    cmds.append(cmd)

    return cmds


def main():
    """entry point for module execution
    """

    rbridge_id_spec = dict(
        id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    session_vlan_spec = dict(
        vlan_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    keep_alive_vlan_spec = dict(
        vlan_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    icl_spec = dict(
        name=dict(type='str', required=True),
        ethernet=dict(type='str'),
        lag=dict(type='int'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    rbridge_spec = dict(
        id=dict(type='int', required=True),
        icl_name=dict(type='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    timers_spec = dict(
        keep_alive=dict(type='int', required=True),
        hold_time=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    peer_spec = dict(
        ip=dict(type='str', required=True),
        disable_fast_failover=dict(type='bool'),
        rbridge=dict(type='dict', options=rbridge_spec),
        timers=dict(type='dict', options=timers_spec)
    )
    config_spec = dict(
        deploy_all=dict(type='bool'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    ethernet_spec = dict(
        port=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    start_spec = dict(
        config_deploy_all=dict(type='bool'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    client_auto_detect_spec = dict(
        config=dict(type='dict', options=config_spec),
        ethernet=dict(type='dict', options=ethernet_spec),
        start=dict(type='dict', options=start_spec),
        stop=dict(type='bool')
    )
    client_rbridge_id_spec = dict(
        id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    client_interface_spec = dict(
        ethernet=dict(type='str'),
        lag=dict(type='int'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    client_spec = dict(
        name=dict(type='str', required=True),
        rbridge_id=dict(type='dict', options=client_rbridge_id_spec),
        client_interface=dict(type='dict', options=client_interface_spec, required_one_of=[['ethernet', 'lag']],
                              mutually_exclusive=[['ethernet', 'lag']]),
        deploy=dict(type='str', choices=['present', 'absent']),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    argument_spec = dict(
        cluster_name=dict(type='str'),
        cluster_id=dict(type='int', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent']),
        rbridge_id=dict(type='dict', options=rbridge_id_spec),
        session_vlan=dict(type='dict', options=session_vlan_spec),
        keep_alive_vlan=dict(type='dict', options=keep_alive_vlan_spec),
        icl=dict(type='dict', options=icl_spec, required_one_of=[['ethernet', 'lag']], mutually_exclusive=[['ethernet', 'lag']]),
        peer=dict(type='dict', options=peer_spec, required_one_of=[['disable_fast_failover', 'rbridge', 'timers']]),
        client_interfaces=dict(type='str', choices=['present', 'absent']),
        client_isolation=dict(type='str', choices=['present', 'absent']),
        client_auto_detect=dict(type='dict', options=client_auto_detect_spec, required_one_of=[['config', 'ethernet', 'start', 'stop']]),
        deploy=dict(type='str', choices=['present', 'absent']),
        client=dict(type='list', elements='dict', options=client_spec)
    )
    mutually_exclusive = [['keep_alive_vlan', 'client_isolation']]
    module = AnsibleModule(argument_spec=argument_spec,
                           mutually_exclusive=mutually_exclusive,
                           supports_check_mode=True)

    warnings = list()
    results = {'changed': False}
    cluster_name = module.params["cluster_name"]
    cluster_id = module.params["cluster_id"]
    state = module.params["state"]
    rbridge_id = module.params["rbridge_id"]
    session_vlan = module.params["session_vlan"]
    keep_alive_vlan = module.params["keep_alive_vlan"]
    icl = module.params["icl"]
    peer = module.params["peer"]
    client_interfaces = module.params["client_interfaces"]
    client_isolation = module.params["client_isolation"]
    client_auto_detect = module.params["client_auto_detect"]
    deploy = module.params["deploy"]
    client = module.params["client"]

    if warnings:
        results['warnings'] = warnings

    commands = build_command(
        module, cluster_name, cluster_id, state, rbridge_id, session_vlan, keep_alive_vlan, icl,
        peer, client_interfaces, client_isolation, client_auto_detect, deploy, client)
    results['commands'] = commands

    if commands:
        if not module.check_mode:
            response = load_config(module, commands)

        results['changed'] = True

    module.exit_json(**results)


if __name__ == '__main__':
    main()
