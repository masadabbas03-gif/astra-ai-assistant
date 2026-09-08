import json


CONTACTS_FILE = "memory/contacts.json"


def update_contact(

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

        return "Contacts file not found."

    for contact in data["contacts"]:

        if contact["name"] == name.lower():

            if phone:

                contact["phone"] = phone

            if email:

                contact["email"] = email

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

            return f"{name} updated successfully."

    return f"{name} not found."