import json


def load_profile():

    with open(

        "memory/profile.json",

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(file)