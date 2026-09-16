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
from tools.laptop_tools import (
    get_battery_status,
    get_system_stats,
    set_volume,
    get_volume,
    volume_up,
    volume_down,
    mute_volume,
    unmute_volume,
    set_brightness,
    get_brightness,
    lock_laptop,
    close_application,
    take_desktop_screenshot
)
from startup.manage_startup import (
    enable_windows_startup,
    disable_windows_startup,
    check_startup_status
)
from tools.linkedin_tools import (
    search_linkedin_jobs,
    open_linkedin_job,
    create_linkedin_post,
    update_linkedin_profile
)



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

    "function": open_whatsapp,

    "description": "Open WhatsApp Web",

    "category": "browser",

    "parameters": []

 },

 
    "send_email": {
        "function": send_email_n8n,
        "description": "Send an email using n8n Gmail workflow",
        "category": "automation",
        "parameters": [
            {"name": "to", "type": "string"},
            {"name": "subject", "type": "string"},
            {"name": "message", "type": "string"},
        ],
    },
    "get_battery_status": {
        "function": get_battery_status,
        "description": "Get laptop battery level and charging status",
        "category": "laptop",
        "parameters": [],
    },
    "get_system_stats": {
        "function": get_system_stats,
        "description": "Get current CPU, RAM, and Disk utilization",
        "category": "laptop",
        "parameters": [],
    },
    "set_volume": {
        "function": set_volume,
        "description": "Set system audio volume percentage (0 to 100)",
        "category": "laptop",
        "parameters": [{"name": "level_percent", "type": "integer"}],
    },
    "get_volume": {
        "function": get_volume,
        "description": "Get current system audio volume level",
        "category": "laptop",
        "parameters": [],
    },
    "volume_up": {
        "function": volume_up,
        "description": "Increase system audio volume by 10 percent",
        "category": "laptop",
        "parameters": [],
    },
    "volume_down": {
        "function": volume_down,
        "description": "Decrease system audio volume by 10 percent",
        "category": "laptop",
        "parameters": [],
    },
    "mute_volume": {
        "function": mute_volume,
        "description": "Mute system audio",
        "category": "laptop",
        "parameters": [],
    },
    "unmute_volume": {
        "function": unmute_volume,
        "description": "Unmute system audio",
        "category": "laptop",
        "parameters": [],
    },
    "set_brightness": {
        "function": set_brightness,
        "description": "Set laptop screen brightness percentage (0 to 100)",
        "category": "laptop",
        "parameters": [{"name": "level_percent", "type": "integer"}],
    },
    "get_brightness": {
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

    "function": open_whatsapp,

    "description": "Open WhatsApp Web",

    "category": "browser",

    "parameters": []

 },

 
    "send_email": {
        "function": send_email_n8n,
        "description": "Send an email using n8n Gmail workflow",
        "category": "automation",
        "parameters": [
            {"name": "to", "type": "string"},
            {"name": "subject", "type": "string"},
            {"name": "message", "type": "string"},
        ],
    },
    "get_battery_status": {
        "function": get_battery_status,
        "description": "Get laptop battery level and charging status",
        "category": "laptop",
        "parameters": [],
    },
    "get_system_stats": {
        "function": get_system_stats,
        "description": "Get current CPU, RAM, and Disk utilization",
        "category": "laptop",
        "parameters": [],
    },
    "set_volume": {
        "function": set_volume,
        "description": "Set system audio volume percentage (0 to 100)",
        "category": "laptop",
        "parameters": [{"name": "level_percent", "type": "integer"}],
    },
    "get_volume": {
        "function": get_volume,
        "description": "Get current system audio volume level",
        "category": "laptop",
        "parameters": [],
    },
    "volume_up": {
        "function": volume_up,
        "description": "Increase system audio volume by 10 percent",
        "category": "laptop",
        "parameters": [],
    },
    "volume_down": {
        "function": volume_down,
        "description": "Decrease system audio volume by 10 percent",
        "category": "laptop",
        "parameters": [],
    },
    "mute_volume": {
        "function": mute_volume,
        "description": "Mute system audio",
        "category": "laptop",
        "parameters": [],
    },
    "unmute_volume": {
        "function": unmute_volume,
        "description": "Unmute system audio",
        "category": "laptop",
        "parameters": [],
    },
    "set_brightness": {
        "function": set_brightness,
        "description": "Set laptop screen brightness percentage (0 to 100)",
        "category": "laptop",
        "parameters": [{"name": "level_percent", "type": "integer"}],
    },
    "get_brightness": {
        "function": get_brightness,
        "description": "Get current laptop screen brightness percentage",
        "category": "laptop",
        "parameters": [],
    },
    "lock_laptop": {
        "function": lock_laptop,
        "description": "Lock laptop workstation / screen immediately",
        "category": "laptop",
        "parameters": [],
    },
    "close_application": {
        "function": close_application,
        "description": "Close a running application by name (e.g. notepad, chrome, calc)",
        "category": "laptop",
        "parameters": [{"name": "app_name", "type": "string"}],
    },
    "take_desktop_screenshot": {
        "function": take_desktop_screenshot,
        "description": "Take a screenshot of the entire laptop desktop screen",
        "category": "laptop",
        "parameters": [],
    },
    "enable_windows_startup": {
        "function": enable_windows_startup,
        "description": "Enable Astra auto-launch whenever the laptop is turned on or logged in",
        "category": "system",
        "parameters": [],
    },
    "disable_windows_startup": {
        "function": disable_windows_startup,
        "description": "Disable Astra auto-launch on Windows startup",
        "category": "system",
        "parameters": [],
    },
    "check_startup_status": {
        "function": check_startup_status,
        "description": "Check if Astra auto-launch on Windows startup is currently enabled or disabled",
        "category": "system",
        "parameters": [],
    },
    "search_linkedin_jobs": {
        "function": search_linkedin_jobs,
        "description": "Searches and curates top 10 most relevant jobs matching CV from LinkedIn, computes match scores, and saves to neat CSV and Markdown files",
        "category": "browser",
        "parameters": [
            {"name": "keywords", "type": "string"},
            {"name": "location", "type": "string"},
            {"name": "limit", "type": "integer"}
        ],
    },
    "open_linkedin_job": {
        "function": open_linkedin_job,
        "description": "Opens a curated LinkedIn job page from the top 10 list by rank number (1-10) in the browser, and optionally clicks Easy Apply with user confirmation before submission",
        "category": "browser",
        "parameters": [
            {"name": "job_index", "type": "integer"},
            {"name": "click_easy_apply", "type": "boolean"},
            {"name": "auto_fill_steps", "type": "boolean"}
        ],
    },
    "create_linkedin_post": {
        "function": create_linkedin_post,
        "description": "Creates and drafts or publishes a post on LinkedIn about a project or custom topic",
        "category": "browser",
        "parameters": [
            {"name": "text", "type": "string"},
            {"name": "project_name", "type": "string"},
            {"name": "auto_publish", "type": "boolean"}
        ],
    },
    "update_linkedin_profile": {
        "function": update_linkedin_profile,
        "description": "Updates your LinkedIn profile headline or about description automatically",
        "category": "browser",
        "parameters": [
            {"name": "headline", "type": "string"},
            {"name": "about", "type": "string"},
            {"name": "auto_save", "type": "boolean"}
        ],
    },
}

