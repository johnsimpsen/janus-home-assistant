from pydantic import BaseModel


class Device(BaseModel):
    nickname: str  # nickname of the device
    dimmable: bool  # determines if the device dims or toggles
    togglePin: int   # associate gpio pin the device is connected to


class Zone(BaseModel):
    ip: str  # associate ip of the zone
    devices: list[Device]  # list of connected devices to that zone


class Config(BaseModel):
    zones: list[Zone]  # list of all zones
