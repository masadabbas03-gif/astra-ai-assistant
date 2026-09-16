from playwright.sync_api import sync_playwright
from agent.state import state
import os

playwright = None
browser = None
page = None



def start_browser():

    global playwright
    global browser
    global page

    if state["browser_running"]:

        return "Browser already running."

    profile_path = os.path.abspath(

        "browser_profile"

    )

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch_persistent_context(

        user_data_dir=profile_path,

        headless=False

    )

    pages = browser.pages

    if pages:

        page = pages[0]

    else:

        page = browser.new_page()

    state["browser_running"] = True

    return "Browser started."


def get_browser_page():
    global page
    if page is None:
        start_browser()
    return page


def open_website(url):

    global page

    if page is None:

        start_browser()

    page.goto(


        url,

        wait_until="domcontentloaded",

        timeout=120000

    )

    state["current_website"] = url

    return f"Opened {url}"

def search_google(query):

    global page

    if page is None:

        start_browser()

    page.goto(f"https://www.google.com/search?q={query}")

    return f"Searching for {query}"


def close_browser():

    global browser
    global playwright
    global page

    if browser is not None:

        browser.close()

    if playwright is not None:

        playwright.stop()

    browser = None
    page = None
    playwright = None

    state["browser_running"] = False
    state["current_website"] = None

    return "Browser closed."


def click_element(selector):

    global page

    if page is None:

        return "Browser is not running."

    page.click(selector)

    return f"Clicked: {selector}"


def fill_input(selector, text):

    global page

    if page is None:

        return "Browser is not running."

    page.fill(selector, text)

    return f"Entered '{text}'"


def get_text(selector):

    global page

    if page is None:

        return "Browser is not running."

    text = page.text_content(selector)

    return text


def take_screenshot(filename="screenshot.png"):

    global page

    if page is None:

        return "Browser is not running."

    page.screenshot(path=filename)

    return f"Screenshot saved as {filename}"


def select_option(selector, value):

    global page

    if page is None:

        return "Browser not started."

    page.select_option(selector, value)

    return f"Selected {value}"


def upload_file(selector, file_path):

    global page

    if page is None:

        return "Browser not started."

    page.set_input_files(selector, file_path)

    return f"Uploaded {file_path}"


def extract_text(selector):

    global page

    if page is None:

        return "Browser not started."

    text = page.text_content(selector)

    return text


def extract_multiple(selector):

    global page

    if page is None:

        return []

    elements = page.locator(selector)

    count = elements.count()

    results = []

    for i in range(count):

        results.append(elements.nth(i).text_content())

    return results


def get_status():

    return state


def open_whatsapp():

    return open_website(

        "https://web.whatsapp.com"

    )


def search_whatsapp_contact(name):

    global page

    if page is None:

        return "Browser not started."

    search_box = page.locator(

        'div[contenteditable="true"]'

    ).first

    search_box.click()

    search_box.fill(

        name

    )

    return f"Searching for {name} on WhatsApp."

def send_whatsapp_message(name, message):

    global page

    if page is None:

        return "Browser not started."

    try:

        page.wait_for_timeout(

            5000

        )

        search_box = page.locator(

            'input[aria-label="Search or start a new chat"]'

        )

        search_box.click()

        search_box.fill(

            ""

        )

        search_box.fill(

            name

        )

        page.wait_for_timeout(

            3000

        )

        page.keyboard.press(

            "Enter"

        )

        page.wait_for_timeout(

            3000

        )

        message_box = page.locator(

            'div[contenteditable="true"][role="textbox"]'

        ).last

        message_box.click()

        page.keyboard.type(

            message

        )

        page.keyboard.press(

            "Enter"

        )

        return f"Message sent to {name}"

    except Exception as e:

        return f"Error sending message: {e}"