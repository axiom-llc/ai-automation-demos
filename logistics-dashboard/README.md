# Logistics Dashboard — AI-Powered Operations POC

Proof-of-concept operational intelligence dashboard for a logistics company. Delivered in ~4 hours. Demonstrates end-to-end AI integration: data ingestion → REST API → live dashboard with Gemini-powered compliance analysis.

## Architecture

```
maverick_data_ingestion_service.py   ← generates/loads operational data into SQLite
maverick_operations_api_service.py   ← Flask REST API over SQLite
maverick_live_dashboard.py           ← Dash live dashboard consuming the API
compliance_dashboard.gemini.py       ← Gemini API compliance analysis layer
demo.sh                              ← one-command orchestration
```

## Running the Demo

```bash
pip install flask dash dash-bootstrap-components plotly pandas requests
chmod +x demo.sh
./demo.sh
```

Dashboard: http://127.0.0.1:8050
API: http://127.0.0.1:5000

## API Endpoints

```
GET /api/logistics/daily_summary
GET /api/partner_performance/status?partner_contract=Amazon-Prime
```

## Stack

Python · Flask · Dash · SQLite · Gemini API · Plotly

## Scenarios

`scenario1.py`, `scenario2.py`, `scenario3.py` — simulate operational edge cases for demo purposes.
