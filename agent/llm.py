from langchain_ollama import ChatOllama


llm = ChatOllama(

    model="qwen2.5:3b",

    temperature=0.3,

    timeout=120

)

def ask_llm(prompt):

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        print(
            f"\nLLM Error: {e}"
        )
        return """{
    "type": "chat",
    "response": "Sorry Boss, I am having some problems right now."
}"""