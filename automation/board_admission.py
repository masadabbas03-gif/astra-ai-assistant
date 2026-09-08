from tools.student_tools import get_student_by_name
from automation.generic_form import fill_form
from config.form_mapping import MAPPING

from tools.browser_tools import start_browser, open_website, take_screenshot


def submit_admission(student_name):

    student = get_student_by_name(student_name)

    if student is None:

        return "Student not found."

    start_browser()

    open_website("https://demoqa.com/automation-practice-form")

    fill_form(student, MAPPING)

    take_screenshot(f"{student_name}.png")

    return f"{student_name} form submitted."
