from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import requests
from src.agent.commands import run_enable_by_number, run_disable_by_number, run_enable_by_nickname, run_disable_by_nickname, run_set

# all tools the AI has access to
tool_list = [
    run_enable_by_number,
    run_disable_by_number,
    run_enable_by_nickname,
    run_disable_by_nickname,
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
6. If required information is missing, ask the user for clarification.
7. Never execute unrelated requests.
8. If you do not recognize anything related to the tools, do not try to guess the command
9. Be careful, device nicknames can be multiple words
10. device numbers are always going to be a number or digits, and device nicknames will always be words
11. device nickname can be 'all', this just disables all the devices

USER REQUEST:
{user_input}
"""

#TODO: Give AI access to zone and device data
# it can then choose from a list of valid zone_numbers, device_numbers, and device_nicknames
# maybe it should automatically convert a device_nickname into the corresponding zone_number and device_number
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def prompt_llm(user_input):
    """returns a specific command based on user input"""
    output = chain.invoke({
        "user_input": user_input
    })

    return output.tool_calls
