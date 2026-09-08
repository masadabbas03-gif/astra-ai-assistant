from voice.speaker import speak

from personality.personality import (
    get_greeting
)

from agent.profile import (
    load_profile
)


def startup_message():

    profile = load_profile()

    message = f"""

{get_greeting()}

Welcome back {profile["nickname"]}.

I am {profile["assistant_name"]}.

Ready to help you.

"""

    print(message)

    speak(message)