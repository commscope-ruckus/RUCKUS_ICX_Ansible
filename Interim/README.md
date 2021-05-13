# Ansible-Release Interim module updates

The ansible module in this folder are interim updates which are yet to be approved by Ansible community.
The Interim ansible modules are submitted to community for approval on quarterly basis [JFM/AMJ/JAS/OND].

# Documentation for ICX module that are part of official ansible release:
https://docs.ansible.com/ansible/2.9/modules/list_of_network_modules.html#icx

To use interim release:
1. Download ansible.tar.gz and easy_install
2. Run on terminal:
- chmod +x easy_install
- ./easy_instal
Above commands will detect where Ansible is installed, overwrite modified files and add new icx_modules.

# Bug Jiras:Modules
FI-223408:Ping to self fails, FI-218627:ICX ping validation playbook failing sporadically due to timeout errors: icx_ping.py  

FI-220089:skip for all modules, change check_running_config default: icx_banner.py, icx_config.py, icx_facts.py, icx_l3_interface.py, icx_lldp.py, icx_ping.py, icx_system.py,  icx_vlan.py, icx_command.py, icx_copy.py,icx_interface.py, icx_linkagg.py, icx_logging.py, icx_static_route.py, icx_user.py

FI-223410:unable to add a new vlan to interface as tagged or untagged, FI-218629:Unable to perform purge operation using ansible icx_vlan module, FI-218628:Incorrect interface configured under vlan using icx_vlan module, FI-215508:Unable to configure dhcp snooping and arp inspection using vlan playbook: icx_vlan.py

FI-215386:ip ssh pub-key-file tftp ip rsa_pub_keys.txt command missing line break hence prompt is missing: icx_command.py

FI-216707:visible errors in this module…, FI-220009:ansible_net_neighbors in playbook_facts.yml returns null value: icx_facts.py

FI-216695:Unable to config 'radius server', 'radius key', and 'aaa authentication' parameter using playbook icx_system: icx_system.py  


