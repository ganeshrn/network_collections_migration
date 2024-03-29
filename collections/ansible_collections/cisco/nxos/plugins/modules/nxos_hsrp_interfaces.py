#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Cisco and/or its affiliates.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The module file for nxos_hsrp_interfaces
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'network'
}

DOCUMENTATION = '''module: nxos_hsrp_interfaces
short_description: Manages HSRP attributes of NXOS interfaces.
description: Manages Hot Standby Router Protocol (HSRP) interface attributes.
author: Chris Van Heuveln (@chrisvanheuveln)
notes: null
options:
  config:
    description: The provided configuration
    type: list
    elements: dict
    suboptions:
      name:
        type: str
        description: The name of the interface.
      bfd:
        type: str
        description:
        - Enable/Disable HSRP Bidirectional Forwarding Detection (BFD) on the interface.
        choices:
        - enable
        - disable
  state:
    description:
    - The state the configuration should be left in
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    default: merged
'''
EXAMPLES = """
# Using deleted

- name: Configure hsrp attributes on interfaces
  nxos_hsrp_interfaces:
    config:
      - name: Ethernet1/1
      - name: Ethernet1/2
    operation: deleted


# Using merged

- name: Configure hsrp attributes on interfaces
  nxos_hsrp_interfaces:
    config:
      - name: Ethernet1/1
        bfd: enable
      - name: Ethernet1/2
        bfd: disable
    operation: merged


# Using overridden

- name: Configure hsrp attributes on interfaces
  nxos_hsrp_interfaces:
    config:
      - name: Ethernet1/1
        bfd: enable
      - name: Ethernet1/2
        bfd: disable
    operation: overridden


# Using replaced

- name: Configure hsrp attributes on interfaces
  nxos_hsrp_interfaces:
    config:
      - name: Ethernet1/1
        bfd: enable
      - name: Ethernet1/2
        bfd: disable
    operation: replaced


"""
RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The resulting configuration model invocation.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['interface Ethernet1/1', 'hsrp bfd']
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.hsrp_interfaces.hsrp_interfaces import Hsrp_interfacesArgs
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.hsrp_interfaces.hsrp_interfaces import Hsrp_interfaces


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=Hsrp_interfacesArgs.argument_spec,
                           supports_check_mode=True)

    result = Hsrp_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
