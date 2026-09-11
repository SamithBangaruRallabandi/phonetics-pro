from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import FileResponse
from modules.tts import generate_audio
from modules.analyzer import analyze_text
from modules.speech_recognition import speech_to_text
from modules.scoring import pronunciation_score


app = FastAPI(
    title="Phonetics-PRO API",
    description="English Pronunciation Analysis API",
    version="1.0.0"
)


# ==================================================
# Request Model
# ==================================================

class TextRequest(BaseModel):
    text: str


# ==================================================
# Root Endpoint
# ==================================================

@app.get("/")
def root():

    return {
        "message": "Phonetics-PRO API is running"
    }


# ==================================================
# Text Analysis Endpoint
# ==================================================

@app.post("/analyze")
def analyze(request: TextRequest):

    if not request.text.strip():

        return {
            "error": "Text cannot be empty"
        }

    return analyze_text(
        request.text
    )


# ==================================================
# Speech Analysis Endpoint
# ==================================================

@app.post("/analyze-speech")
async def analyze_speech(
    file: UploadFile = File(...)
):

    try:

        audio_data = await file.read()

        speech_text, error = speech_to_text(
            audio_data
        )

        if error:

            return {
                "error": error
            }


        analysis = analyze_text(
            speech_text
        )


        return {
            "speech_text": speech_text,
            "analysis": analysis
        }


    except Exception as e:

        return {
            "error": str(e)
        }
    

@app.post("/tts")
def text_to_speech(request: TextRequest):
    if not request.text.strip():
        return {"error": "Text cannot be empty"}

    audio_path = generate_audio(request.text)

    if not audio_path:
        return {"error": "Could not generate audio"}

    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        filename="pronunciation.mp3"
    )

@app.post("/score")
def score_pronunciation(request: dict):

    expected_text = request.get("expected_text", "")
    recognized_text = request.get("recognized_text", "")

    if not expected_text.strip():
        return {
            "error": "Expected text cannot be empty"
        }

    if not recognized_text.strip():
        return {
            "error": "Recognized text cannot be empty"
        }

    result = pronunciation_score(
        expected_text,
        recognized_text
    )

    return result