import webbrowser
from agent.state import state
import os


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

    os.system("notepad")

    return "Notepad opened."


def open_calculator():

    os.system("calc")

    return "Calculator opened."


def open_vscode():

    os.system("code")

    return "VS Code opened."