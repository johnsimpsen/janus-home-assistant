from langchain_core.tools import tool


@tool
def run_unrelated():
    """
    Call this when the user request does not involve a supported device action.

    This tool is intended to execute nothing.

    :return: "unrelated"
    """

    return "unrelated"
