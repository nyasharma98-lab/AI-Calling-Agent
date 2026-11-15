import sounddevice as sd
from scipy.io.wavfile import write

from voice.speech_to_text import convert_speech_to_text
from voice.text_to_speech import speak_text
from voice.gemini_brain import get_gemini_response
import time
from src.call_manager import add_call


def record_audio():

    duration = 5
    sample_rate = 16000
    audio_file = "voice/recording.wav"

    print("\nListening... Speak now.")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()
    write(audio_file, sample_rate, recording)

    print("Recording completed!")

    return convert_speech_to_text(audio_file)


def start_call(mode):
    customer_id = int(input("Enter existing customer ID: "))
    start_time = time.time()
    conversation_text = []

    print("\nAI Calling Agent Started!")

    if mode == "inbound":
        print("Simulating an incoming customer call.")

        greeting = (
            "Hello! Thank you for calling. "
            "How may I help you today?"
        )

    else:
        print("Simulating an outgoing customer call.")

        greeting = (
            "Hello! This is your AI Calling Agent. "
            "I am calling to assist you. "
            "Is this a good time to talk?"
        )

    print("Agent:", greeting)
    speak_text(greeting)

    while True:

        recognized_text = record_audio()

        print("You said:", recognized_text)
        conversation_text.append(recognized_text)

        if not recognized_text:
            print("I could not understand. Please try again.")
            continue

        response = get_gemini_response(recognized_text)

        print("Agent:", response)
        speak_text(response)

        exit_words = [
            "bye",
            "goodbye",
            "end the call",
            "hang up"
        ]

        if any(word in recognized_text.lower() for word in exit_words):
            print("\nCall ended.")
            break

    duration = int(time.time() - start_time)

    summary = " ".join(conversation_text)

    result = add_call(
        customer_id=customer_id,
        call_type=mode,
        duration_seconds=duration,
        status="completed",
        summary=summary
    )

    print("Call saved successfully!")
    print(result)


if __name__ == "__main__":

    print("\n===== AI CALLING AGENT =====")
    print("1. Inbound Call Simulation")
    print("2. Outbound Call Simulation")

    choice = input("\nChoose a mode (1 or 2): ")

    if choice == "1":
        start_call("inbound")

    elif choice == "2":
        start_call("outbound")

    else:
        print("Invalid choice. Please select 1 or 2.")