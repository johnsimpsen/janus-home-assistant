import requests
from src.network.zones import zone_data


def run_enable_disable(command_name, params):
    """run the enable/disable command"""
    match len(params): #determine behavior based on number of parameters passed
        case 2:
            zone_number = params[0]
            device_number = params[1]
            current_zone = zone_data.get(str(zone_number))

            if device_number == "all":
                response = requests.get(f'http://{current_zone.get("ip")}/{command_name}')
            else:
                response = requests.get(f'http://{current_zone.get("ip")}/{command_name}?pin=' + str(device_number))
            print(response.text)

        case _:
            raise Exception("Incorrect number of parameters")

def run_set(command_name, params):
    match len(params):  # determine behavior based on number of parameters passed
        case 2:
            zone_number = params[0]
            level = params[1]
            current_zone = zone_data.get(str(zone_number))

            response = requests.get(f'http://{current_zone.get("ip")}/level?level=' + str(level))
            print(response.text)

        case _:
            raise Exception("Incorrect number of parameters")


#maps commands to functions
function_map = {
    "enable": run_enable_disable,
    "disable": run_enable_disable,
    'set': run_set,
}


def parse_command(input_command):
    """separate the command and its parameters"""
    arr = input_command.split()
    command = arr[0]
    params = arr[1:]

    command = command.lower()

    for i in range(len(arr)):
        arr[i] = arr[i].lower()

    return {"command": command, "params": params}


def run_command(parsed_command):
    """attempt to run a parsed command by finding its associated function"""
    command_name = parsed_command["command"]
    params = parsed_command["params"]

    #if associated function found, run the command
    if command_name in function_map:
        command_function = function_map.get(command_name)
        command_function(command_name, params)
    else:
        raise Exception("Command not found")

