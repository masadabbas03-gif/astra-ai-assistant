def get_paid_students(students):

    paid_students = []

    for student in students:

        if student["fee_paid"].lower() == "yes":

            paid_students.append(student)

    return paid_students
