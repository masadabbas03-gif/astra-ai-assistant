import json


CONTACTS_FILE = "memory/contacts.json"


def get_contact(name):

    try:

        with open(

            CONTACTS_FILE,

            "r",

            encoding="utf-8"

        ) as file:

            data = json.load(

                file

            )

    except:

        return None

    for contact in data["contacts"]:

        if contact["name"] == name.lower():

            return contact

    return None