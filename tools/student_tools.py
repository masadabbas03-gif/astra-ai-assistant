from tools.csv_reader import read_csv


def get_all_students():

    result = read_csv("data/students.csv")

    if result["success"]:

        return result["data"]

    return []


def get_student_by_name(name):

    students = get_all_students()

    for student in students:

        if student["name"].lower() == name.lower():

            return student

    return None
