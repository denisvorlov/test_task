#!/usr/bin/python3
"""Orlov Denis 25.03.2021"""

from typing import Tuple, Set
import pynetbox
from pynetbox.core.api import Api
from libs import Device, DeviceParams

def get_netbox_devices(netbox_client: Api, filter_params: DeviceParams) -> Set[Device]:
    """docstring description for get_netbox_devices"""
    devices = netbox_client.dcim.devices.filter(status=filter_params.status,
                                                tenant=filter_params.tenant)
    returnset = set()
    for dev in devices:
        returnset.add(Device(dev.id,
                             dev.name,
                             dev.status,
                             dev.tenant,
                             sw_version=dev.custom_fields['sw_version']))
    return returnset

def set_sw_version(nb_client: Api, sw_version: str) -> Tuple[Set[Device], Set[Device]]:
    """docstring description for set_sw_version"""
    ok_result, fail_result = set(), set()
    for dev in nb_client.dcim.devices.all():
        device = Device(dev.id,
                        dev.name,
                        status=dev.status,
                        tenant=dev.tenant,
                        sw_version=dev.custom_fields['sw_version'])
        dev.custom_fields['sw_version'] = sw_version
        try:
            dev.save()
            ok_result.add(Device(dev.id,
                                 dev.name,
                                 status=dev.status,
                                 tenant=dev.tenant,
                                 sw_version=sw_version))
        except Exception as error:
            print(f'failed to update custom field for {device}, {error}')
            fail_result.add(Device(dev.id,
                                   dev.name,
                                   status=dev.status,
                                   tenant=dev.tenant,
                                   sw_version=sw_version))
    return ok_result, fail_result


if __name__ == '__main__':
    NB_URL = 'http://netbox.test.ru'
    NB_TOKEN = '38b94ed6f95bf5df3fb36c3facaccc6f74cb20f5'
    NEW_SW_VERSION = 'my new sw version'
    NB_CLIENT = pynetbox.api(url=NB_URL, token=NB_TOKEN)
    FILTERED_DEVICE_LIST = get_netbox_devices(NB_CLIENT,
                                              DeviceParams(status='active', tenant='noc'))
    print(f'####Devices with status=active and tenant="noc". Total devices:'
          f' {len(FILTERED_DEVICE_LIST )}')
    for item in get_netbox_devices(NB_CLIENT, DeviceParams(status='active', tenant='noc')):
        print(f'Device name: {item.name} | Sw_version: {item.custom_fields["sw_version"]}')
    print('#####Starting to update sw_version field for devices')
    SW_VERSION_UPDATE_RESULT = set_sw_version(NB_CLIENT, NEW_SW_VERSION)[0]
