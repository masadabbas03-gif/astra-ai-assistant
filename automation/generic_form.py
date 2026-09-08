from tools.browser_tools import fill_input, click_element


def fill_form(student, mapping):

    for field, config in mapping.items():

        selector = config["selector"]

        action_type = config["type"]

        value = str(student.get(field, ""))

        if action_type == "input":

            fill_input(selector, value)

        elif action_type == "click":

            click_element(selector)

    return "Form filled successfully."
