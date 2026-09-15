import webbrowser
import subprocess
from agent.state import state


def open_chrome():

    webbrowser.open("https://www.google.com")

    return "Chrome opened."


def search_google(query):

    webbrowser.open(f"https://www.google.com/search?q={query}")

    return f"Searching Google for: {query}"


def open_website(url):

    webbrowser.open(url)

    return f"Opened {url}"


def get_status():

    return state


def open_notepad():

    subprocess.Popen("notepad", shell=True)

    return "Notepad opened."


def open_calculator():

    subprocess.Popen("calc", shell=True)

    return "Calculator opened."


def open_vscode():

    subprocess.Popen("code", shell=True)

    return "VS Code opened."