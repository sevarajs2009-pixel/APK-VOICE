from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
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

# Serve static frontend files and PWA requirements
@app.get("/")
async def serve_index():
    return FileResponse("index.html")

@app.get("/manifest.json")
async def serve_manifest():
    return FileResponse("manifest.json")

@app.get("/pwabuilder-sw.js")
async def serve_sw():
    return FileResponse("pwabuilder-sw.js")

# Multilingual speech recognition model
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
