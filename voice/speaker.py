import os
import re
import sys
import time
import ctypes
import asyncio
import concurrent.futures

# High-Quality Natural Neural Male Voices
VOICE_URDU_MALE = "ur-PK-AsadNeural"               # Authentic Pakistani male Urdu neural voice
VOICE_ENGLISH_MALE = "en-US-AndrewMultilingualNeural"  # Highly natural, clear male English voice

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_AUDIO_PATH = os.path.join(BASE_DIR, "temp_voice.mp3")

# Roman Urdu common detection keywords
ROMAN_URDU_WORDS = {
    "boss", "main", "hoon", "mein", "aap", "kaam", "assalam", "theek", "shukriya", 
    "kya", "hai", "hain", "kar", "karo", "karna", "liya", "diya", "khol", "kholo", 
    "dhund", "dhundo", "acha", "achha", "batao", "sunaiye", "tayyar", "rakho", 
    "aaj", "kuch", "shukran", "walekum", "salaam", "bhai", "janaab"
}


def is_urdu_text(text: str) -> bool:
    """Detect if text is in Urdu (either Urdu script or Roman Urdu)."""
    if not text:
        return False
        
    # Check for Urdu/Arabic Unicode characters
    if re.search(r"[\u0600-\u06FF]", text):
        return True
        
    # Check for Roman Urdu markers
    words = set(re.findall(r"\b\w+\b", text.lower()))
    urdu_matches = words.intersection(ROMAN_URDU_WORDS)
    if len(urdu_matches) >= 2 or (len(urdu_matches) >= 1 and len(words) <= 5):
        return True
        
    return False


def play_audio_file(file_path: str):
    """Play MP3 audio through Windows native MCI without external player popups or hanging."""
    abs_path = os.path.abspath(file_path)
    alias = f"astra_v_{int(time.time() * 1000)}"
    buf = ctypes.create_unicode_buffer(128)

    try:
        # Open media file
        ctypes.windll.winmm.mciSendStringW(f'open "{abs_path}" type mpegvideo alias {alias}', None, 0, None)
        
        # Get duration in milliseconds
        ctypes.windll.winmm.mciSendStringW(f'set {alias} time format milliseconds', None, 0, None)
        ctypes.windll.winmm.mciSendStringW(f'status {alias} length', buf, 128, None)
        length_ms = int(buf.value) if buf.value.isdigit() else 2000

        # Start playback
        ctypes.windll.winmm.mciSendStringW(f'play {alias}', None, 0, None)

        # Wait until playback completes
        start_time = time.time()
        timeout_sec = (length_ms / 1000.0) + 0.3
        while True:
            ctypes.windll.winmm.mciSendStringW(f'status {alias} mode', buf, 128, None)
            mode = buf.value.strip().lower()
            if mode != "playing" or (time.time() - start_time) > timeout_sec:
                break
            time.sleep(0.04)

    except Exception as e:
        print(f"[Speaker Playback Error]: {e}")
    finally:
        ctypes.windll.winmm.mciSendStringW(f'close {alias}', None, 0, None)


async def _synthesize_edge_tts(text: str, voice: str, output_path: str):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def _synthesize(text: str, voice: str, output_path: str):
    """Run async Edge-TTS safely in any context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(asyncio.run, _synthesize_edge_tts(text, voice, output_path)).result()
    else:
        asyncio.run(_synthesize_edge_tts(text, voice, output_path))


def fallback_speak_pyttsx3(text: str):
    """Offline fallback using Windows SAPI5 Male Voice (David)."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        for v in voices:
            if "david" in v.name.lower() or "male" in v.name.lower():
                engine.setProperty("voice", v.id)
                break
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Fallback TTS Error]: {e}")


def speak(text: str, force_voice: str = None):
    """
    Synthesizes and speaks text using a natural male voice.
    Automatically chooses:
    - ur-PK-AsadNeural for Urdu / Roman Urdu
    - en-US-AndrewMultilingualNeural for English
    """
    if not text or not text.strip():
        return

    clean_text = text.strip()
    print(f"\nAstra: {clean_text}")

    # Determine optimal voice
    if force_voice:
        selected_voice = force_voice
    elif is_urdu_text(clean_text):
        selected_voice = VOICE_URDU_MALE
    else:
        selected_voice = VOICE_ENGLISH_MALE

    try:
        # Edge TTS High-Fidelity Natural Voice
        _synthesize(clean_text, selected_voice, TEMP_AUDIO_PATH)
        play_audio_file(TEMP_AUDIO_PATH)
    except Exception as e:
        print(f"[Edge TTS Error]: {e}. Using offline fallback male voice...")
        fallback_speak_pyttsx3(clean_text)


if __name__ == "__main__":
    print("Testing Urdu natural male voice...")
    speak("Assalam-o-Alaikum Boss! Main Astra hoon, aapka personal AI assistant.")
    print("Testing English natural male voice...")
    speak("Hello Boss! All systems are fully operational and ready.")