#!/bin/bash
# deploy.sh - Deploy to Google Cloud Run

# Configuration
PROJECT_ID="project555-485303"  # CHANGE THIS
SERVICE_NAME="axiom-voice-agent"
REGION="us-eastern1"  # Change if needed

# Rename your file to vae.py (or update Dockerfile CMD)
# Make sure vae.py is in this directory

# Deploy
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY="$GEMINI_API_KEY" \
  --set-env-vars TWILIO_ACCOUNT_SID="$TWILIO_ACCOUNT_SID" \
  --set-env-vars TWILIO_AUTH_TOKEN="$TWILIO_AUTH_TOKEN" \
  --set-env-vars MY_PHONE_NUMBER="$MY_PHONE_NUMBER" \
  --project $PROJECT_ID

echo "Deployment complete! Update Twilio webhook to the URL shown above."
