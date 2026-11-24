from pydantic import BaseModel


class Device(BaseModel):
    zone_number: int  # the zone of the device
    device_number: int  # the device's number


class Group(BaseModel):
    nickname: str  # nickname of the group
    devices: list[Device]  # list of connected devices to that zone


class GroupData(BaseModel):
    groups: list[Group]  # list of all groups
