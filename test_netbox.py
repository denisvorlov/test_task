#!/usr/bin/python3
# pylint: disable=W0621
"""netbox pytests Denis Orlov 1.04.2021"""

import copy
import pytest
import mock
from netbox import get_and_update_sw_version
from libs import Device, NB_Device, DeviceParams

ALL_DEVICES = {NB_Device('11',
                         'name1',
                         'active',
                         'noc',
                         '192.168.10.5',
                         'Cisco Catalyst IOS',
                         sw_version="sw_version1"),
               NB_Device('22',
                         'name2',
                         'not_active',
                         'noc',
                         '192.168.10.1',
                         'Cisco NEXUS OS',
                         sw_version='sw_version1'),
               NB_Device('33',
                         'name3',
                         'active',
                         'not_noc',
                         '192.168.10.2',
                         'Cisco ASA',
                         sw_version='sw_version1')}

FILTERED_DEVICES = {NB_Device('11',
                              'name1',
                              'active',
                              'noc',
                              '192.168.10.5',
                              'Cisco Catalyst IOS',
                              sw_version="sw_version1")}

CHANGED_DEVICE = {NB_Device('11',
                            'name1',
                            'active',
                            'noc',
                            '192.168.10.5',
                            'Cisco Catalyst IOS',
                            sw_version="test_sw_version1")}

SNMP_COMMUNITY = 'public'
SNMP_SW_VERSION_OIDS = {"Cisco Catalyst IOS": ".1.3.6.1.2.1.1.1.0",
                        "Cisco Nexus OS": ".1.3.6.1.2.1.47.1.1.1.1.9",
                        "Cisco ASA": ".1.3.6.1.2.1.47.1.1.1.1.9",
                        "PaloAlto PAN-OS": "1.3.6.1.4.1.25461.2.1.2.1.1.0",
                        "Aruba OS": ".1.3.6.1.2.1.47.1.1.1.1.9"}

def nb_filter(device_list):
    """docstring description for nb_filter"""
    filtered_device_list = []
    for device in device_list:
        if device.status == "active" and device.tenant == "noc":
            filtered_device_list.append(device)
    return filtered_device_list


@pytest.fixture
def nb_client():
    """docstring description for nb_client"""
    client = mock.Mock()
    client.dcim.devices.filter.return_value = nb_filter(ALL_DEVICES)
    client.dcim.devices.all.return_value = copy.deepcopy(ALL_DEVICES)
    return client

def test_get_and_update_sw_version(nb_client):
    """docstring description for test_set_sw_version"""
    Device.get_snmp_oid = mock.Mock(return_value='test_sw_version')
    result = get_and_update_sw_version(nb_client,
                                       DeviceParams(status='active', tenant='noc'),
                                       SNMP_COMMUNITY,
                                       SNMP_SW_VERSION_OIDS)
    assert result[0] == CHANGED_DEVICE
