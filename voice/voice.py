import os
import sys
import tempfile
import speech_recognition as sr
import whisper

# Ensure Unicode characters (Urdu / Arabic / UTF-8) print cleanly on Windows
try:
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_model = None

def get_whisper_model():
    """Lazy-load Whisper multilingual model."""
    global _model
    if _model is None:
        print("\nLoading Whisper model (multilingual English & Urdu)...")
        _model = whisper.load_model("base")
        print("Whisper loaded successfully.")
    return _model


WAKE_WORDS = [
    "hey astra",
    "hi astra",
    "hello astra",
    "astra",
    "astro",
    "assistant",
    "استرا",
    "سنو استرا"
]


def clean_voice_command(raw_text: str) -> str:
    """Strips wake words, leading punctuation, and standardizes spoken command."""
    if not raw_text:
        return ""
    
    text = raw_text.strip()
    
    # Strip common wake words from beginning
    lower_text = text.lower()
    for ww in WAKE_WORDS:
        if lower_text.startswith(ww):
            text = text[len(ww):].strip()
            lower_text = text.lower()
            break
            
    # Strip leading commas, colons, hyphens
    text = text.lstrip(",.:;!- ").strip()
    return text


def transcribe_audio(audio) -> str:
    """Transcribes audio using Whisper with auto-detection for English and Urdu."""
    model = get_whisper_model()
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio.get_wav_data())
        temp_path = temp_audio.name

    try:
        # Provide domain & bilingual context via initial_prompt
        initial_prompt = "Astra, LinkedIn, YouTube, jobs, search, volume, calculator, notepad, WhatsApp, Boss, اردو, السلام علیکم"
        
        result = model.transcribe(
            temp_path,
            fp16=False,
            language=None,  # Whisper automatically detects English or Urdu
            task="transcribe",
            initial_prompt=initial_prompt,
            condition_on_previous_text=False
        )

        raw_text = result["text"].strip()
        detected_lang = result.get("language", "unknown")
        
        print(f"\n[STT] Detected language: {detected_lang}")
        clean_text = clean_voice_command(raw_text)
        print(f"[STT] Transcribed: '{clean_text}' (raw: '{raw_text}')")
        return clean_text

    except Exception as e:
        print(f"\n[STT Error]: {e}")
        return ""
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


def listen(timeout=None, phrase_time_limit=7) -> str:
    """Listens to the microphone and returns the transcribed English or Urdu command."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 500
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.5
    recognizer.phrase_threshold = 0.4

    try:
        with sr.Microphone() as source:
            print("\n🎙️ Listening for your voice (English or Urdu)...")
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        print("\n⏳ Processing speech...")
        command = transcribe_audio(audio)
        return command

    except sr.UnknownValueError:
        print("\nCould not understand audio.")
        return ""

    except sr.WaitTimeoutError:
        return ""

    except KeyboardInterrupt:
        print("\nStopping voice listener...")
        return ""

    except Exception as e:
        print(f"\nVoice Error: {e}")
        return ""