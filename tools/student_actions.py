from tools.student_tools import get_student_by_name as fetch_student_by_name
from automation.generic_form import fill_form
from automation.board_admission import submit_admission


def get_student_by_name(students_or_name, name=None):
    if name is not None:
        students = students_or_name
        for student in students:
            if student.get("name", "").lower() == name.lower():
                return student
        return None
    return fetch_student_by_name(students_or_name)


def get_all_students(students=None):
    if students is not None:
        return students
    from tools.student_tools import get_all_students as fetch_all
    return fetch_all()


def submit_student_form(name):
    student = get_student_by_name(name)

    if student is None:

        return "Student not found."

    mapping = {
        "name": "#student_name",
        "father_name": "#father_name",
        "class": "#student_class",
    }

    fill_form(student, mapping)

    return f"{name} form submitted successfully."


def submit_student_admission(name):

    return submit_admission(name)
