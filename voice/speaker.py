import os
import subprocess
import winsound


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PIPER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "piper",
    "piper.exe"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "piper",
    "voices",
    "en_US-lessac-medium.onnx"
)


def speak(text):

    print(f"\nAstra: {text}")

    try:

        output_file = os.path.join(
            BASE_DIR,
            "temp_voice.wav"
        )

        subprocess.run(
            [
                PIPER_PATH,
                "--model",
                MODEL_PATH,
                "--output_file",
                output_file
            ],
            input=text,
            text=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        winsound.PlaySound(
            output_file,
            winsound.SND_FILENAME
        )

    except Exception as e:

        print(
            f"\nSpeaker Error: {e}"
        )