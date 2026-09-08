from config.websites import WEBSITES


def create_plan(command):

    command = command.lower()

    steps = []

    for name, url in WEBSITES.items():

        if name in command:

            steps.append(

                {

                    "tool": "start_browser",

                    "arguments": {}

                }

            )

            steps.append(

                {

                    "tool": "open_website",

                    "arguments": {

                        "url": url

                    }

                }

            )

            break

    if "search" in command:

        query = command.split(

            "search",

            1

        )[1].strip()

        steps.append(

            {

                "tool": "search_google",

                "arguments": {

                    "query": query

                }

            }

        )

    return steps