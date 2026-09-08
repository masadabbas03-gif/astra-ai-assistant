from tools.csv_reader import read_csv
from tools.system_tools import open_chrome, open_website, search_google
from tools.student_filter import get_paid_students
from tools.student_actions import get_student_by_name, get_all_students
from tools.file_tools import list_files, create_folder


def process_command(command):

    command = command.lower()

    result = read_csv("data/students.csv")

    if not result["success"]:
        return result["error"]

    students = result["data"]

    # Paid students
    if "paid" in command:
        return get_paid_students(students)

    # All students
    if "all students" in command or command == "students":
        return get_all_students(students)

    # Search by name
    words = command.split()

    for word in words:
        student = get_student_by_name(students, word)

        if student:
            return student

    # Open Chrome
    if "open chrome" in command:
        return open_chrome()

    # Open YouTube
    if "open youtube" in command:
        return open_website("https://www.youtube.com")

    # Open Google
    if "open google" in command:
        return open_website("https://www.google.com")

    # Open WhatsApp
    if "open whatsapp" in command:
        return open_website("https://www.whatsapp.com")

    # Search
    if command.startswith("search "):
        query = command.replace("search ", "").strip()
        return search_google(query)

    # Show files
    if "show files" in command:
        return list_files(".")

    # Create folder
    if command.startswith("create folder"):
        folder_name = command.replace("create folder", "").strip()

        return create_folder(folder_name)

    return "Sorry, I don't understand this command."
