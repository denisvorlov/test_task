#!/usr/bin/python3
"""netbox Denis Orlov1.04.2021"""

from typing import Tuple, Set
import pynetbox
from pynetbox.core.api import Api
from libs import Device, DeviceParams

def get_and_update_sw_version(netbox_client: Api,
                              filter_params: DeviceParams,
                              snmp_community: str,
                              snmp_oids: str) -> Tuple[Set[Device], Set[Device]]:
    """docstring description for get_and_update_sw_version"""
    ok_result, fail_result = set(), set()
    devices = netbox_client.dcim.devices.filter(status=filter_params.status,
                                                tenant=filter_params.tenant)
    for dev in devices:
        device = Device(dev.id, dev.name,
                        status=dev.status,
                        tenant=dev.tenant,
                        primary_ip4=dev.primary_ip4["address"],
                        platform_name=dev.platform["name"],
                        sw_version=dev.custom_fields['sw_version'])
        snmp_sw_version = device.get_snmp_oid(snmp_community, snmp_oids)
        if snmp_sw_version:
            device = Device(dev.id, dev.name,
                            status=dev.status,
                            tenant=dev.tenant,
                            primary_ip4=dev.primary_ip4["address"],
                            platform_name=dev.platform["name"],
                            sw_version=dev.custom_fields['sw_version'])
            dev.custom_fields['sw_version'] = snmp_sw_version
            if dev.save():
                print(f'Update "sw_version" for {device.name} ok...')
                ok_result.add(Device(dev.id, dev.name,
                                     status=dev.status,
                                     tenant=dev.tenant,
                                     primary_ip4=dev.primary_ip4["address"],
                                     platform_name=dev.platform["name"],
                                     sw_version=snmp_sw_version))
            else:
                print(f'Update "sw_version" for {device.name} failed...')
                fail_result.add(Device(dev.id, dev.name,
                                       status=dev.status,
                                       tenant=dev.tenant,
                                       primary_ip4=dev.primary_ip4["address"],
                                       platform_name=dev.platform["name"],
                                       sw_version=dev.custom_fields['sw_version']))
        else:
            fail_result.add(Device(dev.id, dev.name,
                                   status=dev.status,
                                   tenant=dev.tenant,
                                   primary_ip4=dev.primary_ip4["address"],
                                   platform_name=dev.platform["name"],
                                   sw_version=dev.custom_fields['sw_version']))
    return ok_result, fail_result

if __name__ == '__main__':
    NB_URL = 'http://netbox.test.ru'
    NB_TOKEN = '38b94ed6f95bf5df3fb36c3facaccc6f74cb20f5'
    NB_CLIENT = pynetbox.api(url=NB_URL, token=NB_TOKEN)
    SNMP_COMMUNITY = 'public'
    SNMP_SW_VERSION_OIDS = {"Cisco Catalyst IOS": ".1.3.6.1.2.1.1.1.0",
                            "Cisco Nexus OS": ".1.3.6.1.2.1.47.1.1.1.1.9",
                            "Cisco ASA": ".1.3.6.1.2.1.47.1.1.1.1.9",
                            "PaloAlto PAN-OS": "1.3.6.1.4.1.25461.2.1.2.1.1.0",
                            "Aruba OS": ".1.3.6.1.2.1.47.1.1.1.1.9"}
    RESULT = get_and_update_sw_version(NB_CLIENT,
                                       DeviceParams(status='active', tenant='noc'),
                                       SNMP_COMMUNITY, SNMP_SW_VERSION_OIDS)
