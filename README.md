# axiom-demos

Focused demonstrations of applied AI integration and automation delivery.
Each project is self-contained, runnable, and maps to a real client problem.

![CI](https://github.com/axiom-llc/axiom-demos/actions/workflows/ci.yml/badge.svg)

---

## Demos

### [logistics-dashboard](./logistics-dashboard/)

AI-powered operational intelligence dashboard for a logistics company.
Gemini API + Flask REST API + Dash live dashboard + SQLite.
Delivered as a working POC in ~4 hours.

### [voice-agent](./voice-agent/)

AI-powered voice IVR with telephony integration.
Gemini API + Flask + Twilio — automated call handling, AI conversation loop, and intelligent call routing.
Containerized for GCP Cloud Run deployment.

---

## Tests

```bash
pip install pytest flask requests google-genai
pytest tests/ -q
```

Smoke tests cover all Flask routes in both demos. Gemini API and Twilio calls are fully mocked — no credentials or network access required. CI runs on Python 3.11 and 3.12 on every push, plus a Docker build verification of the voice agent image.

---

Built by [Axiom LLC](https://axiom-llc.github.io)
