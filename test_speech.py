from voice.speech_to_text import convert_speech_to_text

print("Starting speech recognition...")

try:
    result = convert_speech_to_text("voice/recording.m4a")

    print("Speech recognition finished.")
    print("TRANSCRIPTION:", repr(result))

except Exception as e:
    print("ERROR:", e)