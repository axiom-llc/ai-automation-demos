# logistics-dashboard

AI-powered operational intelligence dashboard for a logistics company. Built as a working POC in ~4 hours.

## Stack

- **Gemini 2.5 Flash** — contract compliance analysis and scenario Q&A
- **Flask** — REST API serving shipment and partner metrics
- **Dash + Plotly** — live operational dashboard with auto-refresh
- **SQLite** — ingested shipment and partner task data
- **pandas** — CSV ingestion and on-time delivery calculation

## Structure

```
data_ingestion.py       ← ingests shipments.csv + partner API data into SQLite
operations_api.py       ← Flask REST API (daily summary, partner performance)
live_dashboard.py       ← Dash dashboard consuming the API
compliance_dashboard.py ← Gemini-powered contract compliance assistant
dashboard.html          ← static dashboard mockup
website.html            ← static marketing/landing page mockup
shipments.csv           ← sample shipment data
demo.sh                 ← orchestrates full demo: ingest → API → dashboard
```

## Setup

```bash
pip install pandas requests flask dash dash-bootstrap-components plotly google-genai
export GEMINI_API_KEY=your-key
```

## Usage

```bash
# Run full demo (ingest → start API + dashboard servers)
./demo.sh

# Or run components individually:
python data_ingestion.py      # populate SQLite DB
python operations_api.py      # start API on :5000
python live_dashboard.py      # start dashboard on :8050
python compliance_dashboard.py # start compliance assistant on :8051
```

**API endpoints:**
- `GET /api/logistics/daily_summary`
- `GET /api/partner_performance/status?partner_contract=Amazon-Prime`
