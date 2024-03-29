#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
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
The module file for eos_lag_interfaces
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'network'
}

DOCUMENTATION = '''module: eos_lag_interfaces
short_description: Manages link aggregation groups on Arista EOS devices
description: This module manages attributes of link aggregation groups on Arista EOS
  devices.
author: Nathaniel Case (@Qalthos)
notes:
- Tested against Arista EOS 4.20.10M
- This module works with connection C(network_cli). See the L(EOS Platform Options,../network/user_guide/platform_eos.html).
options:
  config:
    description: A list of link aggregation group configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Name of the port-channel interface of the link aggregation group (LAG) e.g.,
          Port-Channel5.
        type: str
        required: true
      members:
        description:
        - Ethernet interfaces that are part of the group.
        type: list
        elements: dict
        suboptions:
          member:
            description:
            - Name of ethernet interface that is a member of the LAG.
            type: str
          mode:
            description:
            - LAG mode for this interface.
            type: str
            choices:
            - active
            - 'on'
            - passive
  state:
    description:
    - The state of the configuration after module completion.
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    default: merged
'''

EXAMPLES = """
---

# Using merged

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#   channel group 5 mode on
# interface Ethernet2

- name: Merge provided LAG attributes with existing device configuration
  eos_lag_interfaces:
    config:
      - name: 5
        members:
          - member: Ethernet2
            mode: on
    state: merged

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
#   channel group 5 mode on
# interface Ethernet2
#   channel group 5 mode on


# Using replaced

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#   channel group 5 mode on
# interface Ethernet2

- name: Replace all device configuration of specified LAGs with provided configuration
  eos_lag_interfaces:
    config:
      - name: 5
        members:
          - member: Ethernet2
            mode: on
    state: replaced

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
# interface Ethernet2
#   channel group 5 mode on


# Using overridden

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#   channel group 5 mode on
# interface Ethernet2

- name: Override all device configuration of all LAG attributes with provided configuration
  eos_lag_interfaces:
    config:
      - name: 10
        members:
          - member: Ethernet2
            mode: on
    state: overridden

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
# interface Ethernet2
#   channel group 10 mode on


# Using deleted

# Before state:
# -------------
#
# veos#show running-config | section interface
# interface Ethernet1
#   channel group 5 mode on
# interface Ethernet2
#   channel group 5 mode on

- name: Delete LAG attributes of the given interfaces.
  eos_lag_interfaces:
    config:
      - name: 5
        members:
          - member: Ethernet1
    state: deleted

# After state:
# ------------
#
# veos#show running-config | section interface
# interface Ethernet1
# interface Ethernet2
#   channel group 5 mode on


"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['command 1', 'command 2', 'command 3']
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.arista.eos.plugins.module_utils.network.eos.argspec.lag_interfaces.lag_interfaces import Lag_interfacesArgs
from ansible_collections.arista.eos.plugins.module_utils.network.eos.config.lag_interfaces.lag_interfaces import Lag_interfaces


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=Lag_interfacesArgs.argument_spec,
                           supports_check_mode=True)

    result = Lag_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
