# 🔒 Phantom Agent V1

**Lightweight, ethical, user-consented forensic monitoring system.**

> Hackathon prototype • Python-based desktop agent • REST API ready

---

## ✨ Features

| Feature | Description |
|---|---|
| **Consent-first** | Agent refuses to run without explicit user agreement |
| **System Telemetry** | Collects processes, connections, public IP every 12s |
| **Log Rotation** | CSV logs rotate every 30 minutes |
| **Anomaly Detection** | Rule-based engine (suspicious processes, high connections, login failures) |
| **Evidence Packaging** | Screenshot + logs + metadata + SHA-256 hashes |
| **Tamper Verification** | Re-hash and compare to detect modifications |
| **Multi-channel Alerts** | OS notification + SMTP email + REST webhook |
| **Demo Mode** | `--demo` flag simulates threats for live demos |

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your SMTP credentials and API URL

# 3. Run the agent
python -m agent.main run

# 4. Run in demo mode (simulates threats)
python -m agent.main run --demo

# 5. Verify evidence integrity
python -m agent.main verify
```

---

## 📂 Project Structure

```
phantom-agent-v1/
├── .env.example              # Environment template
├── .gitignore
├── requirements.txt
├── README.md
│
├── agent/
│   ├── __init__.py
│   ├── main.py               # CLI entry point
│   ├── config.py             # .env loader, constants
│   ├── consent.py            # User consent gate
│   ├── collector.py          # psutil + httpx telemetry
│   ├── logger.py             # CSV logging + rotation
│   ├── detector.py           # Rule-based threat detection
│   ├── evidence.py           # Screenshot + packaging + hashing
│   ├── alerter.py            # OS notify + email + webhook
│   └── integrity.py          # SHA-256 tamper verification
│
├── logs/                     # Auto-created: rotating temp logs
├── evidence/                 # Auto-created: permanent incidents
└── tests/                    # Unit tests
```

---

## 🛡️ Security Model

- **Zero hardcoded credentials** — all secrets via `.env`
- **SHA-256 evidence chain** — every file hashed at capture time
- **Tamper detection** — `verify` subcommand re-checks all hashes
- **Consent record** — JSON with user, hostname, OS, timestamp
- **Minimal footprint** — reads only process list and connection count

---

## ⚙️ Configuration (.env)

| Variable | Default | Description |
|---|---|---|
| `SMTP_HOST` | `smtp.gmail.com` | SMTP server |
| `SMTP_PORT` | `587` | SMTP port |
| `SMTP_USER` | — | Email address |
| `SMTP_PASS` | — | App password |
| `ALERT_RECIPIENT` | — | Alert recipient |
| `API_BASE_URL` | `http://localhost:5000/api` | MERN backend URL |
| `DASHBOARD_URL` | `http://localhost:3000/dashboard` | Web dashboard URL |
| `COLLECTION_INTERVAL` | `12` | Seconds between snapshots |
| `LOG_ROTATION_MINUTES` | `30` | Minutes before log rotation |
| `CONNECTION_THRESHOLD` | `50` | Alert if connections exceed |
| `SUSPICIOUS_PROCESS_THRESHOLD` | `3` | Alert if process seen N times |

---

## 🔌 REST API Integration

The agent POSTs to `{API_BASE_URL}/alerts` on threat detection:

```json
{
  "incident_id": "incident_20260324_193000",
  "alert_count": 1,
  "alerts": [{
    "rule": "HIGH_CONNECTION_COUNT",
    "severity": "MEDIUM",
    "description": "Active connections (87) exceed threshold (50)",
    "details": { "connections": 87, "threshold": 50 },
    "timestamp": "2026-03-24T14:30:00+00:00"
  }],
  "evidence_path": "/evidence/incident_20260324_193000",
  "dashboard_url": "http://localhost:3000/dashboard"
}
```

---

## 📜 License

MIT — Built for educational and ethical security research only.
