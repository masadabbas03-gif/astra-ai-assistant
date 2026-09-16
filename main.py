import sys
import json
import time
from datetime import datetime

# UTF-8 console output for Windows to support Urdu characters
try:
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from agent.brain import think
from agent.executor import execute_tool
from agent.planner import create_plan
from agent.memory import save_task, save_conversation
from agent.state import update_last_command, add_message
from startup.startup import startup_message
from voice.speaker import speak

TASK_KEYWORDS = [
    "open", "search", "close", "start", "stop", "play", "create", 
    "delete", "show", "status", "calculator", "notepad", "browser",
    "volume", "battery", "lock", "screenshot", "kholo", "dhundo", "barhao", "kam"
]


def execute_user_command(user_input: str):
    """Executes a user command through planner or brain, and speaks the response."""
    if not user_input or not user_input.strip():
        return

    user_input = user_input.strip()

    # Save command to memory
    if any(keyword in user_input.lower() for keyword in TASK_KEYWORDS):
        save_task(user_input)

    update_last_command(user_input)
    add_message("user", user_input)

    # ============================
    # 1. Planner (Fast Bilingual Router)
    # ============================
    steps = create_plan(user_input)

    if steps:
        data = {
            "type": "steps",
            "steps": steps
        }
    else:
        # ============================
        # 2. Brain (LLM / Conversation)
        # ============================
        response = think(user_input)
        print("\nBrain Response:\n")
        print(response)

        # Save assistant log
        try:
            with open("logs/assistant.log", "a", encoding="utf-8") as file:
                file.write(f"\n=================================\n[{datetime.now()}]\nUser: {user_input}\nResponse: {response}\n=================================\n")
        except Exception:
            pass

        try:
            data = json.loads(response)
        except Exception:
            print("\nAstra:\n")
            print(response)
            speak(response)
            time.sleep(0.5)
            return

    # ============================
    # Chat Response Mode
    # ============================
    if data.get("type") == "chat":
        message = data.get("response", "Okay Boss.")
        add_message("assistant", message)
        print("\nAstra:\n")
        print(message)
        save_conversation(user_input, message)
        # Speak Astra's response using natural male voice (English or Urdu)
        speak(message)
        time.sleep(0.5)
        return

    # ============================
    # Multi-Step Execution Mode
    # ============================
    if data.get("type") == "steps":
        steps = data.get("steps", [])
        for index, step in enumerate(steps, start=1):
            tool_name = step.get("tool")
            arguments = step.get("arguments", {})
            if tool_name is None:
                continue

            print(f"\nExecuting Step {index}: {tool_name}")
            if isinstance(arguments, dict):
                result = execute_tool(tool_name, **arguments)
            else:
                result = execute_tool(tool_name, *arguments)

            add_message("assistant", str(result))
            print("\nAssistant:\n")
            print(result)

            # Speak result for non-LinkedIn tools (LinkedIn tools have their own dedicated speech)
            if result and isinstance(result, str) and not tool_name.startswith("search_linkedin") and not tool_name.startswith("open_linkedin"):
                # Shorten long text if necessary
                spoken_text = result if len(result) < 180 else f"Command completed: {tool_name}"
                speak(spoken_text)

            time.sleep(0.5)
        return

    # ============================
    # Single Tool Mode
    # ============================
    if data.get("type") == "tool":
        tool_name = data.get("tool")
        arguments = data.get("arguments", {})
        if tool_name is None:
            print("\nNo tool selected.")
            return

        print(f"\nExecuting: {tool_name}")
        if isinstance(arguments, dict):
            result = execute_tool(tool_name, **arguments)
        else:
            result = execute_tool(tool_name, *arguments)

        add_message("assistant", str(result))
        print("\nAssistant:\n")
        print(result)
        
        if result and isinstance(result, str) and not tool_name.startswith("search_linkedin") and not tool_name.startswith("open_linkedin"):
            spoken_text = result if len(result) < 180 else f"Completed {tool_name}"
            speak(spoken_text)

        time.sleep(0.5)
        return


def main():
    print("Main function started")
    startup_message()

    voice_mode = "--voice" in sys.argv

    if voice_mode:
        print("\n[🎙️ Astra Voice Mode Activated] Speak in English or Urdu...")
        speak("Voice mode active Boss. Main sun raha hoon.")

    while True:
        try:
            if voice_mode:
                from voice.voice import listen
                user_input = listen(timeout=10, phrase_time_limit=7)
                if not user_input:
                    continue
                print(f"\nYou (Voice): {user_input}")
            else:
                user_input = input("\nYou (or type 'voice' for hands-free): ").strip()

        except KeyboardInterrupt:
            print("\nStopping Astra...")
            speak("Goodbye Boss. Take care!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            continue

        if user_input == "":
            continue

        # Toggle Voice Mode
        if user_input.lower() == "voice":
            voice_mode = True
            print("\n[🎙️ Astra Voice Mode Activated] Speak in English or Urdu...")
            speak("Hands-free voice mode active. Main tayyar hoon Boss.")
            continue

        if user_input.lower() == "text":
            voice_mode = False
            print("\n[⌨️ Text Mode Activated]")
            continue

        if user_input.lower() in ["exit", "quit", "stop astra", "bye"]:
            print("\nGoodbye Boss!")
            speak("Goodbye Boss! Have a productive day.")
            break

        execute_user_command(user_input)


if __name__ == "__main__":
    main()