from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import requests
from src.agent.commands import run_enable, run_disable, run_set

# all tools the AI has access to
tool_list = [
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
5. If no device is specified, use None.
6. Convert written numbers into integers.
7. If required information is missing, ask the user for clarification.
8. Never execute unrelated requests.
9. If you do not recognize anything related to the tools, do not try to guess the command

USER REQUEST:
{user_input}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def prompt_llm(user_input):
    """returns a specific command based on user input"""
    output = chain.invoke({
        "user_input": user_input
    })

    return output.tool_calls
