# Deploy to Google Cloud Run

## Quick Setup

1. **Install gcloud CLI** (if not installed):
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

2. **Set your project ID** in `deploy.sh`:
```bash
PROJECT_ID="your-project-id"  # Find at console.cloud.google.com
```

3. **Ensure file is named vae.py** (or update Dockerfile)

4. **Deploy**:
```bash
chmod +x deploy.sh
./deploy.sh
```

5. **Update Twilio webhook** with the URL shown (ends in `.run.app`)

## Files Needed
- `vae.py` (your voice agent)
- `Dockerfile`
- `requirements.txt`
- `deploy.sh`

## Environment Variables
Set these in your shell before running deploy.sh:
```bash
export GEMINI_API_KEY="your_key"
export TWILIO_ACCOUNT_SID="ACxxxx"
export TWILIO_AUTH_TOKEN="your_token"
export MY_PHONE_NUMBER="+1234567890"
```

## Cost
Free tier: 2 million requests/month, 360,000 GB-seconds
Your usage: ~$0.50-2/month after free tier

## Troubleshooting
View logs: `gcloud run services logs read axiom-voice-agent --region us-central1`
