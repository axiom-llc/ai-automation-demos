# voice-agent-simple.py
from flask import Flask, request, Response
import os
import requests
from google import genai
from google.genai import types

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

conversations = {}

@app.route("/", methods=["POST"])
def main_menu():
    return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather action="/route" numDigits="1" timeout="5">
        <Say>
            Welcome to Adam Tacon's line. 
            Press 1 for services and rates. 
            Press 2 to speak with my A I assistant. 
            Press 3 for contact information. 
            Press 4 for availability. 
            Press 5 to reach me directly.
        </Say>
    </Gather>
    <Hangup/>
</Response>""", mimetype="text/xml")

@app.route("/route", methods=["POST"])
def route():
    digit = request.form.get("Digits")
    
    # Preset responses
    presets = {
        "1": """I specialize in Python and Bash automation, A I agent orchestration with Gemini and Ollama, 
                data pipeline engineering, and DevOps infrastructure. My rate is 35 dollars per hour, 
                with fixed-price arrangements preferred for defined project scope. 
                Typical turnaround is 24 to 72 hours.""",
        
        "3": """You can reach me at at253341@gmail.com, that's A T 2 5 3 3 4 1 at gmail dot com. 
                My phone number is 8 4 8, 3 1 8, 8 1 1 3. 
                Find my portfolio at github dot com slash axiom dash L L C, 
                or hire me on Freelancer dot com at username adam0641.""",
        
        "4": """I'm available for immediate engagement, 20 to 40 hours per week, Eastern Standard Time. 
                I respond to initial consultations within 12 hours on business days. 
                Standard project delivery is 24 to 72 hours depending on scope.""",
    }
    
    if digit in presets:
        return Response(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{presets[digit]}</Say>
    <Say>Press star to return to the main menu.</Say>
    <Gather action="/main_menu_check" numDigits="1" timeout="3" finishOnKey="*"/>
    <Redirect>/</Redirect>
</Response>""", mimetype="text/xml")
    
    elif digit == "2":
        return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Connecting to my A I assistant. Speak after the beep.</Say>
    <Record action="/ai" maxLength="30" playBeep="true"/>
</Response>""", mimetype="text/xml")
    
    elif digit == "5":
        your_phone = os.environ.get("MY_PHONE_NUMBER")
        return Response(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Connecting you to Adam now. Please hold.</Say>
    <Dial timeout="20" action="/voicemail">
        <Number>{your_phone}</Number>
    </Dial>
</Response>""", mimetype="text/xml")
    
    return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")

@app.route("/main_menu_check", methods=["POST"])
def main_menu_check():
    if request.form.get("Digits") == "*":
        return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")
    return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")

@app.route("/ai", methods=["POST"])
def ai_conversation():
    caller = request.form.get("From", "unknown")
    recording_url = request.form.get("RecordingUrl")
    
    if not recording_url:
        return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")
    
    try:
        r = requests.get(
            recording_url,
            auth=(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))
        )
        
        if caller not in conversations:
            conversations[caller] = []
        
        contents = conversations[caller].copy()
        contents.append(
            types.Content(
                parts=[
                    types.Part.from_bytes(data=r.content, mime_type="audio/wav"),
                    types.Part(text="Transcribe and respond.")
                ],
                role="user"
            )
        )
        
        system_instruction = """You are Adam Tacon's AI assistant. You help potential clients learn about his services.

Key information:
- Specializes in: Python/Bash automation, AI agent orchestration (Gemini/Ollama), data pipelines, DevOps
- Rate: $35/hour, prefers fixed-price for defined scope
- Turnaround: 24-72 hours typically
- Availability: 20-40 hrs/week, EST timezone, immediate start
- Contact: at253341@gmail.com, +1-848-318-8113
- Portfolio: github.com/axiom-llc
- Freelancer: freelancer.com/u/adam0641

Notable projects:
- Multi-agent orchestration systems with Gemini Pro API
- 4-hour logistics dashboard POC (led to $15k contract)
- Production DevOps automation reducing ops time from 15hrs to 2hrs/week
- 75% processing time reduction for insurance workflows

Be helpful, professional, and concise. If asked technical questions, provide specific details.
If they want to hire or discuss a project, get their contact info or direct them to press 5 to speak with Adam directly."""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        ai_text = response.text.strip()
        
        conversations[caller].append(
            types.Content(parts=[types.Part(text=ai_text)], role="model")
        )
        
        if len(conversations[caller]) > 20:
            conversations[caller] = conversations[caller][-20:]
        
        return Response(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{ai_text}</Say>
    <Say>Press star for main menu, or continue speaking.</Say>
    <Gather action="/check_star" numDigits="1" timeout="2" finishOnKey="*">
        <Record action="/ai" maxLength="30" playBeep="true"/>
    </Gather>
</Response>""", mimetype="text/xml")
        
    except Exception as e:
        print(f"Error: {e}")
        return Response('<Response><Say>Error occurred.</Say><Redirect>/</Redirect></Response>', mimetype="text/xml")

@app.route("/check_star", methods=["POST"])
def check_star():
    if request.form.get("Digits") == "*":
        return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")
    return ai_conversation()

@app.route("/voicemail", methods=["POST"])
def voicemail():
    status = request.form.get("DialCallStatus")
    
    if status in ["no-answer", "busy", "failed"]:
        return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Adam is unavailable. Please leave a detailed message including your name, contact information, and project details.</Say>
    <Record maxLength="120" playBeep="true"/>
    <Say>Thank you for your message. Adam will return your call within 12 hours on business days.</Say>
</Response>""", mimetype="text/xml")
    
    return Response('<Response><Hangup/></Response>', mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
