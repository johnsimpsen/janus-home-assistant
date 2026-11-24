from src.agent.commands import *

# all tools the AI has access to
tool_map = {
    "run_unrelated": run_unrelated,
    "run_enable": run_enable,
    "run_disable": run_disable,
    "run_enable_group": run_enable_group,
    "run_disable_group": run_disable_group,
    "run_set": run_set
}

# all associated schemas for tools
tool_schemas = {
    "run_enable": EnableArgs,
    "run_disable": DisableArgs,
    "run_enable_group": EnableGroupArgs,
    "run_disable_group": DisableGroupArgs,
    "run_set": SetArgs,
}


def validate_command(command):
    """returns an error if the zone is not activated or does not exist at all"""

    tool_name = command[0]["name"]
    arguments = command[0]["args"]

    if tool_name == "run_unrelated":
        return command

    tool_schema = tool_schemas.get(tool_name)
    validated_args = tool_schema.model_validate(arguments)

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
