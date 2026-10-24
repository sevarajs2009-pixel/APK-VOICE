
from fastapi import FastAPI, UploadFile, File, HTTPException
from faster_whisper import WhisperModel
import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://apk-voice.onrender.com",
    ],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

# Multilingual speech recognition.
# "small" is a reasonable starting point, but needs sufficient RAM.

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    temp_path = None

    try:
        suffix = os.path.splitext(audio.filename or "")[1] or ".webm"

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:
            temp.write(await audio.read())
            temp_path = temp.name

        segments, info = model.transcribe(
            temp_path,
            language="ta",  # Force Tamil transcription for this test
            beam_size=5,
            vad_filter=True
        )

        text = "".join(segment.text for segment in segments).strip()

        return {
            "text": text,
            "language": info.language
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
