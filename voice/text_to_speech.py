import pyttsx3
import tempfile
import os


def speak_text(text):

    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()


def generate_speech_audio(text):

    audio_path = tempfile.mktemp(suffix=".wav")

    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    engine.save_to_file(text, audio_path)
    engine.runAndWait()

    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    os.remove(audio_path)

    return audio_bytes