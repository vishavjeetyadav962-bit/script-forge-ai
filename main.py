import os
import uuid
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import edge_tts
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
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class GlobalVideoRequest(BaseModel):
    niche: str = "AI & Future Tech"
    topic: str
    target_country: str = "United States"
    accent_voice: str = "en-US-ChristopherNeural"

def fetch_pexels_videos(query: str):
    if not PEXELS_API_KEY:
        return []
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=3&orientation=portrait"
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            videos = []
            for video in data.get("videos", []):
                files = video.get("video_files", [])
                hd_file = next((f for f in files if f.get("quality") == "hd"), files[0] if files else None)
                if hd_file:
                    videos.append(hd_file["link"])
            return videos
    except Exception as e:
        print("Pexels Error:", e)
    return []

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Global Shorts Engine $</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d0f12; color: #e0e6ed; padding: 20px; max-width: 700px; margin: auto; }
            h1 { color: #00e676; text-align: center; font-size: 28px; }
            p.subtitle { text-align: center; color: #8b949e; margin-top: -10px; font-size: 14px; }
            .card { background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
            label { display: block; margin-top: 15px; font-weight: 600; color: #58a6ff; }
            input, select, button { width: 100%; padding: 12px; margin-top: 6px; border-radius: 8px; border: 1px solid #30363d; box-sizing: border-box; font-size: 15px; }
            input, select { background: #0d1117; color: #c9d1d9; }
            button { background: linear-gradient(135deg, #00e676, #00b0ff); color: #000; font-weight: bold; cursor: pointer; margin-top: 25px; font-size: 16px; border: none; transition: 0.3s; }
            button:hover { opacity: 0.9; }
            #output { margin-top: 20px; background: #0d1117; padding: 18px; border-radius: 8px; white-space: pre-wrap; word-wrap: break-word; border: 1px solid #30363d; font-family: monospace; }
            audio, video { width: 100%; margin-top: 15px; border-radius: 8px; }
            .video-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        </style>
    </head>
    <body>
        <h1>🌐 Global Faceless Video Engine</h1>
        <p class="subtitle">Generate High-CPM Dollar Shorts for US / Worldwide Audience</p>

        <div class="card">
            <label>High-CPM Category (विषय प्रकार)</label>
            <select id="niche">
                <option>AI & Future Tech</option>
                <option>Dark Psychology & Mysteries</option>
                <option>True Crime Stories</option>
                <option>Finance & Wealth Mindset</option>
                <option>Space & Universe Secrets</option>
            </select>
            
            <label>Video Concept / Topic (मूळ विषय)</label>
            <input type="text" id="topic" placeholder="e.g. What happens if Earth stops spinning for 5 seconds?">
            
            <label>Target Audience (लक्ष्य देश)</label>
            <select id="target_country">
                <option>United States (High CPM $)</option>
                <option>United Kingdom</option>
                <option>Canada / Australia</option>
                <option>Worldwide / Global</option>
            </select>

            <label>AI Voice Accent (परदेशी आवाज)</label>
            <select id="accent_voice">
                <option value="en-US-ChristopherNeural">US Male (Deep & Engaging)</option>
                <option value="en-US-AvaNeural">US Female (Clear & Viral)</option>
                <option value="en-GB-RyanNeural">UK Male (Narrative British)</option>
                <option value="en-GB-SoniaNeural">UK Female (Sophisticated British)</option>
            </select>

            <button onclick="generateGlobalContent()">⚡ Generate Complete Video Assets</button>
        </div>

        <div id="output">तुम्हाला पटकन स्क्रिप्ट, व्हॉईस आणि बॅकग्राउंड व्हिडिओ क्लिप्स मिळतील...</div>
        <audio id="audioPlayer" controls style="display:none;"></audio>
        <div id="videoContainer" class="video-grid"></div>

        <script>
            async function generateGlobalContent() {
                const outputDiv = document.getElementById('output');
                const audioPlayer = document.getElementById('audioPlayer');
                const videoContainer = document.getElementById('videoContainer');
                
                outputDiv.innerText = '🚀 Generating Script, US Voiceover & Fetching HD Background Videos... Please wait 10-15 seconds...';
                audioPlayer.style.display = 'none';
                videoContainer.innerHTML = '';
                
                const body = {
                    niche: document.getElementById('niche').value,
                    topic: document.getElementById('topic').value,
                    target_country: document.getElementById('target_country').value,
                    accent_voice: document.getElementById('accent_voice').value
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
                        if (data.audio_url) {
                            audioPlayer.src = data.audio_url;
                            audioPlayer.style.display = 'block';
                        }
                        if (data.video_urls && data.video_urls.length > 0) {
                            data.video_urls.forEach(url => {
                                const v = document.createElement('video');
                                v.src = url;
                                v.controls = true;
                                videoContainer.appendChild(v);
                            });
                        }
                    } else {
                        outputDiv.innerText = 'Error: ' + (data.detail || JSON.stringify(data));
                    }
                } catch (e) {
                    outputDiv.innerText = 'Generation failed: ' + e;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/generate")
async def generate_script(request: GlobalVideoRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY missing in Render settings.")

    # ट्राय-कॅच मॉडेल फॉलबॅक (एकापेक्षा जास्त मॉडेल नावे चेक करेल)
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    response = None
    last_error = None

    prompt = f"""
    You are an expert viral content strategist targeting a worldwide high-CPM audience ({request.target_country}).
    Create a high-retention video package for Youtube Shorts and Instagram Reels.
    
    Category: {request.niche}
    Topic: {request.topic}
    Target Region: {request.target_country}
    
    Rules:
    1. Language must be Fluent, Native English tailored for {request.target_country}.
    2. First 3 seconds MUST have a strong viral HOOK.
    3. Simple words, high suspense, fast pace.

    Format Output cleanly:
    🔥 [VIRAL HOOK] (0-3 sec text)
    📖 [NARRATION SCRIPT] (For voiceover - word-for-word)
    🎬 [STOCK FOOTAGE PROMPTS] (3 detailed prompts)
    📌 [HIGH-CPM TITLE & HASHTAGS] (Top 5 trending hashtags in USA)
    ⏰ [BEST POSTING TIME] (In US Eastern Time / UK Time)
    """

    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt)
            if response and response.text:
                break
        except Exception as e:
            last_error = e

    if not response or not response.text:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(last_error)}")

    script_text = response.text

    # Audio Generation
    audio_filename = f"global_voice_{uuid.uuid4().hex[:8]}.mp3"
    communicate = edge_tts.Communicate(script_text[:1200], request.accent_voice)
    await communicate.save(audio_filename)

    # Background Videos Fetch (Pexels)
    video_links = fetch_pexels_videos(request.topic)

    return {
        "status": "success", 
        "data": script_text,
        "audio_url": f"/audio/{audio_filename}",
        "video_urls": video_links
    }

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    if os.path.exists(filename):
        return FileResponse(filename, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio file not found")
