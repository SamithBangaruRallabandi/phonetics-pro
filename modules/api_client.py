import os
import requests

import os
import requests

try:
    import streamlit as st

    API_URL = st.secrets.get(
        "API_URL",
        "http://127.0.0.1:8000"
    )

except Exception:
    API_URL = os.getenv(
        "API_URL",
        "http://127.0.0.1:8000"
    )

def analyze_text_api(text):
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={"text": text},
            timeout=30
        )

        response.raise_for_status()
        return response.json(), None

    except requests.exceptions.ConnectionError:
        return None, "Could not connect to the FastAPI server."

    except requests.exceptions.Timeout:
        return None, "The FastAPI server took too long to respond."

    except requests.exceptions.RequestException as e:
        return None, f"API error: {e}"


def analyze_speech_api(audio_file):
    try:
        audio_file.seek(0)

        files = {
            "file": ("speech.wav", audio_file, "audio/wav")
        }

        response = requests.post(
            f"{API_URL}/analyze-speech",
            files=files,
            timeout=60
        )

        response.raise_for_status()
        return response.json(), None

    except requests.exceptions.ConnectionError:
        return None, "Could not connect to the FastAPI server."

    except requests.exceptions.Timeout:
        return None, "Speech analysis timed out."

    except requests.exceptions.RequestException as e:
        return None, f"API error: {e}"

def generate_tts_api(text):
    try:
        response = requests.post(
            f"{API_URL}/tts",
            json={"text": text},
            timeout=60
        )

        response.raise_for_status()
        return response.content, None

    except requests.exceptions.ConnectionError:
        return None, "Could not connect to the FastAPI server."

    except requests.exceptions.Timeout:
        return None, "Text-to-speech request timed out."

    except requests.exceptions.RequestException as e:
        return None, f"TTS API error: {e}"

def score_pronunciation_api(expected_text, recognized_text):
    try:
        response = requests.post(
            f"{API_URL}/score",
            json={
                "expected_text": expected_text,
                "recognized_text": recognized_text
            },
            timeout=30
        )

        response.raise_for_status()
        return response.json(), None

    except requests.exceptions.ConnectionError:
        return None, "Could not connect to the FastAPI server."

    except requests.exceptions.Timeout:
        return None, "Pronunciation scoring timed out."

    except requests.exceptions.RequestException as e:
        return None, f"Scoring API error: {e}"