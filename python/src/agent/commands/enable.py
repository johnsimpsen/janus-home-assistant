import requests
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel, Field, field_validator
from langchain_core.tools import tool

from src.config import HTTP_TIMEOUT_SECONDS
from src.home.zones import zone_data, zone_activation_data
from src.home.groups import nickname_to_devices


class EnableArgs(BaseModel):
    zone_number: int = Field(
        description="The zone number"
    )
    device_number: int = Field(
        description="The device number, if known",
    )

    @field_validator("zone_number")
    @classmethod
    def validate_zone_number(cls, value):
        # check if current zone is activated
        if not zone_activation_data.get(value, False):
            raise ValueError("Zone not activated")

        return value


@tool(args_schema=EnableArgs)
def run_enable(zone_number: int, device_number: int):
    """
    Command name: *enable*

    Makes an HTTP request to the specified zone and device to enable it.

    Enable a device using its NUMERIC device ID.

    ONLY use this tool when the user explicitly identifies the device using a numeric ID.

    The device_number argument MUST be an integer.

    **Examples:**

    - Enable zone 0 device 2.
    - Turn on device number 3 in zone 1.
    - Activate device 0 in zone 2.

    :param zone_number: used to find the associated ip
    :param device_number: the device's number
    :return: the response from the zone
    :raise HTTP Timeout:
    """

    current_zone_ip = zone_data[int(zone_number)]

    response = requests.get(
        f'http://{current_zone_ip.get("ip")}/enable?deviceId={str(device_number)}',
        timeout=HTTP_TIMEOUT_SECONDS
    )

    return response.text


class EnableGroupArgs(BaseModel):
    group_nickname: str = Field(
        description="The nickname of the group"
    )

    @field_validator("group_nickname")
    @classmethod
    def validate_zone_numbers(cls, value):
        #check if nickname is a valid group
        if value not in nickname_to_devices:
            raise ValueError("Unknown group nickname")

        devices = nickname_to_devices[value]
        # check if all zones are activated
        for device in devices:
            zone_number = device["zone_number"]
            if not zone_activation_data.get(zone_number, False):
                raise ValueError("Zone not activated")

        return value


@tool(args_schema=EnableGroupArgs)
def run_enable_group(group_nickname: str):
    """
    Command name: *group enable*

    Runs the run_enable command on a group of devices

    **Examples:**

    - Enable group1.
    - Turn on the main lights.
    - Activate my lamps.

    :param group_nickname: the nickname of the group
    :return: the response from the zone
    :raise HTTP Timeout:
    """

    responses = []
    devices = nickname_to_devices[group_nickname]

    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        futures = []

        for device in devices:
            arguments = {
                "zone_number": device["zone_number"],
                "device_number": device["device_number"],
            }

            future = executor.submit(lambda: run_enable.invoke(arguments))
            futures.append((device, future))

        for device, future in futures:
            try:
                response = future.result()
                responses.append(response)
            except Exception:
                print(str(device) + " failed to enable")
                responses.append(str(device) + " failed to enable")

    return responses
