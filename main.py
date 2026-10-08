import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class ScriptRequest(BaseModel):
    source: str = "Google Trends"
    topic: str
    format_type: str = "Shorts"
    language: str = "Marathi"
    target_country: str = "India"

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ScriptForge AI</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #121212; color: #fff; padding: 20px; max-width: 600px; margin: auto; }
            h1 { color: #00e676; text-align: center; }
            label { display: block; margin-top: 15px; font-weight: bold; }
            input, select, button { width: 100%; padding: 12px; margin-top: 5px; border-radius: 6px; border: none; box-sizing: border-box; }
            input, select { background: #222; color: #fff; border: 1px solid #444; font-size: 15px; }
            button { background: #00e676; color: #000; font-weight: bold; cursor: pointer; margin-top: 25px; font-size: 16px; }
            button:hover { background: #00c853; }
            #output { margin-top: 20px; background: #1e1e1e; padding: 15px; border-radius: 6px; white-space: pre-wrap; word-wrap: break-word; border: 1px solid #333; }
        </style>
    </head>
    <body>
        <h1>🚀 ScriptForge AI</h1>
        
        <label>डाटा सोर्स (Data Source)</label>
        <select id="source">
            <option>Google Trends</option>
            <option>Reddit</option>
            <option>Wikipedia</option>
        </select>
        
        <label>विषय / टॉपिक (Topic)</label>
        <input type="text" id="topic" placeholder="उदा. AI News, Sci-Fi Mystery">
        
        <label>व्हिडिओ फॉरमॅट (Format)</label>
        <select id="format_type">
            <option>Shorts</option>
            <option>Long-Form</option>
        </select>

        <label>भाषा (Language)</label>
        <select id="language">
            <option>Marathi</option>
            <option>English</option>
            <option>Hindi</option>
        </select>

        <label>टार्गेट देश (Target Region)</label>
        <select id="target_country">
            <option>India</option>
            <option>USA/UK</option>
        </select>

        <button onclick="generateScript()">⚡ ऑल-इन-वन डेटा जनरेट करा</button>

        <div id="output">तुमची जनरेट झालेली स्क्रिप्ट इथे दिसेल...</div>

        <script>
            async function generateScript() {
                const outputDiv = document.getElementById('output');
                outputDiv.innerText = 'स्क्रिप्ट जनरेट होत आहे... कृपया थोडा वेळ थांबा...';
                
                const body = {
                    source: document.getElementById('source').value,
                    topic: document.getElementById('topic').value,
                    format_type: document.getElementById('format_type').value,
                    language: document.getElementById('language').value,
                    target_country: document.getElementById('target_country').value
                };

                try {
                    const res = await fetch('/api/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(body)
                    });
                    const data = await res.json();
                    if (data.data) {
                        outputDiv.innerText = data.data;
                    } else {
                        outputDiv.innerText = 'एरर आला: ' + JSON.stringify(data);
                    }
                } catch (e) {
                    outputDiv.innerText = 'स्क्रिप्ट जनरेट झाली नाही: ' + e;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/generate")
async def generate_script(request: ScriptRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set.")

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an advanced viral video automation assistant.
        Generate a complete content package based on:
        - Data Source: {request.source}
        - Topic: {request.topic}
        - Video Type: {request.format_type}
        - Language: {request.language}
        - Target Audience Region: {request.target_country}

        Provide the output formatted with clear headers in {request.language}:
        📌 [TITLE & SEO TAGS] (Catchy YouTube title + 5 viral hashtags)
        ⏰ [BEST UPLOADING TIME] (Optimal posting time for {request.target_country})
        🔥 [HOOK] (First 3 seconds)
        📖 [FULL SCRIPT / STORY] (Structured narrative)
        🎬 [STOCK FOOTAGE PROMPTS] (Detailed visual prompts for editing tools)
        🎯 [CALL TO ACTION]
        """
        
        response = model.generate_content(prompt)
        return {"status": "success", "data": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
