import requests
from src.network.zones import zone_data, zone_activation
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class EnableArgs(BaseModel):
    zone_number: int = Field(description="The zone number")
    device_number: int = Field(description="The device number")


@tool(args_schema=EnableArgs)
def run_enable(zone_number: int, device_number: int):
    """
    Makes an HTTP request to the specified zone and device to enable it.
    :param zone_number: used to find the associated ip
    :param device_number: used to choose the specific device
    :raise HTTP Timeout:
    """

    current_zone_ip = zone_data[int(zone_number)]

    response = requests.get(
        f'http://{current_zone_ip.get("ip")}/enable?deviceId={str(device_number)}',
        timeout=5
    )

    return response.text


class DisableArgs(BaseModel):
    zone_number: int = Field(description="The zone number")
    device_number: int = Field(description="The device number")


@tool(args_schema=DisableArgs)
def run_disable(zone_number: int, device_number: int):
    """
    Makes an HTTP request to the specified zone and device to disable it.
    :param zone_number: used to find the associated ip
    :param device_number: used to choose the specific device
    :raise HTTP Timeout:
    """

    print(type(zone_number))

    current_zone_ip = zone_data[int(zone_number)]

    response = requests.get(
        f'http://{current_zone_ip.get("ip")}/disable?deviceId={str(device_number)}',
        timeout=5
    )

    return response.text


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
    :raise Incorrect number of parameters
    :raise HTTP Timeout:
    """

    current_zone = zone_data[int(zone_number)]

    response = requests.get(
        f'http://{current_zone.get("ip")}/set?level={str(level)}&deviceId={device_number}',
        timeout=5
    )

    return response.text


# all tools the AI has access to
tool_map = {
    "run_enable": run_enable,
    "run_disable": run_disable,
    "run_set": run_set
}

# all associated schemas for tools
tool_schemas = {
    "run_enable": EnableArgs,
    "run_disable": DisableArgs,
    "run_set": SetArgs
}


def validate_command(command):
    """returns an error if the zone is not activated or does not exist at all"""

    arguments = command[0]["args"]
    command_name = command[0]["name"]

    command_schema = tool_schemas.get(command_name)
    validated_args = command_schema.model_validate(arguments)

    zone_number = validated_args.zone_number

    # check if current zone is activated
    if not zone_activation.get(zone_number, False):
        print("Zone not activated")
        raise Exception("Zone not activated")

    command[0]["args"] = validated_args.model_dump()
    return command


def run_command(command):
    """attempt to run a parsed command by finding its associated function"""

    arguments = command[0]["args"]
    tool_name = command[0]["name"]

    #if associated function found, run the command
    if tool_name in tool_map:
        return tool_map.get(tool_name).invoke(arguments)  # fetch associated function in tool_map and pass in args
    else:
        print("Command not found")
        raise Exception("Command not found")
