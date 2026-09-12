

#separate the command and it's params
def parse_command(input_command):
    arr = input_command.split()
    command = arr[0]
    params = arr[1:]

    command = command.lower()

    for i in range(len(arr)):
        arr[i] = arr[i].lower()

    return {"command": command, "params": params}