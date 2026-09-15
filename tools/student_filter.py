def get_paid_students(students):

    paid_students = []

    for student in students:

        if str(student.get("fee_paid", "")).strip().lower() == "yes":

            paid_students.append(student)

    return paid_students

