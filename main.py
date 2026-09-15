from datetime import datetime
import json
import time

from agent.brain import think
from agent.executor import execute_tool
from agent.planner import create_plan

from agent.memory import (
    save_task,
    save_conversation
)

from agent.state import (
    update_last_command,
    add_message
)

from startup.startup import startup_message


TASK_KEYWORDS = [

    "open",
    "search",
    "close",
    "start",
    "stop",
    "play",
    "create",
    "delete",
    "show",
    "status",
    "calculator",
    "notepad",
    "browser"

]


def main():

    print(

        "Main function started"

    )

    startup_message()

    while True:

        try:

            user_input = input(

                "\nYou: "

            ).strip()

        except KeyboardInterrupt:

            print(

                "\nStopping Astra..."

            )

            break

        except Exception as e:

            print(

                f"\nError: {e}"

            )

            continue

        if user_input == "":

            continue

        if user_input.lower() == "exit":

            print(

                "\nGoodbye!"

            )

            break

        # ============================
        # Save only useful commands
        # ============================

        if any(

            keyword in user_input.lower()

            for keyword in TASK_KEYWORDS

        ):

            save_task(

                user_input

            )

        update_last_command(

            user_input

        )

        add_message(

            "user",

            user_input

        )

        # ============================
        # Planner
        # ============================

        steps = create_plan(

            user_input

        )

        if steps:

            data = {

                "type": "steps",

                "steps": steps

            }

        else:

            response = think(

                user_input

            )

            print(

                "\nBrain Response:\n"

            )

            print(

                response

            )

            # ============================
            # Save Logs
            # ============================

            with open(

                "logs/assistant.log",

                "a",

                encoding="utf-8"

            ) as file:

                file.write(

                    f"""

=================================

[{datetime.now()}]

User:

{user_input}

Response:

{response}

=================================

"""

                )

            try:

                data = json.loads(

                    response

                )

            except Exception:

                print(

                    "\nAstra:\n"

                )

                print(

                    response

                )

                time.sleep(

                    1

                )

                continue

        # ============================
        # Chat Mode
        # ============================

        if data.get(

            "type"

        ) == "chat":

            message = data.get(

                "response",

                "Okay Boss."

            )

            add_message(

                "assistant",

                message

            )

            print(

                "\nAstra:\n"

            )

            print(

                message

            )

            save_conversation(

                user_input,

                message

            )

            time.sleep(

                1

            )

            continue

        # ============================
        # Multi-step Commands
        # ============================

        if data.get(

            "type"

        ) == "steps":

            steps = data.get(

                "steps",

                []

            )

            for index, step in enumerate(

                steps,

                start=1

            ):

                tool_name = step.get(

                    "tool"

                )

                arguments = step.get(

                    "arguments",

                    {}

                )

                if tool_name is None:

                    continue

                print(

                    f"\nExecuting Step {index}: {tool_name}"

                )

                if isinstance(arguments, dict):
                    result = execute_tool(
                        tool_name,
                        **arguments
                    )
                else:
                    result = execute_tool(
                        tool_name,
                        *arguments
                    )


                add_message(

                    "assistant",

                    str(result)

                )

                print(

                    "\nAssistant:\n"

                )

                print(

                    result

                )

                time.sleep(

                    1

                )

            continue

        # ============================
        # Tool Mode
        # ============================

        if data.get(

            "type"

        ) == "tool":

            tool_name = data.get(

                "tool"

            )

            arguments = data.get(

                "arguments",

                {}

            )

            if tool_name is None:

                print(

                    "\nNo tool selected."

                )

                continue

            print(

                f"\nExecuting: {tool_name}"

            )

            if isinstance(arguments, dict):
                result = execute_tool(
                    tool_name,
                    **arguments
                )
            else:
                result = execute_tool(
                    tool_name,
                    *arguments
                )


            add_message(

                "assistant",

                str(result)

            )

            print(

                "\nAssistant:\n"

            )

            print(

                result

            )

            time.sleep(

                1

            )

            continue

        # ============================
        # Invalid Response
        # ============================

        print(

            "\nInvalid response."

        )

        print(

            data

        )


if __name__ == "__main__":

    print(

        "Calling main..."

    )

    main()