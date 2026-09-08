import json
import random


with open(

    "personality/identity.json",

    "r",

    encoding="utf-8"

) as file:

    identity = json.load(file)


def get_greeting():

    return random.choice(

        identity["greetings"]

    )


def who_created_you():

    return random.choice(

        identity["creator_answers"]

    )


def how_are_you():

    return random.choice(

        identity["mood_answers"]

    )


def get_identity():

    return identity