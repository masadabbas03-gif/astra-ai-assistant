state = {

    "current_website": None,

    "logged_in": False,

    "current_user": None,

    "last_command": None,

    "browser_running": False,

    "conversation": []
}


def update_last_command(command):

    state["last_command"] = command

def add_message(role, content):

    state["conversation"].append(

        {
            "role": role,
            "content": content
        }

    )

    if len(

        state["conversation"]

    ) > 10:

        state["conversation"].pop(0)