import speech_recognition as sr
import whisper
import tempfile
import os


print("\nLoading Whisper model...")

model = whisper.load_model(
    "base"
)

print(
    "Whisper loaded successfully."
)


WAKE_WORDS = [

    "astra",
    "astro",
    "assistant"

]


def transcribe_audio(audio):

    with tempfile.NamedTemporaryFile(

        suffix=".wav",
        delete=False

    ) as temp_audio:

        temp_audio.write(

            audio.get_wav_data()

        )

        temp_path = temp_audio.name

    try:

        result = model.transcribe(

            temp_path,

            fp16=False,

            language=None,

            task="transcribe",

            condition_on_previous_text=False

        )

        text = result[
            "text"
        ].strip()

        language = result[
            "language"
        ]

        print(

            f"\nDetected language: {language}"

        )

        return text

    finally:

        if os.path.exists(
            temp_path
        ):

            os.remove(
                temp_path
            )


def listen():

    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 500

    recognizer.dynamic_energy_threshold = True

    recognizer.pause_threshold = 1.5

    recognizer.phrase_threshold = 0.5

    try:

        with sr.Microphone() as source:

            print(
                "\nListening..."
            )

            recognizer.adjust_for_ambient_noise(

                source,

                duration=1

            )

            audio = recognizer.listen(

                source,

                timeout=None,

                phrase_time_limit=5

            )

        print(
            "\nProcessing..."
        )

        command = transcribe_audio(

            audio

        )

        command = command.lower()

        print(

            f"\nYou said: {command}"

        )

        return command

    except sr.UnknownValueError:

        print(

            "\nCould not understand audio."

        )

        return ""

    except sr.WaitTimeoutError:

        print(

            "\nListening timed out."

        )

        return ""

    except KeyboardInterrupt:

        print(

            "\nStopping Astra..."

        )

        raise SystemExit

    except Exception as e:

        print(

            f"\nVoice Error: {e}"

        )

        return ""