from agent.memory import (
    save_preference,
    load_preferences
)

save_preference(

    "favorite_voice",

    "jarvis"
)

save_preference(

    "language",

    "urdu + english"
)

print(

    load_preferences()

)