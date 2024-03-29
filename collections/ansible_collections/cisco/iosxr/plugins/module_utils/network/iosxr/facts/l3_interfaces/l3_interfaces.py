#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The iosxr_l3_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from copy import deepcopy
import re
from ansible_collections.network.common.plugins.module_utils.network.common import utils
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.utils.utils import get_interface_type
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.argspec.l3_interfaces.l3_interfaces import L3_InterfacesArgs


class L3_InterfacesFacts(object):
    """ The iosxr_l3_interfaces fact class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = L3_InterfacesArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for interfaces
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        objs = []

        if not data:
            data = connection.get('show running-config interface')
        # operate on a collection of resource x
        config = data.split('interface ')
        for conf in config:
            if conf:
                obj = self.render_config(self.generated_spec, conf)
                if obj:
                    objs.append(obj)
        facts = {}

        if objs:
            facts['l3_interfaces'] = []
            params = utils.validate_config(self.argument_spec, {'config': objs})
            for cfg in params['config']:
                facts['l3_interfaces'].append(utils.remove_empties(cfg))
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts

    def render_config(self, spec, conf):
        """
        Render config as dictionary structure and delete keys from spec for null values
        :param spec: The facts tree, generated from the argspec
        :param conf: The configuration
        :rtype: dictionary
        :returns: The generated config
        """
        config = deepcopy(spec)
        match = re.search(r'^(\S+)', conf)

        intf = match.group(1)
        if match.group(1).lower() == "preconfigure":
            match = re.search(r'^(\S+) (.*)', conf)
            if match:
                intf = match.group(2)

        if get_interface_type(intf) == 'unknown':
            return {}

        # populate the facts from the configuration
        config['name'] = intf

        # Get the configured IPV4 details
        ipv4 = []
        ipv4_all = re.findall(r"ipv4 address (\S+.*)", conf)
        for each in ipv4_all:
            each_ipv4 = dict()
            if 'secondary' in each:
                each_ipv4['address'] = each.split(' secondary')[0]
                each_ipv4['secondary'] = True
            else:
                each_ipv4['address'] = each
            ipv4.append(each_ipv4)
            config['ipv4'] = ipv4

        # Get the configured IPV6 details
        ipv6 = []
        ipv6_all = re.findall(r"ipv6 address (\S+)", conf)
        for each in ipv6_all:
            each_ipv6 = dict()
            each_ipv6['address'] = each
            ipv6.append(each_ipv6)
            config['ipv6'] = ipv6

        return utils.remove_empties(config)
