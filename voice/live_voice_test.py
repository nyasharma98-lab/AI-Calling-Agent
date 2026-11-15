import sounddevice as sd
from scipy.io.wavfile import write

from voice.speech_to_text import convert_speech_to_text
from voice.text_to_speech import speak_text
from voice.gemini_brain import get_gemini_response


def live_voice_test():

    duration = 5
    sample_rate = 16000

    audio_file = "voice/recording.wav"

    print("AI Calling Agent is ready!")
    print("Say 'Bye' to end the conversation.")

    while True:

        print("\nSpeak now...")

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        write(audio_file, sample_rate, recording)

        print("Recording completed!")

        recognized_text = convert_speech_to_text(audio_file)

        print("You said:", recognized_text)

        if not recognized_text:
            print("I could not understand. Please try again.")
            continue

        response = get_gemini_response(recognized_text)

        print("Agent:", response)

        speak_text(response)

        exit_words = ["bye", "goodbye", "end the call", "hang up"]

        if any(word in recognized_text.lower() for word in exit_words):
         print("Conversation ended. Thank you for calling!")
        break


if __name__ == "__main__":
    live_voice_test()