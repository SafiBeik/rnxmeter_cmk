#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2022 Xelon AG
#          Safi Beik Karbouj <s.karbouj@xelon.ch>

from typing import Dict, List
from .agent_based_api.v1 import (
    contains,
    register,
    Metric,
    Result,
    SNMPTree,
    Service,
    State,
)
from .agent_based_api.v1.type_defs import (
    StringTable,
    CheckResult,
    DiscoveryResult,
)
#from cmk.base.check_legacy_includes.rnxemeter import check_rnxemeter
#from cmk.base.plugins.agent_based.agent_based_api.v1 import *


#------------------------------------------------------------------------------------------------------PARSER

def parse_rnxemeter_activeenergy(string_table: List[StringTable]) -> Dict[str, Dict[str, int]]:
    section = {}
    for line in string_table[0]:
        section[line[0]] = {
            'CH1': int(line[0])/1000,
            'CH2': int(line[1])/1000,
            'CH3': int(line[2])/1000,
        }
    return section

def parse_rnxemeter_activepower(string_table: List[StringTable]) -> Dict[str, Dict[str, int]]:
    section = {}
    for line in string_table[0]:
        section[line[0]] = {
            'CH1': int(line[0]),
            'CH2': int(line[1]),
            'CH3': int(line[2]),
        }
    return section


def parse_rnxemeter_voltage(string_table: List[StringTable]) -> Dict[str, Dict[str, int]]:
    section = {}
    for line in string_table[0]:
        section[line[0]] = {
            'CH1': int(line[0]) / 1000,
            'CH2': int(line[1]) / 1000,
            'CH3': int(line[2]) / 1000,
        }
    return section


def parse_rnxemeter_current(string_table: List[StringTable]) -> Dict[str, Dict[str, int]]:
    section = {}
    for line in string_table[0]:
        section[line[0]] = {
            'CH1': int(line[0]) / 1000,
            'CH2': int(line[1]) / 1000,
            'CH3': int(line[2]) / 1000,
            'N': int(line[3]) / 1000,
        }
    return section
#------------------------------------------------------------------------------------------------------PARSER


register.snmp_section(
    name="rnxemeter_active_energy",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.21695.1"),
    parse_function=parse_rnxemeter_activeenergy,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.21695.1.10.7.2.1.4",
            oids=[#------------------- + + +
                "0", # L1
                "1", # L2
                "2", # L3
            ]),
    ],
)



register.snmp_section(
    name="rnxemeter_active_power",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.21695.1"),
    parse_function=parse_rnxemeter_activepower,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.21695.1.10.7.2.1.5",
            oids=[#------------------- + + +
                "0", # L1
                "1", # L2
                "2", # L3
            ]),
    ],
)


register.snmp_section(
    name="rnxemeter_active_voltage",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.21695.1"),
    parse_function=parse_rnxemeter_voltage,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.21695.1.10.7.2.1.8",
            oids=[#------------------- + + +
                "0", # L1
                "1", # L2
                "2", # L3
            ]),
    ],
)


register.snmp_section(
    name="rnxemeter_active_current",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.21695.1"),
    parse_function=parse_rnxemeter_current,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.21695.1.10.7.2.1.9",
            oids=[#------------------- + + +
                "0", # L1
                "1", # L2
                "2", # L3
                "3", # N
            ]),
    ],
)



def discover_rnxemeter_values(section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)

def check_rnxemeter_values(item, params, section) -> CheckResult:
    for state, text, perfdata in check_rnxemeter(item, params, section):
        yield Result(state=State(state), summary=text)
        for p in perfdata:
            if len(p) == 4:
                yield Metric(p[0], p[1], levels=(p[2], p[3]))
            else:
                yield Metric(p[0], p[1])




#------------------------------------------------------------------------------------------------------REGISTER

register.check_plugin(
    name='rnxemeter_active_energy',
    sections=['rnxemeter_active_energy'],
    service_name='Active Energy kWh %s',
    check_default_parameters={},
    discovery_function=discover_rnxemeter_values,
    check_function=check_rnxemeter_values,
    check_ruleset_name='rnx_activeenergy',
)

register.check_plugin(
    name='rnxemeter_active_power',
    sections=['rnxemeter_active_power'],
    service_name='Active Power W %s',
    check_default_parameters={},
    discovery_function=discover_rnxemeter_values,
    check_function=check_rnxemeter_values,
    check_ruleset_name='rnx_activepower',
)

register.check_plugin(
    name='rnxemeter_active_voltage',
    sections=['rnxemeter_active_voltage'],
    service_name='Active Voltage V %s',
    check_default_parameters={},
    discovery_function=discover_rnxemeter_values,
    check_function=check_rnxemeter_values,
    check_ruleset_name='rnx_activevoltage',
)

register.check_plugin(
    name='rnxemeter_active_current',
    sections=['rnxemeter_active_current'],
    service_name='Active Current A %s',
    check_default_parameters={},
    discovery_function=discover_rnxemeter_values,
    check_function=check_rnxemeter_values,
    check_ruleset_name='rnx_activecurrent',
)

#------------------------------------------------------------------------------------------------------REGISTER