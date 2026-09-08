import json


CONTACTS_FILE = "memory/contacts.json"


def add_contact(

    name,

    phone=None,

    email=None

):

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

        data = {

            "contacts": []

        }

    contact = {

        "name": name.lower(),

        "phone": phone,

        "email": email

    }

    data["contacts"].append(

        contact

    )

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

    return f"{name} saved successfully."