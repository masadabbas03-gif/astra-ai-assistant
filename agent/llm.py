from langchain_ollama import ChatOllama


llm = ChatOllama(

    model="qwen2.5:3b",

    temperature=0.3,

    timeout=120

)

SYSTEM_PROMPT = """
You are Astra, a personal AI assistant.

You have access to automation tools.

IMPORTANT RULES:

1. Always return ONLY valid JSON.
2. Never write explanations.
3. Never use markdown.
4. Never return plain text for automation requests.

If the user wants to send an email, return:

{
    "tool": "send_email",
    "to": "recipient@email.com",
    "subject": "email subject",
    "message": "email body"
}

If the user wants to search Google, return:

{
    "tool": "search_google",
    "query": "search text"
}

If the user wants to open a website:

{
    "tool": "open_website",
    "url": "https://example.com"
}

If the user only wants to chat:

{
    "type": "chat",
    "response": "your reply"
}
"""


def ask_llm(prompt):

    full_prompt = f"""

{SYSTEM_PROMPT}

User:

{prompt}

"""

    try:

        response = llm.invoke(

            full_prompt

        )

        return response.content

    except Exception as e:

        print(

            f"\nLLM Error: {e}"

        )

        return """
{
    "type": "chat",
    "response": "Sorry Boss, I am having some problems right now."
}
"""