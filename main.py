from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScriptRequest(BaseModel):
    topic: str
    genre: str = "Sci-Fi Suspense"

@app.get("/")
def home():
    return {"status": "ScriptForge AI Engine is Live"}

@app.post("/api/generate")
async def generate_script(req: ScriptRequest):
    script_output = f"""
--- 🎬 SCRIPTFORGE PRO GENERATED SCRIPT ---
TOPIC: {req.topic}
GENRE: {req.genre}

[Visual: Dark cinematic shot with glowing lights]
VOICEOVER: What if the story behind '{req.topic}' is not what you think?

[Visual: Fast cuts of mysterious shadows and high tension scenes]
VOICEOVER: In a reality governed by hidden rules, one discovery changed everything.

[Visual: Dramatic zoom-in on the main character]
VOICEOVER: Stay tuned as we unravel the truth. Subscribe for Part 2!
-------------------------------------------
"""
    return {"status": "success", "script": script_output}
