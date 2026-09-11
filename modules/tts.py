import os
import tempfile

from gtts import gTTS


def generate_audio(text):
    """
    Convert English text to speech.
    Returns the generated MP3 file path.
    """

    if not text.strip():
        return None

    try:

        tts = gTTS(
            text=text,
            lang="en",
            slow=False
        )

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        temp_file.close()

        tts.save(
            temp_file.name
        )

        return temp_file.name

    except Exception:
        return None