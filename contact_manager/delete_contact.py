import json


CONTACTS_FILE = "memory/contacts.json"


def delete_contact(name):

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

        return "Contacts file not found."

    new_contacts = [

        contact

        for contact in data["contacts"]

        if contact["name"] != name.lower()

    ]

    if len(

        new_contacts

    ) == len(

        data["contacts"]

    ):

        return f"{name} not found."

    data["contacts"] = new_contacts

    with open(

        CONTACTS_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            data,

            file,

            indent=4

        )

    return f"{name} deleted successfully."