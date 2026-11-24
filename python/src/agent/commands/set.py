import requests
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.config import HTTP_TIMEOUT_SECONDS
from src.home.zones import zone_data


class SetArgs(BaseModel):
    zone_number: int = Field(description="The zone number")
    device_number: int = Field(description="The device number")
    level: int = Field(description="The level the device should be set to")


@tool(args_schema=SetArgs)
def run_set(zone_number: int, device_number: int, level: int):
    """
    Makes an HTTP request to the specified zone and device to set its specific level
    :param zone_number: used to find the associated ip
    :param device_number: used to choose the specific device
    :param level: number 0-100 determines the strength of the device
    :raise HTTP Timeout:
    """

    current_zone = zone_data[int(zone_number)]

    response = requests.get(
        f'http://{current_zone.get("ip")}/set?level={str(level)}&deviceId={device_number}',
        timeout=HTTP_TIMEOUT_SECONDS
    )

    return response.text
