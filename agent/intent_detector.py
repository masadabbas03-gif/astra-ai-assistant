def detect_intent(command):

    command = command.lower().strip()

    # Status

    if "status" in command:

        return {
            "tool": "get_status",
            "arguments": {}
        }

    # Browser

    if "browser" in command and "start" in command:

        return {
            "tool": "start_browser",
            "arguments": {}
        }

    if "close" in command and "browser" in command:

        return {
            "tool": "close_browser",
            "arguments": {}
        }

    # Search

    if command.startswith("search "):

        query = command.replace(
            "search",
            "",
            1
        ).strip()

        return {
            "tool": "search_google",
            "arguments": {
                "query": query
            }
        }

    # Students

    if command == "students":

        return {
            "tool": "get_all_students",
            "arguments": {}
        }

    # Show student

    if command.startswith("show "):

        name = command.replace(
            "show",
            "",
            1
        ).strip()

        return {
            "tool": "get_student_by_name",
            "arguments": {
                "name": name
            }
        }

    # Submit admission

    if command.startswith(
        "submit admission "
    ):

        name = command.replace(
            "submit admission",
            "",
            1
        ).strip()

        return {
            "tool": "submit_student_admission",
            "arguments": {
                "name": name
            }
        }

    # Open Notepad

    if "notepad" in command:

        return {
            "tool": "open_notepad",
            "arguments": {}
        }

    # Open Calculator

    if "calculator" in command:

        return {
            "tool": "open_calculator",
            "arguments": {}
        }

    # Open VS Code

    if "vs code" in command:

        return {
            "tool": "open_vscode",
            "arguments": {}
        }

    # Open website (ye hamesha last mein hoga)

    if command.startswith("open "):

        url = command.replace(
            "open",
            "",
            1
        ).strip()

        if not url.startswith(
            ("http://", "https://")
        ):

            url = "https://" + url

        return {
            "tool": "open_website",
            "arguments": {
                "url": url
            }
        }

    return None