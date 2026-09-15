from agent.tool_registry import TOOLS


def execute_tool(tool_name, *args, **kwargs):

    print(f"\nTool Name: {tool_name}")
    if args:
        print(f"Arguments (args): {args}")
    if kwargs:
        print(f"Arguments (kwargs): {kwargs}")

    tool = TOOLS.get(tool_name)

    if tool is None:
        return f"Tool '{tool_name}' not found."

    function = tool["function"]

    try:
        if kwargs and not args:
            return function(**kwargs)
        elif args and not kwargs:
            return function(*args)
        elif args and kwargs:
            return function(*args, **kwargs)
        else:
            return function()
    except TypeError as e:
        if kwargs:
            try:
                return function(*kwargs.values())
            except Exception:
                pass
        return f"Tool Execution Error: {e}"
    except Exception as e:
        return f"Tool Execution Error: {e}"



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
