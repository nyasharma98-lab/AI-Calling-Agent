import re

# Words the model often gets wrong -> what you want instead
CORRECTIONS = {
    r"\bEI\b": "AI",
    r"\bhope and help\b": "here to help",
}

def correct_text(text):
    for wrong, right in CORRECTIONS.items():
        text = re.sub(wrong, right, text, flags=re.IGNORECASE)
    return text
import os
import bz2
import tempfile
from faster_whisper import WhisperModel

PHYSICAL_CORES = max(1, (os.cpu_count() or 8) // 2)

model = WhisperModel(
    "tiny.en",
    device="cpu",
    compute_type="int8",
    cpu_threads=PHYSICAL_CORES
)


def ensure_plain_audio(audio_file):
    """If the file is bzip2-wrapped, decompress it to a temp file and return that path.
    Otherwise return the original path unchanged."""
    with open(audio_file, "rb") as f:
        head = f.read(3)
    if head != b"BZh":
        return audio_file

    with open(audio_file, "rb") as f:
        data = bz2.decompress(f.read())
    ext = os.path.splitext(audio_file)[1] or ".m4a"
    out = os.path.join(tempfile.gettempdir(), "stt_decompressed" + ext)
    with open(out, "wb") as f:
        f.write(data)
    return out


def convert_speech_to_text(audio_file):
    try:
        print(f"Opening audio file: {audio_file}")
        audio_file = ensure_plain_audio(audio_file)

        segments, info = model.transcribe(
            audio_file,
            beam_size=1,
            language="en",
            vad_filter=False,
            condition_on_previous_text=False
        )

        extracted_text = []
        for segment in segments:
            print(f"Found segment text: {segment.text}")
            extracted_text.append(segment.text)

        full_text = correct_text(" ".join(extracted_text).strip())
        print(f"Final transcribed text: '{full_text}'")
        return full_text

    except Exception as e:
        import traceback
        traceback.print_exc()
        return ""