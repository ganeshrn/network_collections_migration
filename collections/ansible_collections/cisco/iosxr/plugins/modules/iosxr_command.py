#!/usr/bin/python
#
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = '''module: iosxr_command
author: Ricardo Carrillo Cruz (@rcarrillocruz)
short_description: Run commands on remote devices running Cisco IOS XR
description:
- Sends arbitrary commands to an IOS XR node and returns the results read from the
  device. This module includes an argument that will cause the module to wait for
  a specific condition before returning or timing out if the condition is not met.
- This module does not support running commands in configuration mode. Please use
  M(iosxr_config) to configure iosxr devices.
extends_documentation_fragment:
- cisco.iosxr.iosxr
notes:
- This module works with C(network_cli). See L(the IOS-XR Platform Options,../network/user_guide/platform_iosxr.html).
- This module does not support C(netconf) connection.
- Tested against IOS XR 6.1.3
options:
  commands:
    description:
    - List of commands to send to the remote iosxr device over the configured provider.
      The resulting output from the command is returned. If the I(wait_for) argument
      is provided, the module is not returned until the condition is satisfied or
      the number of retries has expired.
    required: true
  wait_for:
    description:
    - List of conditions to evaluate against the output of the command. The task will
      wait for each condition to be true before moving forward. If the conditional
      is not true within the configured number of retries, the task fails. See examples.
    aliases:
    - waitfor
  match:
    description:
    - The I(match) argument is used in conjunction with the I(wait_for) argument to
      specify the match policy.  Valid values are C(all) or C(any).  If the value
      is set to C(all) then all conditionals in the wait_for must be satisfied.  If
      the value is set to C(any) then only one of the values must be satisfied.
    default: all
    choices:
    - any
    - all
  retries:
    description:
    - Specifies the number of retries a command should by tried before it is considered
      failed. The command is run on the target device every retry and evaluated against
      the I(wait_for) conditions.
    default: 10
  interval:
    description:
    - Configures the interval in seconds to wait between retries of the command. If
      the command does not pass the specified conditions, the interval indicates how
      long to wait before trying the command again.
    default: 1
'''

EXAMPLES = """
tasks:
  - name: run show version on remote devices
    iosxr_command:
      commands: show version

  - name: run show version and check to see if output contains iosxr
    iosxr_command:
      commands: show version
      wait_for: result[0] contains IOS-XR

  - name: run multiple commands on remote nodes
    iosxr_command:
      commands:
        - show version
        - show interfaces
        - { command: example command that prompts, prompt: expected prompt, answer: yes}

  - name: run multiple commands and evaluate the output
    iosxr_command:
      commands:
        - show version
        - show interfaces
      wait_for:
        - result[0] contains IOS-XR
        - result[1] contains Loopback0
"""

RETURN = """
stdout:
  description: The set of responses from the commands
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: ['...', '...']
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: [['...', '...'], ['...'], ['...']]
failed_conditions:
  description: The list of conditionals that have failed
  returned: failed
  type: list
  sample: ['...', '...']
"""
import time

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.network.common.plugins.module_utils.network.common.parsing import Conditional
from ansible_collections.network.common.plugins.module_utils.network.common.utils import to_lines
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.iosxr import run_commands, iosxr_argument_spec
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.iosxr import command_spec


def parse_commands(module, warnings):
    commands = module.params['commands']
    for item in list(commands):
        try:
            command = item['command']
        except Exception:
            command = item
        if module.check_mode and not command.startswith('show'):
            warnings.append(
                'Only show commands are supported when using check mode, not '
                'executing %s' % command
            )
            commands.remove(item)

    return commands


def main():
    argument_spec = dict(
        commands=dict(type='list', required=True),

        wait_for=dict(type='list', aliases=['waitfor']),
        match=dict(default='all', choices=['all', 'any']),

        retries=dict(default=10, type='int'),
        interval=dict(default=1, type='int')
    )

    argument_spec.update(iosxr_argument_spec)
    argument_spec.update(command_spec)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    warnings = list()
    result = {'changed': False, 'warnings': warnings}
    commands = parse_commands(module, warnings)
    wait_for = module.params['wait_for'] or list()

    try:
        conditionals = [Conditional(c) for c in wait_for]
    except AttributeError as exc:
        module.fail_json(msg=to_text(exc))

    retries = module.params['retries']
    interval = module.params['interval']
    match = module.params['match']

    while retries > 0:
        responses = run_commands(module, commands)

        for item in list(conditionals):
            if item(responses):
                if match == 'any':
                    conditionals = list()
                    break
                conditionals.remove(item)

        if not conditionals:
            break

        time.sleep(interval)
        retries -= 1

    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = 'One or more conditional statements have not been satisfied'
        module.fail_json(msg=msg, failed_conditions=failed_conditions)

    result.update({
        'stdout': responses,
        'stdout_lines': list(to_lines(responses)),
    })

    module.exit_json(**result)


if __name__ == '__main__':
    main()
