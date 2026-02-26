# Voice Agent - Local Testing

## Setup

1. **Install dependencies**
```bash
pip install flask google-genai requests
```

2. **Set environment variables**
```bash
export GEMINI_API_KEY="your_key"
export TWILIO_ACCOUNT_SID="ACxxxx"
export TWILIO_AUTH_TOKEN="your_token"
export MY_PHONE_NUMBER="+1234567890"
```

3. **Run server**
```bash
python3 voice-agent-simple.py
```
0
4. **Expose with ngrok**
```bash
ngrok http 5000
```

5. **Configure Twilio**
- Go to: Console → Phone Numbers → Active Numbers
- Click your number
- Voice Configuration → A CALL COMES IN
- Webhook: `https://YOUR-NGROK-URL.ngrok.io/`
- HTTP POST
- Save

## Test Flow

Call your Twilio number:
- Press 1 → Automated status
- Press 2 → Talk with AI (press * to exit)
- Press 3 → Forwards to your phone → Voicemail if no answer

## Files

- `voice-agent-simple.py` - Main server
- `context.txt` - AI personality (not used yet, add if needed)

## Endpoints

- `/` - Main menu
- `/route` - Routes based on keypress
- `/ai` - AI conversation loop
- `/voicemail` - Fallback when you don't answer
