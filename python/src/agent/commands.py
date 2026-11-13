import requests
from src.network.zones import zone_data, zone_activation_data, cleanup_nickname
from pydantic import BaseModel, Field, field_validator
from langchain_core.tools import tool


class EnableDisableByNumberArgs(BaseModel):
    zone_number: int = Field(
        description="The zone number"
    )
    device_number: int = Field(
        description="The device number, if known",
    )


@tool(args_schema=EnableDisableByNumberArgs)
def run_enable_by_number(zone_number: int, device_number: int):
    """
    Makes an HTTP request to the specified zone and device to enable it.

    Enable a device using its NUMERIC device ID.

    ONLY use this tool when the user explicitly identifies
    the device using a numeric ID.

    Examples:
    - Enable zone 0 device 2.
    - Turn on device number 3 in zone 1.
    - Activate device 0 in zone 2.

    The device_number argument MUST be an integer.

    NEVER use this tool when the user identifies a device
    using a name, nickname, or word.

    :param zone_number: used to find the associated ip
    :param device_number: the device's number
    :raise HTTP Timeout:
    """

    current_zone_ip = zone_data[int(zone_number)]

    response = requests.get(
        f'http://{current_zone_ip.get("ip")}/enable?deviceId={str(device_number)}',
        timeout=5
    )

    return response.text


@tool(args_schema=EnableDisableByNumberArgs)
def run_disable_by_number(zone_number: int, device_number: int):
    """
    Makes an HTTP request to the specified zone and device to disable it.

    Disable a device using its NUMERIC device ID.

    ONLY use this tool when the user explicitly identifies
    the device using a number, such as:
    - Disable zone 0 device 2
    - Turn off device number 3 in zone 1

    NEVER use this tool when the user provides a device name,
    nickname, or word.

    :param zone_number: used to find the associated ip
    :param device_number: the device's number
    :raise HTTP Timeout:
    """

    current_zone_ip = zone_data[int(zone_number)]

    response = requests.get(
        f'http://{current_zone_ip.get("ip")}/disable?deviceId={str(device_number)}',
        timeout=5
    )

    return response.text


class EnableDisableByNicknameArgs(BaseModel):
    zone_number: int = Field(
        description="The zone number"
    )
    device_nickname: str = Field(
        description="The device nickname, if known",
    )

    # TODO: Will expand implementation with AI model or RapidFuzz to validate from a set of existing nicknames
    @field_validator("device_nickname")
    @classmethod
    def normalize_nickname(cls, value):
        return cleanup_nickname(value)


@tool(args_schema=EnableDisableByNicknameArgs)
def run_enable_by_nickname(zone_number: int, device_nickname: str):
    """
    Makes an HTTP request to the specified zone and device to enable it.

    Enable a device using its STRING nickname.

    ONLY use this tool when the user identifies the device
    using its name or nickname.

    Examples:
    - Enable zone 0 red_led.
    - Turn on the bedroom light.
    - Activate the kitchen lamp in zone 1.

    The device_nickname argument MUST be a string.

    NEVER use this tool when the user explicitly identifies
    the device using a numeric device ID.

    :param zone_number: used to find the associated ip
    :param device_nickname: the device's number
    :raise HTTP Timeout:
    """

    current_zone_ip = zone_data[int(zone_number)]

    response = requests.get(
        f'http://{current_zone_ip.get("ip")}/enable?deviceId={device_nickname}',
        timeout=5
    )

    return response.text


@tool(args_schema=EnableDisableByNicknameArgs)
def run_disable_by_nickname(zone_number: int, device_nickname: str):
    """
    Makes an HTTP request to the specified zone and device to disable it.

    Disable a device using its STRING nickname.

    ONLY use this tool when the user identifies the device
    by its name or nickname, such as:
    - Disable zone 0 red_led
    - Turn off the bedroom light
    - Disable the kitchen lamp

    NEVER use this tool when the user explicitly provides
    a numeric device ID.

    :param zone_number: used to find the associated ip
    :param device_nickname: the device's number
    :raise HTTP Timeout:
    """

    current_zone_ip = zone_data[int(zone_number)]

    response = requests.get(
        f'http://{current_zone_ip.get("ip")}/disable?deviceId={device_nickname}',
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
    "run_enable_by_number": run_enable_by_number,
    "run_disable_by_number": run_disable_by_number,
    "run_enable_by_nickname": run_enable_by_nickname,
    "run_disable_by_nickname": run_disable_by_nickname,
    "run_set": run_set
}

# all associated schemas for tools
tool_schemas = {
    "run_enable_by_number": EnableDisableByNumberArgs,
    "run_disable_by_number": EnableDisableByNumberArgs,
    "run_enable_by_nickname": EnableDisableByNicknameArgs,
    "run_disable_by_nickname": EnableDisableByNicknameArgs,
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
    if not zone_activation_data.get(zone_number, False):
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
