# voice-agent-server.py
from flask import Flask, request, Response
import os
import requests
from google import genai
from google.genai import types

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# AI conversation memory per caller
conversations = {}

@app.route("/", methods=["POST"])
def main_menu():
    """Entry point"""
    return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather action="/route" numDigits="1" timeout="5">
        <Say>Press 1 for status. Press 2 for A I agent. Press 3 to reach me.</Say>
    </Gather>
    <Hangup/>
</Response>""", mimetype="text/xml")

@app.route("/route", methods=["POST"])
def route():
    """Route based on keypress"""
    digit = request.form.get("Digits")
    
    if digit == "1":
        return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>All systems operational.</Say>
    <Redirect>/</Redirect>
</Response>""", mimetype="text/xml")
    
    elif digit == "2":
        return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Connecting to A I agent. Speak after the beep.</Say>
    <Record action="/ai" maxLength="30" playBeep="true"/>
</Response>""", mimetype="text/xml")
    
    elif digit == "3":
        your_phone = os.environ.get("MY_PHONE_NUMBER")
        return Response(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Connecting now.</Say>
    <Dial timeout="20" action="/voicemail">
        <Number>{your_phone}</Number>
    </Dial>
</Response>""", mimetype="text/xml")
    
    return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")

@app.route("/ai", methods=["POST"])
def ai_conversation():
    """AI agent conversation"""
    caller = request.form.get("From", "unknown")
    recording_url = request.form.get("RecordingUrl")
    
    if not recording_url:
        return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")
    
    try:
        # Download audio
        r = requests.get(
            recording_url,
            auth=(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))
        )
        
        # Get conversation history
        if caller not in conversations:
            conversations[caller] = []
        
        # Build request
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
        
        # Call Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful AI assistant."
            )
        )
        
        ai_text = response.text.strip()
        
        # Save response
        conversations[caller].append(
            types.Content(parts=[types.Part(text=ai_text)], role="model")
        )
        
        # Trim history
        if len(conversations[caller]) > 20:
            conversations[caller] = conversations[caller][-20:]
        
        return Response(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{ai_text}</Say>
    <Say>Press star for menu, or continue.</Say>
    <Gather action="/check_star" numDigits="1" timeout="2" finishOnKey="*">
        <Record action="/ai" maxLength="30" playBeep="true"/>
    </Gather>
</Response>""", mimetype="text/xml")
        
    except Exception as e:
        print(f"Error: {e}")
        return Response('<Response><Say>Error occurred.</Say><Redirect>/</Redirect></Response>', mimetype="text/xml")

@app.route("/check_star", methods=["POST"])
def check_star():
    """Check if user pressed *"""
    if request.form.get("Digits") == "*":
        return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")
    return ai_conversation()

@app.route("/voicemail", methods=["POST"])
def voicemail():
    """Voicemail fallback"""
    status = request.form.get("DialCallStatus")
    
    if status in ["no-answer", "busy", "failed"]:
        return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Unavailable. Leave a message.</Say>
    <Record maxLength="120" playBeep="true"/>
    <Say>Message saved. Goodbye.</Say>
</Response>""", mimetype="text/xml")
    
    return Response('<Response><Hangup/></Response>', mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
