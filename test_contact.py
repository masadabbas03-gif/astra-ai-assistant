from contact_manager.add_contact import add_contact
from contact_manager.get_contact import get_contact


add_contact(

    "Asad",

    phone="03001234567",

    email="asad@gmail.com"

)

print(

    get_contact(

        "Asad"

    )

)

from contact_manager.update_contact import update_contact
from contact_manager.delete_contact import delete_contact


print(

    update_contact(

        "Asad",

        phone="03123456789"

    )

)

print(

    delete_contact(

        "Asad"

    )

)