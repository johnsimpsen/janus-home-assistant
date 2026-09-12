import requests
from src.agent.agent import prompt_llm
from src.command.parser import parse_command

def togglePin(pinNum):
    try:
        response = requests.get('http://192.168.1.167/pin?gpio=' + str(pinNum))
        #response = requests.get('http://97.99.90.190:5000/pin?gpio=' + str(pinNum))
        ledStatus = response.text
    except:
        print("Something went wrong")
        return

    if (ledStatus == "0"):
        print("Pin " + str(pinNum) + " off")
    else:
        print("Pin " + str(pinNum) + " on")


#run the enable command
def run_enable(params):
    #determine behavior based on number of parameters passed
    match len(params):
        case 2:
            zone_number = params[0]
            device_number = params[1]
            if device_number == "all":
                response = requests.get('http://192.168.1.167/enable')
            else:
                response = requests.get('http://192.168.1.167/enable?pin=' + str(device_number))
            print(response.text)

        case _:
            raise Exception("Params are missing")


#run the disable command
def run_disable(params):
    #determine behavior based on number of parameters passed
    match len(params):
        case 2:
            zone_number = params[0]
            device_number = params[1]
            if device_number == "all":
                response = requests.get('http://192.168.1.167/disable')
            else:
                response = requests.get('http://192.168.1.167/disable?pin=' + str(device_number))
            print(response.text)

        case _:
            raise Exception("Params are missing")


#maps commands to functions
function_map = {
    "enable": run_enable,
    "disable": run_disable
}


#prompt the LLM with the input command, then attempt to parse the command and map it to a function
def run_command(input_command):
    output_command = prompt_llm(input_command)
    parsed_command = parse_command(output_command)

    command_name = parsed_command["command"]
    params = parsed_command["params"]

    #if associated function found, run the command
    if command_name in function_map:
        #find associated functions
        command_function = function_map.get(command_name)
        command_function(params)
    else:
        print("Command not found")


