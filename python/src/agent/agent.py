from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import requests
from src.agent.commands import run_unrelated, run_enable, run_disable, run_set
from src.network.zones import zone_data, device_nickname_data

# all tools the AI has access to
tool_list = [
    run_unrelated,
    run_enable,
    run_disable,
    run_set
]

model = ChatOllama(
    model="llama3.2",
    temperature=0,  # minimize randomness
    keep_alive="30m"
).bind_tools(tool_list)


def preload_llm():
    print("Model loading...")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "temperature": 0,
            "keep_alive": "30m"
        },
        timeout=None
    )
    response.raise_for_status()
    print("Model loaded!")


template = """

You are Janus, an AI home assistant and multimedia controller.

Your job is to interpret user requests and select the appropriate tool.

RULES:

1. Only use tools when the user explicitly requests a supported action.
2. Never guess missing information.
3. Zone numbers must be explicitly identified.
4. Device numbers must be explicitly identified if a specific device is requested.
5. Convert written numbers into integers.
6. Unrelated requests have a delegated tool
7. If you do not recognize anything related to the tools, do not try to guess the command and use unrelated instead
8. Be careful, device nicknames can be multiple words
9. If s nickname, device_number, or zone are given but not the command itself, output unrelated
10. device numbers are always going to be a number or digits, and device nicknames will always be words
11. If specified, all will be a device_number of -1
12: Do not attempt to use the set command on a device that is not labelled as dimmable

Here is the data of all the zones:
{zone_data}

Here is a dictionary of nickname to zone_number and device_number
{device_nickname_data}

If you are given something very similar to a device nickname, but not exactly the same, try and interpret the correct
nickname being provided

USER REQUEST:
{user_input}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def prompt_llm(user_input):
    """returns a specific command based on user input"""
    output = chain.invoke({
        "user_input": user_input,
        "device_nickname_data": device_nickname_data,
        "zone_data": zone_data,
    })

    if not output.tool_calls:
        return None

    if len(output.tool_calls) != 1:
        return None

    return output.tool_calls
