import pyttsx3


def speak_text(text):

    engine = pyttsx3.init()

    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":

    speak_text("Hello! I am your AI Calling Agent.")