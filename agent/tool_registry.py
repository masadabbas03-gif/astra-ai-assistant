from tools.system_tools import open_chrome, search_google, open_website, get_status

from tools.file_tools import list_files, create_folder

from tools.browser_tools import (
    start_browser,
    open_website,
    search_google,
    close_browser,
    click_element,
    fill_input,
    get_text,
    take_screenshot,
    upload_file,
    open_whatsapp,

)
from tools.student_tools import get_all_students, get_student_by_name
from tools.student_actions import submit_student_form
from tools.student_actions import submit_student_admission
from agent.state import state
from tools.system_tools import (
    open_notepad,
    open_calculator,
    open_vscode
)
from tools.browser_tools import (

    search_whatsapp_contact,
    send_whatsapp_message

)
from tools.n8n_tools import send_email_n8n

TOOLS = {
    "open_chrome": {
        "function": open_chrome,
        "description": "Open Google Chrome browser",
        "category": "system",
        "parameters": [],
    },
    "search_google": {
        "function": search_google,
        "description": "Search anything on Google",
        "category": "browser",
        "parameters": [{"name": "query", "type": "string"}],
    },
    "list_files": {
        "function": list_files,
        "description": "List files in a folder",
        "category": "file",
        "parameters": [{"name": "folder_path", "type": "string"}],
    },
    "create_folder": {
        "function": create_folder,
        "description": "Create a new folder",
        "category": "file",
        "parameters": [{"name": "folder_name", "type": "string"}],
    },
    "start_browser": {
        "function": start_browser,
        "description": "Start browser",
        "category": "browser",
        "parameters": [],
    },
    "open_website": {
        "function": open_website,
        "description": "Open a website",
        "category": "browser",
        "parameters": [{"name": "url", "type": "string"}],
    },
    "close_browser": {
        "function": close_browser,
        "description": "Close browser",
        "category": "browser",
        "parameters": [],
    },
    "click_element": {
        "function": click_element,
        "description": "Click an element on the page",
        "category": "browser",
        "parameters": [{"name": "selector", "type": "string"}],
    },
    "fill_input": {
        "function": fill_input,
        "description": "Fill text in an input field",
        "category": "browser",
        "parameters": [
            {"name": "selector", "type": "string"},
            {"name": "text", "type": "string"},
        ],
    },
    "take_screenshot": {
        "function": take_screenshot,
        "description": "Take a screenshot",
        "category": "browser",
        "parameters": [],
    },
    "get_all_students": {
        "function": get_all_students,
        "description": "Get all students",
        "category": "student",
        "parameters": [],
    },
    "get_student_by_name": {
        "function": get_student_by_name,
        "description": "Get student information by name",
        "category": "student",
        "parameters": [{"name": "name", "type": "string"}],
    },
    "submit_student_form": {
        "function": submit_student_form,
        "description": "Submit student form automatically",
        "category": "automation",
        "parameters": [{"name": "name", "type": "string"}],
    },
    "submit_student_admission": {
        "function": submit_student_admission,
        "description": "Submit student admission form",
        "category": "automation",
        "parameters": [{"name": "name", "type": "string"}],
    },
    "upload_file": {
        "function": upload_file,
        "description": "Upload a file to a website",
        "category": "browser",
        "parameters": [
            {"name": "selector", "type": "string"},
            {"name": "file_path", "type": "string"},
        ],
    },
    "get_status": {
        "function": get_status,
        "description": "Get assistant status",
        "category": "system",
        "parameters": [],
    },
    
    "open_notepad": {

    "function": open_notepad,

    "description": "Open Notepad",

    "category": "system",

    "parameters": []

 },

 "open_calculator": {

    "function": open_calculator,

    "description": "Open Calculator",

    "category": "system",

    "parameters": []

 },

 "open_vscode": {

    "function": open_vscode,

    "description": "Open VS Code",

    "category": "system",

    "parameters": []

 }, 
 
 "search_whatsapp_contact": {

    "function": search_whatsapp_contact,

    "description": "Search a contact on WhatsApp",

    "category": "browser",

    "parameters": [

        "name"

    ]

 },

 "send_whatsapp_message": {

    "function": send_whatsapp_message,

    "description": "Send a WhatsApp message to a contact",

    "category": "browser",

    "parameters": [

        "name",

        "message"

    ]

 },
 
 "open_whatsapp": {

    "function": open_website,

    "description": "Open WhatsApp Web",

    "category": "browser",

    "parameters": [

        "https://web.whatsapp.com"

    ]

 },
 
 "send_email": {

    "function": send_email_n8n,

    "description": "Send an email using n8n Gmail workflow",

    "category": "automation",

    "parameters": [

        {
            "name": "to",
            "type": "string"
        },

        {
            "name": "subject",
            "type": "string"
        },

        {
            "name": "message",
            "type": "string"
        }

    ]

},
 
    
}
