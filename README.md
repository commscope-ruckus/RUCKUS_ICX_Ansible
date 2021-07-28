# Commscope ICX collection
The Ansible Commscope ICX collection includes a variety of Ansible content to help automate the management of Commscope ICX network devices.

This collection has been tested against Commscope ICX version 08.0.95

## Ansible version compatability
This collection has been tested against following Ansible versions: >=2.9.10.

Plugins and modules within a collection may be tested with only specific Ansible versions. A collection may contain metadata that identifies these versions. PEP440 is the schema used to describe the versions of Ansible.

### Supported connections
The Commscope ICX collection supports network_cli connections.

## Included content

<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
commscope.icx.icx|Use icx cliconf to run command on Commscope ICX platform

### Modules
Name | Description
--- | ---
commscope.icx.icx_banner|Manage multiline banners on Ruckus ICX 7K series switches
commscope.icx.icx_command|Run arbitrary commands on remote Ruckus ICX 7K series switches
commscope.icx.icx_config|Manage configuration sections of Ruckus ICX 7K series switches
commscope.icx.icx_copy|Transfer files from or to remote Ruckus ICX 7K series switches
commscope.icx.icx_facts|Collect facts from remote Ruckus ICX 7K series switches
commscope.icx.icx_firmware_upgrade|Upgrades firmware of Ruckus ICX 7K series switches
commscope.icx.icx_interface|Manage Interface on Ruckus ICX 7K series switches
commscope.icx.icx_l3_interface|Manage Layer-3 interfaces on Ruckus ICX 7K series switches
commscope.icx.icx_linkagg|Manage link aggregation groups on Ruckus ICX 7K series switches
commscope.icx.icx_lldp|Manage LLDP configuration on Ruckus ICX 7K series switches
commscope.icx.icx_logging|Manage logging on Ruckus ICX 7K series switches
commscope.icx.icx_ping|Tests reachability using ping from Ruckus ICX 7K series switches
commscope.icx.icx_qos|Configures qos features on ICX 7K series switches
commscope.icx.icx_rate_limit|Configures rate limit on ICX 7K switch
commscope.icx.icx_static_route|Manage static IP routes on Ruckus ICX 7K series switches
commscope.icx.icx_static_route6|Manage static IPV6 routes on Ruckus ICX 7K series switches
commscope.icx.icx_system|Manage the system attributes on Ruckus ICX 7K series switches
commscope.icx.icx_user|Manage the user accounts on Ruckus ICX 7K series switches
commscope.icx.icx_vlan|Manage VLANs on Ruckus ICX 7K series switches

<!--end collection content-->
## Installing this collection

You can install the Commscope ICX collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install commscope.icx

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: commscope.icx
```
## Using this collection


This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the Commscope ICX collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `commscope.icx.icx_vlan`.
The following example task replaces configuration changes in the existing configuration on a Cisco IOS network device, using the FQCN:

```yaml
---
  - name: Add a single ethernet 1/1/48 as access(untagged) port to vlan 20
    commscope.icx.icx_vlan:
      name: test-vlan
      vlan_id: 20
      interfaces:
        name:
          - ethernet 1/1/48

```

**NOTE**: For Ansible 2.9, you may not see deprecation warnings when you run your playbooks with this collection. Use this documentation to track when a module is deprecated.


### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

If you find problems, please open an issue against the [Commscope ICX collection repository](https://github.com/commscope-ruckus/commscope.icx). 

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Release notes
<!--Add a link to a changelog.md file or an external docsite to cover this information. -->
Release notes will be added soon.

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
