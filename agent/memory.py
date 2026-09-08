import json


# ============================
# Tasks
# ============================

def save_task(command):

    try:

        with open(

            "memory/tasks.json",

            "r",

            encoding="utf-8"

        ) as file:

            tasks = json.load(file)

    except:

        tasks = []

    tasks.append(command)

    with open(

        "memory/tasks.json",

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            tasks,

            file,

            indent=4,

            ensure_ascii=False

        )


# ============================
# Conversations
# ============================

def save_conversation(

    user_message,

    assistant_message

):

    try:

        with open(

            "memory/conversations.json",

            "r",

            encoding="utf-8"

        ) as file:

            conversations = json.load(file)

    except:

        conversations = []

    conversations.append(

        {

            "user": user_message,

            "assistant": assistant_message

        }

    )

    with open(

        "memory/conversations.json",

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            conversations,

            file,

            indent=4,

            ensure_ascii=False

        )


def load_conversations():

    try:

        with open(

            "memory/conversations.json",

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    except:

        return []

def search_memory(query):

    conversations = load_conversations()

    results = []

    for conversation in conversations:

        user_text = conversation["user"].lower()

        assistant_text = conversation["assistant"].lower()

        if (

            query.lower() in user_text

            or

            query.lower() in assistant_text

        ):

            results.append(

                conversation

            )

    return results    

def save_preference(key, value):

    try:

        with open(
            "memory/preferences.json",
            "r",
            encoding="utf-8"
        ) as file:

            preferences = json.load(file)

    except:

        preferences = {}

    preferences[key] = value

    with open(
        "memory/preferences.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            preferences,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_preferences():

    try:

        with open(
            "memory/preferences.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return {}   
    
def load_profile():

    try:

        with open(

            "memory/profile.json",

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    except:

        return {}


def get_profile_value(key):

    profile = load_profile()

    return profile.get(

        key,

        None

    )    