"""Orlov Denis 25.03.2021"""

from dataclasses import dataclass

class Device:
    """dataclass for Device"""
    def __init__(self, id, name, status, tenant, **kwargs):
        self.id = id
        self.name = name
        self.status = status
        self.tenant = tenant
        self.custom_fields = kwargs

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __getitem__(self, key):
        return self.key

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.name)

class NB_Device:
    """dataclass for NB_Device"""
    def __init__(self, id, name, status, tenant, **kwargs):
        self.id = id
        self.name = name
        self.status = status
        self.tenant = tenant
        self.custom_fields = kwargs

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __getitem__(self, key):
        return self.key

    def save(self):
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
