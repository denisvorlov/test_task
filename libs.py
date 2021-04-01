# pylint: disable=C0103
# pylint: disable=E1101
# pylint: disable=E0103
# pylint: disable=R0201
# pylint: disable=R0913
# pylint: disable=W0612
# pylint: disable=W0622
# pylint: disable=W0703
"""libs.py Denis Orlov 1.04.2021"""

from dataclasses import dataclass
from pysnmp.hlapi import getCmd,\
    SnmpEngine,\
    CommunityData,\
    UdpTransportTarget,\
    ContextData,\
    ObjectType,\
    ObjectIdentity

class Device:
    """dataclass for Device"""
    def __init__(self, id, name, status, tenant, primary_ip4, platform_name, **kwargs):
        self.id = id
        self.name = name
        self.status = status
        self.tenant = tenant
        self.primary_ip4 = {"address": primary_ip4}
        self.platform = {"name": platform_name}
        self.custom_fields = kwargs

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __getitem__(self, key):
        return self.key

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.name)

    def get_snmp_oid(self, snmp_community, oids):
        """docstring description for get_snmp_oid"""
        snmp_data = getCmd(SnmpEngine(), CommunityData(snmp_community),
                           UdpTransportTarget(
                               (str(self.primary_ip4["address"]).split("/")[0], 161)),
                           ContextData(),
                           ObjectType(ObjectIdentity(oids[str(self.platform["name"])])))
        error_indication, error_status, error_index, var_binds = next(snmp_data)
        try:
            if error_indication:
                raise error_indication
            return str(var_binds[0][1])
        except Exception as error:
            print(f'ERROR: {error}, '
                  f'while getting snmp data from {self.name} '
                  f'with ip {self.primary_ip4["address"]}')

class NB_Device:
    """dataclass for NB_Device (used in testing purposes)"""
    def __init__(self, id, name, status, tenant, primary_ip4, platform_name, **kwargs):
        self.id = id
        self.name = name
        self.status = status
        self.tenant = tenant
        self.primary_ip4 = {"address": primary_ip4}
        self.platform = {"name": platform_name}
        self.custom_fields = kwargs

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __getitem__(self, key):
        return self.key

    def save(self):
        """docstring description for save method"""
        return "pass"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.name)

@dataclass
class DeviceParams:
    """dataclass for DeviceParams"""
    status: str
    tenant: str
