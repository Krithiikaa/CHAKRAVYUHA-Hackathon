"""
config.py — Centralised configuration loader.
All secrets and tunables come from .env (never hardcoded).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Paths ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

LOGS_DIR = BASE_DIR / "logs"
EVIDENCE_DIR = BASE_DIR / "evidence"
CONSENT_FILE = BASE_DIR / "consent.json"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
EVIDENCE_DIR.mkdir(exist_ok=True)

# ── SMTP ─────────────────────────────────────────────────
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
ALERT_RECIPIENT = os.getenv("ALERT_RECIPIENT", "")

# ── API ──────────────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/api")
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "http://localhost:3000/dashboard")

# ── Agent Tunables ───────────────────────────────────────
COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", "12"))       # seconds
LOG_ROTATION_MINUTES = int(os.getenv("LOG_ROTATION_MINUTES", "30"))     # minutes
CONNECTION_THRESHOLD = int(os.getenv("CONNECTION_THRESHOLD", "50"))
SUSPICIOUS_PROCESS_THRESHOLD = int(os.getenv("SUSPICIOUS_PROCESS_THRESHOLD", "3"))

# ── Suspicious process watchlist (extend as needed) ──────
SUSPICIOUS_PROCESSES = [
    "mimikatz", "lazagne", "keylogger", "nmap", "wireshark",
    "metasploit", "hydra", "john", "hashcat", "netcat",
    "nc.exe", "powershell_empire", "cobaltstrike",
]
