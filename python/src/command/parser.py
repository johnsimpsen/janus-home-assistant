

#separate the command and it's params
def parse_command(input_command):
    arr = input_command.split()
    command = arr[0]
    params = arr[1:]

    return {"command": command, "params": params}