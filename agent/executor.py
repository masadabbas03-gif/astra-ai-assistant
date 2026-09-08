from agent.tool_registry import TOOLS


def execute_tool(tool_name, *args):

    print(f"\nTool Name: {tool_name}")
    print(f"Arguments: {args}")

    tool = TOOLS.get(tool_name)

    if tool is None:
        return "Tool not found."

    function = tool["function"]

    return function(*args)


def get_available_tools():

    tools_info = []

    for name, tool in TOOLS.items():

        tools_info.append(
            {
                "name": name,
                "description": tool["description"],
                "category": tool["category"],
                "parameters": tool["parameters"],
            }
        )

    return tools_info
