import io

import speech_recognition as sr


def speech_to_text(audio_data):
    """
    Convert WAV audio bytes into English text.
    """

    recognizer = sr.Recognizer()

    try:

        audio_stream = io.BytesIO(
            audio_data
        )

        with sr.AudioFile(audio_stream) as source:

            audio = recognizer.record(
                source
            )


        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )


        return text, None


    except sr.UnknownValueError:

        return (
            None,
            "Could not understand the audio."
        )


    except sr.RequestError:

        return (
            None,
            "Speech recognition service is unavailable."
        )


    except Exception as e:

        return (
            None,
            f"Speech recognition error: {e}"
        )