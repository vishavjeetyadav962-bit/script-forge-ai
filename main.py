import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fetch Gemini API Key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

class ScriptRequest(BaseModel):
    topic: str
    language: str = "Marathi"
    platform: str = "Instagram Reels"

@app.post("/api/generate")
async def generate_script(request: ScriptRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key is not set in environment variables.")

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
        You are a professional content creator and scriptwriter.
        Write an engaging, highly addictive short video script for {request.platform}.
        
        Topic: {request.topic}
        Language: {request.language}
        
        Structure the output as follows:
        1. [Hook] - Catchy opening line for the first 3 seconds.
        2. [Body/Story] - Engaging narrative or key facts (under 100 words).
        3. [Call to Action] - Strong ending asking viewers to follow, like, or comment.
        4. [Visual/Audio Cues] - Brief scene descriptions or background music recommendations.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        return {"status": "success", "script": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve frontend static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
