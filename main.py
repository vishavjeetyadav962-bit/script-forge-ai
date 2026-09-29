from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="ScriptForge AI Engine")

class ScriptRequest(BaseModel):
    topic: str
    platform: str = "Instagram Reel"
    tone: str = "Suspenseful"
    language: str = "Marathi"

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="mr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ScriptForge AI</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; }
            .container { max-width: 600px; width: 100%; background: #1e293b; padding: 25px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
            h1 { text-align: center; color: #38bdf8; margin-bottom: 20px; }
            label { font-weight: bold; margin-top: 10px; display: block; color: #94a3b8; }
            input, select, button { width: 100%; padding: 12px; margin-top: 8px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: #fff; box-sizing: border-box; font-size: 16px; }
            button { background: #0284c7; font-weight: bold; border: none; margin-top: 20px; cursor: pointer; transition: 0.3s; }
            button:hover { background: #0369a1; }
            .result-box { margin-top: 25px; background: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #334155; white-space: pre-wrap; font-size: 15px; line-height: 1.6; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬 ScriptForge AI</h1>
            <label for="topic">विषय / Topic:</label>
            <input type="text" id="topic" placeholder="उदा. भयाण रात्र, टाइम ट्रॅव्हल...">
            
            <label for="language">भाषा / Language:</label>
            <select id="language">
                <option value="Marathi">मराठी (Marathi)</option>
                <option value="English">English</option>
            </select>

            <label for="platform">प्लॅटफॉर्म / Platform:</label>
            <select id="platform">
                <option value="Instagram Reel">Instagram Reel</option>
                <option value="YouTube Shorts">YouTube Shorts</option>
            </select>

            <label for="tone">टोन / Tone:</label>
            <select id="tone">
                <option value="Suspenseful">Suspenseful (रहस्यमयी)</option>
                <option value="Dramatic">Dramatic (ड्रामा)</option>
                <option value="Sci-Fi">Sci-Fi (विज्ञानपट)</option>
            </select>

            <button onclick="generateScript()">🚀 Generate Script</button>

            <div id="result" class="result-box" style="display:none;"></div>
        </div>

        <script>
            async function generateScript() {
                const topic = document.getElementById('topic').value;
                const platform = document.getElementById('platform').value;
                const tone = document.getElementById('tone').value;
                const language = document.getElementById('language').value;
                const resultDiv = document.getElementById('result');

                if (!topic) { alert("कृपया विषय टाका!"); return; }

                resultDiv.style.display = "block";
                resultDiv.innerHTML = "⏳ AI स्क्रीप्ट तयार होत आहे...";

                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ topic, platform, tone, language })
                    });
                    const data = await response.json();
                    resultDiv.innerHTML = "<strong>✨ तयार झालेली स्क्रीप्ट:</strong><br><br>" + data.script;
                } catch (err) {
                    resultDiv.innerHTML = "❌ काहीतरी चूक झाली. पुन्हा प्रयत्न करा.";
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/generate")
def generate_script(req: ScriptRequest):
    if req.language == "Marathi":
        generated_text = f"🎬 --- SCRIPTFORGE PRO GENERATED SCRIPT ---\n"
        generated_text += f"📌 विषय: {req.topic}\n"
        generated_text += f"🎭 टोन: {req.tone} | 📱 प्लॅटफॉर्म: {req.platform}\n\n"
        generated_text += f"[दृश्य: अंधारात चमकणारे लाईट्स आणि डार्क सिनेमॅटिक शॉट]\n"
        generated_text += f"वॉइसओव्हर: 'काय वाटतं? {req.topic} या गोष्टीमागे दडलेलं सत्य आपल्याला जे दिसतं तेच आहे की अजून काही रहस्य आहे...?'\n\n"
        generated_text += f"[दृश्य: वेगाने बदलणारे रहस्यमयी चेहरे, सावल्या आणि हाय-टेंशन सीन]\n"
        generated_text += f"वॉइसओव्हर: 'अदृश्य नियमांवर चालणाऱ्या या जगात, एका अनपेक्षित घटनेने सगळंच बदलून टाकलं...'\n\n"
        generated_text += f"[दृश्य: मुख्य पात्रावर कॅमेरा झूम-इन होतो]\n"
        generated_text += f"वॉइसओव्हर: 'पूर्ण सत्य जाणून घेण्यासाठी फॉलो आणि सबस्क्राईब करायला विसरू नका!'"
    else:
        generated_text = f"🎬 --- SCRIPTFORGE PRO GENERATED SCRIPT ---\n"
        generated_text += f"📌 TOPIC: {req.topic}\n"
        generated_text += f"🎭 GENRE: {req.tone} | 📱 PLATFORM: {req.platform}\n\n"
        generated_text += f"[Visual: Dark cinematic shot with glowing lights]\n"
        generated_text += f"VOICEOVER: What if the story behind '{req.topic}' is not what you think?\n\n"
        generated_text += f"[Visual: Fast cuts of mysterious shadows and high tension scenes]\n"
        generated_text += f"VOICEOVER: In a reality governed by hidden rules, one discovery changed everything.\n\n"
        generated_text += f"[Visual: Dramatic zoom-in on the main character]\n"
        generated_text += f"VOICEOVER: Stay tuned as we unravel the truth. Subscribe for Part 2!"
    
    return {"status": "success", "script": generated_text}
