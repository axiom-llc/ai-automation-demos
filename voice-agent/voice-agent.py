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
    <Gather action="/route" numDigits="1" timeout="7">
        <Say>
            Welcome to Axiom L L C. 
            Press 1 for automation services. 
            Press 2 for A I and machine learning services.
            Press 3 for DevOps and infrastructure.
            Press 4 for data pipeline engineering.
            Press 5 for rates and availability.
            Press 6 for portfolio and case studies.
            Press 7 for contact information.
            Press 8 to speak with our A I assistant.
            Press 9 to connect directly to C E O Adam Tacon.
        </Say>
    </Gather>
    <Hangup/>
</Response>""", mimetype="text/xml")

@app.route("/route", methods=["POST"])
def route():
    digit = request.form.get("Digits")
    
    presets = {
        "1": """Python and Bash automation services include: Production-ready scripts for data processing and system administration. 
                Workflow optimization with zero-dependency design philosophy. ETL automation for CSV and Excel transformation. 
                Comprehensive error handling and logging. Cron and Systemd scheduling. Standard delivery 24 to 72 hours. 
                Recent project delivered 30 percent operational efficiency improvement and 75 percent processing time reduction 
                for insurance benefits administration.""",
        
        "2": """A I and machine learning services include: Multi-agent orchestration systems using Gemini Pro A P I and Ollama. 
                L L M integration with self-correcting logic and deterministic execution. Prompt engineering and N L P implementation. 
                Research automation and intelligent data extraction. Recent project: 4-hour proof of concept A I powered logistics dashboard 
                using Gemini A P I, Flask, and Dash, which led to 15 thousand dollar implementation contract. 
                Extensive experience with Gemini Pro, Ollama, and production L L M deployments.""",
        
        "3": """DevOps and infrastructure services include: Google Cloud Platform optimization and cost reduction. 
                Continuous integration and deployment pipelines. Docker containerization and orchestration. 
                Infrastructure monitoring and system administration. Comprehensive Arch Linux expertise. 
                Recent project: Production DevOps automation suite reduced weekly manual operations from 15 hours to 2 hours, 
                achieving 99.98 percent sync reliability and 87 percent auto-remediation of operational issues without manual intervention.""",
        
        "4": """Data pipeline engineering services include: E T L workflow design and implementation. PostgreSQL database integration. 
                API connector development with RESTful design. CSV and Excel data transformation at scale. 
                Probabilistic quality assurance frameworks achieving 100 percent error detection for mission-critical operations. 
                Flask backend development. Comprehensive data validation and error handling. 
                Recent projects include enterprise-scale data processing pipelines with zero data loss.""",
        
        "5": """Rate structure: 35 dollars per hour with fixed-price arrangements preferred for defined project scope. 
                Volume discounts available for ongoing engagements or multi-project commitments. 
                Availability: immediate engagement, 20 to 40 hours per week, Eastern Standard Time. 
                Response time: initial consultation responses within 12 hours on business days. 
                Standard project turnaround 24 to 72 hours depending on scope. 
                Fastest delivery on record: complete 4-hour proof of concept for logistics dashboard.""",
        
        "6": """Portfolio highlights: Multi-agent orchestration system with Gemini Pro featuring zero-regression production deployments. 
                A I powered logistics dashboard proof of concept delivered in under 4 hours, leading to 15 thousand dollar contract. 
                Production DevOps automation suite with 99.98 percent reliability over 12 months. 
                RESTful A P I integration framework reducing typical integration timeline from 2 weeks to 3 days. 
                Complete code portfolio available at github dot com slash axiom dash L L C. 
                Verified freelancer profile with client feedback at freelancer dot com slash u slash adam0641.""",
        
        "7": """Contact information: Email at253341@gmail.com, that's A T, 2 5 3 3 4 1, at gmail dot com. 
                Phone number: area code 8 4 8, 3 1 8, 8 1 1 3. 
                Portfolio and open source code: github dot com slash axiom dash L L C. 
                Freelancer platform for project engagements: freelancer dot com slash u slash adam0641. 
                Location: New Jersey, United States, Eastern Time Zone. 
                Response guarantee: 12 hours on business days for initial consultation.""",
    }
    
    if digit in presets:
        return Response(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{presets[digit]}</Say>
    <Say>Press star to return to the main menu, or press pound to repeat this information.</Say>
    <Gather action="/menu_navigation" numDigits="1" timeout="4" finishOnKey="*#"/>
    <Redirect>/</Redirect>
</Response>""", mimetype="text/xml")
    
    elif digit == "8":
        return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Connecting to Axiom's A I assistant who can answer detailed technical questions and discuss project requirements. Speak after the beep.</Say>
    <Record action="/ai" maxLength="30" playBeep="true"/>
</Response>""", mimetype="text/xml")
    
    elif digit == "9":
        your_phone = os.environ.get("MY_PHONE_NUMBER")
        return Response(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Connecting you to C E O Adam Tacon now. Please hold.</Say>
    <Dial timeout="25" action="/voicemail">
        <Number>{your_phone}</Number>
    </Dial>
</Response>""", mimetype="text/xml")
    
    return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")

@app.route("/menu_navigation", methods=["POST"])
def menu_navigation():
    digit = request.form.get("Digits")
    if digit == "*":
        return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")
    elif digit == "#":
        # Repeat last message - redirect back to route with stored digit
        return Response('<Response><Redirect>/route</Redirect></Response>', mimetype="text/xml")
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
                    types.Part(text="Transcribe and respond conversationally.")
                ],
                role="user"
            )
        )
        
        system_instruction = """You are Axiom LLC's AI assistant helping potential clients understand our services and expertise. CEO Adam Tacon leads all technical delivery.

CORE SERVICES:
1. Python/Bash Automation: Production scripts, workflow optimization, zero-dependency design, 24-72hr delivery
2. AI Agent Orchestration: Gemini Pro API, Ollama, multi-agent systems, self-correcting logic
3. Data Pipeline Engineering: ETL workflows, PostgreSQL, API connectors, 100% error detection frameworks
4. DevOps/Infrastructure: GCP optimization, Docker, CI/CD, Arch Linux expertise, system monitoring

KEY PROJECTS:
- Multi-agent orchestration: Zero-regression deployments, advanced meta-prompting, Git integration
- 4-hour logistics dashboard POC: Gemini API + Flask + Dash → $15K contract in <4 hours
- DevOps automation suite: 15hrs→2hrs/week ops time, 99.98% reliability, 87% auto-remediation
- Insurance workflow automation: 75% processing time reduction, 30% efficiency improvement
- RESTful API framework: 2 weeks→3 days integration timeline reduction

TECHNICAL STACK:
Languages: Python 3.x, Bash, C, JavaScript, SQL
AI/ML: Gemini Pro API, Ollama, prompt engineering, NLP
Data: PostgreSQL, Flask, ETL, data validation
DevOps: Linux (Arch), Docker, Git, GCP, CI/CD
Frontend: React, Dash, Plotly, HTML/CSS

BUSINESS DETAILS:
- Rate: $35/hour, fixed-price preferred for defined scope
- Availability: 20-40 hrs/week, EST, immediate start
- Response: 12 hours on business days
- Delivery: 24-72 hours typical, fastest was 4 hours for full POC
- Contact: at253341@gmail.com, +1-848-318-8113
- Portfolio: github.com/axiom-llc
- Freelancer: freelancer.com/u/adam0641

CONVERSATION STYLE:
- Be professional, technical, and specific
- Provide concrete examples from past projects when relevant
- If asked about capabilities, cite actual delivered results
- For project inquiries, gather: scope, timeline, budget, technical requirements
- If ready to hire, direct them to press 9 to speak with CEO Adam Tacon or collect contact info
- Keep responses concise but information-dense
- Use metrics and outcomes (%, hours saved, $ value) when discussing projects"""
        
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
    <Say>Press star for main menu, press 9 to speak with C E O Adam Tacon directly, or continue the conversation.</Say>
    <Gather action="/check_ai_navigation" numDigits="1" timeout="2" finishOnKey="*9">
        <Record action="/ai" maxLength="30" playBeep="true"/>
    </Gather>
</Response>""", mimetype="text/xml")
        
    except Exception as e:
        print(f"Error: {e}")
        return Response('<Response><Say>Error occurred.</Say><Redirect>/</Redirect></Response>', mimetype="text/xml")

@app.route("/check_ai_navigation", methods=["POST"])
def check_ai_navigation():
    digit = request.form.get("Digits")
    if digit == "*":
        return Response('<Response><Redirect>/</Redirect></Response>', mimetype="text/xml")
    elif digit == "9":
        your_phone = os.environ.get("MY_PHONE_NUMBER")
        return Response(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Transferring you to C E O Adam Tacon now.</Say>
    <Dial timeout="25" action="/voicemail">
        <Number>{your_phone}</Number>
    </Dial>
</Response>""", mimetype="text/xml")
    return ai_conversation()

@app.route("/voicemail", methods=["POST"])
def voicemail():
    status = request.form.get("DialCallStatus")
    
    if status in ["no-answer", "busy", "failed"]:
        return Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>C E O Adam Tacon is currently unavailable. Please leave a detailed message including: your name, contact information, 
    project type, timeline requirements, and budget range. Messages are reviewed within 12 hours on business days.</Say>
    <Record maxLength="180" playBeep="true"/>
    <Say>Thank you for contacting Axiom L L C. You will receive a response within 12 hours on business days. 
    For immediate questions, email at253341@gmail.com or visit freelancer.com/u/adam0641.</Say>
</Response>""", mimetype="text/xml")
    
    return Response('<Response><Hangup/></Response>', mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
