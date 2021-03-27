#!/usr/bin/python3
"""netbox pytests"""

import copy
import pytest
import mock
from netbox import get_netbox_devices, set_sw_version, DeviceParams
from libs import NB_Device

ALL_DEVICES = set([NB_Device('11', 'name1', 'active', 'noc', sw_version="sw_version1"),
                   NB_Device('22', 'name2', 'not_active', 'noc', sw_version='sw_version1'),
                   NB_Device('33', 'name3', 'active', 'not_noc', sw_version='sw_version1')])

ALL_CHANGED_DEVICES = set([NB_Device('11', 'name1', 'active', 'noc', sw_version='new_sw_version'),
                           NB_Device('22', 'name2', 'active', 'noc', sw_version='new_sw_version'),
                           NB_Device('33', 'name3', 'active', 'noc', sw_version='new_sw_version')])

FILTERED_DEVICES = set([NB_Device('11', 'name1', 'active', 'noc', sw_version="sw_version1")])

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

def test_get_netbox_devices(nb_client):
    """docstring description for test_get_netbox_devices"""
    results = get_netbox_devices(nb_client, DeviceParams(status='active', tenant='noc'))
    assert results == FILTERED_DEVICES

def test_set_sw_version(nb_client):
    """docstring description for test_set_sw_version"""
    result = set_sw_version(nb_client, "my_new_sw_version")
    assert result[0] == ALL_CHANGED_DEVICES
