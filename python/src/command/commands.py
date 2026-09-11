import requests
from src.agent.agent import prompt_LLM
from src.command.parser import parseCommand

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

#maps commands to functions
function_map = {
    "enable 1 12": lambda: togglePin(12),
    "enable 1 13": lambda: togglePin(13),
    "enable 1 14": lambda: togglePin(14)
}

#prompt the LLM with the input command, then attempt to parse the command and map it to a function
def run_command(input_command):
    output_command = prompt_LLM(input_command)
    parsed_command = parseCommand(output_command)

    if parsed_command in function_map:
        result = function_map.get(parsed_command)()
    else:
        print("Command not found")

