from datetime import datetime
from voice.speaker import speak
from personality.personality import get_greeting
from agent.profile import load_profile
from tools.laptop_tools import get_battery_status


def get_time_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Good night"


def startup_message():
    profile = load_profile()
    nickname = profile.get("nickname", "Boss")
    assistant_name = profile.get("assistant_name", "Astra")
    time_greeting = get_time_greeting()
    battery_info = get_battery_status()
    current_time = datetime.now().strftime("%I:%M %p")

    message = f"""
{time_greeting}, {nickname}!
I am {assistant_name}, your laptop AI operating system.
The time is {current_time}.
{battery_info}
All systems are online and ready to assist you.
"""
    print(message)
    speak(f"{time_greeting} {nickname}. I am {assistant_name}. {battery_info}. Ready to assist you.")