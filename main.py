import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

class ScriptRequest(BaseModel):
    source: str = "Google Trends"  # Google Trends, Reddit, Wikipedia
    topic: str
    format_type: str = "Shorts"    # Shorts (Reels) or Long-Form (Documentary)
    language: str = "Marathi"
    target_country: str = "India" # India or USA/UK

@app.post("/api/generate")
async def generate_script(request: ScriptRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key is not set.")

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
        You are an advanced viral video automation assistant.
        Generate a complete content package based on:
        - Data Source: {request.source}
        - Topic: {request.topic}
        - Video Type: {request.format_type}
        - Language: {request.language}
        - Target Audience Region: {request.target_country}

        Perform live search on {request.source} for real-time trending info.

        Provide the output formatted with clear headers:
        📌 **[TITLE & SEO TAGS]** (Catchy YouTube title + 5 viral hashtags)
        ⏰ **[BEST UPLOADING TIME]** (Optimal posting time for {request.target_country})
        🔥 **[HOOK]** (First 3 seconds)
        📖 **[FULL SCRIPT / STORY]** (Structured narrative)
        🎬 **[STOCK FOOTAGE PROMPTS]** (Detailed visual prompts for editing tools)
        🎯 **[CALL TO ACTION]**
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"tools": [{"google_search": {}}]}
        )
        
        return {"status": "success", "data": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory="static", html=True), name="static")
