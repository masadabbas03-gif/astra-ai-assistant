import json
import re

from agent.executor import get_available_tools
from agent.llm import ask_llm
from agent.profile import load_profile

from personality.personality import (
    get_greeting,
    who_created_you,
    how_are_you
)

from contact_manager.add_contact import add_contact
from contact_manager.get_contact import get_contact
from contact_manager.update_contact import update_contact
from contact_manager.delete_contact import delete_contact


def think(user_input):

    text = user_input.lower().strip()

    profile = load_profile()

    # ======================
    # Save contact
    # ======================

    contact_patterns = [

        r"remember (.+?)'?s number is (\d+)",

        r"save (.+?)'?s number (\d+)",

        r"save contact (.+?) (\d+)",

        r"add contact (.+?) (\d+)",

        r"remember contact (.+?) (\d+)",

        r"(.+?) ka number yaad rakho (\d+)",

        r"(.+?) ka contact save karo (\d+)"

    ]

    match = None

    for pattern in contact_patterns:

        match = re.search(

            pattern,

            text

        )

        if match:

            break

    if match:

        name = match.group(

            1

        ).strip()

        phone = match.group(

            2

        ).strip()

        result = add_contact(

            name=name,

            phone=phone

        )

        return json.dumps(

            {

                "type": "chat",

                "response": result

            },

            ensure_ascii=False

        )

    # ======================
    # Get contact
    # ======================

    match = re.search(

        r"what is (.+?)'?s number",

        text

    )

    if match:

        name = match.group(

            1

        ).strip()

        contact = get_contact(

            name

        )

        if contact:

            return json.dumps(

                {

                    "type": "chat",

                    "response": f"{name}'s number is {contact['phone']}"

                },

                ensure_ascii=False

            )

        return json.dumps(

            {

                "type": "chat",

                "response": "Contact not found."

            },

            ensure_ascii=False

        )

    # ======================
    # Update contact
    # ======================

    match = re.search(

        r"update (.+?)'?s number to (\d+)",

        text

    )

    if match:

        name = match.group(

            1

        ).strip()

        phone = match.group(

            2

        ).strip()

        result = update_contact(

            name,

            phone

        )

        return json.dumps(

            {

                "type": "chat",

                "response": result

            },

            ensure_ascii=False

        )

    # ======================
    # Delete contact
    # ======================

    match = re.search(

        r"delete (.+?)'?s contact",

        text

    )

    if match:

        name = match.group(

            1

        ).strip()

        result = delete_contact(

            name

        )

        return json.dumps(

            {

                "type": "chat",

                "response": result

            },

            ensure_ascii=False

        )
    
    
     # ======================
    # Send WhatsApp Message
    # ======================

    match = re.search(

        r'send "(.*?)" to (.+)',

        text

    )

    if match:

        message = match.group(

            1

        ).strip()

        name = match.group(

            2

        ).strip()

        contact = get_contact(

            name

        )

        steps = [

            {

                "tool": "open_whatsapp",

                "arguments": {}

            }

        ]

        if contact:

            steps.append(

                {

                    "tool": "send_whatsapp_message",

                    "arguments": {

                        "name": contact["name"],

                        "message": message

                    }

                }

            )

        else:

            steps.append(

                {

                    "tool": "send_whatsapp_message",

                    "arguments": {

                        "name": name,

                        "message": message

                    }

                }

            )

        return json.dumps(

            {

                "type": "steps",

                "steps": steps

            },

            ensure_ascii=False

        )
    # ======================
    # Open WhatsApp
    # ======================

    match = re.search(

        r"open whatsapp and search for (.+)",

        text

    )

    if match:

        name = match.group(

            1

        ).strip()

        return json.dumps(

            {

                "type": "steps",

                "steps": [

                    {

                        "tool": "open_whatsapp",

                        "arguments": {}

                    },

                    {

                        "tool": "search_whatsapp_contact",

                        "arguments": {

                            "name": name

                        }

                    }

                ]

            },

            ensure_ascii=False

        )

    # ======================
    # Small talk
    # ======================

    if (

        "kis ne banaya" in text

        or "who created you" in text

    ):

        return json.dumps(

            {

                "type": "chat",

                "response": who_created_you()

            },

            ensure_ascii=False

        )

    if (

        "kya haal" in text

        or "kaise ho" in text

        or "how are you" in text

    ):

        return json.dumps(

            {

                "type": "chat",

                "response": how_are_you()

            },

            ensure_ascii=False

        )

    if re.search(r"\b(hello|hi|hey|assalamualaikum|assalam o alaikum)\b", text):


        return json.dumps(

            {

                "type": "chat",

                "response": get_greeting()

            },

            ensure_ascii=False

        )

    # ======================
    # Tools
    # ======================

    tools = get_available_tools()

    # ======================
    # Prompt
    # ======================

    prompt = f"""
You are {profile["assistant_name"]}.

You were created by {profile["creator"]}.

Your owner is {profile["name"]}.

He is a {profile["profession"]}.

His goals:

{profile["goals"]}

Available tools:

{tools}

Important Rules:

1. You are Astra.
2. Understand both English and Urdu.
3. Reply in the same language as the user.
4. Never answer in Chinese, Korean, Russian, Hindi, or any other language.
5. Keep responses short and natural.
6. Sometimes call the user "{profile["nickname"]}".
7. If someone asks who created you, say:

   "Muhammad Assad Abbas created me."

8. If the user's command is unclear, ask for clarification.
9. Return ONLY valid JSON.
10. Never explain your reasoning.
11. Never return markdown.
12. Never return code blocks.

If the user only wants to chat, return:

{{
    "type": "chat",
    "response": "your response"
}}

If the user wants to use a tool, return:

{{
    "type": "tool",
    "tool": "tool_name",
    "arguments": {{}}
}}

If multiple steps are needed, return:

{{
    "type": "steps",
    "steps": [
        {{
            "tool": "tool_name",
            "arguments": {{}}
        }}
    ]
}}

User:

{user_input}
"""

    response = ask_llm(

        prompt

    )

    return response